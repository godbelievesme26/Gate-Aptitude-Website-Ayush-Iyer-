import json

with open('internal/ae/forensic_audit_2007_2026.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

summary = d['summary']
qs = d['questions']

out = []
out.append('# GATE Aerospace 2007-2026 Forensic Audit Report\n')
out.append('## Executive Summary')
out.append(f'- **Total Questions:** {summary["total_questions"]}')
out.append(f'- **PASS:** {summary["pass"]}')
out.append(f'- **FAIL:** {summary["fail"]}')
out.append(f'- **UNVERIFIABLE:** {summary["unverifiable"]}')
out.append(f'- **REQUIRES HUMAN REVIEW:** {summary["requires_human_review"]}\n')

out.append('## Per-Year Status Breakdown')
years = {}
for q in qs:
    y = q['year']
    st = q['status']
    if y not in years:
        years[y] = {'PASS': 0, 'FAIL': 0, 'UNVERIFIABLE': 0, 'REQUIRES_HUMAN_REVIEW': 0}
    years[y][st] += 1

for y in sorted(years.keys(), reverse=True):
    counts = years[y]
    out.append(f'- **AE{y}:** {counts["PASS"]} PASS, {counts["FAIL"]} FAIL, {counts["UNVERIFIABLE"]} UNVERIFIABLE')

out.append('\n## Categorical Failure Analysis')
fig_fails = [q['id'] for q in qs if any('Figure margin' in r for r in q['reasons'])]
prov_fails = [q['id'] for q in qs if any('Provenance' in r for r in q['reasons'])]
num_fails = [q['id'] for q in qs if any('Numbering' in r for r in q['reasons'])]
scan_unv = [q['id'] for q in qs if any('Image-only scan' in r for r in q['reasons'])]

out.append(f'### 1. Figure Margin Failures ({len(fig_fails)})')
out.append('These questions have tight crops or lack bounding boxes entirely. They must be re-rendered via the safe-margin algorithm.')
if fig_fails:
    out.append(f'Sample IDs: {", ".join(fig_fails[:5])} ...')

out.append(f'\n### 2. Answer Provenance Failures ({len(prov_fails)})')
out.append('These questions were tagged official key verified but lack a valid PDF source lineage (nswerSource.url).')
if prov_fails:
    out.append(f'Sample IDs: {", ".join(prov_fails[:5])} ...')

out.append(f'\n### 3. Numbering Discrepancies ({len(num_fails)})')
out.append('The JSON numbering differs from the physical printed PDF max question number.')
if num_fails:
    out.append(f'Sample IDs: {", ".join(num_fails[:5])} ...')

out.append(f'\n### 4. Image-Only / OCR-Unverifiable ({len(scan_unv)})')
out.append('These questions belong to scanned PDFs (e.g., AE2007, AE2008, AE2009, AE2010, AE2019, AE2021). The textual JSON content cannot be programmatically validated without OCR.')
if scan_unv:
    out.append(f'Sample IDs: {", ".join(scan_unv[:5])} ...')

out.append('\n## Recommended Repair Categories')
out.append('1. **Mass Demote Provenance:** Any question lacking a .pdf URL should have gradingStatus changed to provided answer key.')
out.append('2. **Run Global Safe-Margins:** Apply the collision-aware safe_margins_algo.py to all remaining years (2025-2011).')
out.append('3. **Manual OCR Verification Pass:** Implement a UI tool or human-review workflow for the 425 UNVERIFIABLE scanned questions.')

out.append('\n## Status Conclusion')
out.append('**AUDITED - REPAIR REQUIRED**')

with open('internal/ae/forensic_audit_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('Report generated')
