// Genera el PDF del informe a partir de informe.html (uso: node generar_pdf.js)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'informe.html'), { waitUntil: 'load' });
  await page.pdf({ path: path.resolve(__dirname, 'PreEntrega7_S_Maureira.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})();
