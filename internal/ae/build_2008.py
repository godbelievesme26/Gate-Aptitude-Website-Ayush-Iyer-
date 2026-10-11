import json
import hashlib
import os

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

PDF_PATH = 'internal/ae/AE2008.pdf'
KEY_PDF_PATH = 'internal/ae/AE2008-key.pdf'
pdf_hash = sha256_file(PDF_PATH)
key_pdf_hash = sha256_file(KEY_PDF_PATH)

# Figure assets hashes
figures_info = {}
for fig in [
    'figures/gate-2008-ae-ae-32-figure-1.png',
    'figures/gate-2008-ae-ae-51-figure-1.png',
    'figures/gate-2008-ae-ae-63-figure-1.png',
    'figures/gate-2008-ae-ae-65-figure-1.png',
    'figures/gate-2008-ae-ae-66-figure-1.png',
    'figures/gate-2008-ae-ae-66-figure-2.png',
    'figures/gate-2008-ae-ae-67-figure-1.png',
    'figures/gate-2008-ae-ae-69-figure-1.png',
    'figures/gate-2008-ae-ae-84-figure-1.png',
]:
    figures_info[fig] = {
        'file': fig,
        'sha256': sha256_file(fig)
    }

# Key answers
key_answers = {
    1: 'D', 2: 'D', 3: 'C', 4: 'A', 5: 'D', 6: 'C', 7: 'C', 8: 'A', 9: 'B', 10: 'B',
    11: 'C', 12: 'B', 13: 'D', 14: 'B', 15: 'C', 16: 'A', 17: 'B', 18: 'C', 19: 'C', 20: 'A',
    21: 'D', 22: 'B', 23: 'C', 24: 'D', 25: 'B', 26: 'A', 27: 'B', 28: 'A', 29: 'D', 30: 'B',
    31: 'B', 32: 'A', 33: 'D', 34: 'B', 35: 'D', 36: 'B', 37: 'A', 38: 'A', 39: 'B', 40: 'B',
    41: 'A', 42: 'C', 43: 'D', 44: 'D', 45: 'B', 46: 'D', 47: 'A', 48: 'A', 49: 'D', 50: 'A',
    51: 'A', 52: 'A', 53: 'A', 54: 'B', 55: 'D', 56: 'A', 57: 'C', 58: 'D', 59: 'D', 60: 'C',
    61: 'D', 62: 'B', 63: 'D', 64: 'A', 65: 'B', 66: 'C', 67: 'A', 68: 'C', 69: 'C', 70: 'B',
    71: 'A', 72: 'C', 73: 'B', 74: 'D', 75: 'C', 76: 'C', 77: 'D', 78: 'B', 79: 'C', 80: 'B',
    81: 'B', 82: 'B', 83: 'B', 84: 'A', 85: 'B'
}

# Key JSON
key_rows = []
for q_num in range(1, 86):
    marks = 1 if q_num <= 20 else 2
    key_rows.append({
        'number': q_num,
        'type': 'MCQ',
        'section': 'AE',
        'rawKey': key_answers[q_num],
        'marks': marks
    })

key_json = {
    'paper': 'AE2008',
    'source': KEY_PDF_PATH,
    'sha256': key_pdf_hash,
    'rows': key_rows
}

with open('internal/ae/AE2008-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_json, f, indent=2)
    f.write('\n')

def get_page_for_q(n):
    if 1 <= n <= 6: return 2
    if 7 <= n <= 17: return 3
    if 18 <= n <= 25: return 4
    if 26 <= n <= 31: return 5
    if 32 <= n <= 37: return 6
    if 38 <= n <= 46: return 7
    if 47 <= n <= 54: return 8
    if 55 <= n <= 62: return 9
    if 63 <= n <= 65: return 10
    if 66 <= n <= 68: return 11
    if 69 <= n <= 73: return 12
    if 74 <= n <= 81: return 13
    if 82 <= n <= 85: return 14
    return 1

# Build Questions
questions = []

def make_q(number, marks, body, options, answer, negative_marks=None, group_id=None):
    negative_marks = marks * 0.25
    q_id = f'gate-2008-ae-ae-{number:02d}'
    page_num = get_page_for_q(number)

    q_texts = []
    q_figures = []
    for item in body:
        if item['type'] == 'text':
            q_texts.append(item['text'])
        elif item['type'] in ('figure', 'image'):
            src = item['src']
            alt = item['alt']
            q_figures.append({
                'src': src,
                'alt': alt,
                'source': {
                    'file': PDF_PATH,
                    'page': page_num,
                    'sha256': pdf_hash
                },
                'verificationStatus': 'source-verified'
            })

    formatted_options = []
    for opt in options:
        label = opt.get('label') or opt.get('id')
        text = opt.get('text')
        if text is None and 'content' in opt:
            text = opt['content'][0]['text']
        formatted_options.append({
            'label': label,
            'text': text
        })

    q_obj = {
        'id': q_id,
        'number': number,
        'year': 2008,
        'paper': 'AE',
        'section': 'AE',
        'subject': 'Aerospace Engineering',
        'type': 'MCQ',
        'marks': marks,
        'negativeMarks': negative_marks,
        'question': '\n'.join(q_texts),
        'options': formatted_options,
        'answer': answer,
        'acceptedAnswers': [answer],
        'markingRule': 'gate-2008-official',
        'hasFigure': len(q_figures) > 0,
        'figures': q_figures,
        'groupId': group_id,
        'source': {
            'paper': 'AE',
            'year': 2008,
            'questionNumber': number,
            'section': 'AE',
            'file': PDF_PATH,
            'sha256': pdf_hash,
            'pages': [
                {
                    'page': page_num,
                    'coordinateSystem': 'PDF points, top-left origin'
                }
            ],
            'verificationStatus': 'source-verified',
            'verifiedOn': '2026-10-08'
        },
        'transcriptionStatus': 'source-verified',
        'solution': None,
        'solutionAvailability': 'not-provided-in-source',
        'gradingStatus': 'official key verified'
    }
    return q_obj

# Q1
questions.append(make_q(
    1, 1,
    [
        {'type': 'text', 'text': 'The function defined by\n$$f(x) = \\begin{cases} \\sin x, & x < 0 \\\\ 0, & x = 0 \\\\ 3x^3, & x > 0 \\end{cases}$$'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'is neither continuous nor differentiable at $x = 0$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'is continuous and differentiable at $x = 0$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'is differentiable but not continuous at $x = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'is continuous but not differentiable at $x = 0$'}]}
    ],
    'D'
))

# Q2
questions.append(make_q(
    2, 1,
    [
        {'type': 'text', 'text': 'The product of the eigenvalues of the matrix\n$$\\begin{bmatrix} 1 & 0 & 1 \\\\ 0 & 2 & 1 \\\\ 1 & 1 & -3 \\end{bmatrix}$$\nis'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '4'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '-6'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '-9'}]}
    ],
    'D'
))

