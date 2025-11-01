// Azure Function: /api/callback
// Completes GitHub OAuth, returns token to Netlify CMS via postMessage

const fetch = require('node-fetch');

module.exports = async function (context, req) {
  const clientId = process.env.GITHUB_CLIENT_ID;
  const clientSecret = process.env.GITHUB_CLIENT_SECRET;
  const redirectUri = process.env.OAUTH_REDIRECT_URI || `${getOrigin(req)}/api/callback`;

  const code = req.query.code;
  const state = req.query.state;
  const cookieState = parseCookie(req.headers?.cookie || '').oauth_state;

  if (!clientId || !clientSecret) {
    context.res = {
      status: 500,
      headers: { 'content-type': 'text/plain' },
      body: 'Missing GITHUB_CLIENT_ID or GITHUB_CLIENT_SECRET environment variable.'
    };
    return;
  }

  if (!code) {
    context.res = { status: 400, body: 'Missing code' };
    return;
  }

  if (!state || !cookieState || state !== cookieState) {
    context.res = { status: 400, body: 'Invalid state' };
    return;
  }

  try {
    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ client_id: clientId, client_secret: clientSecret, code, redirect_uri: redirectUri })
    });
    const tokenJson = await tokenRes.json();
    const token = tokenJson.access_token;
    if (!token) throw new Error(JSON.stringify(tokenJson));

    // HTML handshake compatible with Netlify CMS
    const html = `<!doctype html><html><body><script>
      (function() {
        function send() {
          var payload = 'authorization:github:success:' + JSON.stringify({token: '${token}'});
          window.opener.postMessage(payload, '*');
          window.close();
        }
        // Some versions expect a handshake — send and also listen
        window.addEventListener('message', function(e){ if (e.data === 'authorizing:github') send(); });
        // Kick things off
        send();
      })();
    </script></body></html>`;

    context.res = {
      status: 200,
      headers: { 'content-type': 'text/html; charset=utf-8' },
      body: html
    };
  } catch (err) {
    context.log('OAuth error', err);
    context.res = { status: 500, body: 'OAuth failure' };
  }
};

function getOrigin(req) {
  const hdr = (n) => (req.headers?.[n.toLowerCase()] || '');
  const proto = hdr('x-forwarded-proto') || 'https';
  const host = hdr('x-forwarded-host') || hdr('host');
  return `${proto}://${host}`;
}

function parseCookie(header) {
  return header.split(/;\s*/).reduce((acc, part) => {
    const i = part.indexOf('=');
    if (i > -1) acc[decodeURIComponent(part.slice(0, i))] = decodeURIComponent(part.slice(i + 1));
    return acc;
  }, {});
}

