import json
import hashlib
import os
import re

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

PDF_PATH = 'internal/ae/AE2007.pdf'
KEY_PDF_PATH = 'internal/ae/AE2007-key.pdf'
pdf_hash = sha256_file(PDF_PATH)
key_pdf_hash = sha256_file(KEY_PDF_PATH)

# Figure assets hashes
figures_info = {}
for fig in [
    'figures/gate-2007-ae-ae-25-figure-1.png',
    'figures/gate-2007-ae-ae-44-figure-1.png',
    'figures/gate-2007-ae-ae-54-figure-1.png',
    'figures/gate-2007-ae-ae-57-figure-1.png',
    'figures/gate-2007-ae-ae-60-figure-1.png',
    'figures/gate-2007-ae-ae-67-figure-1.png',
    'figures/gate-2007-ae-ae-68-figure-1.png',
    'figures/gate-2007-ae-ae-74-figure-1.png',
    'figures/gate-2007-ae-ae-76-figure-1.png',
]:
    figures_info[fig] = {
        'file': fig,
        'sha256': sha256_file(fig)
    }

# Key answers
key_answers = {
    1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'D', 6: 'D', 7: 'A', 8: 'D', 9: 'A', 10: 'C',
    11: 'B', 12: 'C', 13: 'D', 14: 'C', 15: 'B', 16: 'B', 17: 'B', 18: 'D', 19: 'B', 20: 'B',
    21: 'D', 22: 'D', 23: 'B', 24: 'B', 25: 'A', 26: 'B', 27: 'C', 28: 'A', 29: 'D', 30: 'C',
    31: 'D', 32: 'B', 33: 'C', 34: 'C', 35: 'A', 36: 'C', 37: 'A', 38: 'A', 39: 'B', 40: 'B',
    41: 'A', 42: 'B', 43: 'A', 44: 'B', 45: 'A', 46: 'A', 47: 'B', 48: 'C', 49: 'A', 50: 'C',
    51: 'B', 52: 'B', 53: 'A', 54: 'B', 55: 'B', 56: 'B', 57: 'A', 58: 'A', 59: 'B', 60: 'A',
    61: 'C', 62: 'D', 63: 'B', 64: 'A', 65: 'C', 66: 'B', 67: 'A', 68: 'C', 69: 'C', 70: 'A',
    71: 'B', 72: 'A', 73: 'D', 74: 'B', 75: 'C', 76: 'C', 77: 'B', 78: 'C', 79: 'B', 80: 'D',
    81: 'B', 82: 'A', 83: 'A', 84: 'C', 85: 'B'
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
    'paper': 'AE2007',
    'source': KEY_PDF_PATH,
    'sha256': key_pdf_hash,
    'rows': key_rows
}