# Q3
questions.append(make_q(
    3, 1,
    [
        {'type': 'text', 'text': 'Which of the following equations is a LINEAR ordinary differential equation?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\frac{d^2y}{dx^2} + \\frac{dy}{dx} + 2y^2 = 0$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\frac{d^2y}{dx^2} + y\\frac{dy}{dx} + 2y = 0$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\frac{d^2y}{dx^2} + x\\frac{dy}{dx} + 2y = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\left(\\frac{dy}{dx}\\right)^2 + \\frac{dy}{dx} + 2y = 0$'}]}
    ],
    'C'
))

# Q4
questions.append(make_q(
    4, 1,
    [
        {'type': 'text', 'text': 'To transfer a satellite from an elliptical orbit to a circular orbit having radius equal to the apogee distance of the elliptical orbit, the speed of the satellite should be'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'increased at the apogee'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'decreased at the apogee'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'increased at the perigee'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'decreased at the perigee'}]}
    ],
    'A'
))

# Q5
questions.append(make_q(
    5, 1,
    [
        {'type': 'text', 'text': 'The service ceiling of a transport aircraft is defined as the altitude'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'that is halfway between sea-level and absolute ceiling'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'at which it can cruise with one engine operational'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'at which its maximum rate of climb is zero'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'at which its maximum rate of climb is 0.508 m/s'}]}
    ],
    'D'
))

# Q6
questions.append(make_q(
    6, 1,
    [
        {'type': 'text', 'text': 'The drag of an aircraft in steady climbing flight at a given forward speed is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'inversely proportional to climb angle'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'higher than drag in steady level flight at the same forward speed'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'lower than drag in steady level flight at the same forward speed'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'independent of climb angle'}]}
    ],
    'C'
))

# Q7
questions.append(make_q(
    7, 1,
    [
        {'type': 'text', 'text': 'In steady, level turning flight of an aircraft at a load factor \'$n$\', the ratio of the horizontal component of lift and aircraft weight is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\sqrt{n - 1}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sqrt{n + 1}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\sqrt{n^2 - 1}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\sqrt{n^2 + 1}$'}]}
    ],
    'C'
))

# Q8
questions.append(make_q(
    8, 1,
    [
        {'type': 'text', 'text': 'The parameters that remain constant in a cruise-climb of an aircraft are'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'equivalent airspeed and lift coefficient'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'altitude and lift coefficient'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'equivalent airspeed and altitude'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'lift coefficient and aircraft mass'}]}
    ],
    'A'
))

# Q9
questions.append(make_q(
    9, 1,
    [
        {'type': 'text', 'text': 'The maximum thickness to chord ratio for the NACA 24012 airfoil is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.01'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.12'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.24'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.40'}]}
    ],
    'B'
))

# Q10
questions.append(make_q(
    10, 1,
    [
        {'type': 'text', 'text': 'The maximum possible value of pressure coefficient $\\text{C}_\\text{p}$ in incompressible flow is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.5'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\pi$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\infty$'}]}
    ],
    'B'
))

# Q11
questions.append(make_q(
    11, 1,
    [
        {'type': 'text', 'text': 'An irrotational and inviscid flow can become rotational on passing through a'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'normal shock wave'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'oblique shock wave'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'curved shock wave'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Mach wave'}]}
    ],
    'C'
))

# Q12
questions.append(make_q(
    12, 1,
    [
        {'type': 'text', 'text': 'Laminar flow airfoils are used to reduce'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'trim drag'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'skin friction drag'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'induced drag'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'wave drag'}]}
    ],
    'B'
))

# Q13
questions.append(make_q(
    13, 1,
    [
        {'type': 'text', 'text': 'The degree of reaction of an impulse turbine is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.75'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.5'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0'}]}
    ],
    'D'
))

# Q14
questions.append(make_q(
    14, 1,
    [
        {'type': 'text', 'text': 'In a convergent-divergent (CD) nozzle of a rocket motor, the wall heat flux is maximum at'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'the exit of the divergent portion of the CD nozzle'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'the entry to the convergent portion of the CD nozzle'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'the throat of the CD nozzle'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'the mid-length of the divergent portion of the CD nozzle'}]}
    ],
    'B'
))

# Q15
questions.append(make_q(
    15, 1,
    [
        {'type': 'text', 'text': 'In a scramjet engine, the Mach number at the entry to the combustion chamber is around'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.3'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '2'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '6'}]}
    ],
    'C'
))

# Q16
questions.append(make_q(
    16, 1,
    [
        {'type': 'text', 'text': 'DB denotes double base solid propellant.\nLOX-RP1 denotes liquid oxygen – kerosene combination.\n$\\text{LOX-LH}_2$ denotes liquid oxygen – hydrogen combination.\n\nThe correct order of increasing specific impulse is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\text{DB} < \\text{LOX-RP1} < \\text{LOX-LH}_2$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\text{LOX-RP1} < \\text{DB} < \\text{LOX-LH}_2$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\text{LOX-LH}_2 < \\text{DB} < \\text{LOX-RP1}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\text{DB} < \\text{LOX-LH}_2 < \\text{LOX-RP1}$'}]}
    ],
    'A'
))

# Q17
questions.append(make_q(
    17, 1,
    [
        {'type': 'text', 'text': 'In the absence of body moments, the symmetry of the stress tensor is derived from'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'force equilibrium conditions'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'moment equilibrium conditions'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'linear relations between stresses and strains'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'compatibility conditions'}]}
    ],
    'B'
))

# Q18
questions.append(make_q(
    18, 1,
    [
        {'type': 'text', 'text': 'In a 3-D orthotropic material, the number of elastic constants in linear stress-strain relationship is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '3'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '5'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '9'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '21'}]}
    ],
    'C'
))

# Q19
questions.append(make_q(
    19, 1,
    [
        {'type': 'text', 'text': 'The compatibility conditions in theory of elasticity ensure that'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'there is compatibility between various direct and shear stresses'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'relationships between stresses and strains are consistent with constitutive relations'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'displacements are single-valued and continuous'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'stresses satisfy bi-harmonic equation'}]}
    ],
    'C'
))

# Q20
questions.append(make_q(
    20, 1,
    [
        {'type': 'text', 'text': 'In a spring-mass-damper single degree of freedom system, the mass is 2 kg and the undamped natural frequency is 20 Hz. The critical damping constant of the system is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$160\\pi\\text{ N}\\cdot\\text{s/m}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$80\\pi\\text{ N}\\cdot\\text{s/m}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$1\\text{ N}\\cdot\\text{s/m}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$0\\text{ N}\\cdot\\text{s/m}$'}]}
    ],
    'A'
))

