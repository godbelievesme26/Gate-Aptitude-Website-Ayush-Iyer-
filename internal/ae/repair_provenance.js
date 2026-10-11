const fs = require('fs');

const d = JSON.parse(fs.readFileSync('internal/ae/forensic_audit_granular.json', 'utf8'));

let demotedCount = 0;
let demotedIds = [];
let affectedYears = new Set();

const yearsToProcess = Array.from(new Set(d.questions.map(q => q.year)));

yearsToProcess.forEach(y => {
    let changed = false;
    const jsonPath = \data/ae/\.json\;
    if (!fs.existsSync(jsonPath)) return;
    
    const yearData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    
    yearData.questions.forEach(q => {
        const auditRecord = d.questions.find(aq => aq.id === q.id);
        if (auditRecord && auditRecord.components.answerProvenance === 'FAIL') {
            q.gradingStatus = 'provided answer key';
            q.answerSource = null;
            demotedCount++;
            demotedIds.push(q.id);
            affectedYears.add(y);
            changed = true;
        }
    });
    
    if (changed) {
        fs.writeFileSync(jsonPath, JSON.stringify(yearData, null, 2));
    }
});

fs.writeFileSync('internal/ae/demoted_provenance.json', JSON.stringify({
    count: demotedCount,
    affectedYears: Array.from(affectedYears).sort(),
    ids: demotedIds
}, null, 2));

console.log('Demoted Count:', demotedCount);
console.log('Affected Years:', Array.from(affectedYears).sort());
