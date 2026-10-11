import {esc} from './ui.js';
import {assetPath} from './corpus.js';

// A deliberately small notation grammar for source-reviewed exponents/subscripts.
// Text is always escaped; this is not an HTML or general Markdown interpreter.
const SYMBOLS = {
  '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
  '\\epsilon': 'ε', '\\varepsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η',
  '\\theta': 'θ', '\\vartheta': 'θ', '\\iota': 'ι', '\\kappa': 'κ',
  '\\lambda': 'λ', '\\mu': 'μ', '\\nu': 'ν', '\\xi': 'ξ',
  '\\pi': 'π', '\\varpi': 'ϖ', '\\rho': 'ρ', '\\varrho': 'ϱ',
  '\\sigma': 'σ', '\\varsigma': 'σ', '\\tau': 'τ', '\\upsilon': 'υ',
  '\\phi': 'φ', '\\varphi': 'ϕ', '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
  '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ',
  '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Upsilon': 'Υ',
  '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω',
  '\\times': '×', '\\cdot': '·', '\\pm': '±', '\\mp': '∓', '\\div': '÷',
  '\\approx': '≈', '\\neq': '≠', '\\ne': '≠',
  '\\leq': '≤', '\\le': '≤', '\\geq': '≥', '\\ge': '≥',
  '\\ll': '≪', '\\gg': '≫', '\\propto': '∝',
  '\\partial': '∂', '\\nabla': '∇',
  '\\infty': '∞', '\\circ': '°',
  '\\int': '∫', '\\iint': '∬', '\\oint': '∮', '\\sum': '∑', '\\prod': '∏',
  '\\to': '→', '\\rightarrow': '→', '\\longrightarrow': '⟶',
  '\\leftarrow': '←', '\\longleftarrow': '⟵', '\\leftrightarrow': '↔',
  '\\dots': '…', '\\cdots': '…', '\\quad': '  ', '\\qquad': '    ',
  '\\imath': 'i', '\\jmath': 'j',
  '\\oplus': '⊕', '\\odot': '⊙',
  '\\{': '{', '\\}': '}', '\\%': '%'
};

const MATH_FUNCTIONS = new Set([
  'sin', 'cos', 'tan', 'ln', 'log', 'exp', 'det', 'lim', 'max', 'min',
  'sinh', 'cosh', 'tanh', 'arcsin', 'arccos', 'arctan', 'sec', 'csc', 'cot'
]);