# Q21
questions.append(make_q(
    21, 2,
    [
        {'type': 'text', 'text': 'Which of the following quantities remains constant for a satellite in an elliptical orbit around the earth?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'Kinetic energy'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Product of speed and radial distance from the center of the earth'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'Rate of area swept by the radial vector from the center of the orbit'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Rate of area swept by the radial vector from the center of the earth'}]}
    ],
    'D'
))

# Q22
questions.append(make_q(
    22, 2,
    [
        {'type': 'text', 'text': 'A planet is observed to be at its slowest when it is at a distance $r_1$ from the sun and at its fastest when it is at a distance $r_2$ from the sun. The eccentricity $e$ of the planet\'s orbit is given by'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$e = \\frac{r_1}{r_2}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$e = \\frac{r_1 - r_2}{r_1 + r_2}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$e = \\frac{r_2}{r_1}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$e = \\frac{r_1 + r_2}{r_1 - r_2}$'}]}
    ],
    'B'
))

# Q23
questions.append(make_q(
    23, 2,
    [
        {'type': 'text', 'text': 'The function $f(x, y, z) = \\frac{1}{2}x^2y^2z^2$ satisfies'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\operatorname{grad} f = 0$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\operatorname{div}(\\operatorname{grad} f) = 0$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\operatorname{curl}(\\operatorname{grad} f) = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\operatorname{grad}(\\operatorname{div}(\\operatorname{grad} f)) = 0$'}]}
    ],
    'C'
))

# Q24
questions.append(make_q(
    24, 2,
    [
        {'type': 'text', 'text': 'Which of the following is true for all choices of vectors $\\vec{p}, \\vec{q}, \\vec{r}$?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\vec{p} \\times \\vec{q} + \\vec{q} \\times \\vec{r} + \\vec{r} \\times \\vec{p} = 0$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$(\\vec{p} \\cdot \\vec{q})\\vec{r} + (\\vec{q} \\cdot \\vec{r})\\vec{p} + (\\vec{r} \\cdot \\vec{p})\\vec{q} = 0$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\vec{p} \\cdot (\\vec{q} \\times \\vec{r}) + \\vec{q} \\cdot (\\vec{r} \\times \\vec{p}) + \\vec{r} \\cdot (\\vec{p} \\times \\vec{q}) = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\vec{p} \\times (\\vec{q} \\times \\vec{r}) + \\vec{q} \\times (\\vec{r} \\times \\vec{p}) + \\vec{r} \\times (\\vec{p} \\times \\vec{q}) = 0$'}]}
    ],
    'D'
))

# Q25
questions.append(make_q(
    25, 2,
    [
        {'type': 'text', 'text': 'The value of the line integral $\\frac{1}{2\\pi} \\oint (x\\,dy - y\\,dx)$ taken anticlockwise along a circle of unit radius is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.5'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '2'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\pi$'}]}
    ],
    'B'
))

# Q26
questions.append(make_q(
    26, 2,
    [
        {'type': 'text', 'text': 'Which of the following is a solution of $\\frac{d^2y}{dx^2} + 2\\frac{dy}{dx} + y = 0$?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$e^{-x} + xe^{-x}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$e^x + xe^{-x}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$e^x + e^{-x}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$e^{-x} + xe^x$'}]}
    ],
    'A'
))

# Q27
questions.append(make_q(
    27, 2,
    [
        {'type': 'text', 'text': 'Suppose the non-constant functions $F(x)$ and $G(t)$ satisfy\n$$\\frac{d^2F}{dx^2} + p^2F = 0, \\quad \\frac{dG}{dt} + c^2p^2G = 0, \\quad \\text{where } p \\text{ and } c \\text{ are constants.}$$\nThen the function $u(x, t) = F(x)G(t)$ definitely satisfies'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\frac{\\partial^2 u}{\\partial x^2}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\frac{\\partial u}{\\partial t} = c^2 \\frac{\\partial^2 u}{\\partial x^2}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\nabla^2 u = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\frac{\\partial^2 u}{\\partial t^2} + c^2 u^2 = 0$'}]}
    ],
    'B'
))

# Q28
questions.append(make_q(
    28, 2,
    [
        {'type': 'text', 'text': 'The following set of equations\n$$\\begin{bmatrix} 1 & 1 & 2 \\\\ 1 & 0 & 1 \\\\ 0 & 1 & 1 \\end{bmatrix}\\begin{bmatrix} x_1 \\\\ x_2 \\\\ x_3 \\end{bmatrix} = \\begin{bmatrix} 1 \\\\ -1 \\\\ 0 \\end{bmatrix}$$\nhas'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'no solution'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'a unique solution'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'two solutions'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'infinite solutions'}]}
    ],
    'A'
))

# Q29
questions.append(make_q(
    29, 2,
    [
        {'type': 'text', 'text': 'The function $f(x) = x^2 - 5x + 6$'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'has its maximum value at $x = 2.0$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'has its maximum value at $x = 2.5$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'is increasing on the interval $(2.0, 2.5)$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'is increasing on the interval $(2.5, 3.0)$'}]}
    ],
    'D'
))

# Q30
questions.append(make_q(
    30, 2,
    [
        {'type': 'text', 'text': 'Let $Y(s)$ denote the Laplace transform $\\mathcal{L}(y(t))$ of the function $y(t) = \\cosh(at)\\sin(at)$. Then'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\mathcal{L}\\left(\\frac{dy}{dt}\\right) = \\frac{dY}{ds}, \\quad \\mathcal{L}(t\\,y(t)) = sY(s)$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\mathcal{L}\\left(\\frac{dy}{dt}\\right) = sY(s), \\quad \\mathcal{L}(t\\,y(t)) = -\\frac{dY}{ds}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\mathcal{L}\\left(\\frac{dy}{dt}\\right) = \\frac{dY}{ds}, \\quad \\mathcal{L}(t\\,y(t)) = Y(s-1)$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\mathcal{L}\\left(\\frac{dy}{dt}\\right) = sY(s), \\quad \\mathcal{L}(t\\,y(t)) = e^{as}Y(s)$'}]}
    ],
    'B'
))

# Q31
questions.append(make_q(
    31, 2,
    [
        {'type': 'text', 'text': 'The velocity required for a spacecraft to escape earth\'s gravitational field depends on'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'the mass of the spacecraft'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'the distance between earth\'s center and the spacecraft'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'the earth\'s rotational speed about its own axis'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'the earth\'s orbital speed'}]}
    ],
    'B'
))

