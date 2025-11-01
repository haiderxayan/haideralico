import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(__dirname, '..');
const source = resolve(projectRoot, 'src/assets/stayunfinished_emblem.svg');

const targets = [
	{ size: 32, name: 'favicon-32.png' },
	{ size: 180, name: 'apple-touch-icon.png' },
	{ size: 192, name: 'favicon-192.png' },
	{ size: 512, name: 'favicon-512.png' },
];

async function main() {
	await Promise.all(
		targets.map(async ({ size, name }) => {
			const outPath = resolve(projectRoot, 'public', name);
			await sharp(source)
				.resize(size, size, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
				.png()
				.toFile(outPath);
			console.log(`Generated ${name}`);
		}),
	);
}

main().catch((error) => {
	console.error('Failed to generate icons', error);
	process.exit(1);
});
