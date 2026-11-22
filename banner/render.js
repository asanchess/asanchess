// Renders every out/*.html to PNG at its own size (node banner/render.js)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = path.join(__dirname, 'out');
  const browser = await chromium.launch();
  for (const f of fs.readdirSync(out).filter(f => f.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(out, f), 'utf8');
    const [w, h] = html.match(/html,body\{width:(\d+)px;height:(\d+)px/).slice(1).map(Number);
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
    await page.close();
    console.log('png', f);
  }
  await browser.close();
})();