# Q32
questions.append(make_q(
    32, 2,
    [
        {'type': 'text', 'text': 'The figure below shows the variation of $C_m$ versus $\\alpha$ for an aircraft for three combinations of elevator deflections and locations of centre of gravity. In the figure, lines P and Q are parallel, while lines Q and R have the same intercept on the $C_m$ axis.'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-32-figure-1.png',
            'alt': 'Variation of Cm versus alpha for lines P, Q, and R',
            'source': figures_info['figures/gate-2008-ae-ae-32-figure-1.png']
        },
        {'type': 'text', 'text': 'Which of the following statements is true?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'Lines P and Q correspond to the same centre of gravity location.'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Lines Q and R correspond to the same centre of gravity location.'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'Lines P and Q correspond to the same elevator deflection.'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Lines P and R correspond to the same centre of gravity location.'}]}
    ],
    'A'
))

# Q33
questions.append(make_q(
    33, 2,
    [
        {'type': 'text', 'text': 'Which of the following statements is TRUE as the altitude increases in stratosphere of International Standard Atmosphere?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'Temperature increases and dynamic viscosity decreases.'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Temperature remains constant and pressure increases.'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'Temperature decreases and sound speed decreases.'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Temperature remains constant and density decreases.'}]}
    ],
    'D'
))

# Q34
questions.append(make_q(
    34, 2,
    [
        {'type': 'text', 'text': 'Which of the following statements is TRUE?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'Wing dihedral reduces roll stability while a low wing increases roll stability.'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Wing dihedral increases roll stability while a low wing reduces roll stability.'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'Wing dihedral, as well as low wing reduces roll stability.'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Wing dihedral, as well as low wing increases roll stability.'}]}
    ],
    'B'
))

# Q35
questions.append(make_q(
    35, 2,
    [
        {'type': 'text', 'text': 'An aircraft has a level flight stalling speed of 60 m/s EAS (equivalent air speed). As per the V-n diagram, what is the minimum speed at which it should be designed to withstand the maximum vertical load factor of 9?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '20 m/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '60 m/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '120 m/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '180 m/s'}]}
    ],
    'D'
))

# Q36
questions.append(make_q(
    36, 2,
    [
        {'type': 'text', 'text': 'Match each mode of aircraft motion listed in Group I to its corresponding property from Group II.\n\n| Group I: Aircraft mode | Group II: Property |\n| :--- | :--- |\n| P: Short period mode | 1: Coupled roll-yaw oscillations |\n| Q: Wing rock | 2: Angle of attack remains constant |\n| R: Phugoid mode | 3: Roll oscillations |\n| S: Dutch roll | 4: Speed remains constant |'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'P-2, Q-1, R-4, S-3'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'P-4, Q-3, R-2, S-1'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'P-4, Q-1, R-2, S-3'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'P-2, Q-3, R-4, S-1'}]}
    ],
    'B'
))

# Q37
questions.append(make_q(
    37, 2,
    [
        {'type': 'text', 'text': 'An aircraft is cruising at a true air speed (TAS) of 100 m/s under ISA conditions, at an altitude at which the density of free stream is $0.526\\text{ kg/m}^3$. What will be the equivalent air speed (EAS)?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '65.5 m/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '72.5 m/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '110.5 m/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '152.7 m/s'}]}
    ],
    'A'
))

# Q38
questions.append(make_q(
    38, 2,
    [
        {'type': 'text', 'text': 'In the definition of the aircraft Euler angles $\\varphi$ (roll), $\\theta$ (pitch), and $\\psi$ (yaw), the correct sequence of rotations required to make the inertial frame coincide with the aircraft body frame is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'first $\\psi$ about $z$ axis, second $\\theta$ about $y$ axis, third $\\varphi$ about $x$ axis'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'first $\\theta$ about $y$ axis, second $\\varphi$ about $x$ axis, third $\\psi$ about $z$ axis'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'first $\\varphi$ about $x$ axis, second $\\theta$ about $y$ axis, third $\\psi$ about $z$ axis'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'first $\\psi$ about $z$ axis, second $\\varphi$ about $x$ axis, third $\\theta$ about $y$ axis'}]}
    ],
    'A'
))

# Q39
questions.append(make_q(
    39, 2,
    [
        {'type': 'text', 'text': 'To maximize range of a jet engine aircraft, it should be flown at a velocity that maximizes'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$C_L/C_D$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$C_L^{0.5}/C_D$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$C_L^{1.5}/C_D$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$C_L^2/C_D$'}]}
    ],
    'B'
))

# Q40
questions.append(make_q(
    40, 2,
    [
        {'type': 'text', 'text': 'The primary function of the fin in the vertical tail of an aircraft is to provide'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'yaw control'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'yaw stability'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'roll damping'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'roll stability'}]}
    ],
    'B'
))

# Q41
questions.append(make_q(
    41, 2,
    [
        {'type': 'text', 'text': 'An aircraft requires the trailing edge of the elevator to be deflected upwards from its initial position to lower the trim speed. Which of the following statements about the static stick-fixed stability of this aircraft is true?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'The aircraft is unstable.'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'The aircraft is neutrally stable.'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'The aircraft is stable.'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'The stability of the aircraft cannot be determined from the given information.'}]}
    ],
    'A'
))

# Q42
questions.append(make_q(
    42, 2,
    [
        {'type': 'text', 'text': 'Which of the following statements is true for an aircraft flying at a low angle of attack?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'Yawing motion generates yawing moment and pitching moment.'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Rolling motion generates rolling moment and pitching moment.'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'Yawing motion generates yawing moment and rolling moment.'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'Pitching motion generates yawing moment and rolling moment.'}]}
    ],
    'C'
))

# Q43
questions.append(make_q(
    43, 2,
    [
        {'type': 'text', 'text': 'Consider 2-D flow with stream function $\\psi = \\frac{1}{2}\\ln\\left(\\sqrt{x^2 + y^2}\\right)$. The absolute value of circulation along a unit circle centered at $(x = 0, y = 0)$ is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\pi/2$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\pi$'}]}
    ],
    'D'
))

# Q44
questions.append(make_q(
    44, 2,
    [
        {'type': 'text', 'text': 'Consider a symmetric airfoil at an angle of attack of 4 degrees. Using thin airfoil theory, the magnitude of the moment coefficient about the leading edge is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$2\\pi$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\pi$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\pi^2/60$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\pi^2/90$'}]}
    ],
    'D'
))

# Q45
questions.append(make_q(
    45, 2,
    [
        {'type': 'text', 'text': 'Consider steady, inviscid flow in a convergent-divergent (CD) nozzle, with a normal shock in the divergent portion. The static pressure along the nozzle downstream of the normal shock'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'remains constant'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'increases isentropically to the static pressure at the nozzle exit'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'decreases isentropically to the static pressure at the nozzle exit'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'can increase or decrease, depending on the magnitude of the static pressure at the nozzle exit'}]}
    ],
    'B'
))

# Q46
questions.append(make_q(
    46, 2,
    [
        {'type': 'text', 'text': 'For a free stream Mach number of 0.7 the critical pressure coefficient ($C_{p,\\text{cr}}$) is $-0.78$. If the minimum pressure coefficient for a given airfoil in incompressible flow is $-0.6$, then the flow over the airfoil at a free stream Mach number of 0.7 is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'subsonic and compressible'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'completely supersonic'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'incompressible'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'partly subsonic and partly supersonic'}]}
    ],
    'D'
))

# Q47
questions.append(make_q(
    47, 2,
    [
        {'type': 'text', 'text': 'If the flow Mach number in a turbulent boundary layer over a flat plate is increased keeping the Reynolds number unchanged, the skin friction coefficient $C_f$'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'decreases'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'increases'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'remains constant'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'initially decreases, followed by a rapid increase'}]}
    ],
    'A'
))

