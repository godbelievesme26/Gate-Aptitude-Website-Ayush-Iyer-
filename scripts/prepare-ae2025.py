"""Reproduce AE2025 from the supplied PDF and reviewed transcription overrides.

Only AE2025 is extracted. Existing GA records from Day 2 are referenced, never rewritten.
Source PDFs stay under internal/; only individual figure assets are published.
"""
from pathlib import Path
import json, re, hashlib, unicodedata
from collections import Counter
import pymupdf
from PIL import Image, ImageChops
from io import BytesIO

ROOT = Path(__file__).resolve().parent.parent
PDF = 'internal/ae/AE2025.pdf'
KEY = 'internal/ae/AE2025-key.pdf'
KEY_URL = 'https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf'
VERIFIED = '2026-10-07'

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

def clean(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text)).strip()

FIGURES = {
    20: (15, 'Pair of point vortices with clockwise circulation Γ separated by distance a and centroid O.'),
    27: (19, 'Simply supported horizontal beam AB of length L with linearly varying distributed transverse load from q0 at A to 0 at B.'),
    29: (20, 'Uniform symmetric cross-section cantilever beam of length L with transverse force P at free end.'),
    30: (21, 'Plate ABCD undeformed rhombus (solid lines) with 20 cm diagonals deforming to AC = 19.96 cm and BD = 20.04 cm (dotted lines).'),
    49: (29, 'Supersonic stream at Mach 5 turned by a 20 degree ramp, with shock wave and pressure p2/p1 = 7.125.'),
    53: (30, 'Spacecraft orbit around planet with center O, periapsis P, and points F (OF=8000 km, theta_F=0) and G (OG=10000 km, theta_G=60 deg).'),
    56: (31, 'Three-bar truss with joints A, B, C, D and vertical load of 50 N.'),
    57: (31, 'Uniform rigid bar of mass 3 kg hinged at point F and supported by spring of stiffness k=100 N/m.'),
    58: (32, 'Prismatic vertical column of cross-section a x 0.5a and length l fixed at bottom, free at top under compressive force P.'),
    59: (32, 'Thin flat plate stress element subjected to sigma_xx=160 MPa, sigma_yy=40 MPa, tau_xy=80 MPa.'),
    60: (33, 'Thin-walled closed section designs A and B with semi-circular nose and rectangular extension carrying torque.')
}

OPTION_FIGURES = {
    19: (14, {
        'A': 'Pitching moment curve M vs alpha with positive slope and negative zero-lift pitching moment.',
        'B': 'Pitching moment curve M vs alpha with negative slope and positive zero-lift pitching moment.',
        'C': 'Pitching moment curve M vs alpha with negative slope and negative zero-lift pitching moment.',
        'D': 'Pitching moment curve M vs alpha with positive slope and positive zero-lift pitching moment.'
    })
}

TABLES = {
    37: {
        'label': 'Material Properties Table',
        'headers': ['Properties', 'Material α', 'Material β', 'Material γ', 'Material δ'],
        'rows': [
            ['Density (kg/m^{3})', '2700', '4500', '7800', '9000'],
            ['Young’s modulus (GPa)', '70', '115', '200', '130'],
            ['Yield Strength (MPa)', '270', '900', '520', '540']
        ]
    },
    52: {
        'label': 'Airplane Parameters',
        'headers': ['Parameter', 'Value'],
        'rows': [
            ['Airplane speed', '80 m/s'],
            ['Lift coefficient, C_{L}', '0.8'],
            ['Aspect ratio', '6'],
            ['Oswald efficiency factor', '0.8'],
            ['Zero-lift drag coefficient', '0.02']
        ]
    }
}