with open('internal/ae/AE2007-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_json, f, indent=2)
    f.write('\n')

def get_page_for_q(n):
    if 1 <= n <= 7: return 2
    if 8 <= n <= 14: return 3
    if 15 <= n <= 20: return 4
    if 21 <= n <= 24: return 5
    if 25 <= n <= 27: return 6
    if 28 <= n <= 33: return 7
    if 34 <= n <= 39: return 8
    if 40 <= n <= 43: return 9
    if 44 <= n <= 45: return 10
    if 46 <= n <= 49: return 11
    if 50 <= n <= 53: return 12
    if 54 <= n <= 56: return 13
    if 57 <= n <= 59: return 14
    if 60 <= n <= 64: return 15
    if 65 <= n <= 67: return 16
    if 68 <= n <= 70: return 17
    if 71 <= n <= 74: return 18
    if 75 <= n <= 77: return 19
    if 78 <= n <= 83: return 20
    if 84 <= n <= 85: return 21
    return 1

# Clean LaTeX to custom notation grammar & Unicode
def clean_notation(text):
    if not text:
        return text
    s = text
    # Matrix replacement
    def repl_matrix(m):
        content = m.group(1).strip()
        rows = [r.strip() for r in content.split(r'\\')]
        row_strs = []
        for r in rows:
            cells = [c.strip() for c in r.split('&')]
            row_strs.append(' & '.join(cells))
        return r'\matrix{' + ' ; '.join(row_strs) + '}'
    s = re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', repl_matrix, s, flags=re.DOTALL)

    # Overlines
    s = re.sub(r'\\bar\{([a-zA-Z0-9]+)\}', r'\\overline{\1}', s)
    s = re.sub(r'\\overline\{([a-zA-Z0-9]+)\}', r'\\overline{\1}', s)

    # Greek and Math replacements
    reps = [
        (r'\alpha', 'α'),
        (r'\beta', 'β'),
        (r'\gamma', 'γ'),
        (r'\theta', 'θ'),
        (r'\lambda', 'λ'),
        (r'\sigma', 'σ'),
        (r'\tau', 'τ'),
        (r'\pi', 'π'),
        (r'\phi', 'ϕ'),
        (r'\rho', 'ρ'),
        (r'\eta', 'η'),
        (r'\omega', 'ω'),
        (r'\zeta', 'ζ'),
        (r'\Delta', 'Δ'),
        (r'\times', '×'),
        (r'\pm', '±'),
        (r'\le', '≤'),
        (r'\ge', '≥'),
        (r'\infty', '∞'),
        (r'\partial', '∂'),
        (r'\cdot', '·'),
        (r'\longrightarrow', '→'),
        (r'\to', '→'),
        (r'\dot{x}', 'ẋ'),
        (r'\sqrt[3]{c}', '∛c'),
        (r'\sqrt{-1}', '√(-1)'),
        (r'\sqrt{2}', '√2'),
        (r'\,', ' '),
        (r'$$', ''),
        (r'$', '')
    ]
    for old, new in reps:
        s = s.replace(old, new)
    return s.strip()

# Build Questions
questions = []

def make_q(number, marks, body, options, answer, group_id=None):
    negative_marks = marks * 0.25
    q_id = f'gate-2007-ae-ae-{number:02d}'
    page_num = get_page_for_q(number)

    q_texts = []
    q_figures = []
    for item in body:
        if item['type'] == 'text':
            q_texts.append(clean_notation(item['text']))
        elif item['type'] in ('figure', 'image'):
            src = item['asset']['src']
            alt = item['asset']['alt']
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
        formatted_options.append({
            'label': opt['label'],
            'text': clean_notation(opt['text'])
        })

    q_obj = {
        'id': q_id,
        'number': number,
        'year': 2007,
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
        'markingRule': 'gate-2007-official',
        'hasFigure': len(q_figures) > 0,
        'figures': q_figures,
        'groupId': group_id,
        'source': {
            'paper': 'AE',
            'year': 2007,
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

def opt(label, text):
    return {'label': label, 'text': text}

def fig_block(src, alt, page_num):
    return {
        'type': 'figure',
        'asset': {
            'src': src,
            'alt': alt,
            'verificationStatus': 'source-verified',
            'source': {
                'file': PDF_PATH,
                'page': page_num,
                'sha256': pdf_hash
            }
        }
    }

# ==================== Q1 to Q20 (1 Mark each) ====================
questions.append(make_q(
    1, 1,
    [{'type': 'text', 'text': 'Which one of the following engines should be used by a subsonic passenger transport airplane for minimum specific fuel consumption?'}],
    [
        opt('A', 'Turbojet engine with afterburner'),
        opt('B', 'Turbofan engine'),
        opt('C', 'Ramjet engine'),
        opt('D', 'Scramjet engine')
    ],
    'B'
))

questions.append(make_q(
    2, 1,
    [{'type': 'text', 'text': 'A spring-mass-damper system with a mass of 1 kg is found to have a damping ratio of 0.2 and a natural frequency of 5 rad/s. The damping of the system is given by'}],
    [
        opt('A', '2 Ns/m'),
        opt('B', '2 N/s'),
        opt('C', '0.2 kg/s'),
        opt('D', '0.2 N/s')
    ],
    'A'
))

questions.append(make_q(
    3, 1,
    [{'type': 'text', 'text': 'If f(θ) = \\matrix{cos θ & sin θ ; -sin θ & cos θ}, then f(α) f(β) ='}],
    [
        opt('A', 'f(α / β)'),
        opt('B', 'f(α + β)'),
        opt('C', 'f(α - β)'),
        opt('D', '2 × 2 zero matrix')
    ],
    'B'
))

questions.append(make_q(
    4, 1,
    [{'type': 'text', 'text': 'An artificial satellite remains in orbit and does not fall to the earth because'}],
    [
        opt('A', 'the centrifugal force acting on it balances the gravitational attraction'),
        opt('B', 'the on-board rocket motors provide continuous boost to keep it in orbit'),
        opt('C', 'its transverse velocity keeps it from hitting the earth although it falls continuously'),
        opt('D', 'due to its high speed it derives sufficient lift from the rarefied atmosphere')
    ],
    'A'
))

questions.append(make_q(
    5, 1,
    [{'type': 'text', 'text': 'The Euler iteration formula for numerically integrating a first order nonlinear differential equation of the form ẋ = f(x), with a constant step size of Δt is'}],
    [
        opt('A', 'x_{k+1} = x_{k} - Δt × f(x_{k})'),
        opt('B', 'x_{k+1} = x_{k} + (Δt^{2} / 2) × f(x_{k})'),
        opt('C', 'x_{k+1} = x_{k} - (1 / Δt) × f(x_{k})'),
        opt('D', 'x_{k+1} = x_{k} + Δt × f(x_{k})')
    ],
    'D'
))

questions.append(make_q(
    6, 1,
    [{'type': 'text', 'text': 'The number of natural frequencies of an elastic beam with cantilever boundary conditions is'}],
    [
        opt('A', '1'),
        opt('B', '3'),
        opt('C', '1000'),
        opt('D', 'Infinite')
    ],
    'D'
))

questions.append(make_q(
    7, 1,
    [{'type': 'text', 'text': 'For maximum range of a glider, which of the following conditions is true?'}],
    [
        opt('A', 'lift to drag ratio is maximum'),
        opt('B', 'rate of descent is minimum'),
        opt('C', 'descent angle is maximum'),
        opt('D', 'lift to weight ratio is maximum')
    ],
    'A'
))

questions.append(make_q(
    8, 1,
    [{'type': 'text', 'text': 'An airplane with a larger wing as compared to a smaller wing will necessarily have'}],
    [
        opt('A', 'more longitudinal static stability'),
        opt('B', 'less longitudinal static stability'),
        opt('C', 'same longitudinal static stability'),
        opt('D', 'more longitudinal static stability for an aft tail airplane if aerodynamic center of the larger wing is behind the center of gravity of the airplane')
    ],
    'D'
))

questions.append(make_q(
    9, 1,
    [{'type': 'text', 'text': 'The minimum value of J(x) = x^{2} - 7x + 30 occurs at'}],
    [
        opt('A', 'x = 7/2'),
        opt('B', 'x = 7/30'),
        opt('C', 'x = 30/7'),
        opt('D', 'x = 30')
    ],
    'A'
))

questions.append(make_q(
    10, 1,
    [{'type': 'text', 'text': 'Two airplanes are identical except for the location of the wing. The longitudinal static stability of the airplane with low wing configuration will be'}],
    [
        opt('A', 'more than the airplane with high wing configuration'),
        opt('B', 'less than the airplane with high wing configuration'),
        opt('C', 'same as the airplane with high wing configuration'),
        opt('D', 'more if elevator is deflected')
    ],
    'C'
))

questions.append(make_q(
    11, 1,
    [{'type': 'text', 'text': 'For a fixed center of gravity location of an airplane, when the propeller is mounted on the nose of the fuselage'}],
    [
        opt('A', 'longitudinal static stability increases'),
        opt('B', 'longitudinal static stability decreases'),
        opt('C', 'longitudinal static stability remains same'),
        opt('D', 'longitudinal static stability is maximum')
    ],
    'B'
))

questions.append(make_q(
    12, 1,
    [{'type': 'text', 'text': 'Let an airplane in a steady level flight be trimmed at a certain speed. A level and steady flight at a higher speed could be achieved by changing'}],
    [
        opt('A', 'engine throttle only'),
        opt('B', 'elevator only'),
        opt('C', 'throttle and elevator together'),
        opt('D', 'rudder only')
    ],
    'C'
))

questions.append(make_q(
    13, 1,
    [{'type': 'text', 'text': 'For a plane strain problem in the x - y plane, in general, the non-zero stress terms are'}],
    [
        opt('A', 'σ_{zz}, σ_{xz}, σ_{yz}, σ_{xy}'),
        opt('B', 'σ_{zz}, σ_{xz}, σ_{yz}, σ_{xy}'),
        opt('C', 'σ_{xx}, σ_{xy}, σ_{yy}, σ_{xz}'),
        opt('D', 'σ_{xx}, σ_{yy}, σ_{xy}, σ_{zz}')
    ],
    'D'
))

questions.append(make_q(
    14, 1,
    [{'type': 'text', 'text': 'For an elastic anisotropic solid, the number of independent elastic constants in its constitutive equations is'}],
    [
        opt('A', '2'),
        opt('B', '9'),
        opt('C', '21'),
        opt('D', '36')
    ],
    'C'
))

questions.append(make_q(
    15, 1,
    [{'type': 'text', 'text': 'Total pressure at a point is defined as the pressure when the flow is brought to rest'}],
    [
        opt('A', 'adiabatically'),
        opt('B', 'isentropically'),
        opt('C', 'isothermally'),
        opt('D', 'isobarically')
    ],
    'B'
))

questions.append(make_q(
    16, 1,
    [{'type': 'text', 'text': 'The drag divergence Mach number of an airfoil'}],
    [
        opt('A', 'is a fixed number for a given airfoil'),
        opt('B', 'is always higher than the critical Mach number'),
        opt('C', 'is equal to the critical Mach number at zero angle of attack'),
        opt('D', 'is the Mach number at which a shock wave first appears on the airfoil')
    ],
    'B'
))

questions.append(make_q(
    17, 1,
    [{'type': 'text', 'text': 'On which one of the following thermodynamic cycles does an ideal ramjet operate?'}],
    [
        opt('A', 'The Rankine cycle'),
        opt('B', 'The Brayton cycle'),
        opt('C', 'The Carnot cycle'),
        opt('D', 'The Otto cycle')
    ],
    'B'
))

questions.append(make_q(
    18, 1,
    [{'type': 'text', 'text': 'Across a normal shock'}],
    [
        opt('A', 'both total temperature and total pressure decrease'),
        opt('B', 'both total temperature and total pressure remain constant'),
        opt('C', 'total pressure remains constant but total temperature decreases'),
        opt('D', 'total temperature remains constant but total pressure decreases')
    ],
    'D'
))

questions.append(make_q(
    19, 1,
    [{'type': 'text', 'text': 'The Joukowskii airfoil is studied in aerodynamics because'}],
    [
        opt('A', 'it is used in many aircraft'),
        opt('B', 'it is easily transformed into a circle, mathematically'),
        opt('C', 'it has a simple geometry'),
        opt('D', 'it has the highest lift curve slope among all airfoils')
    ],
    'B'
))

questions.append(make_q(
    20, 1,
    [{'type': 'text', 'text': 'One of the criteria for high-speed airplanes is that the critical Mach number should be as high as possible. Therefore, high-speed subsonic airplanes are usually designed with'}],
    [
        opt('A', 'thick airfoils'),
        opt('B', 'thin airfoils'),
        opt('C', 'laminar flow airfoils'),
        opt('D', 'diamond airfoils')
    ],
    'B'
))

# ==================== Q21 to Q70 (2 Marks each) ====================
questions.append(make_q(
    21, 2,
    [{'type': 'text', 'text': 'Two identical earth satellites A and B are in circular orbits at altitudes h_{A} and h_{B} above the earth\'s surface respectively, with h_{A} > h_{B}. If E denotes the total mechanical energy, T the kinetic energy and V the gravitational potential energy of a satellite, then:'}],
    [
        opt('A', 'E_{A} > E_{B} and V_{A} < V_{B}'),
        opt('B', 'E_{A} > E_{B} and T_{A} > T_{B}'),
        opt('C', 'E_{A} < E_{B} and T_{A} > T_{B}'),
        opt('D', 'E_{A} > E_{B} and T_{A} < T_{B}')
    ],
    'D'
))

questions.append(make_q(
    22, 2,
    [
        {'type': 'text', 'text': 'Let P and Q be two square matrices of same size. Consider the following statements:\n(i) PQ = 0 implies P = 0 or Q = 0 or both\n(ii) PQ = I^{2} implies P = Q^{-1}\n(iii) (P + Q)^{2} = P^{2} + 2PQ + Q^{2}\n(iv) (P - Q)^{2} = P^{2} - 2PQ + Q^{2}\nwhere I is the identity matrix. Which of the following statements is correct?'}
    ],
    [
        opt('A', '(i), (ii) and (iii) are false, but (iv) is true'),
        opt('B', '(i), (ii) and (iv) are false, but (iii) is true'),
        opt('C', '(ii), (iii) and (iv) are false, but (i) is true'),
        opt('D', '(i), (iii) and (iv) are false, but (ii) is true')
    ],
    'D'
))

questions.append(make_q(
    23, 2,
    [{'type': 'text', 'text': 'A 1 kg mass attached to a spring elongates it by 16mm. The mass is then pulled from its equilibrium position by 10mm and released from rest. Assuming the acceleration due to gravity of 9.81 m/s^{2}, the response of the mass in mm is given by'}],
    [
        opt('A', 'x = 10 sin 24.76t'),
        opt('B', 'x = 10 cos 24.76t'),
        opt('C', 'x = sin 16t'),
        opt('D', 'x = 10 cos 16t')
    ],
    'B'
))

questions.append(make_q(
    24, 2,
    [{'type': 'text', 'text': 'The earth\'s radius is 6.37 × 10^{6} m and the acceleration due to gravity on its surface is 9.81 m/s^{2}. A satellite is in a circular orbit at a height of 6.30 × 10^{5} m above the earth\'s surface. The minimum additional speed it needs to escape from the earth\'s gravitational field is'}],
    [
        opt('A', '3.66 × 10^{3} m/s'),
        opt('B', '3.12 × 10^{3} m/s'),
        opt('C', '3.27 × 10^{3} m/s'),
        opt('D', '3.43 × 10^{3} m/s')
    ],
    'B'
))

questions.append(make_q(
    25, 2,
    [
        {'type': 'text', 'text': 'Shown in the figure below is a model of an Euler-Bernoulli beam made up of two materials subjected to pure bending moment M. The Young\'s modulus of material A and B are E_{A} and E_{B}, respectively. The sectional moment of area, about the neutral axis, of the cross-sectional areas made of materials A and B, are I_{A} and I_{B}, respectively. The radius of curvature ρ of the flexural deflection of this composite beam to the bending moment M is then'},
        fig_block('figures/gate-2007-ae-ae-25-figure-1.png', 'Model of Euler-Bernoulli beam made up of two materials under pure bending moment M', 6)
    ],
    [
        opt('A', 'ρ = \\frac{E_{A} I_{A} + E_{B} I_{B}}{M}'),
        opt('B', 'ρ = \\frac{E_{A} I_{B} + E_{B} I_{A}}{M}'),
        opt('C', 'ρ = \\frac{M}{E_{A} I_{A} + E_{B} I_{B}}'),
        opt('D', 'ρ = \\frac{(E_{A} + E_{B})(I_{A} + I_{B})}{M}')
    ],
    'A'
))

questions.append(make_q(
    26, 2,
    [{'type': 'text', 'text': 'Two pipes of constant sections but different diameters carry water at the same volume flow rate. The Reynolds number, based on the pipe diameter, is'}],
    [
        opt('A', 'the same in both pipes'),
        opt('B', 'is larger in the narrower pipe'),
        opt('C', 'is smaller in the narrower pipe'),
        opt('D', 'depends on the material of the pipes')
    ],
    'B'
))

questions.append(make_q(
    27, 2,
    [{'type': 'text', 'text': 'Two airfoils of the same family are operating at the same angle of attack. The dimensions of one airfoil are twice as large as the other one. The ratio of the minimum pressure coefficient of the larger airfoil to the minimum pressure coefficient of the smaller airfoil is'}],
    [
        opt('A', '4.0'),
        opt('B', '2.0'),
        opt('C', '1.0'),
        opt('D', '0.5')
    ],
    'C'
))

questions.append(make_q(
    28, 2,
    [{'type': 'text', 'text': 'Wing A has a constant chord c and span b. Wing B is identical but has a span 4b. When both wings are operating at the same geometric angle of attack at subsonic speed, then:'}],
    [
        opt('A', 'wings A and B produce the same lift coefficient'),
        opt('B', 'wing A produces a smaller lift coefficient than wing B'),
        opt('C', 'wing A produces a greater lift coefficient than wing B'),
        opt('D', 'the freestream Mach number decides which wing produces the greater lift coefficient')
    ],
    'A'
))

questions.append(make_q(
    29, 2,
    [{'type': 'text', 'text': 'A spring-mass-damper system is excited by a force F_{0} sin(ωt). The amplitude at resonance is measured to be 1 cm. At half the resonant frequency, the amplitude is 0.5 cm. The damping ratio of the system is'}],
    [
        opt('A', '0.1026'),
        opt('B', '0.3242'),
        opt('C', '0.7211'),
        opt('D', '0.1936')
    ],
    'D'
))

questions.append(make_q(
    30, 2,
    [{'type': 'text', 'text': 'The eigenvalues of the matrix, A = \\matrix{2 & 1 ; 0 & 3}, are'}],
    [
        opt('A', '1 and 2'),
        opt('B', '1 and 2'),
        opt('C', '2 and 3'),
        opt('D', '2 and 4')
    ],
    'C'
))

questions.append(make_q(
    31, 2,
    [{'type': 'text', 'text': 'The eigenvalues of the matrix A^{-1}, where A = \\matrix{2 & 1 ; 0 & 3}, are'}],
    [
        opt('A', '1 and 1/2'),
        opt('B', '1 and 1/3'),
        opt('C', '2 and 3'),
        opt('D', '1/2 and 1/3')
    ],
    'D'
))

questions.append(make_q(
    32, 2,
    [{'type': 'text', 'text': 'The radius of the earth is 6.37 × 10^{6} m and the acceleration due to gravity at its surface is 9.81 m/s^{2}. A satellite is in circular orbit at a height of 35.9 × 10^{6} m above the earth\'s surface. This orbit is inclined at 10.5 degrees to the equator. The velocity change needed to make the orbit equatorial is:'}],
    [
        opt('A', '561 m/s at 84.75 degrees to the initial direction'),
        opt('B', '561 m/s at 95.25 degrees to the initial direction'),
        opt('C', '281 m/s at 84.75 degrees to the initial direction'),
        opt('D', '281 m/s at 95.25 degrees to the initial direction')
    ],
    'B'
))

questions.append(make_q(
    33, 2,
    [{'type': 'text', 'text': 'A piston-prop airplane having propeller efficiency, η_{p} = 0.8 and weighing 73108 N could achieve maximum climb rate of 15 m/s at flight speed of 50 m/s. The excess Brake Power (BP) at the above flight condition will be'}],
    [
        opt('A', '1700 kW'),
        opt('B', '2100 kW'),
        opt('C', '1371 kW'),
        opt('D', '6125 kW')
    ],
    'C'
))

questions.append(make_q(
    34, 2,
    [{'type': 'text', 'text': 'An airplane model with a symmetric airfoil was tested in a wind tunnel. C_{m0} (C_{m} at angle of attack, α = 0) was estimated to be 0.08 and 0 respectively for elevator settings (δe) of 5 degrees up and 5 degrees down. The estimated value of the elevator control power (\\frac{∂C_{m}}{∂δe}) of the model will be'}],
    [
        opt('A', '0.07 per deg'),
        opt('B', '-1.065 per deg'),
        opt('C', '-0.008 per deg'),
        opt('D', '-0.762 per deg')
    ],
    'C'
))

questions.append(make_q(
    35, 2,
    [{'type': 'text', 'text': 'The lateral-directional characteristic equation for an airplane gave the following set of roots: λ_{1} = -0.6, λ_{2} = -0.002, λ_{3,4} = -0.06 ± j 1.5, where j = √(-1). The damping ratio corresponding to the Dutch-roll mode will be'}],
    [
        opt('A', '0.04'),
        opt('B', '0.66'),
        opt('C', '0.35'),
        opt('D', '0.18')
    ],
    'A'
))

questions.append(make_q(
    36, 2,
    [{'type': 'text', 'text': 'An airplane is flying at an altitude of 10km above the sea level. Outside air temperature and density at 10km altitude are 223 K and 0.413 kg/m^{3} respectively. The airspeed indicator of the airplane indicates a speed of 60 m/s. Density of air at sea level is 1.225 kg/m^{3} and value of the gas constant R is 288 J/kg/K. The stagnation pressure (p_{0}) measured by the Pitot tube mounted on the wing tip of the airplane will be of magnitude'}],
    [
        opt('A', '3.5 × 10^{4} N/m^{2}'),
        opt('B', '2.0 × 10^{4} N/m^{2}'),
        opt('C', '2.87 × 10^{4} N/m^{2}'),
        opt('D', '0.6 × 10^{4} N/m^{2}')
    ],
    'C'
))

questions.append(make_q(
    37, 2,
    [{'type': 'text', 'text': 'If the center of gravity of an airplane is moved forward towards the nose of the airplane, the C_{Lmax} (maximum value of the lift coefficient) value for which the airplane can be trimmed (C_{m} = 0) will'}],
    [
        opt('A', 'decrease'),
        opt('B', 'increase'),
        opt('C', 'remain same'),
        opt('D', 'depend upon rudder deflection')
    ],
    'A'
))

questions.append(make_q(
    38, 2,
    [{'type': 'text', 'text': 'If the contribution of only the horizontal tail of an airplane was considered for estimating \\frac{∂C_{m}}{∂α}, and if the tail moment arm l_{t} was doubled, then how many times the original value would the new \\frac{∂C_{m}}{∂α} become?'}],
    [
        opt('A', 'two times'),
        opt('B', 'three times'),
        opt('C', '1.414 times'),
        opt('D', '1.732 times')
    ],
    'A'
))

questions.append(make_q(
    39, 2,
    [{'type': 'text', 'text': 'If the vertical tail of an airplane is inverted and put below the horizontal tail, then the contribution to roll derivative, \\frac{∂C_{l}}{∂β}, will be'}],
    [
        opt('A', 'negative'),
        opt('B', 'positive'),
        opt('C', 'zero'),
        opt('D', 'imaginary')
    ],
    'B'
))

questions.append(make_q(
    40, 2,
    [
        {'type': 'text', 'text': 'Let a system of linear equations be as follows:\nx - y + 2z = 0\n2x + 3y - z = 0\n2x - 2y + 4z = 0\n\nThis system of equations has'}
    ],
    [
        opt('A', 'No non-trivial solution'),
        opt('B', 'Infinite number of non-trivial solutions'),
        opt('C', 'An unique non-trivial solution'),
        opt('D', 'Two non-trivial solutions')
    ],
    'B'
))

questions.append(make_q(
    41, 2,
    [{'type': 'text', 'text': 'A turbulent boundary layer remains attached over a longer distance on the upper surface of an airfoil than does a laminar boundary layer, because'}],
    [
        opt('A', 'the turbulent boundary layer is more energetic and hence can overcome the adverse pressure gradient better'),
        opt('B', 'the laminar boundary layer develops more skin friction and hence slows down more rapidly'),
        opt('C', 'turbulence causes the effective coefficient of viscosity to reduce, resulting in less loss of momentum in the boundary layer'),
        opt('D', 'the turbulent boundary layer is thicker, hence the velocity gradients in it are smaller, therefore viscous losses are less')
    ],
    'A'
))

questions.append(make_q(
    42, 2,
    [{'type': 'text', 'text': 'The laminar boundary layer over a large flat plate held parallel to the freestream is 5 mm thick at a point 0.2 m downstream of the leading edge. The thickness of the boundary layer at a point 0.8 m downstream of the leading edge will be'}],
    [
        opt('A', '20 mm'),
        opt('B', '10 mm'),
        opt('C', '5 mm'),
        opt('D', '2.5 mm')
    ],
    'B'
))

questions.append(make_q(
    43, 2,
    [{'type': 'text', 'text': 'If horizontal tail area is increased while the elevator to horizontal tail area ratio is kept same, then'}],
    [
        opt('A', 'both longitudinal static stability and elevator control power will increase'),
        opt('B', 'only longitudinal static stability will increase'),
        opt('C', 'only elevator control power will increase'),
        opt('D', 'neither stability nor control power changes')
    ],
    'A'
))

questions.append(make_q(
    44, 2,
    [
        {'type': 'text', 'text': 'A circular shaft is made-up of two materials A and B. The inner core is made-up of material A with diameter d_{A}, torsion constant J_{A}, and shear modulus G_{A}. The outer sleeve is made-up of material B with diameter d_{B}, torsion constant J_{B}, and shear modulus G_{B}. The composite shaft is of length L and is subjected to pure torsion moment T. The torsional stiffness, \\frac{T}{ϕ}, where ϕ is the angle of twist, of this composite shaft is then'},
        fig_block('figures/gate-2007-ae-ae-44-figure-1.png', 'Circular composite shaft made of two materials subjected to pure torsion moment T', 10)
    ],
    [
        opt('A', '\\frac{\\left(\\frac{G_{A} J_{A}}{L}\\right)\\left(\\frac{G_{B} J_{B}}{L}\\right)}{\\frac{G_{A} J_{A}}{L} + \\frac{G_{B} J_{B}}{L}}'),
        opt('B', '\\frac{G_{A} J_{A}}{L} + \\frac{G_{B} J_{B}}{L}'),
        opt('C', '\\frac{(G_{A} + G_{B})(J_{A} + J_{B})}{L}'),
        opt('D', '\\frac{G_{A} J_{B}}{L} + \\frac{G_{B} J_{A}}{L}')
    ],
    'B'
))

questions.append(make_q(
    45, 2,
    [{'type': 'text', 'text': 'Air enters through the eye of a centrifugal compressor with a stagnation temperature 300 K and exits the compressor with a stagnation temperature 424 K. If the isentropic efficiency of the compressor is 0.81 and the ratio of specific heats of the flowing gas (assumed as constant) is 1.4, then the pressure ratio across the compressor is'}],
    [
        opt('A', '2.75'),
        opt('B', '5.60'),
        opt('C', '65.00'),
        opt('D', '228.00')
    ],
    'A'
))

questions.append(make_q(
    46, 2,
    [
        {
            'type': 'text',
            'text': 'The boundary conditions for an Euler-Bernoulli column are given in column X and the critical buckling loads are given in column Y. Match the boundary condition of the column to its corresponding buckling load. P_{cr} is the critical buckling load, E is the Young\'s modulus of the column material, I its sectional moment of area, and L is the length of the column.\n\n$$\\begin{array}{|l|l|}\n\\hline\n\\textbf{X. Boundary condition} & \\textbf{Y. Critical buckling load} \\\\\n\\hline\n\\text{X1. Pinned-pinned column} & \\text{Y1. } P_{cr} = \\frac{4\\pi^{2}EI}{L^{2}} \\\\\n\\hline\n\\text{X2. Fixed-free (cantilevered) column} & \\text{Y2. } P_{cr} = \\frac{2.046\\pi^{2}EI}{L^{2}} \\\\\n\\hline\n\\text{X3. Fixed-fixed column} & \\text{Y3. } P_{cr} = \\frac{\\pi^{2}EI}{4L^{2}} \\\\\n\\hline\n\\text{X4. Fixed-pinned column} & \\text{Y4. } P_{cr} = \\frac{\\pi^{2}EI}{L^{2}} \\\\\n\\hline\n\\end{array}$$'
        }
    ],
    [
        opt('A', 'X1-Y4, X2-Y3, X3-Y1, X4-Y2'),
        opt('B', 'X1-Y4, X2-Y2, X3-Y3, X4-Y1'),
        opt('C', 'X1-Y4, X2-Y1, X3-Y2, X4-Y3'),
        opt('D', 'X1-Y4, X2-Y3, X3-Y2, X4-Y1')
    ],
    'A'
))

questions.append(make_q(
    47, 2,
    [{'type': 'text', 'text': 'For an impulse turbine with identical stages, the hot gas exits from the stator blades at the mean blade height at an absolute angle of 70 degrees with the axis of the turbine. If the absolute inlet blade angle with the axis of the turbine at the mean blade height for the rotor blades is 37 degrees, then the absolute exit blade angle with the axis of the turbine at the mean blade height of the rotor blades is'}],
    [
        opt('A', '33 degrees'),
        opt('B', '37 degrees'),
        opt('C', '53 degrees'),
        opt('D', '53.5 degrees')
    ],
    'B'
))

questions.append(make_q(
    48, 2,
    [{'type': 'text', 'text': 'Which one of the following materials should be selected to design an axial flow turbine operating at high temperatures?'}],
    [
        opt('A', 'Steel alloy'),
        opt('B', 'Titanium alloy'),
        opt('C', 'Nickel alloy'),
        opt('D', 'Aluminum alloy')
    ],
    'C'
))

questions.append(make_q(
    49, 2,
    [{'type': 'text', 'text': 'Which one of the following statements is true?'}],
    [
        opt('A', 'The isentropic efficiency of a compressor is constant throughout the compressor'),
        opt('B', 'Flow separation problems are more critical for the axial compressors than for the centrifugal compressors'),
        opt('C', 'The pressure ratio of a centrifugal compressor approaches zero as the compressor mass flow rate approaches zero'),
        opt('D', 'Centrifugal compressors are always designed with multiple stages')
    ],
    'A'
))

questions.append(make_q(
    50, 2,
    [{'type': 'text', 'text': 'An athlete starts running with a speed V_{0}. Subsequently, his speed decreases by an amount that is proportional to the distance that he has already covered. The distance covered will be'}],
    [
        opt('A', 'Linear in time'),
        opt('B', 'Quadratic in time'),
        opt('C', 'Exponential in time'),
        opt('D', 'Logarithmic in time')
    ],
    'C'
))

questions.append(make_q(
    51, 2,
    [{'type': 'text', 'text': 'The on-board rocket motor of a satellite of initial mass 2000 kg provides a specific impulse of 280 seconds. If this motor is fired to give a speed increment of 500 m/s along the direction of motion, the mass of propellant consumed is:'}],
    [
        opt('A', '685 kg'),
        opt('B', '333 kg'),
        opt('C', '1666 kg'),
        opt('D', '167 kg')
    ],
    'B'
))

questions.append(make_q(
    52, 2,
    [{'type': 'text', 'text': 'Combustion between fuel (octane) and oxidizer (air) occurs inside a combustor with the following stoichiometric chemical reaction:\n2C_{8}H_{18} + (25O_{2} + 94N_{2}) → 16CO_{2} + 18H_{2}O + 94N_{2}\n\nThe atomic weights of carbon (C), hydrogen (H), oxygen (O), and nitrogen (N) are 12, 1, 16, and 14, respectively. If the combustion takes place with the fuel to air ratio 0.028, then the equivalence ratio of the fuel-oxidizer mixture is'}],
    [
        opt('A', '0.094'),
        opt('B', '0.422'),
        opt('C', '0.721'),
        opt('D', '2.371')
    ],
    'B'
))

questions.append(make_q(
    53, 2,
    [{'type': 'text', 'text': 'The von Mises yield criterion or the maximum distortion energy criterion for a plane stress problem with σ_{1} and σ_{2} as the principal stresses in the plane, and σ_{Y} as the yield stress, requires'}],
    [
        opt('A', 'σ_{1}^{2} - σ_{1}σ_{2} + σ_{2}^{2} ≤ σ_{Y}^{2}'),
        opt('B', '|σ_{1} - σ_{2}| ≤ σ_{Y}'),
        opt('C', '|σ_{1}| ≤ σ_{Y}'),
        opt('D', '|σ_{2}| ≤ σ_{Y}')
    ],
    'A'
))

questions.append(make_q(
    54, 2,
    [
        {'type': 'text', 'text': 'An Euler-Bernoulli beam having a rectangular cross-section, as shown in the figure, is subjected to a non-uniform bending moment along its length. V_{z} = \\frac{dM_{y}}{dx}. The shear stress distribution τ_{xz} across its cross-section is given by'},
        fig_block('figures/gate-2007-ae-ae-54-figure-1.png', 'Rectangular cross-section of beam with coordinate axes y and z and shear force Vz', 13)
    ],
    [
        opt('A', 'τ_{xz} = \\frac{V_{z}}{2I_{y}} \\frac{z}{(h/2)}'),
        opt('B', 'τ_{xz} = \\frac{V_{z}(h/2)^{2}}{2I_{y}} ( 1 - \\frac{z^{2}}{(h/2)^{2}} )'),
        opt('C', 'τ_{xz} = \\frac{V_{z}}{2I_{y}} ( \\frac{z}{(h/2)} )^{2}'),
        opt('D', 'τ_{xz} = \\frac{V_{z}(h/2)^{2}}{2I_{y}}')
    ],
    'B'
))

questions.append(make_q(
    55, 2,
    [{'type': 'text', 'text': 'At a stationary point of a multi-variable function, which of the following is true?'}],
    [
        opt('A', 'Curl of the function becomes unity'),
        opt('B', 'Gradient of the function vanishes'),
        opt('C', 'Divergence of the function vanishes'),
        opt('D', 'Gradient of the function is maximum')
    ],
    'B'
))

questions.append(make_q(
    56, 2,
    [{'type': 'text', 'text': 'In a rocket engine, the hot gas generated in the combustion chamber exits the nozzle with a mass flow rate 719 kg/sec and velocity 1794 m/s. The area of the nozzle exit section is 0.635 m^{2}. If the nozzle expansion is optimum, then the thrust produced by the engine is'}],
    [
        opt('A', '811 kN'),
        opt('B', '1290 kN'),
        opt('C', '1354 kN'),
        opt('D', '2172 kN')
    ],
    'B'
))

questions.append(make_q(
    57, 2,
    [
        {'type': 'text', 'text': 'For the control volume shown in the figure below, the velocities are measured both at the upstream and the downstream ends.'},
        fig_block('figures/gate-2007-ae-ae-57-figure-1.png', 'Control volume with upstream uniform velocity U_inf and downstream triangular velocity profile', 14),
        {'type': 'text', 'text': 'The flow of density ρ is incompressible, two dimensional and steady. The pressure is p_{∞} over the entire surface of the control volume. The drag on the airfoil is given by,'}
    ],
    [
        opt('A', '\\frac{ρ U_{∞}^{2} h}{3}'),
        opt('B', '0'),
        opt('C', '\\frac{ρ U_{∞}^{2} h}{6}'),
        opt('D', '2 ρ U_{∞}^{2} h')
    ],
    'A'
))

questions.append(make_q(
    58, 2,
    [{'type': 'text', 'text': 'A gas turbine engine operates with a constant area duct combustor with inlet and outlet stagnation temperatures 540 K and 1104 K respectively. Assume that the flow is one dimensional, incompressible and frictionless and that the heat addition is driving the flow inside the combustor. The pressure loss factor (stagnation pressure loss non-dimensionalized by the inlet dynamic pressure) of the combustor is'}],
    [
        opt('A', '0'),
        opt('B', '0.489'),
        opt('C', '1.044'),
        opt('D', '2.044')
    ],
    'A'
))

questions.append(make_q(
    59, 2,
    [{'type': 'text', 'text': 'The diffuser of an airplane engine decelerates the airflow from the flight Mach number 0.85 to the compressor inlet Mach number 0.38. Assume that the ratio of the specific heats is constant and equal to 1.4. If the diffuser pressure recovery ratio is 0.92, then the isentropic efficiency of the diffuser is'}],
    [
        opt('A', '0.631'),
        opt('B', '0.814'),
        opt('C', '0.892'),
        opt('D', '1.343')
    ],
    'B'
))

questions.append(make_q(
    60, 2,
    [
        {'type': 'text', 'text': 'An airfoil section is known to generate lift when placed in a uniform stream of speed U_{∞} at an incidence α. A biplane consisting of two such sections of identical chord c, separated by a distance h is shown in the following figure:'},
        fig_block('figures/gate-2007-ae-ae-60-figure-1.png', 'Biplane consisting of two identical chord airfoils separated by distance h', 15),
        {'type': 'text', 'text': 'With regard to this biplane, which of the following statements is true?'}
    ],
    [
        opt('A', 'Both the airfoils experience an upwash and an increased approach velocity'),
        opt('B', 'Both the airfoils experience a downwash and a decreased approach velocity'),
        opt('C', 'Both the airfoils experience an upwash and airfoil A experiences a decreased approach velocity while airfoil B experiences an increased approach velocity'),
        opt('D', 'The incidence for the individual sections of the biplane is not altered')
    ],
    'A'
))

questions.append(make_q(
    61, 2,
    [{'type': 'text', 'text': 'Numerical value of the integral J = ∫_{0}^{1} \\frac{1}{1+x^{2}} dx, if evaluated numerically using the Trapezoidal rule with dx = 0.2 would be'}],
    [
        opt('A', '1'),
        opt('B', 'π / 4'),
        opt('C', '0.7837'),
        opt('D', '0.2536')
    ],
    'C'
))

questions.append(make_q(
    62, 2,
    [{'type': 'text', 'text': 'The purpose of a fuel injection system in the combustor is'}],
    [
        opt('A', 'to accelerate the flow in the combustor'),
        opt('B', 'to increase the stagnation pressure of the fuel-air mixture'),
        opt('C', 'to ignite the fuel-air mixture'),
        opt('D', 'to convert the bulk fuel into tiny droplets')
    ],
    'D'
))

questions.append(make_q(
    63, 2,
    [{'type': 'text', 'text': 'Which one of the following values is nearer to the vacuum specific impulse of a rocket engine using liquid hydrogen and liquid oxygen as propellants?'}],
    [
        opt('A', '49 sec'),
        opt('B', '450 sec'),
        opt('C', '6000 sec'),
        opt('D', '40000 sec')
    ],
    'B'
))

questions.append(make_q(
    64, 2,
    [{'type': 'text', 'text': 'A circular cylinder is placed in an uniform stream of ideal fluid with its axis normal to the flow. Relative to the forward stagnation point, the angular positions along the circumference where the speed along the surface of the cylinder is equal to the free stream speed are'}],
    [
        opt('A', '30, 150, 210 and 330 degrees'),
        opt('B', '45, 135, 225 and 315 degrees'),
        opt('C', '0, 90, 180 and 270 degrees'),
        opt('D', '60, 120, 240 and 300 degrees')
    ],
    'A'
))

questions.append(make_q(
    65, 2,
    [{'type': 'text', 'text': 'The Newton-Raphson iteration formula to find a cube root of a positive number c is'}],
    [
        opt('A', 'x_{k+1} = \\frac{2x_{k}^{3} + ∛c}{3x_{k}^{2}}'),
        opt('B', 'x_{k+1} = \\frac{2x_{k}^{3} - ∛c}{-3x_{k}^{2}}'),
        opt('C', 'x_{k+1} = \\frac{2x_{k}^{3} + c}{3x_{k}^{2}}'),
        opt('D', 'x_{k+1} = \\frac{x_{k}^{3} + c}{3x_{k}^{2}}')
    ],
    'C'
))

questions.append(make_q(
    66, 2,
    [{'type': 'text', 'text': 'The torsion constant J of a thin-walled closed tube of thickness t and mean radius r is given by'}],
    [
        opt('A', 'J = 2π r t^{3}'),
        opt('B', 'J = 2π r^{3} t'),
        opt('C', 'J = 2π r^{2} t^{2}'),
        opt('D', 'J = 2π r^{4}')
    ],
    'B'
))

questions.append(make_q(
    67, 2,
    [
        {'type': 'text', 'text': 'An aerospace system shown in the following figure is designed in such a way that the expansion generated at A is completely absorbed by wall B for p_{1} = p_{d}, where p_{d} corresponds to the design condition.'},
        fig_block('figures/gate-2007-ae-ae-67-figure-1.png', 'Expansion generated at corner A absorbed by contoured wall B', 16),
        {'type': 'text', 'text': 'For p_{1} > p_{∞}, which of the following statements is NOT true?'}
    ],
    [
        opt('A', 'For p_{1} < p_{d}, the expansion fan from A gets reflected from B as a compression wave'),
        opt('B', 'For p_{1} > p_{d}, the expansion fan from A gets reflected from B as an expansion wave'),
        opt('C', 'For p_{1} < p_{d}, the expansion fan from A gets reflected from B as an expansion wave'),
        opt('D', 'For p_{1} > p_{d}, B always sees an expansion')
    ],
    'A'
))

questions.append(make_q(
    68, 2,
    [
        {'type': 'text', 'text': 'The span-wise lift distribution for three wings is shown in the following figure:'},
        fig_block('figures/gate-2007-ae-ae-68-figure-1.png', 'Span-wise lift distribution c_l/C_L vs y/s for three wings P, Q, R', 17),
        {'type': 'text', 'text': 'In the above figure, c_{l} refers to the section lift coefficient, C_{L} refers to the lift coefficient of the wing, y is the coordinate along the span and s is the span of the wing. A designer prefers to use a wing for which the stall begins at the root. Which of the wings will he choose?'}
    ],
    [
        opt('A', 'P'),
        opt('B', 'Q'),
        opt('C', 'R'),
        opt('D', 'None')
    ],
    'C'
))

questions.append(make_q(
    69, 2,
    [{'type': 'text', 'text': 'lim_{x → 0} \\frac{sin x}{e^{x} x} ='}],
    [
        opt('A', '10'),
        opt('B', '0'),
        opt('C', '1'),
        opt('D', '∞')
    ],
    'C'
))

questions.append(make_q(
    70, 2,
    [{'type': 'text', 'text': 'Let a dynamical system be described by the differential equation:\n2\\frac{dx}{dt} + cos x = 0\n\nWhich of the following differential equations describes this system in a close approximation sense for small perturbation about x = π / 4?'}],
    [
        opt('A', '2\\frac{dx}{dt} + sin x = 0'),
        opt('B', '2\\frac{dx}{dt} - \\frac{1}{√2} x = 0'),
        opt('C', '\\frac{dx}{dt} + cos x = 0'),
        opt('D', '\\frac{dx}{dt} + x = 0')
    ],
    'A'
))

# ==================== Common Data Questions (Q71 to Q75) ====================
# Group: Common Data for Questions 71, 72 & 73
questions.append(make_q(
    71, 2,
    [{'type': 'text', 'text': 'The most forward location of the airplane center of gravity permitted to fulfill the designer\'s requirement on longitudinal static stability margin is'}],
    [
        opt('A', '0.35 \\overline{c}'),
        opt('B', '0.25 \\overline{c}'),
        opt('C', '0.15 \\overline{c}'),
        opt('D', '0.52 \\overline{c}')
    ],
    'B',
    group_id='gate-2007-ae-common-data-71-73'
))

questions.append(make_q(
    72, 2,
    [{'type': 'text', 'text': 'The most aft location of the airplane center of gravity permitted to fulfill designer\'s requirement on longitudinal static stability is'}],
    [
        opt('A', '0.35 \\overline{c}'),
        opt('B', '0.45 \\overline{c}'),
        opt('C', '0.52 \\overline{c}'),
        opt('D', '0.67 \\overline{c}')
    ],
    'A',
    group_id='gate-2007-ae-common-data-71-73'
))

questions.append(make_q(
    73, 2,
    [{'type': 'text', 'text': 'The center of gravity location to have \\frac{dδe}{dC_{L}} = 0 is'}],
    [
        opt('A', '0.35 \\overline{c}'),
        opt('B', '0.45 \\overline{c}'),
        opt('C', '0.5 \\overline{c}'),
        opt('D', '0.4 \\overline{c}')
    ],
    'D',
    group_id='gate-2007-ae-common-data-71-73'
))

# Group: Common Data for Questions 74 & 75
questions.append(make_q(
    74, 2,
    [{'type': 'text', 'text': 'The system shows the following type of coordinate coupling'}],
    [
        opt('A', 'static coupling'),
        opt('B', 'dynamic coupling'),
        opt('C', 'static and dynamic coupling'),
        opt('D', 'no coupling')
    ],
    'B',
    group_id='gate-2007-ae-common-data-74-75'
))

questions.append(make_q(
    75, 2,
    [{'type': 'text', 'text': 'The two natural frequencies of the system are given as'}],
    [
        opt('A', '√(\\frac{4 ± √5}{3} \\frac{k}{m})'),
        opt('B', '√(\\frac{4 ± √3}{3} \\frac{k}{m})'),
        opt('C', '√(\\frac{4 ± √7}{3} \\frac{k}{m})'),
        opt('D', '√(\\frac{4 ± √11}{3} \\frac{k}{m})')
    ],
    'C',
    group_id='gate-2007-ae-common-data-74-75'
))

# ==================== Linked Answer Questions (Q76 to Q85) ====================
# Group: Linked Answer Questions 76 & 77
questions.append(make_q(
    76, 2,
    [{'type': 'text', 'text': 'The maximum rate of climb achievable by this airplane at 5 km altitude will be'}],
    [
        opt('A', '1.65 m/s'),
        opt('B', '0.51 m/s'),
        opt('C', '1.43 m/s'),
        opt('D', '3.65 m/s')
    ],
    'C',
    group_id='gate-2007-ae-linked-76-77'
))

questions.append(make_q(
    77, 2,
    [{'type': 'text', 'text': 'If during the maximum rate of climb at 5 km altitude, the airplane was flying at an angle of attack of 4 degrees and attitude (pitch) angle of 5 degrees, what was equivalent airspeed of the airplane?'}],
    [
        opt('A', '40.2 m/s'),
        opt('B', '63.7 m/s'),
        opt('C', '130.3 m/s'),
        opt('D', '20.2 m/s')
    ],
    'B',
    group_id='gate-2007-ae-linked-76-77'
))

# Group: Linked Answer Questions 78 & 79
questions.append(make_q(
    78, 2,
    [{'type': 'text', 'text': 'The lift curve slope of this wing is'}],
    [
        opt('A', '0.10 per deg'),
        opt('B', '0.092 per deg'),
        opt('C', '0.075 per deg'),
        opt('D', '0.050 per deg')
    ],
    'C',
    group_id='gate-2007-ae-linked-78-79'
))

questions.append(make_q(
    79, 2,
    [{'type': 'text', 'text': 'The span efficiency factor of this wing is'}],
    [
        opt('A', '1.0'),
        opt('B', '0.91'),
        opt('C', '0.75'),
        opt('D', '0.63')
    ],
    'B',
    group_id='gate-2007-ae-linked-78-79'
))

# Group: Linked Answer Questions 80 & 81
questions.append(make_q(
    80, 2,
    [{'type': 'text', 'text': 'The partial fraction expansion of F(s) = \\frac{s+10}{(s+2)(s+20)} is'}],
    [
        opt('A', '\\frac{1}{s+2} + \\frac{1}{s+20}'),
        opt('B', '\\frac{5}{s+2} + \\frac{2}{s+20}'),
        opt('C', '\\frac{2}{s+2} + \\frac{20}{s+20}'),
        opt('D', '\\frac{4/9}{s+2} + \\frac{5/9}{s+20}')
    ],
    'D',
    group_id='gate-2007-ae-linked-80-81'
))

questions.append(make_q(
    81, 2,
    [{'type': 'text', 'text': 'The inverse Laplace transform of F(s) is'}],
    [
        opt('A', '2 e^{-2t} + 20 e^{-20t}'),
        opt('B', '\\frac{4}{9} e^{-2t} + \\frac{5}{9} e^{-20t}'),
        opt('C', '5 e^{-2t} + 2 e^{-20t}'),
        opt('D', '\\frac{9}{4} e^{-2t} + \\frac{9}{5} e^{-20t}')
    ],
    'B',
    group_id='gate-2007-ae-linked-80-81'
))

# Group: Linked Answer Questions 82 & 83
questions.append(make_q(
    82, 2,
    [{'type': 'text', 'text': 'The boundary conditions needed for a rod fixed at the root (x = 0) and free at the tip (x = l) are'}],
    [
        opt('A', 'u(x=0) = 0, \\frac{∂u}{∂x}(x=l) = 0'),
        opt('B', 'u(x=l) = 0, \\frac{∂u}{∂x}(x=l) = 0'),
        opt('C', 'u(x=0) = 0, u(x=l) = 0'),
        opt('D', '\\frac{∂u}{∂x}(x=0) = 0, \\frac{∂u}{∂x}(x=l) = 0')
    ],
    'A',
    group_id='gate-2007-ae-linked-82-83'
))

questions.append(make_q(
    83, 2,
    [{'type': 'text', 'text': 'The natural frequencies ω of the fixed-free rod can then be obtained using'}],
    [
        opt('A', 'cos(\\frac{ω l}{c}) = 0'),
        opt('B', 'sin(\\frac{ω l}{c}) = 0'),
        opt('C', 'cos(\\frac{ω c}{l}) = 0'),
        opt('D', 'cos(\\frac{ω}{c}) = 0')
    ],
    'A',
    group_id='gate-2007-ae-linked-82-83'
))

# Group: Linked Answer Questions 84 & 85
questions.append(make_q(
    84, 2,
    [{'type': 'text', 'text': 'The compressor pressure ratio is'}],
    [
        opt('A', '0.22'),
        opt('B', '0.28'),
        opt('C', '3.50'),
        opt('D', '3.90')
    ],
    'C',
    group_id='gate-2007-ae-linked-84-85'
))

questions.append(make_q(
    85, 2,
    [{'type': 'text', 'text': 'If the polytropic efficiency of the compressor is 0.89, then the isentropic efficiency of the compressor is'}],
    [
        opt('A', '0.613'),
        opt('B', '0.869'),
        opt('C', '0.89'),
        opt('D', '0.98')
    ],
    'B',
    group_id='gate-2007-ae-linked-84-85'
))

# ==================== Question Groups ====================
question_groups = [
    {
        'id': 'gate-2007-ae-common-data-71-73',
        'type': 'common-data',
        'title': 'Common Data Questions',
        'content': [
            {'type': 'text', 'text': 'Common Data for Questions 71, 72 and 73: An airplane designer wants to keep longitudinal static stability margin (SM) within 5% to 15% of mean aerodynamic chord. A wind tunnel test of the model showed that for \\overline{X}_{CG} = 0.3, \\frac{dC_{m}}{dC_{L}} = -0.1. Note that the distance from the wing leading edge to the center of gravity (X_{CG}) has been non-dimensionalized by dividing it with mean aerodynamic chord, \\overline{c}, such that \\overline{X}_{CG} = X_{CG} / \\overline{c}. Note also that the relation \\frac{dC_{m}}{dC_{L}} = -SM holds true for this airplane.'}
        ],
        'questionIds': ['gate-2007-ae-ae-71', 'gate-2007-ae-ae-72', 'gate-2007-ae-ae-73']
    },
    {
        'id': 'gate-2007-ae-common-data-74-75',
        'type': 'common-data',
        'title': 'Common Data Questions',
        'content': [
            {'type': 'text', 'text': 'Common Data for Questions 74 and 75: Consider the spring mass system shown in the figure below. This system has two degrees of freedom representing the motions of the two masses.'},
            fig_block('figures/gate-2007-ae-ae-74-figure-1.png', 'Two degree of freedom spring mass system with masses m and 3m and springs k', 18)
        ],
        'questionIds': ['gate-2007-ae-ae-74', 'gate-2007-ae-ae-75']
    },
    {
        'id': 'gate-2007-ae-linked-76-77',
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 76 and 77: For a piston propeller airplane weighing 20000 N, the flight testing at 5 km pressure altitude in standard atmosphere gave the variation of power required versus true air speed as shown in figure below. The student forgot to label the air speed axis. The maximum climb rate at sea level was calculated to be 4 m/s. Assume shaft power available to be independent of speed of flight. For piston propeller airplane, it can be assumed that the shaft power available is proportional to ambient density. Values of air density at sea level and at 5 km pressure altitude are 1.225 kg/m^{3} and 0.74 kg/m^{3}, respectively.'},
            fig_block('figures/gate-2007-ae-ae-76-figure-1.png', 'Power Required vs True air speed at Sea level and 5km', 19)
        ],
        'questionIds': ['gate-2007-ae-ae-76', 'gate-2007-ae-ae-77'],
        'dependencies': [
            {
                'questionId': 'gate-2007-ae-ae-77',
                'dependsOn': 'gate-2007-ae-ae-76'
            }
        ]
    },
    {
        'id': 'gate-2007-ae-linked-78-79',
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 78 and 79: A model wing of rectangular planform has a chord of 0.2 m and a span of 1.2 m. It has a symmetric airfoil section whose lift curve slope is 0.1 per degree. When this wing is mounted at 8 degrees angle of attack in a freestream of 20 m/s it is found to develop 35.3 N lift when the density of air is 1.225 kg/m^{3}.'}
        ],
        'questionIds': ['gate-2007-ae-ae-78', 'gate-2007-ae-ae-79'],
        'dependencies': [
            {
                'questionId': 'gate-2007-ae-ae-79',
                'dependsOn': 'gate-2007-ae-ae-78'
            }
        ]
    },
    {
        'id': 'gate-2007-ae-linked-80-81',
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 80 and 81: Let F(s) = \\frac{s+10}{(s+2)(s+20)}'}
        ],
        'questionIds': ['gate-2007-ae-ae-80', 'gate-2007-ae-ae-81'],
        'dependencies': [
            {
                'questionId': 'gate-2007-ae-ae-81',
                'dependsOn': 'gate-2007-ae-ae-80'
            }
        ]
    },
    {
        'id': 'gate-2007-ae-linked-82-83',
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 82 and 83: The equation of motion of a vibrating rod is given by \\frac{∂^{2} u}{∂x^{2}} = \\frac{1}{c^{2}} \\frac{∂^{2} u}{∂t^{2}}. Here u is the displacement along the rod and is a function of both position x and time t. To find the response of the vibrating rod, we need to solve this equation using boundary conditions and initial conditions.'}
        ],
        'questionIds': ['gate-2007-ae-ae-82', 'gate-2007-ae-ae-83'],
        'dependencies': [
            {
                'questionId': 'gate-2007-ae-ae-83',
                'dependsOn': 'gate-2007-ae-ae-82'
            }
        ]
    },
    {
        'id': 'gate-2007-ae-linked-84-85',
        'type': 'linked-answer',
        'title': 'Linked Answer Questions',
        'content': [
            {'type': 'text', 'text': 'Statement for Linked Answer Questions 84 and 85: Air enters the compressor of a gas turbine engine with velocity 127 m/s, density 1.2 kg/m^{3} and stagnation pressure 0.9 MPa. Air exits the compressor with velocity 139 m/s and stagnation pressure 3.15 MPa. Assume that the ratio of specific heats is constant and equal to 1.4.'}
        ],
        'questionIds': ['gate-2007-ae-ae-84', 'gate-2007-ae-ae-85'],
        'dependencies': [
            {
                'questionId': 'gate-2007-ae-ae-85',
                'dependsOn': 'gate-2007-ae-ae-84'
            }
        ]
    }
]

# Paper structure
paper_data = {
    'schemaVersion': 1,
    'id': 'gate-2007-ae',
    'exam': 'GATE',
    'year': 2007,
    'paper': 'AE',
    'title': 'GATE 2007 Aerospace Engineering (AE)',
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
    'questionRefs': [
        {
            'id': q['id'],
            'number': q['number'],
            'section': q['section'],
            'type': q['type']
        }
        for q in questions
    ],
    'questionGroups': question_groups,
    'source': {
        'paper': 'AE',
        'year': 2007,
        'file': PDF_PATH,
        'sha256': pdf_hash,
        'keyFile': KEY_PDF_PATH,
        'keySha256': key_pdf_hash
    },
    'questions': questions
}

# Write out data/ae/2007.json
with open('data/ae/2007.json', 'w', encoding='utf-8') as f:
    json.dump(paper_data, f, indent=2)
    f.write('\n')

print(f"Generated 2007.json successfully with {len(questions)} questions!")