# Q48
questions.append(make_q(
    48, 2,
    [
        {'type': 'text', 'text': 'In supersonic wind-tunnel design, an oblique shock diffuser is preferred over a normal shock diffuser because'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'it reduces total pressure loss'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'the flow is slowed down more rapidly'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'the flow is accelerated more rapidly'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'it increases total pressure loss'}]}
    ],
    'A'
))

# Q49
questions.append(make_q(
    49, 2,
    [
        {'type': 'text', 'text': 'The variation of downwash along the span of an untwisted wing of elliptic planform is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'sinusoidal'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'parabolic'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'elliptic'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'constant'}]}
    ],
    'D'
))

# Q50
questions.append(make_q(
    50, 2,
    [
        {'type': 'text', 'text': 'Flow past an airfoil is to be modeled using a vortex sheet. The strength of the vortex sheet at the trailing edge will be'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$2\\pi$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\infty$'}]}
    ],
    'A'
))

# Q51
questions.append(make_q(
    51, 2,
    [
        {'type': 'text', 'text': 'Consider a 2-D body in supersonic flow with an attached oblique shock as shown below'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-51-figure-1.png',
            'alt': '2-D body in supersonic flow with attached oblique shock',
            'source': figures_info['figures/gate-2008-ae-ae-51-figure-1.png']
        },
        {'type': 'text', 'text': 'An increase in free stream Mach number $\\text{M}_\\infty$ will cause the oblique shock wave to'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'move closer to the body'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'move away from the body'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'detach from the body'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'become a normal shock'}]}
    ],
    'A'
))

# Q52
questions.append(make_q(
    52, 2,
    [
        {'type': 'text', 'text': 'The geometrical features of a supercritical airfoil are'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'rounded leading edge, flat upper surface and high camber at the rear'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'sharp leading edge, curved upper surface and high camber at the rear'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'rounded leading edge, curved upper surface and no camber at the rear'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'sharp leading edge, flat upper surface and no camber at the rear'}]}
    ],
    'A'
))

# Q53
questions.append(make_q(
    53, 2,
    [
        {'type': 'text', 'text': 'Which one of the following high lift device results in higher stalling angle?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'split flap'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'Fowler flap'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'plain flap'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'leading edge flap'}]}
    ],
    'A'
))

# Q54
questions.append(make_q(
    54, 2,
    [
        {'type': 'text', 'text': 'A turbofan engine has a bypass ratio of 5 and a total mass flow rate of 120 kg/s. The mass flow rate through the bypass duct is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '20 kg/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '100 kg/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '120 kg/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '600 kg/s'}]}
    ],
    'B'
))

# Q55
questions.append(make_q(
    55, 2,
    [
        {'type': 'text', 'text': 'A turbojet engine is operating with afterburner off. If the afterburner is switched on, then'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'both thrust and sfc decrease'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'thrust increases and sfc decreases'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'thrust decreases and sfc increases'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'both thrust and sfc increase'}]}
    ],
    'D'
))

# Q56
questions.append(make_q(
    56, 2,
    [
        {'type': 'text', 'text': 'A centrifugal compressor operates with a tip blade speed of 340 m/s. The air leaves the impeller with a radial velocity of 88 m/s. If the slip factor is 0.85, the relative velocity at the blade tip is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '101.7 m/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '120.3 m/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '132.6 m/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '135.8 m/s'}]}
    ],
    'A'
))

# Q57
questions.append(make_q(
    57, 2,
    [
        {'type': 'text', 'text': 'An ideal ramjet engine is flying at a Mach number $M$. The exhaust gas static temperature at the outlet of the nozzle is $T_e$. The ambient static temperature is $T_a$. Gas constant $R$ and specific heat ratio $\\gamma$ do not vary through the ramjet. Assuming that nozzle exhaust static pressure is equal to the ambient pressure and fuel air ratio $f \\ll 1$, the thrust per unit mass flow rate is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\sqrt{\\gamma R T_a} \\left[ \\sqrt{\\frac{T_e}{T_a}} \\right]$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sqrt{\\gamma R T_a} \\left[ \\sqrt{\\frac{T_e}{T_a}} - 1 \\right]$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$M\\sqrt{\\gamma R T_a} \\left[ \\sqrt{\\frac{T_e}{T_a}} - 1 \\right]$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$M\\sqrt{\\gamma R T_a} \\left[ \\sqrt{\\frac{T_e}{T_a}} \\right]$'}]}
    ],
    'C'
))

# Q58
questions.append(make_q(
    58, 2,
    [
        {'type': 'text', 'text': 'A 50 percent degree of reaction axial flow turbine operates with a mean blade speed of 180 m/s. The flow leaves the stator and enters the rotor at an angle of 60 degrees to the axial direction. The axial velocity is 150 m/s, and remains constant throughout the stage. The turbine power per unit mass flow is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '29.76 kJ/kg'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '41.12 kJ/kg'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '58.33 kJ/kg'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '61.13 kJ/kg'}]}
    ],
    'D'
))

# Q59
questions.append(make_q(
    59, 2,
    [
        {'type': 'text', 'text': 'The chamber stagnation temperature inside a rocket motor is $T_c$. Only a convergent nozzle is used, and the flow at the exit of this nozzle is choked. Assume that the nozzle exhaust static pressure is equal to ambient static pressure. Gas constant for exhaust gases is $R$ and ratio of specific heats is $\\gamma$. The specific impulse of the rocket motor is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\sqrt{\\frac{2\\gamma R T_c}{\\gamma - 1}}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sqrt{\\frac{\\gamma R T_c}{\\gamma - 1}}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\sqrt{\\frac{\\gamma R T_c}{\\gamma + 1}}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\sqrt{\\frac{2\\gamma R T_c}{\\gamma + 1}}$'}]}
    ],
    'D'
))

# Q60
questions.append(make_q(
    60, 2,
    [
        {'type': 'text', 'text': 'Air enters the combustor of a gas turbine engine at total temperature of 500 K and leaves the combustor at total temperature of 1800 K. If $c_p$ remains constant at 1.005 kJ/kgK and heating value of the fuel used is 44 MJ/kg, the fuel to air ratio is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.003'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.012'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.031'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.074'}]}
    ],
    'C'
))

# Q61
questions.append(make_q(
    61, 2,
    [
        {'type': 'text', 'text': 'The initial temperature sensitivity of burn rate of a solid rocket motor propellant is positive. If the initial temperature increases then'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'thrust increases but burn time decreases'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'thrust decreases and burn time decreases too'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'thrust remains same but burn time increases'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'thrust increases but burn time remains same'}]}
    ],
    'D'
))