export function notation(value){
 let input=String(value??'').replace(/\$\$(.*?)\$\$/gs, '$1');
 function part(start,inside=false){
  let html='',plain='';
  const flush=()=>{html+=esc(plain);plain='';};
  for(let i=start;i<input.length;i++){
   if(inside&&input[i]==='}'){flush();return {html,end:i,closed:true};}

   // Degrees symbol ^\circ
   if(input.startsWith('^\\circ',i)){
    flush();html+='°';i+=5;continue;
   }

   // Fraction \frac{num}{den}
   if(input.startsWith('\\frac{',i)){
    const numerator=part(i+6,true),denominator=input[numerator.end+1]==='{'?part(numerator.end+2,true):null;
    if(numerator.closed&&denominator?.closed){flush();html+=`<span class="math-fraction"><span>${numerator.html}</span><span>${denominator.html}</span></span>`;i=denominator.end;continue;}
   }

   // Square root \sqrt{content}
   if(input.startsWith('\\sqrt{',i)){
    const child=part(i+6,true);
    if(child.closed){flush();html+=`<span class="math-sqrt"><span class="math-sqrt-radical">√</span><span class="math-sqrt-body">${child.html}</span></span>`;i=child.end;continue;}
   }

   // Matrix \matrix{...}
   if(input.startsWith('\\matrix{',i)){
    const end=input.indexOf('}',i+8);
    if(end!==-1){const rows=input.slice(i+8,end).split(';').map(row=>row.split('&'));if(rows.length&&rows.every(row=>row.length===rows[0].length)){flush();html+=`<span class="math-matrix" role="math" aria-label="${esc(rows.map(row=>row.join(', ')).join('; '))}" style="--matrix-columns:${rows[0].length}">${rows.flatMap(row=>row.map(cell=>`<span>${notation(cell.trim())}</span>`)).join('')}</span>`;i=end;continue;}}
   }

   // Overline \overline{...}
   if(input.startsWith('\\overline{',i)){
    const child=part(i+10,true);
    if(child.closed){flush();html+=`<span class="math-overline">${child.html}</span>`;i=child.end;continue;}
   }

   // Text labels \text{...}
   if(input.startsWith('\\text{',i)){
    const child=part(i+6,true);
    if(child.closed){flush();html+=`<span class="math-text">${child.html}</span>`;i=child.end;continue;}
   }

   // Bold text \textbf{...}
   if(input.startsWith('\\textbf{',i)){
    const child=part(i+8,true);
    if(child.closed){flush();html+=`<strong>${child.html}</strong>`;i=child.end;continue;}
   }

   // Vectors \vec{...}
   if(input.startsWith('\\vec{',i)){
    const child=part(i+5,true);
    if(child.closed){flush();html+=`<span class="math-vec">${child.html}⃗</span>`;i=child.end;continue;}
   }

   // Unit vectors / hats \hat{...}
   if(input.startsWith('\\hat{',i)){
    const child=part(i+5,true);
    if(child.closed){
     flush();
     if(child.html==='i'||child.html==='\\imath')html+='î';
     else if(child.html==='j'||child.html==='\\jmath')html+='ĵ';
     else if(child.html==='k')html+='k̂';
     else html+=`<span class="math-hat">${child.html}̂</span>`;
     i=child.end;continue;
    }
   }

   // Accents \bar{...} and \dot{...}
   if(input.startsWith('\\bar{',i)){
    const child=part(i+5,true);
    if(child.closed){flush();html+=`<span class="math-bar">${child.html}̄</span>`;i=child.end;continue;}
   }
   if(input.startsWith('\\dot{',i)){
    const child=part(i+5,true);
    if(child.closed){flush();html+=`<span class="math-dot">${child.html}̇</span>`;i=child.end;continue;}
   }

   // Delimiter sizing commands \left and \right
   if(input.startsWith('\\left',i)){
    const after=input.slice(i+5);
    if(after.startsWith('.')||after.startsWith('(')||after.startsWith('[')||after.startsWith('|')){
     flush();if(after[0]!=='.')plain+=after[0];i+=5;continue;
    }
   }
   if(input.startsWith('\\right',i)){
    const after=input.slice(i+6);
    if(after.startsWith('.')||after.startsWith(')')||after.startsWith(']')||after.startsWith('|')){
     flush();if(after[0]!=='.')plain+=after[0];i+=6;continue;
    }
   }

   // Braced Exponents and Subscripts ^{...} and _{...}
   if((input[i]==='^'||input[i]==='_')&&input[i+1]==='{'){
    const child=part(i+2,true);
    if(child.closed){flush();const tag=input[i]==='^'?'sup':'sub';html+=`<${tag}>${child.html}</${tag}>`;i=child.end;continue;}
   }

   // Single-character Exponents and Subscripts
   if(input[i]==='^'||input[i]==='_'){
    const m=input.slice(i+1).match(/^([+-]?[0-9a-zA-Z])/);
    if(m){
     flush();const tag=input[i]==='^'?'sup':'sub';html+=`<${tag}>${esc(m[1])}</${tag}>`;i+=m[1].length;continue;
    }
   }

   // TeX Symbols and functions
   if(input[i]==='\\'){
    if(input[i+1]===','||input[i+1]===';'||input[i+1]===':'){flush();plain+=' ';i+=1;continue;}
    if(input[i+1]==='!'){i+=1;continue;}
    const cmdMatch=input.slice(i).match(/^(\\[a-zA-Z]+|\\[}{%])/);
    if(cmdMatch){
     const cmd=cmdMatch[1],name=cmd.slice(1);
     if(SYMBOLS[cmd]){flush();plain+=SYMBOLS[cmd];i+=cmd.length-1;continue;}
     if(MATH_FUNCTIONS.has(name)){flush();html+=`<span class="math-fn">${esc(name)}</span>`;i+=cmd.length-1;continue;}
    }
   }

   // Inline math dollar sign delimiter
   if(input[i]==='$')continue;

   plain+=input[i];
  }
  flush();return {html,end:input.length,closed:false};
 }
 return part(0).html;
}

