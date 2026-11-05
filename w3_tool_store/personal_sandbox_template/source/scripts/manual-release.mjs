import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const read = path => readFileSync(resolve(root, path), 'utf8');
const hash = value => createHash('sha256').update(value).digest('hex');
const walk = path => readdirSync(resolve(root, path), { withFileTypes: true }).flatMap(entry => {
  const name = `${path}/${entry.name}`;
  return entry.isDirectory() ? walk(name) : [name];
});
const fail = message => { throw new Error(`Manual release check: ${message}`); };
const version = Number(read('core/appVersion.ts').match(/APP_VERSION_CODE = (\d+)/)?.[1]);
const versionName = read('core/appVersion.ts').match(/APP_VERSION_NAME = '([^']+)'/)?.[1];
const gradle = read('android-app/app/build.gradle');
if (!version || !versionName || Number(gradle.match(/versionCode (\d+)/)?.[1]) !== version || gradle.match(/versionName '([^']+)'/)?.[1] !== versionName) fail('Android and web version differ');
const manual = read('docs/คู่มือใช้งานภาษาไทย.md');
if (!manual.includes(`<!-- manual-version: ${version} -->`) || !manual.includes(`<!-- reviewed-version: ${version} -->`)) fail('guide version/review is missing');
const nav = [...read('features/editor/LeftNav.tsx').matchAll(/\{ id: '([^']+)', label:/g)].map(match => match[1]);
const required = [...nav, 'library', 'shared', 'battle', 'commands', 'update', 'storage', 'tileLibrary'];
for (const menu of required) {
  const marker = `<!-- menu: ${menu} -->`;
  if (!manual.includes(marker) || manual.split(marker)[1].split(/\n## /)[0].trim().length < 150) fail(`missing detailed section: ${menu}`);
}
// UI AND runtime changes invalidate the last explicit human/agent review.
const inputs = [...walk('features'), ...walk('ui'), ...walk('core'), 'types.ts', 'index.css', 'App.tsx', 'android-app/app/src/main/java/com/w3personalsandbox/app/MainActivity.java'].sort();
const expected = {
  schema: 'w3.sandbox.manual-release.v1', versionCode: version, versionName,
  manualSha256: hash(manual), sourceSha256: hash(inputs.map(path => `${path}\0${hash(read(path))}`).join('\n')),
  menus: required,
};
const path = 'public/release-info.json';
if (process.argv.includes('--review')) {
  writeFileSync(resolve(root, path), JSON.stringify(expected, null, 2) + '\n');
  writeFileSync(resolve(root, 'public/user-guide.md'), manual);
  console.log(`Recorded manual review for v${version}. Commit the guide and release-info together.`);
} else {
  if (read(path) !== JSON.stringify(expected, null, 2) + '\n' || read('public/user-guide.md') !== manual) fail('content changed since review; review every affected menu, then run npm run review:manual');
  if (process.argv.includes('--bundle')) {
    for (const file of ['release-info.json', 'user-guide.md']) {
      const bundled = `android-app/app/src/main/assets/www/${file}`;
      if (read(bundled) !== read(`public/${file}`)) fail(`stale bundled ${file}; rebuild web assets`);
    }
  }
  console.log(`Manual v${version}: versions, ${required.length} sections, source review and${process.argv.includes('--bundle') ? ' Android assets' : ' source'} match.`);
}