# Q62
questions.append(make_q(
    62, 2,
    [
        {'type': 'text', 'text': 'An aircraft is cruising at a Mach number of 0.8 at an altitude where the ambient static pressure is 95 kPa. The diffuser exit total pressure is 140 kPa. Assuming there is no change in the specific heat at constant pressure across the diffuser, and ratio of specific heats is 1.4, the adiabatic efficiency of the intake is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.988'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.915'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.722'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.684'}]}
    ],
    'B'
))

# Q63
questions.append(make_q(
    63, 2,
    [
        {'type': 'text', 'text': 'A parallelogram shaped plate of dimensions \'$a$\' and \'$b$\' as shown in the figure, is subjected to a uniform loading of normal stresses $\\sigma_1$ and $\\sigma_2$. The plate is in equilibrium for'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-63-figure-1.png',
            'alt': 'Parallelogram shaped plate with normal stresses sigma1 and sigma2',
            'source': figures_info['figures/gate-2008-ae-ae-63-figure-1.png']
        }
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'any value of $\\sigma_1$ and $\\sigma_2$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sigma_2 = \\sigma_1 \\cos\\theta$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\sigma_1 = \\sigma_2 \\cos\\theta$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\sigma_2 = \\sigma_1$'}]}
    ],
    'D'
))

# Q64
questions.append(make_q(
    64, 2,
    [
        {'type': 'text', 'text': 'A column of solid circular cross-section and length $L$ can have various end conditions. Choose the correct set that matches the end conditions (listed in Group I) with the corresponding effective length for buckling (listed in Group II).\n\n| Group I (end conditions) | Group II (effective length) |\n| :--- | :--- |\n| (P) one end built-in and other end free | (1) $1.0\\,L$ |\n| (Q) both ends pinned | (2) $0.7\\,L$ |\n| (R) both ends built-in | (3) $2.0\\,L$ |\n| (S) one end built-in and other end pinned | (4) $0.5\\,L$ |'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'P - 3, Q - 1, R - 4, S - 2'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'P - 4, Q - 1, R - 2, S - 3'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'P - 2, Q - 1, R - 3, S - 4'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'P - 3, Q - 1, R - 2, S - 4'}]}
    ],
    'A'
))

# Q65
questions.append(make_q(
    65, 2,
    [
        {'type': 'text', 'text': 'A thin walled tube of circular cross-section with mean radius $r$ has a central web which divides it into two symmetric cells as shown. A torque $M$ is acting on the section. The shear flow $q$ in the central web is'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-65-figure-1.png',
            'alt': 'Circular tube with central web dividing into two symmetric cells',
            'source': figures_info['figures/gate-2008-ae-ae-65-figure-1.png']
        }
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$q = \\frac{M}{2\\pi r^2}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$q = 0$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$q = \\frac{M}{4\\pi r^2}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$q = \\frac{M}{\\pi r^2}$'}]}
    ],
    'B'
))

# Q66
questions.append(make_q(
    66, 2,
    [
        {'type': 'text', 'text': 'A concentrated bending moment $M$ is acting at mid-span of a beam as shown. The shear force diagram for the beam is:'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-66-figure-1.png',
            'alt': 'Beam with concentrated bending moment M at mid-span',
            'source': figures_info['figures/gate-2008-ae-ae-66-figure-1.png']
        },
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-66-figure-2.png',
            'alt': 'Shear force diagram options (A), (B), (C), (D)',
            'source': figures_info['figures/gate-2008-ae-ae-66-figure-2.png']
        }
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '(A)'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '(B)'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '(C)'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '(D)'}]}
    ],
    'C'
))

# Q67
questions.append(make_q(
    67, 2,
    [
        {'type': 'text', 'text': 'An idealized thin-walled cross-section of a beam and the respective areas of the booms are as shown. A bending moment $M_y$ is acting on the cross-section. The ratio of the magnitude of normal stress in the top booms to that of the bottom boom is'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-67-figure-1.png',
            'alt': 'Cross-section of a beam with boom areas and bending moment My',
            'source': figures_info['figures/gate-2008-ae-ae-67-figure-1.png']
        }
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '5/11'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '2/5'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '1'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '5/2'}]}
    ],
    'A'
))

# Q68
questions.append(make_q(
    68, 2,
    [
        {'type': 'text', 'text': 'An engineer is asked to test a system which can be idealized as SDOF (single degree of freedom) with viscous damping. A frequency response test was conducted and it is found that the quality factor Q is equal to 10. What will be the logarithmic decrement if a free vibration test is performed?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\pi/40$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\pi/20$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\pi/10$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\pi/5$'}]}
    ],
    'C'
))

# Q69
questions.append(make_q(
    69, 2,
    [
        {'type': 'text', 'text': 'A beam occupies a region $0 \\le x \\le L$; $-c \\le y \\le c$; $-0.5 \\le z \\le 0.5$ as shown below. The beam can be considered to be in plane stress condition in $x\\text{-}y$ plane. Airy\'s stress function for the beam is given as:\n$$\\phi(x, y) = -\\frac{Pxy^3}{4c^3} + \\frac{3Pxy}{4c}$$\nwhere $P$ is a constant.'},
        {
            'type': 'image',
            'src': 'figures/gate-2008-ae-ae-69-figure-1.png',
            'alt': 'Beam coordinates in x-y plane',
            'source': figures_info['figures/gate-2008-ae-ae-69-figure-1.png']
        },
        {'type': 'text', 'text': 'The above stress function pertains to a'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': 'simply supported beam carrying a point load $P$ at mid span'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': 'simply supported beam carrying a uniform distributed load of intensity $P$ per unit length'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': 'cantilever beam clamped at end $x = L$ and carrying a shear load $P$ at $x = 0$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': 'cantilever beam clamped at end $x = 0$ and carrying a shear load $P$ at $x = L$'}]}
    ],
    'C'
))

# Q70
questions.append(make_q(
    70, 2,
    [
        {'type': 'text', 'text': 'The equation of motion of a uniform slender beam of length $L$ in flexural vibration is given as $EI\\frac{\\partial^4 w}{\\partial x^4} + \\rho A\\frac{\\partial^2 w}{\\partial t^2} = 0$, where $EI$ is the flexural rigidity, $w$ is the lateral displacement and $\\rho A$ is the mass per unit length. The beam is simply supported at the two ends $x = 0$ and $x = L$. Assuming the mode shape in fundamental mode to be $\\sin\\left(\\frac{\\pi x}{L}\\right)$, the natural frequency in fundamental mode is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$0.5\\sqrt{\\frac{EI}{\\rho A L^4}}\\,\\pi^2$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sqrt{\\frac{EI}{\\rho A L^4}}\\,\\pi^2$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$2\\sqrt{\\frac{EI}{\\rho A L^4}}\\,\\pi^2$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$4\\sqrt{\\frac{EI}{\\rho A L^4}}\\,\\pi^2$'}]}
    ],
    'B'
))

