import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const url = process.env.W3_PROBE_URL || 'http://127.0.0.1:4173/';
const width = Number(process.env.W3_PROBE_WIDTH || 393);
const height = Number(process.env.W3_PROBE_HEIGHT || 873);
const output = resolve(process.env.W3_PROBE_OUTPUT || './output');
if (!/^https?:\/\/[^\s]+$/.test(url) || !Number.isInteger(width) || !Number.isInteger(height) || width < 240 || height < 400) {
  throw new Error('Set a valid W3_PROBE_URL and positive W3_PROBE_WIDTH/HEIGHT');
}

await mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width, height },
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true,
  userAgent: 'Mozilla/5.0 (Linux; Android 16; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
});
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const report = { url, viewport: { width, height }, screenshots: [], errors, checks: [] };
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  const capture = async name => {
    const path = resolve(output, `${name}.png`);
    await page.screenshot({ path, fullPage: true });
    report.screenshots.push(path);
  };
  await capture('home');
  const check = async label => {
    const result = await page.evaluate(() => ({
      bodyWidth: document.body.scrollWidth,
      viewportWidth: window.innerWidth,
      horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 2,
      scrollableElements: [...document.querySelectorAll('*')].filter(el => el.scrollHeight > el.clientHeight + 20 && getComputedStyle(el).overflowY !== 'hidden').length
    }));
    report.checks.push({ label, ...result });
  };
  await check('home');
  const openProject = page.getByRole('button', { name: /เปิด|open/i }).first();
  if (await openProject.count()) {
    await openProject.click();
    await capture('project');
    await check('project');
    const battle = page.getByText('Battle', { exact: true }).first();
    if (await battle.count()) {
      await battle.click();
      await capture('battle');
      await check('battle');
    }
  }
} finally {
  await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
console.log(JSON.stringify(report, null, 2));
if (errors.length || report.checks.some(item => item.horizontalOverflow)) process.exitCode = 1;
