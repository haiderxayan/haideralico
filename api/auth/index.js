// Azure Function: /api/auth
// Starts GitHub OAuth flow for Netlify CMS GitHub backend

module.exports = async function (context, req) {
  const clientId = process.env.GITHUB_CLIENT_ID;
  const redirectUri = process.env.OAUTH_REDIRECT_URI || `${getOrigin(req)}/api/callback`;
  const scope = process.env.GITHUB_SCOPE || 'repo,user';

  if (!clientId) {
    context.res = {
      status: 500,
      headers: { 'content-type': 'text/plain' },
      body: 'Missing GITHUB_CLIENT_ID environment variable.'
    };
    return;
  }

  const state = Math.random().toString(36).slice(2);
  const authorizeUrl = new URL('https://github.com/login/oauth/authorize');
  authorizeUrl.searchParams.set('client_id', clientId);
  authorizeUrl.searchParams.set('redirect_uri', redirectUri);
  authorizeUrl.searchParams.set('scope', scope);
  authorizeUrl.searchParams.set('state', state);

  context.res = {
    status: 302,
    headers: {
      Location: authorizeUrl.toString(),
      'Set-Cookie': `oauth_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax`
    }
  };
};

function getOrigin(req) {
  // Try to infer the public origin for redirects
  const hdr = (name) => (req.headers?.[name.toLowerCase()] || '');
  const proto = hdr('x-forwarded-proto') || 'https';
  const host = hdr('x-forwarded-host') || hdr('host');
  return `${proto}://${host}`;
}