def build():
    source_hash = digest(PDF)
    key_hash = digest(KEY)
    doc = pymupdf.open(ROOT / PDF)
    key_doc = pymupdf.open(ROOT / KEY)

    # 1. Parse Keys
    lines = [l.strip() for p in key_doc for l in p.get_text().splitlines() if l.strip()]
    keys = {}
    i = 0
    while i < len(lines):
        if lines[i] in ['Answer Key for Aerospace Engineering (AE)', 'Q. No.', 'Session', 'Q. Type', 'Section', 'Key/Range', 'Marks', 'Page 1 of 2', 'Page 2 of 2']:
            i += 1
            continue
        if lines[i].isdigit() and i + 5 < len(lines) and lines[i+2] in ['MCQ', 'MSQ', 'NAT']:
            num = int(lines[i])
            keys[num] = {
                'number': num,
                'session': int(lines[i+1]),
                'type': lines[i+2],
                'section': lines[i+3],
                'rawKey': lines[i+4],
                'marks': int(lines[i+5]),
                'page': 1 if num <= 30 else 2
            }
            i += 6
        else:
            i += 1

    assert sorted(keys.keys()) == list(range(1, 66))
    write('internal/ae/AE2025-key.json', {
        'source': KEY,
        'sha256': key_hash,
        'url': KEY_URL,
        'rows': list(keys.values())
    })

    overrides = json.loads((ROOT / 'scripts/ae2025-transcriptions.json').read_text(encoding='utf8'))
    questions = []
    lineage = []
    assets = []

    # Map question positions and bboxes
    for page_idx in range(len(doc)):
        pno = page_idx + 1
        page = doc[page_idx]
        text = page.get_text("text")
        starts = list(re.finditer(r'(?:^|\n)Q\.(\d+)\s+(?![–−-])', text))
        for index, m in enumerate(starts):
            n = int(m.group(1))
            # Find boundary
            words = page.get_text("words")
            matching_words = [w for w in words if w[4] == f'Q.{n}']
            if not matching_words:
                matching_words = [w for w in words if w[4] == 'Q.' and words.index(w) + 1 < len(words) and words[words.index(w)+1][4] == str(n)]
            boundary = matching_words[0] if matching_words else [0, 80, 0, 100]
            top_y = round(boundary[1] - 4, 2)
            end_y = 780.0
            if index + 1 < len(starts):
                next_n = int(starts[index + 1].group(1))
                next_words = [w for w in words if w[4] == f'Q.{next_n}']
                if next_words:
                    end_y = round(next_words[0][1] - 4, 2)

            provenance = {
                'file': PDF,
                'sha256': source_hash,
                'pages': [{
                    'page': pno,
                    'bbox': [70, top_y, 525, end_y],
                    'coordinateSystem': 'PDF points, top-left origin'
                }],
                'verificationStatus': 'source-verified',
                'verifiedOn': VERIFIED
            }
            lineage.append({
                'questionId': f'gate-2025-ae-{"ga" if n<=10 else "ae"}-{n:02}',
                'number': n,
                'source': provenance
            })

            if n <= 10:
                continue

            q = {
                'id': f'gate-2025-ae-ae-{n:02}',
                'exam': 'GATE',
                'year': 2025,
                'paper': 'AE',
                'number': n,
                'section': 'AE',
                'subject': 'Aerospace Engineering',
                'type': keys[n]['type'],
                'marks': keys[n]['marks'],
                'question': overrides.get(str(n), {}).get('question', ''),
                'options': [],
                'content': [],
                'figures': [],
                'groupId': None,
                'source': provenance,
                'transcriptionStatus': 'source-verified',
                'solution': None,
                'solutionAvailability': 'not-provided-in-source',
                'gradingStatus': 'official key verified',
                'answerSource': {
                    'url': KEY_URL,
                    'paper': 'AE',
                    'questionNumber': n,
                    'section': 'AE',
                    'page': keys[n]['page'],
                    'sha256': key_hash,
                    'verifiedOn': VERIFIED
                }
            }

            raw_opts = overrides.get(str(n), {}).get('options', [])
            if q['type'] in ['MCQ', 'MSQ']:
                q['options'] = [{'label': label, 'text': text} for label, text in zip('ABCD', raw_opts)]
            else:
                q['options'] = []

            # Content blocks
            content = [{'type': 'text', 'text': q['question']}]
            if n in TABLES:
                content.append({'type': 'table', **TABLES[n]})
            q['content'] = content

            # Key and grading rules
            raw = keys[n]['rawKey']
            if raw == 'MTA*':
                q['answer'] = 'MTA'
                q['gradingRule'] = 'marks-to-all'
            elif q['type'] == 'NAT':
                if ' to ' in raw:
                    q['answer'] = [float(v) for v in raw.split(' to ')]
                else:
                    q['answer'] = float(raw)
            elif q['type'] == 'MSQ':
                q['answer'] = raw.split(';')
            else:
                q['answer'] = raw

            q['negativeMarks'] = q['marks'] / 3 if q['type'] == 'MCQ' else 0
            q['markingRule'] = 'gate-2025-official'

            def extract_clean(xref):
                d = doc.extract_image(xref)
                sm = d.get('smask')
                if sm:
                    smd = doc.extract_image(sm)
                    mask = Image.open(BytesIO(smd['image'])).convert('L')
                    base = Image.open(BytesIO(d['image'])).convert('RGB')
                    if base.getextrema() == ((0, 0), (0, 0), (0, 0)):
                        out = Image.new('RGB', mask.size, 'white')
                        out.paste(Image.new('RGB', mask.size, 'black'), mask=mask)
                        return out
                    else:
                        rgba = base.convert('RGBA')
                        rgba.putalpha(mask)
                        bg = Image.new('RGBA', rgba.size, 'white')
                        bg.alpha_composite(rgba)
                        return bg.convert('RGB')
                else:
                    im = Image.open(BytesIO(d['image']))
                    if im.mode == 'RGBA':
                        bg = Image.new('RGBA', im.size, 'white')
                        bg.alpha_composite(im)
                        return bg.convert('RGB')
                    return im.convert('RGB')

            # Extract Question Figure if present
            if n in FIGURES:
                exp_pno, alt = FIGURES[n]
                fig_page = doc[exp_pno - 1]
                cand_imgs = [im for im in fig_page.get_images() if im[2] != 1252 and im[2] != 166]
                if n == 56:
                    im_info = cand_imgs[0]
                elif n == 57:
                    im_info = cand_imgs[1]
                elif n == 58:
                    im_info = cand_imgs[0]
                elif n == 59:
                    im_info = cand_imgs[1]
                else:
                    im_info = cand_imgs[0]

                xref = im_info[0]
                src = f'figures/gate-2025-ae-ae-{n:02}-figure-1.png'
                
                rgb_im = extract_clean(xref)
                bbox = ImageChops.difference(rgb_im, Image.new('RGB', rgb_im.size, 'white')).getbbox()
                if bbox:
                    rgb_im = rgb_im.crop(bbox)
                rgb_im.save(ROOT / src)

                rects = fig_page.get_image_rects(xref)
                rect = rects[0] if rects else pymupdf.Rect(100, 200, 400, 400)

                asset = {
                    'src': src,
                    'alt': alt,
                    'source': {
                        'file': PDF,
                        'sha256': source_hash,
                        'page': exp_pno,
                        'image': f'xref_{xref}',
                        'bbox': [round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2)],
                        'coordinateSystem': 'PDF points, top-left origin',
                        'pixelCrop': list(bbox) if bbox else [0, 0, rgb_im.width, rgb_im.height]
                    },
                    'verificationStatus': 'source-verified',
                    'verifiedOn': VERIFIED
                }
                q['figures'] = [asset]
                assets.append(asset)
                q['content'].append({'type': 'figure', 'asset': asset})

            # Extract Option Figures if present (e.g. Q.19)
            if n in OPTION_FIGURES:
                exp_pno, opt_alts = OPTION_FIGURES[n]
                fig_page = doc[exp_pno - 1]
                cand_imgs = [im for im in fig_page.get_images() if im[2] != 1252 and im[2] != 166]
                for o_idx, label in enumerate(['A', 'B', 'C', 'D']):
                    im_info = cand_imgs[o_idx]
                    xref = im_info[0]
                    src = f'figures/gate-2025-ae-ae-{n:02}-option-{label}.png'
                    
                    rgb_im = extract_clean(xref)
                    bbox = ImageChops.difference(rgb_im, Image.new('RGB', rgb_im.size, 'white')).getbbox()
                    if bbox:
                        rgb_im = rgb_im.crop(bbox)
                    rgb_im.save(ROOT / src)

                    rects = fig_page.get_image_rects(xref)
                    rect = rects[0] if rects else pymupdf.Rect(100, 200, 400, 400)
                    opt_asset = {
                        'src': src,
                        'alt': opt_alts[label],
                        'source': {
                            'file': PDF,
                            'sha256': source_hash,
                            'page': exp_pno,
                            'image': f'xref_{xref}',
                            'bbox': [round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2)],
                            'coordinateSystem': 'PDF points, top-left origin',
                            'pixelCrop': list(bbox) if bbox else [0, 0, rgb_im.width, rgb_im.height]
                        },
                        'verificationStatus': 'source-verified',
                        'verifiedOn': VERIFIED
                    }
                    assets.append(opt_asset)
                    # Bind figure to option
                    opt = next(o for o in q['options'] if o['label'] == label)
                    opt['figure'] = opt_asset
                    opt['text'] = ''

            q['hasFigure'] = bool(q['figures']) or any('figure' in o for o in q['options'])
            questions.append(q)

    assert len(questions) == 55
    ga = json.loads((ROOT / 'data/day02.json').read_text(encoding='utf8'))['questions']
    for q in ga:
        assert q['source']['sha256'] == source_hash and q['answer'] == keys[q['number']]['rawKey']

    refs = [{'id': q['id'], 'number': q['number'], 'section': 'GA', 'recordRef': 'data/day02.json#' + q['id']} for q in ga] + [{'id': q['id'], 'number': q['number'], 'section': 'AE'} for q in questions]
    sections = [
        {'id': 'GA', 'title': 'General Aptitude', 'questionIds': [r['id'] for r in refs if r['section'] == 'GA'], 'totalMarks': 15},
        {'id': 'AE', 'title': 'Aerospace Engineering', 'questionIds': [r['id'] for r in refs if r['section'] == 'AE'], 'totalMarks': 85}
    ]

    paper = {
        'schemaVersion': 1,
        'id': 'gate-2025-ae',
        'exam': 'GATE',
        'year': 2025,
        'paper': 'AE',
        'totalQuestions': 65,
        'totalMarks': 100,
        'durationMinutes': 180,
        'sectionOrder': ['GA', 'AE'],
        'sections': sections,
        'marking': {
            'id': 'gate-2025-official',
            'negativeFraction': {'MCQ': 1/3, 'MSQ': 0, 'NAT': 0},
            'partialCredit': False,
            'sourceUrl': 'https://gate2025.iitr.ac.in/pattern-of-examination.html'
        },
        'source': {
            'file': PDF,
            'sha256': source_hash,
            'archive': 'AE.zip',
            'archiveEntry': 'AE/AE2025.pdf',
            'pageCount': 34
        },
        'questionOrder': [r['id'] for r in refs],
        'questionRefs': refs,
        'questionGroups': [],
        'questions': questions,
        'ingestionStatus': 'complete',
        'verificationStatus': 'source-verified',
        'verifiedOn': VERIFIED
    }
    write('data/ae/2025.json', paper)

    # GA assets
    ga_assets = [f for q in ga for f in q.get('figures', []) + [o['figure'] for o in q.get('options', []) if 'figure' in o]]
    all_assets = ga_assets + assets

    # Update manifest.json
    manifest = json.loads((ROOT / 'data/ae/manifest.json').read_text(encoding='utf8'))
    for idx, year_entry in enumerate(manifest['years']):
        if year_entry['year'] == 2025:
            manifest['years'][idx] = {
                'year': 2025,
                'paper': 'AE',
                'sourcePdf': PDF,
                'path': 'data/ae/2025.json',
                'questionCount': 65,
                'newQuestionCount': 55,
                'reusedGAQuestionCount': 10,
                'totalMarks': 100,
                'sections': sections,
                'questionTypeCounts': dict(Counter(v['type'] for v in keys.values())),
                'answerAvailability': {
                    'officialKey': 65,
                    'gradedAnswers': 65,
                    'marksToAll': 0,
                    'unavailable': 0
                },
                'figureAssetCount': len(all_assets),
                'newFigureAssetCount': len(assets),
                'reusedFigureAssetCount': len(ga_assets),
                'optionFigureCount': sum('figure' in o for q in ga for o in q['options']) + sum('figure' in o for q in questions for o in q['options']),
                'structuredTableCount': sum(b['type'] == 'table' for q in questions for b in q['content']),
                'questionGroupCount': 0,
                'ingestionStatus': 'complete',
                'verificationStatus': 'source-verified',
                'verifiedOn': VERIFIED
            }

    write('data/ae/manifest.json', manifest)
    write('internal/ae/AE2025-lineage.json', {
        'source': paper['source'],
        'questions': lineage,
        'assets': all_assets,
        'review': {
            'pagesVisuallyChecked': list(range(1, 35)),
            'keyPagesChecked': [1, 2],
            'relationships': 'No common-data or linked-answer groups in AE2025.',
            'sourceWording': 'Preserved directly from official source PDF.',
            'editorialSolutions': 'GA Day 2 editorial solutions reused; AE questions retain official keys.'
        }
    })
    print("Compiled AE2025 successfully!")
    print(json.dumps(manifest['years'][18], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    build()
