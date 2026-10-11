import fs from 'node:fs';

const paper = JSON.parse(fs.readFileSync('data/ae/2015.json', 'utf8'));

function polishText(text) {
  if (typeof text !== 'string') return text;
  let s = text;
  // Replace LaTeX macros with clean Unicode
  s = s.replace(/\\times/g, '×');
  s = s.replace(/\\le\b/g, '≤');
  s = s.replace(/\\ge\b/g, '≥');
  s = s.replace(/\\leq\b/g, '≤');
  s = s.replace(/\\geq\b/g, '≥');
  s = s.replace(/\\pm\b/g, '±');
  s = s.replace(/\\mp\b/g, '∓');
  s = s.replace(/\\cdot/g, '·');
  s = s.replace(/\\infty/g, '∞');
  s = s.replace(/\\partial/g, '∂');
  s = s.replace(/\\approx/g, '≈');
  s = s.replace(/\\neq/g, '≠');
  s = s.replace(/\\alpha/g, 'α');
  s = s.replace(/\\beta/g, 'β');
  s = s.replace(/\\gamma/g, 'γ');
  s = s.replace(/\\theta/g, 'θ');
  s = s.replace(/\\mu/g, 'μ');
  s = s.replace(/\\rho/g, 'ρ');
  s = s.replace(/\\pi/g, 'π');
  s = s.replace(/\\phi/g, 'ϕ');
  s = s.replace(/\\omega/g, 'ω');
  s = s.replace(/\\lambda/g, 'λ');
  s = s.replace(/\\tau/g, 'τ');
  s = s.replace(/\\sigma/g, 'σ');
  s = s.replace(/\\Delta/g, 'Δ');
  s = s.replace(/\\text\{([^}]+)\}/g, '$1');
  s = s.replace(/\$/g, ''); // strip unnecessary $ delimiters since notation() parses natively
  // Fix exponents/subscripts to standard ^{...} and _{...}
  s = s.replace(/\^([0-9a-zA-Z+-])/g, '^{$1}');
  s = s.replace(/_([0-9a-zA-Z+-])/g, '_{$1}');
  return s;
}

for (const q of paper.questions) {
  q.question = polishText(q.question);
  if (Array.isArray(q.options)) {
    for (const opt of q.options) {
      if (opt.text) {
        opt.text = polishText(opt.text);
      }
    }
  }
}

fs.writeFileSync('data/ae/2015.json', JSON.stringify(paper, null, 2) + '\n');
console.log('Polished 2015 text and formulas.');