export const verifiedText=q=>q.transcriptionStatus==='source-verified';
export const optionShortcut=(q,key)=>q.type==='NAT'||!/^\d$/.test(key)?null:q.options?.[Number(key)-1]?.label??null;
function formatNatInterval(range) {
  if (typeof range === 'number') return String(range);
  if (Array.isArray(range)) {
    if (range.length === 2 && typeof range[0] === 'number' && typeof range[1] === 'number') {
      return range[0] === range[1] ? String(range[0]) : `${range[0]} to ${range[1]}`;
    }
    return range.map(formatNatInterval).join(' OR ');
  }
  return String(range ?? '');
}
export const questionAnswer=q=>q.type==='NAT'?formatNatInterval(q.answer):Array.isArray(q.answer)?q.answer.join(', '):String(q.answer ?? '');
function figure(asset,option=false){
 if(!asset?.source||!assetPath(asset.src))return '<p class="caption">Verified figure unavailable.</p>';
 return `<img class="${option?'option-figure':'content-figure'}" src="${esc(asset.src)}" alt="${esc(asset.alt)}" loading="eager">`;
}
export function optionContent(q,option){
 if(!verifiedText(q))return '<span class="option-copy">Verified option content unavailable.</span>';
 return `<span class="option-copy">${option?.content?contentBlocks(option.content,true):`${option?.text?`<span>${notation(option.text)}</span>`:''}${option?.figure?figure(option.figure,true):''}`}</span>`;
}
export function contentBlocks(blocks,option=false){return blocks.map(block=>{
 if(block.type==='text')return `<${option?'span':'p'} class="question-stem">${notation(block.text)}</${option?'span':'p'}>`;
 if(block.type==='math')return `<span class="content-math">${notation(block.text)}</span>`;
 if(block.type==='figure')return figure(block.asset,option);
 if(block.type==='table')return `<div class="content-table-wrap" tabindex="0" role="region" aria-label="${esc(block.label||'Question table')}"><table class="content-table">${block.label?`<caption class="sr-only">${esc(block.label)}</caption>`:''}${block.headers?`<thead><tr>${block.headers.map(cell=>`<th scope="col">${notation(cell)}</th>`).join('')}</tr></thead>`:''}<tbody>${block.rows.map(row=>`<tr>${row.map((cell,i)=>block.rowHeaders&&i===0?`<th scope="row">${notation(cell)}</th>`:`<td>${notation(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
 return '<p class="caption">Verified content block unavailable.</p>';
}).join('');}
export function questionContent(q,solving=false){
 if(!verifiedText(q))return '<div class="notice" role="status">This question’s content is being verified. Please choose another question.</div>';
 if(q.content){const shared=q.group?`<section class="question-group" aria-label="Shared question context">${contentBlocks(q.group.content)}</section>`:'';return `<div class="question-content">${shared}${contentBlocks(q.content)}</div>${!solving&&q.type!=='NAT'?`<ol class="detail-options">${q.options.map(o=>`<li><span class="option-letter">${esc(o.label)}</span>${optionContent(q,o)}</li>`).join('')}</ol>`:''}`;}
 const table=q.table?`<div class="content-table-wrap"><table class="content-table ${q.table.grouped?'content-table-grouped':''}">${q.table.label?`<caption class="sr-only">${esc(q.table.label)}</caption>`:''}${q.table.headers?`<thead><tr>${q.table.headers.map(x=>`<th scope="col">${notation(x)}</th>`).join('')}</tr></thead>`:''}<tbody>${q.table.rows.map(row=>`<tr>${row.map((x,i)=>q.table.rowHeaders&&i===0?`<th scope="row">${notation(x)}</th>`:`<td>${notation(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:'';
 const figures=(q.figures||[]).map(f=>`<figure>${f.caption?`<figcaption>${esc(f.caption)}</figcaption>`:''}${figure(f)}</figure>`).join('');
 return `<div class="question-content">${q.figureSequence?'':`<p class="question-stem">${notation(q.question)}</p>`}${table}${q.afterTable?`<p class="question-stem">${notation(q.afterTable)}</p>`:''}${figures?`<div class="question-figures ${q.figureSequence?'figure-sequence':''}">${figures}</div>`:''}</div>${!solving&&q.type!=='NAT'?`<ol class="detail-options">${q.options.map(o=>`<li><span class="option-letter">${esc(o.label)}</span>${optionContent(q,o)}</li>`).join('')}</ol>`:''}`;
}

// Previews share verification and notation rules, without leaking options or solutions.
export function questionPreview(q){
 if(!verifiedText(q))return questionContent(q,true);
 return `<p class="question-preview">${notation(q.question)}</p>`;
}
