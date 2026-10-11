import test from 'node:test';
import assert from 'node:assert/strict';
import { notation } from '../js/question-content.js';

test('Notation 1: Fractions render cleanly with semantic spans', () => {
  const result = notation('\\frac{a}{b}');
  assert.equal(result, '<span class="math-fraction"><span>a</span><span>b</span></span>');

  const nested = notation('\\frac{\\frac{1}{2}}{3}');
  assert.equal(nested, '<span class="math-fraction"><span><span class="math-fraction"><span>1</span><span>2</span></span></span><span>3</span></span>');
});

test('Notation 2: Square roots render with radical symbol and enclosed body', () => {
  const result = notation('\\sqrt{x^2 + y^2}');
  assert.equal(result, '<span class="math-sqrt"><span class="math-sqrt-radical">√</span><span class="math-sqrt-body">x<sup>2</sup> + y<sup>2</sup></span></span>');
});

test('Notation 3: Greek letters convert to proper Unicode symbols', () => {
  assert.equal(notation('\\alpha + \\beta = \\gamma'), 'α + β = γ');
  assert.equal(notation('\\sigma_{x} + \\tau_{xy}'), 'σ<sub>x</sub> + τ<sub>xy</sub>');
  assert.equal(notation('\\theta, \\phi, \\psi, \\omega, \\pi'), 'θ, φ, ψ, ω, π');
  assert.equal(notation('\\Gamma(y) \\text{ and } \\Delta P'), 'Γ(y) <span class="math-text"> and </span> Δ P');
});

test('Notation 4: Vectors, hats and unit vectors render cleanly', () => {
  const v = notation('\\vec{v}');
  assert.equal(v, '<span class="math-vec">v⃗</span>');

  assert.equal(notation('\\hat{i} + \\hat{j} + \\hat{k}'), 'î + ĵ + k̂');
});

test('Notation 5: Mathematical relations, operators and degrees render properly', () => {
  assert.equal(notation('a \\le b \\text{ and } c \\ge d'), 'a ≤ b <span class="math-text"> and </span> c ≥ d');
  assert.equal(notation('x \\neq y \\approx z'), 'x ≠ y ≈ z');
  assert.equal(notation('2 \\times 10^{-3} \\pm 0.01'), '2 × 10<sup>-3</sup> ± 0.01');
  assert.equal(notation('\\beta_1 = 44^\\circ'), 'β<sub>1</sub> = 44°');
});

test('Notation 6: Text, bold and math function names render upright', () => {
  assert.equal(notation('\\text{m/s}^2'), '<span class="math-text">m/s</span><sup>2</sup>');
  assert.equal(notation('\\textbf{Boundary Condition}'), '<strong>Boundary Condition</strong>');
  assert.equal(notation('\\sin x + \\cos y = \\ln z'), '<span class="math-fn">sin</span> x + <span class="math-fn">cos</span> y = <span class="math-fn">ln</span> z');
});

test('Notation 7: Sizing commands \\left and \\right are cleanly unwrapped', () => {
  assert.equal(notation('\\left( \\frac{L}{D} \\right)'), '( <span class="math-fraction"><span>L</span><span>D</span></span> )');
});

test('Notation 8: Security & XSS prevention is rigorously preserved', () => {
  assert.equal(notation('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
  assert.equal(notation('^{<img src=x onerror=alert(1)>}'), '<sup>&lt;img src=x onerror=alert(1)&gt;</sup>');
  assert.equal(notation('\\text{<b onmouseover=evil()>}'), '<span class="math-text">&lt;b onmouseover=evil()&gt;</span>');
});

test('Notation 9: Real GATE Aerospace exam expressions render accurately', () => {
  // GATE 2007 AE Q46 Euler buckling
  const q46 = notation('P_{cr} = \\frac{4\\pi^2 EI}{L^2}');
  assert.equal(q46, 'P<sub>cr</sub> = <span class="math-fraction"><span>4π<sup>2</sup> EI</span><span>L<sup>2</sup></span></span>');

  // GATE 2008 AE Q27 PDE / Laplacian
  const q27 = notation('\\nabla^2 u = 0');
  assert.equal(q27, '∇<sup>2</sup> u = 0');

  // GATE 2010 AE Q14 Dynamic viscosity
  const q14 = notation('\\mu = 7 \\times 10^{-3} \\text{ N}\\cdot\\text{s/m}^2');
  assert.equal(q14, 'μ = 7 × 10<sup>-3</sup> <span class="math-text"> N</span>·<span class="math-text">s/m</span><sup>2</sup>');

  // GATE 2026 AE GA Q10 Overline geometry
  const q10 = notation('\\overline{VY} = \\overline{VW} = 4\\text{ cm}');
  assert.equal(q10, '<span class="math-overline">VY</span> = <span class="math-overline">VW</span> = 4<span class="math-text"> cm</span>');
});
