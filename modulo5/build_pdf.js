// Genera los PDF de la entrega con Chromium (Playwright).
// Uso: node modulo5/build_pdf.js
// Las capturas se leen de modulo5/entrega/capturas/ (1_..., 2_..., 3_...png); si falta alguna, se imprime un recuadro indicativo.
const path = require('path');
const { chromium } = require('playwright');

const jobs = [
  ['base_conocimiento/Manual_Comercial_NexoDigital_v3.1.html', 'base_conocimiento/Manual_Comercial_NexoDigital_v3.1.pdf'],
  ['entrega/informe.html', 'entrega/PreEntrega_Modulo5_SandraMaureira.pdf'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [src, out] of jobs) {
    await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'load' });
    await page.pdf({
      path: path.join(__dirname, out), format: 'A4', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="font-size:7pt;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    });
    console.log('OK', out);
  }
  await browser.close();
})();
