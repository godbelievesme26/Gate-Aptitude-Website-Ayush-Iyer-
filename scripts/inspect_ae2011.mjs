import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';
import fs from 'fs';

async function dumpPdf(pdfPath) {
  const data = new Uint8Array(fs.readFileSync(pdfPath));
  const doc = await pdfjs.getDocument({ data }).promise;
  console.log(`=== ${pdfPath} (Pages: ${doc.numPages}) ===`);
  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    console.log(`--- Page ${i} ---`);
    let lastY = null;
    let line = '';
    for (const item of content.items) {
      if (lastY !== null && Math.abs(item.transform[5] - lastY) > 5) {
        console.log(line);
        line = '';
      }
      line += (line ? ' ' : '') + item.str;
      lastY = item.transform[5];
    }
    if (line) console.log(line);
  }
}

async function run() {
  await dumpPdf('internal/ae/AE2011-key.pdf');
}

run().catch(console.error);
