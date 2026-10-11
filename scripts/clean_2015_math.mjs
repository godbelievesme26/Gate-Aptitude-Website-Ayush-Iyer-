import fs from 'node:fs';

const paper = JSON.parse(fs.readFileSync('data/ae/2015.json', 'utf8'));

function cleanMath(text) {
  if (typeof text !== 'string') return text;
  let s = text;
  // Replace \( and \) with $
  s = s.replace(/\\\(/g, '$').replace(/\\\)/g, '$');
  // Replace double-escaped \text with \text
  s = s.replace(/\\text\{/g, '\\text{');
  // Clean cm\(^2\) -> $\text{cm}^2$
  s = s.replace(/cm\(\^2\)/g, '$\\text{cm}^2$');
  s = s.replace(/cm\^2/g, '$\\text{cm}^2$');
  // If consecutive $$ without space between separate inline items, fix
  // Clean up any other weird artifacts
  return s;
}

for (const q of paper.questions) {
  q.question = cleanMath(q.question);
  if (Array.isArray(q.options)) {
    for (const opt of q.options) {
      if (opt.text) {
        opt.text = cleanMath(opt.text);
      }
    }
  }
}

fs.writeFileSync('data/ae/2015.json', JSON.stringify(paper, null, 2) + '\n');
console.log('Cleaned math formatting in data/ae/2015.json');