# Common Data for Questions 71, 72 and 73
group_cd_71_73 = 'gate-2008-ae-common-data-71-73'
questions.append(make_q(
    71, 2,
    [
        {'type': 'text', 'text': 'The principal stresses are'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\sigma_1 = 17c\\text{ MPa}, \\quad \\sigma_2 = -9c\\text{ MPa}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\sigma_1 = 9c\\text{ MPa}, \\quad \\sigma_2 = 17c\\text{ MPa}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\sigma_1 = -17c\\text{ MPa}, \\quad \\sigma_2 = -9c\\text{ MPa}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\sigma_1 = -17c\\text{ MPa}, \\quad \\sigma_2 = 9c\\text{ MPa}$'}]}
    ],
    'A',
    group_id=group_cd_71_73
))

questions.append(make_q(
    72, 2,
    [
        {'type': 'text', 'text': 'The maximum shear stress is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\tau_{\\max} = 7c\\text{ MPa}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\tau_{\\max} = 10c\\text{ MPa}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\tau_{\\max} = 13c\\text{ MPa}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\tau_{\\max} = 15c\\text{ MPa}$'}]}
    ],
    'C',
    group_id=group_cd_71_73
))

questions.append(make_q(
    73, 2,
    [
        {'type': 'text', 'text': 'The maximum value of $c$ for safe loading of the structure, based on von-Mises failure criterion is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '10.2'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '15.3'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '25.4'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '31.8'}]}
    ],
    'B',
    group_id=group_cd_71_73
))

# Common Data for Questions 74 and 75
group_cd_74_75 = 'gate-2008-ae-common-data-74-75'
questions.append(make_q(
    74, 2,
    [
        {'type': 'text', 'text': 'The mass flow rate of fuel is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '300.3 kg/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '269.5 kg/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '87.4 kg/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '49.9 kg/s'}]}
    ],
    'D',
    group_id=group_cd_74_75
))

questions.append(make_q(
    75, 2,
    [
        {'type': 'text', 'text': 'Neglecting gravity and drag effects, if the initial velocity of the liquid rocket engine is 2.5 km/s, the velocity of the rocket at burnout is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '1.2 km/s'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '2.5 km/s'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '10.2 km/s'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '11.8 km/s'}]}
    ],
    'C',
    group_id=group_cd_74_75
))

# Linked Answer Questions 76 and 77
group_la_76_77 = 'gate-2008-ae-linked-76-77'
questions.append(make_q(
    76, 2,
    [
        {'type': 'text', 'text': 'Which of the following gives the correct formula for Simpson\'s rule?'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$\\frac{(b - a)}{2} \\left[ f(b) + f\\left(\\frac{a + b}{2}\\right) \\right]$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$\\frac{(b - a)}{2} \\left[ \\frac{f(a) + f(b)}{2} + f\\left(\\frac{a + b}{2}\\right) \\right]$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$\\frac{(b - a)}{2} \\left[ \\frac{f(a) + f(b)}{3} + \\frac{4}{3}f\\left(\\frac{a + b}{2}\\right) \\right]$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$\\frac{(b - a)}{2} \\left[ \\frac{f(a) + f(b)}{3} + \\frac{4}{3}f\\left(\\frac{a + b}{3}\\right) \\right]$'}]}
    ],
    'C',
    negative_marks=0.5,
    group_id=group_la_76_77
))

questions.append(make_q(
    77, 2,
    [
        {'type': 'text', 'text': 'The percentage error (with respect to the exact solution) in estimation of the integral $\\int_0^1 x^3\\,dx$ using Simpson\'s rule is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '5.3'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '3.5'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '2.8'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0'}]}
    ],
    'D',
    negative_marks=0.0,
    group_id=group_la_76_77
))

# Linked Answer Questions 78 and 79
group_la_78_79 = 'gate-2008-ae-linked-78-79'
questions.append(make_q(
    78, 2,
    [
        {'type': 'text', 'text': 'The thrust required for steady level flight will be minimum when the aircraft operates at a lift coefficient of'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.65'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.70'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.75'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.80'}]}
    ],
    'B',
    negative_marks=0.5,
    group_id=group_la_78_79
))

questions.append(make_q(
    79, 2,
    [
        {'type': 'text', 'text': 'The glide angle that results in maximum range in a power-off glide is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '1.82 degrees'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '2.68 degrees'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '3.64 degrees'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '5.01 degrees'}]}
    ],
    'C',
    negative_marks=0.0,
    group_id=group_la_78_79
))

# Linked Answer Questions 80 and 81
group_la_80_81 = 'gate-2008-ae-linked-80-81'
questions.append(make_q(
    80, 2,
    [
        {'type': 'text', 'text': 'The wing lift coefficient $C_L$ is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.66'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.51'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.44'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.34'}]}
    ],
    'B',
    negative_marks=0.5,
    group_id=group_la_80_81
))

questions.append(make_q(
    81, 2,
    [
        {'type': 'text', 'text': 'The induced drag coefficient of the wing $C_{Di}$ is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '0.0053'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '0.0087'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '0.0118'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '0.0197'}]}
    ],
    'B',
    negative_marks=0.0,
    group_id=group_la_80_81
))

# Linked Answer Questions 82 and 83
group_la_82_83 = 'gate-2008-ae-linked-82-83'
questions.append(make_q(
    82, 2,
    [
        {'type': 'text', 'text': 'The total temperature rise across the compressor is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '310.1 K'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '366.3 K'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '392.1 K'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '405.4 K'}]}
    ],
    'B',
    negative_marks=0.5,
    group_id=group_la_82_83
))

questions.append(make_q(
    83, 2,
    [
        {'type': 'text', 'text': 'The total number of stages required are'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '9'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '10'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '11'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '12'}]}
    ],
    'B',
    negative_marks=0.0,
    group_id=group_la_82_83
))

# Linked Answer Questions 84 and 85
group_la_84_85 = 'gate-2008-ae-linked-84-85'
questions.append(make_q(
    84, 2,
    [
        {'type': 'text', 'text': 'The shear flows $q_1$ and $q_2$ are'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '$q_1 = -2\\text{ N/cm}, \\quad q_2 = +22\\text{ N/cm}$'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '$q_1 = +2\\text{ N/cm}, \\quad q_2 = +22\\text{ N/cm}$'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '$q_1 = +2\\text{ N/cm}, \\quad q_2 = -22\\text{ N/cm}$'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '$q_1 = -2\\text{ N/cm}, \\quad q_2 = -22\\text{ N/cm}$'}]}
    ],
    'A',
    negative_marks=0.5,
    group_id=group_la_84_85
))

