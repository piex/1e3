const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser',
    dumpio: true,
    args: ['--no-sandbox', '--headless'],
    headless: true,
    timeout: 5000
  });
  console.log(await browser.version());
  const page = await browser.newPage();
  await page.goto('http://foreverz.cn');
  await page.screenshot({ path: 'example.png' });

  await browser.close();
})();