questions.append(make_q(
    85, 2,
    [
        {'type': 'text', 'text': 'The torque $M$ is'}
    ],
    [
        {'id': 'A', 'content': [{'type': 'text', 'text': '3360 N.cm'}]},
        {'id': 'B', 'content': [{'type': 'text', 'text': '5760 N.cm'}]},
        {'id': 'C', 'content': [{'type': 'text', 'text': '6960 N.cm'}]},
        {'id': 'D', 'content': [{'type': 'text', 'text': '8160 N.cm'}]}
    ],
    'B',
    negative_marks=0.0,
    group_id=group_la_84_85
))

# Groups definitions
question_groups = [
    {
        'id': group_cd_71_73,
        'type': 'common-data',
        'title': 'Common Data Questions',
        'questionIds': [
            'gate-2008-ae-ae-71',
            'gate-2008-ae-ae-72',
            'gate-2008-ae-ae-73'
        ],
        'content': [
            {'type': 'text', 'text': 'Common Data for Questions 71, 72 and 73: A two-dimensional state of stress in an isotropic material is given by\n$$[\\sigma] = c\\begin{bmatrix} -8 & 5 \\\\ 5 & 16 \\end{bmatrix}\\text{ MPa}$$\nwhere $c$ is linearly proportional to the applied loading. The failure stress is $\\sigma_f = 350\\text{ MPa}$ (which is 0.2 % offset yield stress).'}
        ]
    },
    {
        'id': group_cd_74_75,
        'type': 'common-data',
        'title': 'Common Data Questions',
        'questionIds': [
            'gate-2008-ae-ae-74',
            'gate-2008-ae-ae-75'
        ],
        'content': [
            {'type': 'text', 'text': 'Common Data for Questions 74 and 75: A liquid rocket engine with oxidizer to fuel ratio of 5:1 produces a thrust of 1 MN. The initial mass of the rocket engine is 100,000 kg and its mass at burn out is 10,000 kg. The characteristic velocity $C^*$ and thrust coefficient $C_F$ for the engine are 2386 m/s and 1.4, respectively.'}
        ]
    },
    {
        'id': group_la_76_77,
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'questionIds': [
            'gate-2008-ae-ae-76',
            'gate-2008-ae-ae-77'
        ],
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 76 and 77: The following two questions relate to Simpson\'s rule for approximating the integral $\\int_a^b f(x)\\,dx$ on the interval $[a, b]$.'}
        ],
        'dependencies': [
            {
                'questionId': 'gate-2008-ae-ae-77',
                'dependsOn': 'gate-2008-ae-ae-76'
            }
        ]
    },
    {
        'id': group_la_78_79,
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'questionIds': [
            'gate-2008-ae-ae-78',
            'gate-2008-ae-ae-79'
        ],
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 78 and 79: An aircraft has a zero-lift drag coefficient $C_{D0} = 0.0223$, wing aspect ratio $AR_W = 10.0$, and Oswald\'s efficiency factor $e = 0.7$'}
        ],
        'dependencies': [
            {
                'questionId': 'gate-2008-ae-ae-79',
                'dependsOn': 'gate-2008-ae-ae-78'
            }
        ]
    },
    {
        'id': group_la_80_81,
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'questionIds': [
            'gate-2008-ae-ae-80',
            'gate-2008-ae-ae-81'
        ],
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 80 and 81: Consider an untwisted wing of elliptical planform in inviscid incompressible irrotational flow at an angle of attack of 4 degrees. The wing aspect ratio is 7 and the zero lift angle of attack is $-2\\text{ degrees}$.'}
        ],
        'dependencies': [
            {
                'questionId': 'gate-2008-ae-ae-81',
                'dependsOn': 'gate-2008-ae-ae-80'
            }
        ]
    },
    {
        'id': group_la_82_83,
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'questionIds': [
            'gate-2008-ae-ae-82',
            'gate-2008-ae-ae-83'
        ],
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 82 and 83: A multi-stage axial flow compressor operating at an adiabatic efficiency of 0.9 develops a total pressure ratio of 11. The total temperature at inlet to the compressor is 335 K and the stagnation enthalpy rise across each stage is 37 kJ/kg. Ratio of specific heats is 1.4 and specific heat at constant pressure is 1.005 kJ/kg K.'}
        ],
        'dependencies': [
            {
                'questionId': 'gate-2008-ae-ae-83',
                'dependsOn': 'gate-2008-ae-ae-82'
            }
        ]
    },
    {
        'id': group_la_84_85,
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'questionIds': [
            'gate-2008-ae-ae-84',
            'gate-2008-ae-ae-85'
        ],
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 84 and 85: An idealized thin walled two cell symmetric box beam is as shown. The shear flows in the walls are due to the applied shear forces $V_y = 480\\text{ N}, V_z = 300\\text{ N}$, and a torque $M$, all acting at the shear center.'},
            {
                'type': 'figure',
                'asset': {
                    'src': 'figures/gate-2008-ae-ae-84-figure-1.png',
                    'alt': 'Two-cell symmetric box beam with shear flows and dimensions',
                    'source': {
                        'file': PDF_PATH,
                        'page': 14,
                        'sha256': pdf_hash
                    },
                    'verificationStatus': 'source-verified'
                }
            }
        ],
        'dependencies': [
            {
                'questionId': 'gate-2008-ae-ae-85',
                'dependsOn': 'gate-2008-ae-ae-84'
            }
        ]
    }
]

# Question refs
question_refs = [{'id': q['id'], 'number': q['number'], 'section': q['section'], 'type': q['type']} for q in questions]

# Final 2008.json
paper_2008 = {
    'schemaVersion': 1,
    'id': 'gate-2008-ae',
    'exam': 'GATE',
    'year': 2008,
    'paper': 'AE',
    'title': 'GATE 2008 Aerospace Engineering (AE)',
    'durationMinutes': 180,
    'totalMarks': 150,
    'totalQuestions': 85,
    'marking': {
        'negativeFraction': {
            'MCQ': 0.25,
            'MSQ': 0,
            'NAT': 0
        }
    },
    'sectionOrder': ['AE'],
    'sections': [
        {
            'id': 'AE',
            'title': 'Aerospace Engineering',
            'totalQuestions': 85,
            'totalMarks': 150,
            'questionIds': [q['id'] for q in questions]
        }
    ],
    'questionOrder': [q['id'] for q in questions],
    'questionRefs': question_refs,
    'questionGroups': question_groups,
    'source': {
        'paper': 'AE',
        'year': 2008,
        'file': PDF_PATH,
        'sha256': pdf_hash,
        'keyFile': KEY_PDF_PATH,
        'keySha256': key_pdf_hash
    },
    'questions': questions
}

with open('data/ae/2008.json', 'w', encoding='utf-8') as f:
    json.dump(paper_2008, f, indent=2)
    f.write('\n')

print(f'2008.json generated with {len(questions)} questions.')
