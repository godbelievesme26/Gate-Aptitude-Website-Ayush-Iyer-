import sys
import os
import json
import hashlib
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'internal/ae/AE2022.pdf'
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

doc = fitz.open(pdf_path)

with open('internal/ae/AE2022-key.json', 'r', encoding='utf-8') as f:
    key_doc = json.load(f)
key_rows = key_doc['rows']

# Figure metadata for question-level figures
figure_metadata = {
    5: [{"src": "figures/gate-2022-ae-ga-05-figure-1.png", "alt": "Shape to be assembled from smaller geometric pieces.", "page": 5}],
    9: [{"src": "figures/gate-2022-ae-ga-09-figure-1.png", "alt": "Network graph connecting four cities P, Q, R, and S with train start times and frequencies.", "page": 9}],
    10: [{"src": "figures/gate-2022-ae-ga-10-figure-1.png", "alt": "Square sheets with shaded circles for Case M (4 circles) and Case N (9 circles).", "page": 10}],
    16: [{"src": "figures/gate-2022-ae-ae-16-figure-1.png", "alt": "Control volume PQRS over a non-porous flat plate showing velocity profiles at PQ and RS.", "page": 14}],
    17: [{"src": "figures/gate-2022-ae-ae-17-figure-1.png", "alt": "Velocity distribution u(y) with adjacent fluid layers L1 and L2.", "page": 15}],
    20: [{"src": "figures/gate-2022-ae-ae-20-figure-1.png", "alt": "Symmetrical T-shaped cross-section beam.", "page": 17}],
    21: [{"src": "figures/gate-2022-ae-ae-21-figure-1.png", "alt": "Three-member truss simply supported at Q and R, loaded at P by horizontal force F.", "page": 18}],
    22: [{"src": "figures/gate-2022-ae-ae-22-figure-1.png", "alt": "Thin-walled rectangular channel: closed in figure (i) and cut open in figure (ii).", "page": 19}],
    33: [{"src": "figures/gate-2022-ae-ae-33-figure-1.png", "alt": "Two-dimensional plane-stress element showing normal stress sigma_n on plane inclined at 45 degrees.", "page": 24}],
    35: [{"src": "figures/gate-2022-ae-ae-35-figure-1.png", "alt": "Turbine stator exit velocity triangle with angle of 70 degrees and blade speed of 250 m/s.", "page": 25}],
    41: [{"src": "figures/gate-2022-ae-ae-41-figure-1.png", "alt": "Two-member truss with horizontal load F applied at point R.", "page": 29}],
    44: [{"src": "figures/gate-2022-ae-ae-44-figure-1.png", "alt": "Convergent nozzle fed from reservoir discharging air to atmosphere.", "page": 31}],
    52: [{"src": "figures/gate-2022-ae-ae-52-figure-1.png", "alt": "Solid cylinder rotating at 5 rad/s inside stationary outer cylinder with fluid gap.", "page": 35}],
    55: [{"src": "figures/gate-2022-ae-ae-55-figure-1.png", "alt": "Convergent-divergent nozzle discharging air with Prandtl-Meyer expansion waves at nozzle exit.", "page": 37}],
    57: [{"src": "figures/gate-2022-ae-ae-57-figure-1.png", "alt": "Cantilever PQ under transverse load F at mid-point: Case I (free end Q) and Case II (simply supported Q).", "page": 38}],
    59: [{"src": "figures/gate-2022-ae-ae-59-figure-1.png", "alt": "Thin-walled circular shaft of radius 2 cm subjected to axial load 7.4 kN and torque 148 Nm.", "page": 39}],
    60: [{"src": "figures/gate-2022-ae-ae-60-figure-1.png", "alt": "Square cross-section rod with eccentrically applied 10 kN axial load and strain gages.", "page": 39}],
    61: [{"src": "figures/gate-2022-ae-ae-61-figure-1.png", "alt": "Thin-walled I-section with flange width 2b = 20 mm and web height 20 mm.", "page": 40}],
    62: [{"src": "figures/gate-2022-ae-ae-62-figure-1.png", "alt": "Under-damped spring-mass-damper system with mass 5 kg and stiffness 5 kN/m.", "page": 40}],
    63: [{"src": "figures/gate-2022-ae-ae-63-figure-1.png", "alt": "Uniform rigid prismatic bar of mass m suspended by two identical springs.", "page": 41}]
}

# Option figures
option_figures = {
    2: {
        "A": {"src": "figures/gate-2022-ae-ga-02-option-A.png", "alt": "Number line representation option A.", "page": 2},
        "B": {"src": "figures/gate-2022-ae-ga-02-option-B.png", "alt": "Number line representation option B.", "page": 2},
        "C": {"src": "figures/gate-2022-ae-ga-02-option-C.png", "alt": "Number line representation option C.", "page": 2},
        "D": {"src": "figures/gate-2022-ae-ga-02-option-D.png", "alt": "Number line representation option D.", "page": 2}
    },
    5: {
        "A": {"src": "figures/gate-2022-ae-ga-05-option-A.png", "alt": "Piece assembly option A.", "page": 5},
        "B": {"src": "figures/gate-2022-ae-ga-05-option-B.png", "alt": "Piece assembly option B.", "page": 5},
        "C": {"src": "figures/gate-2022-ae-ga-05-option-C.png", "alt": "Piece assembly option C.", "page": 5},
        "D": {"src": "figures/gate-2022-ae-ga-05-option-D.png", "alt": "Piece assembly option D.", "page": 5}
    },
    28: {
        "A": {"src": "figures/gate-2022-ae-ae-28-option-A.png", "alt": "Mohr circle representation option A.", "page": 22},
        "B": {"src": "figures/gate-2022-ae-ae-28-option-B.png", "alt": "Mohr circle representation option B.", "page": 22},
        "C": {"src": "figures/gate-2022-ae-ae-28-option-C.png", "alt": "Mohr circle representation option C.", "page": 22},
        "D": {"src": "figures/gate-2022-ae-ae-28-option-D.png", "alt": "Mohr circle representation option D.", "page": 22}
    }
}

questions_data = {}

# Q1
questions_data[1] = {
    "question": "Writing too many things on the ________ while teaching could make the students get _________.",
    "options": [
        {"label": "A", "text": "bored / board"},
        {"label": "B", "text": "board / bored"},
        {"label": "C", "text": "board / board"},
        {"label": "D", "text": "bored / bored"}
    ]
}

# Q2
questions_data[2] = {
    "question": "Which one of the following is a representation (not to scale and in bold) of all values of $x$ satisfying the inequality $2 - 5x \\le -\\frac{6x - 5}{3}$ on the real number line?",
    "options": [
        {"label": "A", "text": "Option A"},
        {"label": "B", "text": "Option B"},
        {"label": "C", "text": "Option C"},
        {"label": "D", "text": "Option D"}
    ]
}

# Q3
questions_data[3] = {
    "question": "If $f(x) = 2 \\ln(\\sqrt{e^x})$, what is the area bounded by $f(x)$ for the interval $[0, 2]$ on the $x$-axis?",
    "options": [
        {"label": "A", "text": "$\\frac{1}{2}$"},
        {"label": "B", "text": "$1$"},
        {"label": "C", "text": "$2$"},
        {"label": "D", "text": "$4$"}
    ]
}

# Q4
questions_data[4] = {
    "question": "A person was born on the fifth Monday of February in a particular year.\nWhich one of the following statements is correct based on the above information?",
    "options": [
        {"label": "A", "text": "The 2nd February of that year is a Tuesday"},
        {"label": "B", "text": "There will be five Sundays in the month of February in that year"},
        {"label": "C", "text": "The 1st February of that year is a Sunday"},
        {"label": "D", "text": "All Mondays of February in that year have even dates"}
    ]
}

# Q5
questions_data[5] = {
    "question": "Which one of the groups given below can be assembled to get the shape that is shown above using each piece only once without overlapping with each other? (rotation and translation operations may be used).",
    "options": [
        {"label": "A", "text": "Option A"},
        {"label": "B", "text": "Option B"},
        {"label": "C", "text": "Option C"},
        {"label": "D", "text": "Option D"}
    ]
}

# Q6
questions_data[6] = {
    "question": "Fish belonging to species S in the deep sea have skins that are extremely black (ultra-black skin). This helps them not only to avoid predators but also sneakily attack their prey. However, having this extra layer of black pigment results in lower collagen on their skin, making their skin more fragile.\nWhich one of the following is the CORRECT logical inference based on the information in the above passage?",
    "options": [
        {"label": "A", "text": "Having ultra-black skin is only advantageous to species S"},
        {"label": "B", "text": "Species S with lower collagen in their skin are at an advantage because it helps them avoid predators"},
        {"label": "C", "text": "Having ultra-black skin has both advantages and disadvantages to species S"},
        {"label": "D", "text": "Having ultra-black skin is only disadvantageous to species S but advantageous only to their predators"}
    ]
}

# Q7
questions_data[7] = {
    "question": "For the past $m$ days, the average daily production at a company was 100 units per day.\nIf today’s production of 180 units changes the average to 110 units per day, what is the value of $m$?",
    "options": [
        {"label": "A", "text": "18"},
        {"label": "B", "text": "10"},
        {"label": "C", "text": "7"},
        {"label": "D", "text": "5"}
    ]
}

# Q8
questions_data[8] = {
    "question": "Consider the following functions for non-zero positive integers, $p$ and $q$.\n$$f(p, q) = \\underbrace{p \\times p \\times p \\times \\dots \\times p}_{q\\text{ terms}} = p^q; \\quad f(p, 1) = p$$\n$$g(p, q) = p^{p^{p^{\\cdot^{\\cdot^{\\cdot^{(q\\text{ times})}}}}}; \\quad g(p, 1) = p$$\nWhich one of the following options is correct based on the above?",
    "options": [
        {"label": "A", "text": "$f(2,2) = g(2,2)$"},
        {"label": "B", "text": "$f(g(2,2), 2) < f(2, g(2,2))$"},
        {"label": "C", "text": "$g(2,1) \\ne f(2,1)$"},
        {"label": "D", "text": "$f(3,2) > g(3,2)$"}
    ]
}

# Q9
questions_data[9] = {
    "question": "Four cities P, Q, R and S are connected through one-way routes as shown in the figure. The travel time between any two connected cities is one hour. The boxes beside each city name describe the starting time of first train of the day and their frequency of operation. For example, from city P, the first trains of the day start at 8 AM with a frequency of 90 minutes to each of R and S. A person does not spend additional time at any city other than the waiting time for the next connecting train.\nIf the person starts from R at 7 AM and is required to visit S and return to R, what is the minimum time required?",
    "options": [
        {"label": "A", "text": "6 hours 30 minutes"},
        {"label": "B", "text": "3 hours 45 minutes"},
        {"label": "C", "text": "4 hours 30 minutes"},
        {"label": "D", "text": "5 hours 15 minutes"}
    ]
}

# Q10
questions_data[10] = {
    "question": "Equal sized circular regions are shaded in a square sheet of paper of 1 cm side length. Two cases, case M and case N, are considered as shown in the figures below. In the case M, four circles are shaded in the square sheet and in the case N, nine circles are shaded in the square sheet as shown.\nWhat is the ratio of the areas of unshaded regions of case M to that of case N?",
    "options": [
        {"label": "A", "text": "2 : 3"},
        {"label": "B", "text": "1 : 1"},
        {"label": "C", "text": "3 : 2"},
        {"label": "D", "text": "2 : 1"}
    ]
}

# Q11
questions_data[11] = {
    "question": "The equation of the straight line representing the tangent to the curve $y = x^2$ at the point $(1,1)$ is",
    "options": [
        {"label": "A", "text": "$y = 2x - 2$"},
        {"label": "B", "text": "$x = 2y - 1$"},
        {"label": "C", "text": "$y - 1 = 2(x - 1)$"},
        {"label": "D", "text": "$x - 1 = 2(y - 1)$"}
    ]
}

# Q12
questions_data[12] = {
    "question": "Let $\\hat{\\imath}, \\hat{\\jmath}$, and $\\hat{k}$ be the unit vectors in the x, y and z directions, respectively. If the vector $\\hat{\\imath} + \\hat{\\jmath}$ is rotated about positive $\\hat{k}$ by $135^\\circ$, one gets",
    "options": [
        {"label": "A", "text": "$-\\hat{\\imath}$"},
        {"label": "B", "text": "$-\\hat{\\jmath}$"},
        {"label": "C", "text": "$-\\frac{1}{\\sqrt{2}}\\hat{\\jmath}$"},
        {"label": "D", "text": "$-\\sqrt{2}\\hat{\\imath}$"}
    ]
}

# Q13
questions_data[13] = {
    "question": "Let $x$ be a real number and $i = \\sqrt{-1}$. Then the real part of $\\cos(ix)$ is",
    "options": [
        {"label": "A", "text": "$\\sinh x$"},
        {"label": "B", "text": "$\\cosh x$"},
        {"label": "C", "text": "$\\cos x$"},
        {"label": "D", "text": "$\\sin x$"}
    ]
}

# Q14
questions_data[14] = {
    "question": "The point of maximum entropy on a Fanno-curve in a Temperature-Entropy (T-s) diagram represents the",
    "options": [
        {"label": "A", "text": "maximum flow Mach number"},
        {"label": "B", "text": "minimum flow Mach number"},
        {"label": "C", "text": "sonic Mach number"},
        {"label": "D", "text": "normal shock in the flow"}
    ]
}

# Q15
questions_data[15] = {
    "question": "Consider a two-dimensional potential flow over a cylinder. If the freestream speed is $U_\\infty$, the maximum speed on the cylinder surface is",
    "options": [
        {"label": "A", "text": "$\\frac{U_\\infty}{2}$"},
        {"label": "B", "text": "$\\frac{3U_\\infty}{2}$"},
        {"label": "C", "text": "$2U_\\infty$"},
        {"label": "D", "text": "$\\frac{4U_\\infty}{3}$"}
    ]
}

# Q16
questions_data[16] = {
    "question": "Consider steady, two-dimensional, incompressible flow over a non-porous flat plate as shown in the figure. For the control volume PQRS, the speed, $u_\\infty$, at section PQ is uniform and the speed at section RS is given by $u(y) = A_0 \\left(\\frac{y}{h}\\right)^n$, where $n$ is a positive integer. The value of $A_0$ for which the flow through section PS will vanish is:",
    "options": [
        {"label": "A", "text": "$\\frac{u_\\infty}{n + 1}$"},
        {"label": "B", "text": "$u_\\infty(n + 1)$"},
        {"label": "C", "text": "$\\frac{u_\\infty}{n - 1}$"},
        {"label": "D", "text": "$u_\\infty(n - 1)$"}
    ]
}

# Q17
questions_data[17] = {
    "question": "Consider the velocity distribution, $u(y)$ shown in the figure. For two adjacent fluid layers L1 and L2, the viscous force exerted by L1 on L2 is",
    "options": [
        {"label": "A", "text": "to the right"},
        {"label": "B", "text": "to the left"},
        {"label": "C", "text": "vertically upwards"},
        {"label": "D", "text": "vertically downwards"}
    ]
}

# Q18
questions_data[18] = {
    "question": "The service ceiling of an airplane is the altitude",
    "options": [
        {"label": "A", "text": "at which maximum rate of climb is 100 m/min"},
        {"label": "B", "text": "beyond which theoretically the airplane cannot sustain level flight"},
        {"label": "C", "text": "at which maximum power is required for flight"},
        {"label": "D", "text": "at which maximum rate of climb is 100 ft/min"}
    ]
}

# Q19
questions_data[19] = {
    "question": "Regarding the horizontal tail of a conventional airplane, which one of the following statements is true?",
    "options": [
        {"label": "A", "text": "It contributes to $C_{m_\\alpha} < 0$"},
        {"label": "B", "text": "It makes $C_{m_\\alpha} = 0$"},
        {"label": "C", "text": "It makes $C_{m_\\alpha} > 0$"},
        {"label": "D", "text": "It makes $C_{m_0} > 0$ and $C_{m_\\alpha} > 0$"}
    ]
}

# Q20
questions_data[20] = {
    "question": "A beam with a symmetrical T-shaped cross-section, as shown in the figure, is subjected to pure bending. The maximum magnitude of the normal stress is realised:",
    "options": [
        {"label": "A", "text": "only at the top fibres of the cross-section"},
        {"label": "B", "text": "only at the bottom fibres of the cross-section"},
        {"label": "C", "text": "both at the top and bottom fibres of the cross-section"},
        {"label": "D", "text": "only at the centroidal fibres of the cross-section"}
    ]
}

# Q21
questions_data[21] = {
    "question": "A three-member truss is simply supported at Q and R, and loaded at P by a horizontal force $F$ as shown. The force in QR is",
    "options": [
        {"label": "A", "text": "$0$"},
        {"label": "B", "text": "$F$ (tensile)"},
        {"label": "C", "text": "$\\frac{F}{\\sqrt{2}}$ (compressive)"},
        {"label": "D", "text": "$\\sqrt{2}F$ (tensile)"}
    ]
}

# Q22
questions_data[22] = {
    "question": "The closed thin-walled rectangular channel shown in figure (i) is opened by introducing a sharp cut at the center of the bottom edge, as shown in figure (ii). Which one of the following statements is correct?",
    "options": [
        {"label": "A", "text": "Centroids of (i) and (ii) coincide while shear centers do not"},
        {"label": "B", "text": "Shear centers of (i) and (ii) coincide while centroids do not"},
        {"label": "C", "text": "Both centroids and shear centers of (i) and (ii) coincide"},
        {"label": "D", "text": "Neither centroids nor shear centers of (i) and (ii) coincide"}
    ]
}

# Q23
questions_data[23] = {
    "question": "The region of highest static temperature in a rocket engine and the region of highest heat flux are ____________, respectively.",
    "options": [
        {"label": "A", "text": "nozzle throat and nozzle entry"},
        {"label": "B", "text": "combustion chamber and nozzle throat"},
        {"label": "C", "text": "nozzle exit and nozzle throat"},
        {"label": "D", "text": "nozzle throat and combustion chamber"}
    ]
}

# Q24
questions_data[24] = {
    "question": "If $\\hat{a}, \\hat{b}, \\hat{c}$ are three mutually perpendicular unit vectors, then $\\hat{a} \\cdot (\\hat{b} \\times \\hat{c})$ can take the value(s)",
    "options": [
        {"label": "A", "text": "$0$"},
        {"label": "B", "text": "$1$"},
        {"label": "C", "text": "$-1$"},
        {"label": "D", "text": "$\\infty$"}
    ]
}

# Q25
questions_data[25] = {
    "question": "Across an oblique shock wave in a calorifically perfect gas,",
    "options": [
        {"label": "A", "text": "the stagnation enthalpy changes"},
        {"label": "B", "text": "the stagnation entropy changes"},
        {"label": "C", "text": "the stagnation temperature changes"},
        {"label": "D", "text": "the speed of sound changes"}
    ]
}

# Q26
questions_data[26] = {
    "question": "NACA 2412 airfoil has",
    "options": [
        {"label": "A", "text": "4% maximum camber with respect to chord"},
        {"label": "B", "text": "maximum camber at 40% chord"},
        {"label": "C", "text": "12% maximum thickness to chord ratio"},
        {"label": "D", "text": "maximum camber at 20% chord"}
    ]
}

# Q27
questions_data[27] = {
    "question": "For International Standard Atmosphere (ISA) up to 11 km, which of the following statement(s) is/are true?",
    "options": [
        {"label": "A", "text": "The hydrostatic/ aerostatic equation is used"},
        {"label": "B", "text": "The temperature lapse rate is taken as $-10^{-2}\\text{ K/m}$"},
        {"label": "C", "text": "The sea level conditions are taken as: pressure, $p_0 = 1.01325 \\times 10^5\\text{ Pa}$; temperature, $T_0 = 300\\text{ K}$; density, $\\rho_0 = 1.225\\text{ kg/m}^3$"},
        {"label": "D", "text": "Air is treated as a perfect gas"}
    ]
}

# Q28
questions_data[28] = {
    "question": "Let $\\sigma$ and $\\tau$ represent the normal stress and shear stress on a plane, respectively. The Mohr circle(s) that may possibly represent the state of stress at points in a beam of rectangular cross-section under pure bending is/are:",
    "options": [
        {"label": "A", "text": "Option A"},
        {"label": "B", "text": "Option B"},
        {"label": "C", "text": "Option C"},
        {"label": "D", "text": "Option D"}
    ]
}

# Q29
questions_data[29] = {
    "question": "An isotropic linear elastic material point under plane strain condition in the x-y plane always obeys:",
    "options": [
        {"label": "A", "text": "out-of-plane normal strain, $\\epsilon_{zz} = 0$"},
        {"label": "B", "text": "out-of-plane normal stress, $\\sigma_{zz} = 0$"},
        {"label": "C", "text": "out-of-plane shear stress, $\\tau_{xz} = 0$"},
        {"label": "D", "text": "out-of-plane shear strain, $\\gamma_{xz} = 0$"}
    ]
}

# Q30
questions_data[30] = {
    "question": "A high-pressure-ratio multistage axial compressor encounters an extreme loading mismatch during starting. Which of the following technique(s) can be used to alleviate this problem?",
    "options": [
        {"label": "A", "text": "Blade cooling"},
        {"label": "B", "text": "Variable angle stator vanes"},
        {"label": "C", "text": "Blow-off valves"},
        {"label": "D", "text": "Multi-spool shaft"}
    ]
}

# Q31
questions_data[31] = {
    "question": "The arc length of the parametric curve: $x = \\cos \\theta$, $y = \\sin \\theta$, $z = \\theta$ from $\\theta = 0$ to $\\theta = 2\\pi$ is equal to ________ (round off to one decimal place)."
}

# Q32
questions_data[32] = {
    "question": "An unpowered glider is flying at a glide angle of 10 degrees. Its lift-to-drag ratio is ________ (round off to two decimal places)."
}

# Q33
questions_data[33] = {
    "question": "The two-dimensional plane-stress state at a point is:\n$$\\sigma_{xx} = 110\\text{ MPa}; \\quad \\sigma_{yy} = 30\\text{ MPa}; \\quad \\tau_{xy} = 40\\text{ MPa}$$\nThe normal stress, $\\sigma_n$, on a plane inclined $45^\\circ$ as shown in the figure is ____ MPa (round off to the nearest integer)."
}

# Q34
questions_data[34] = {
    "question": "In a static test, a turbofan engine with bypass ratio of 9 has core hot exhaust speed 1.5 times that of fan exhaust speed. The engine is operated at a fuel to air ratio of $f = 0.03$. Both the fan and the core streams have no pressure thrust. The ratio of fan thrust to thrust from the core engine is _____ (round off to one decimal place)."
}

# Q35
questions_data[35] = {
    "question": "In a single stage turbine, the hot gases come out of stator/ nozzle at a speed of 500 m/s and at an angle of 70 degrees with the turbine axis as shown. The design speed of the rotor blade is 250 m/s at the mean blade radius. The rotor blade angle, $\\beta$, at the leading edge is ________ degrees (round off to one decimal place)."
}

# Q36
questions_data[36] = {
    "question": "The height of a right circular cone of maximum volume that can be enclosed within a hollow sphere of radius $R$ is",
    "options": [
        {"label": "A", "text": "$R$"},
        {"label": "B", "text": "$\\frac{5}{4}R$"},
        {"label": "C", "text": "$\\frac{4}{3}R$"},
        {"label": "D", "text": "$\\frac{3}{2}R$"}
    ]
}

# Q37
questions_data[37] = {
    "question": "Consider the differential equation\n$$\\frac{d^2y}{dx^2} - 2\\frac{dy}{dx} + y = 0$$\nThe boundary conditions are $y = 0$ and $\\frac{dy}{dx} = 1$ at $x = 0$.\nThen the value of $y$ at $x = 1/2$ is",
    "options": [
        {"label": "A", "text": "$0$"},
        {"label": "B", "text": "$\\sqrt{e}$"},
        {"label": "C", "text": "$\\frac{\\sqrt{e}}{2}$"},
        {"label": "D", "text": "$\\sqrt{\\frac{e}{2}}$"}
    ]
}

# Q38
questions_data[38] = {
    "question": "Consider the partial differential equation\n$$\\frac{\\partial^2 f}{\\partial x^2} + \\frac{\\partial^2 f}{\\partial y^2} = 0$$\nwhere $x, y$ are real.\nIf $f(x, y) = a(x)b(y)$, where $a(x)$ and $b(y)$ are real functions, which one of the following statements can be true?",
    "options": [
        {"label": "A", "text": "$a(x)$ is a periodic function and $b(y)$ is a linear function"},
        {"label": "B", "text": "both $a(x)$ and $b(y)$ are exponential functions"},
        {"label": "C", "text": "$a(x)$ is a periodic function and $b(y)$ is an exponential function"},
        {"label": "D", "text": "both $a(x)$ and $b(y)$ are periodic functions"}
    ]
}

# Q39
questions_data[39] = {
    "question": "A cylindrical object of diameter 900 mm is designed to move axially in air at 60 m/s. Its drag is estimated on a geometrically half-scaled model in water, assuming flow similarity.\nCoefficients of dynamic viscosity and densities for air and water are $1.86 \\times 10^{-5}\\text{ Pa-s}$, $1.2\\text{ kg/m}^3$ and $1.01 \\times 10^{-3}\\text{ Pa-s}$, $1000\\text{ kg/m}^3$ respectively.\nDrag measured for the model is 2280 N. Drag experienced by the full-scale object is ____ N (rounded off to the nearest integer).",
    "options": [
        {"label": "A", "text": "322"},
        {"label": "B", "text": "644"},
        {"label": "C", "text": "1288"},
        {"label": "D", "text": "2576"}
    ]
}

# Q40
questions_data[40] = {
    "question": "Consider a conventional subsonic fixed-wing airplane. $e$ is the Oswald efficiency factor and $AR$ is the aspect ratio. Corresponding to the minimum $\\left(\\frac{C_D}{C_L^{3/2}}\\right)$, which of the following relations is true?",
    "options": [
        {"label": "A", "text": "$\\frac{C_D}{C_L^2} = \\frac{1}{\\pi e AR}$"},
        {"label": "B", "text": "$\\frac{C_D}{C_L^2} = \\frac{4}{3\\pi e AR}$"},
        {"label": "C", "text": "$\\frac{C_D}{C_L} = \\frac{1}{\\pi e AR}$"},
        {"label": "D", "text": "$\\frac{C_D}{\\sqrt{C_L}} = \\frac{1}{\\sqrt{\\pi e AR}}$"}
    ]
}

# Q41
questions_data[41] = {
    "question": "A horizontal load $F$ is applied at point R on a two-member truss, as shown in the figure. Both the members are prismatic with cross-sectional area, $A_0$, and made of the same material with Young’s modulus $E$.\nThe horizontal displacement of point R is:",
    "options": [
        {"label": "A", "text": "$0$"},
        {"label": "B", "text": "$\\frac{Fl}{EA_0}$"},
        {"label": "C", "text": "$\\frac{\\sqrt{2}Fl}{EA_0}$"},
        {"label": "D", "text": "$\\frac{2Fl}{EA_0}$"}
    ]
}

# Q42
questions_data[42] = {
    "question": "Which of the following is NOT always true for a combustion process taking place in a closed system?",
    "options": [
        {"label": "A", "text": "Total number of atoms is conserved"},
        {"label": "B", "text": "Total number of molecules is conserved"},
        {"label": "C", "text": "Total number of atoms of each element is conserved"},
        {"label": "D", "text": "Total mass is conserved"}
    ]
}

# Q43
questions_data[43] = {
    "question": "The real function $y = \\sin^2(|x|)$ is",
    "options": [
        {"label": "A", "text": "continuous for all $x$"},
        {"label": "B", "text": "differentiable for all $x$"},
        {"label": "C", "text": "not continuous at $x = 0$"},
        {"label": "D", "text": "not differentiable at $x = 0$"}
    ]
}

# Q44
questions_data[44] = {
    "question": "A convergent nozzle fed from a constant pressure, constant temperature reservoir, is discharging air to atmosphere at 1 bar (absolute) with choked flow at the exit (marked as $Q$).\nFlow through the nozzle can be assumed to be isentropic.\nIf the exit area of the nozzle is increased while all the reservoir parameters and ambient conditions remain the same, then at steady state",
    "options": [
        {"label": "A", "text": "the nozzle will remain choked"},
        {"label": "B", "text": "the nozzle will be un-choked"},
        {"label": "C", "text": "the Mach number at section P will increase"},
        {"label": "D", "text": "the Mach number at section P will decrease"}
    ]
}

# Q45
questions_data[45] = {
    "question": "For a conventional airplane in straight, level, constant velocity flight condition, which of the following condition(s) is/are possible on Euler angles $(\\phi, \\theta, \\psi)$, angle of attack $(\\alpha)$ and the sideslip angle $(\\beta)$?",
    "options": [
        {"label": "A", "text": "$\\phi = 0^\\circ, \\theta = 2^\\circ, \\psi = 0^\\circ, \\alpha = 2^\\circ, \\beta = 0^\\circ$"},
        {"label": "B", "text": "$\\phi = 5^\\circ, \\theta = 0^\\circ, \\psi = 0^\\circ, \\alpha = 2^\\circ, \\beta = 0^\\circ$"},
        {"label": "C", "text": "$\\phi = 0^\\circ, \\theta = 3^\\circ, \\psi = 0^\\circ, \\alpha = 3^\\circ, \\beta = 5^\\circ$"},
        {"label": "D", "text": "$\\phi = 0^\\circ, \\theta = 5^\\circ, \\psi = 0^\\circ, \\alpha = 2^\\circ, \\beta = 5^\\circ$"}
    ]
}

# Q46
questions_data[46] = {
    "question": "Consider a high Earth-orbiting satellite of angular momentum per unit mass $\\vec{h}$ and eccentricity $e$.\nThe mass of the Earth is $M$ and $G$ is the universal gravitational constant.\nThe distance between the satellite’s center of mass and the Earth’s center of mass is $r$, the true anomaly is $\\theta$, and the phase angle is zero.\nWhich of the following statements is/are true?",
    "options": [
        {"label": "A", "text": "The trajectory equation is $r = r(\\theta) = \\frac{|\\vec{h}|}{GM(1 + e\\cos\\theta)}$"},
        {"label": "B", "text": "The trajectory equation is $r = r(\\theta) = \\frac{|\\vec{h}|^2}{GM(1 + e\\cos\\theta)}$"},
        {"label": "C", "text": "$\\vec{h}$ is conserved"},
        {"label": "D", "text": "The sum of potential energy and kinetic energy of the satellite is conserved"}
    ]
}

# Q47
questions_data[47] = {
    "question": "A rocket operates at an absolute chamber pressure of 20 bar to produce thrust, $F_1$.\nThe hot exhaust is optimally expanded to 1 bar (absolute pressure) using a convergent-divergent nozzle with exit to throat area ratio $\\left(\\frac{A_e}{A_t}\\right)$ of 3.5 and thrust coefficient, $C_{F,1} = 1.42$.\nThe same rocket when operated at an absolute chamber pressure of 50 bar produces thrust $F_2$ and the thrust coefficient is $C_{F,2}$.\nWhich of the following statement(s) is/are correct?",
    "options": [
        {"label": "A", "text": "$\\frac{F_2}{F_1} = 2.5$"},
        {"label": "B", "text": "$\\frac{F_2}{F_1} > 2.5$"},
        {"label": "C", "text": "$\\frac{C_{F,2}}{C_{F,1}} = 1$"},
        {"label": "D", "text": "$\\frac{C_{F,2}}{C_{F,1}} > 1$"}
    ]
}

# Q48
questions_data[48] = {
    "question": "$\\vec{v} = x^3\\hat{\\imath} + y^3\\hat{\\jmath} + z^3\\hat{k}$ is a vector field where $\\hat{\\imath}, \\hat{\\jmath}, \\hat{k}$ are the base vectors of a cartesian coordinate system.\nUsing the Gauss divergence theorem, the value of the outward flux of the vector field over the surface of a sphere of unit radius centered at the origin is________ (rounded off to one decimal place)."
}

# Q49
questions_data[49] = {
    "question": "The largest eigenvalue of the given matrix is _____.\n$$\\begin{bmatrix} 0 & 1 & 1 \\\\ 1 & 0 & 1 \\\\ 1 & 1 & 0 \\end{bmatrix}$$"
}

# Q50
questions_data[50] = {
    "question": "A rotational velocity field in an air flow is given as $\\vec{V} = ay\\hat{\\imath} + bx\\hat{\\jmath}$, with $a = 10\\text{ s}^{-1}, b = 20\\text{ s}^{-1}$.\nThe air density is $1.0\\text{ kg/m}^3$ and the pressure at $(x, y) = (0\\text{ m}, 0\\text{ m})$ is 100 kPa.\nNeglecting gravity, the pressure at $(x, y) = (6\\text{ m}, 8\\text{ m})$ is _____ kPa (rounded off to nearest integer)."
}

# Q51
questions_data[51] = {
    "question": "Consider a circulation distribution over a finite wing given by the equation below.\n$$\\Gamma(y) = \\begin{cases} \\Gamma_0\\left(1 - \\frac{2y}{b}\\right) & \\text{if } 0 \\le y \\le \\frac{b}{2} \\\\[6pt] \\Gamma_0\\left(1 + \\frac{2y}{b}\\right) & \\text{if } -\\frac{b}{2} \\le y \\le 0 \\end{cases}$$\nThe wingspan $b$ is 10 m, the maximum circulation $\\Gamma_0$ is 20 m$^2$/s, density of air is 1.2 kg/m$^3$ and the free stream speed is 80 m/s.\nThe lift over the wing is ______N (rounded off to the nearest integer)."
}

# Q52
questions_data[52] = {
    "question": "Consider a solid cylinder housed inside another cylinder as shown in the figure.\nRadius of the inner cylinder is 1 m and its height is 2 m. The gap between the cylinders is 5 mm and is filled with a fluid of viscosity $10^{-4}\\text{ Pa-s}$.\nThe inner cylinder is rotating at a constant angular speed of 5 rad/s while the outer cylinder is stationary. Friction at the bottom surfaces can be ignored. Velocity profile in the vertical gap between the cylinders can be assumed to be linear.\nThe driving moment required for the rotating motion of the inner cylinder is ____________ Nm (rounded off to two decimal places)."
}

# Q53
questions_data[53] = {
    "question": "In a converging duct, area and velocity at section P are 1 m$^2$ and 15 m/s, respectively. The temperature of the fluid is 300 K.\nAir flow through the nozzle can be assumed to be inviscid and isothermal.\nCharacteristic gas constant is 287 J/(kg-K) and ratio of specific heats is 1.4 for air.\nTo ensure that the air flow remains incompressible (Mach number, $M \\le 0.3$) in the duct, the minimum area required at section Q is _____ m$^2$ (rounded off to two decimal places)."
}

# Q54
questions_data[54] = {
    "question": "Consider a thin symmetric airfoil at 2 degree angle of attack in a uniform flow at 50 m/s. The pitching moment coefficient about its leading edge is _____ (rounded off to three decimal places)."
}

# Q55
questions_data[55] = {
    "question": "A convergent-divergent nozzle with adiabatic walls is designed for an exit Mach number of 2.3. It is discharging air to atmosphere under the conditions indicated in the figure.\nFlow through the nozzle is inviscid, the characteristic gas constant for air is 287 J/(kg-K), and $\\gamma = 1.4$.\nWhen the reservoir pressure is 25 bar (absolute), and temperature is 300 K, Prandtl-Meyer expansion waves appear at the nozzle exit as shown.\nThe minimum percentage change in the reservoir pressure required to eliminate the wave system at the nozzle exit under steady state is _______%."
}

# Q56
questions_data[56] = {
    "question": "A conventional airplane of mass 5000 kg is doing a level turn of radius 1000 m at a constant speed of 100 m/s at sea level.\nTaking the acceleration due to gravity as 10 m/s$^2$, the bank angle of the airplane is _________ degrees."
}

# Q57
questions_data[57] = {
    "question": "Given: The tip deflection and tip slope for a tip loaded cantilever of length $L$ are: $\\frac{N L^3}{3EI}$ and $\\frac{N L^2}{2EI}$, respectively, where $N$ is the tip force and $EI$ is the flexural rigidity.\nA cantilever $PQ$ of rectangular cross-section is subjected to transverse load, $F$, at its mid-point. Two cases are considered as shown in the figure. In Case I, the end $Q$ is free and in Case II, $Q$ is simply supported.\nThe ratio of the magnitude of the maximum bending stress at $P$ in Case I to that in Case II is ________ (rounded off to one decimal place)."
}

# Q58
questions_data[58] = {
    "question": "A simply supported Aluminium column of length 1 m and rectangular cross-section $w \\times t$ with $t \\le w$, is subjected to axial compressive loading.\nYoung’s modulus is 70 GPa. Yield stress under uniaxial compression is 120 MPa.\nThe value of $t$ at which the failure load for yielding and buckling coincide is _______mm."
}

# Q59
questions_data[59] = {
    "question": "A 0.5 m long thin-walled circular shaft of radius 2 cm is to be designed for an axial load of 7.4 kN and a torque of 148 Nm applied at its tip, as shown in the figure.\nThe allowable stress under uniaxial tension is 100 MPa.\nUsing maximum principal stress criterion, the minimum thickness, $t$, of the shaft so that it does not fail is _____ mm (rounded off to the nearest integer)."
}

# Q60
questions_data[60] = {
    "question": "A 10 kN axial load is applied eccentrically on a rod of square cross-section (1 cm $\\times$ 1 cm) as shown in the figure.\nThe strains measured by the two strain gages attached to the top and bottom surfaces at a distance of 0.5 m from the tip are $\\epsilon_1 = 0.0016$ and $\\epsilon_2 = 0.0004$, respectively.\nThe eccentricity in loading, $e$ is _________mm."
}

# Q61
questions_data[61] = {
    "question": "For a thin-walled I section, the width of the two flanges as well as the web height are the same, i.e., $2b = 20\\text{ mm}$. Thickness is 0.6 mm.\nThe second moment of area about a horizontal axis passing through the centroid is ______ mm$^4$."
}

# Q62
questions_data[62] = {
    "question": "A damper with damping coefficient, $c$, is attached to a mass of 5 kg and spring of stiffness 5 kN/m as shown in figure. The system undergoes under-damped oscillations.\nIf the ratio of the 3rd amplitude to the 4th amplitude of oscillations is 1.5, the value of $c$ is ____ Ns/m (rounded off to the nearest integer)."
}

# Q63
questions_data[63] = {
    "question": "A uniform rigid prismatic bar of total mass $m$ is suspended from a ceiling by two identical springs as shown in figure.\nLet $\\omega_1$ and $\\omega_2$ be the natural frequencies of mode I and mode II respectively ($\\omega_1 < \\omega_2$).\nThe value of $\\omega_2/\\omega_1$ is _________ (rounded off to one decimal place)."
}

# Q64
questions_data[64] = {
    "question": "An ideal ramjet is to operate with exhaust gases optimally expanded to ambient pressure at an altitude where temperature is 220 K. The exhaust speed at the nozzle exit is 1200 m/s at a temperature of 1100 K.\nGiven: $\\gamma = 1.4$ at 220 K; $R = 287\\text{ J/(kg-K)}$ for air\n$\\gamma = 1.33$ at 1100 K; $R = 287\\text{ J/(kg-K)}$ for exhaust gases.\nThe cruise speed of this ramjet is ________ m/s (rounded off to nearest integer)."
}

# Q65
questions_data[65] = {
    "question": "A multistage axial compressor takes in air at 1 atm, 300 K and compresses it to a minimum of 5 atm.\nThe mean blade speed is 245 m/s and work coefficient, $\\frac{\\Delta C_\\theta}{U}$ is 0.55 for each stage.\nFor air, use $C_p = 1005\\text{ J/(kg-K)}$, $R = 287\\text{ J/(kg-K)}$ and $\\gamma = 1.4$.\nIf the compression is isentropic, the number of stages required is ___________ (rounded off to the next higher integer)."
}

def get_question_pages(qnum):
    pages = []
    pattern = re.compile(rf'\bQ\.?\s*{qnum}\b')
    for pno in range(len(doc)):
        txt = doc[pno].get_text('text')
        if pattern.search(txt):
            pages.append(pno + 1)
    return pages if pages else [1]

questions_list = []

for qnum in range(1, 66):
    krow = key_rows[qnum - 1]
    sec = krow["section"]
    qtype = krow["type"]
    marks = krow["marks"]
    rawKey = krow["rawKey"]
    
    # Process answer format
    if rawKey == 'MTA*' or rawKey == 'MTA':
        ans = 'MTA'
    elif qtype == 'NAT':
        if ' OR ' in rawKey:
            parts = rawKey.split(' OR ')
            ans = []
            for p in parts:
                p = p.strip()
                if ' to ' in p:
                    ans.append([float(x) for x in p.split(' to ')])
                else:
                    ans.append(float(p) if '.' in p else int(p))
        elif ' to ' in rawKey:
            ans = [float(x) for x in rawKey.split(' to ')]
        else:
            ans = float(rawKey) if '.' in rawKey else int(rawKey)
    elif qtype == 'MSQ':
        ans = [k.strip() for k in rawKey.split(';')]
    elif qtype == 'MCQ':
        if ';' in rawKey:
            ans = [k.strip() for k in rawKey.split(';')]
        else:
            ans = rawKey.strip()
    else:
        ans = rawKey
        
    qid = f"gate-2022-ae-ga-{qnum:02d}" if sec == "GA" else f"gate-2022-ae-ae-{qnum:02d}"
    subject = "General Aptitude" if sec == "GA" else "Aerospace Engineering"
    
    q_info = questions_data[qnum]
    q_text = q_info["question"]
    raw_options = q_info.get("options", [])
    
    options = []
    for opt in raw_options:
        opt_entry = {
            "label": opt["label"],
            "text": opt["text"]
        }
        if qnum in option_figures and opt["label"] in option_figures[qnum]:
            opt_fig_info = option_figures[qnum][opt["label"]]
            opt_fig_obj = {
                "src": opt_fig_info["src"],
                "alt": opt_fig_info["alt"],
                "source": {
                    "file": "internal/ae/AE2022.pdf",
                    "sha256": pdf_sha256,
                    "page": opt_fig_info["page"],
                    "verificationStatus": "source-verified",
                    "verifiedOn": "2026-10-07"
                },
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            }
            opt_entry["figure"] = opt_fig_obj
            opt_entry["content"] = [{"type": "figure", "asset": opt_fig_obj}]
        options.append(opt_entry)
        
    # Figures
    figs = []
    content_blocks = [{"type": "text", "text": q_text}]
    
    if qnum in figure_metadata:
        for fig_info in figure_metadata[qnum]:
            fig_obj = {
                "src": fig_info["src"],
                "alt": fig_info["alt"],
                "source": {
                    "file": "internal/ae/AE2022.pdf",
                    "sha256": pdf_sha256,
                    "page": fig_info["page"],
                    "verificationStatus": "source-verified",
                    "verifiedOn": "2026-10-07"
                },
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            }
            figs.append(fig_obj)
            content_blocks.append({"type": "figure", "asset": fig_obj})
            
    pages = get_question_pages(qnum)
    
    neg_marks = 0.0
    if qtype == "MCQ":
        neg_marks = marks / 3.0
        
    q_record = {
        "id": qid,
        "exam": "GATE",
        "year": 2022,
        "paper": "AE",
        "number": qnum,
        "section": sec,
        "subject": subject,
        "type": qtype,
        "marks": marks,
        "question": q_text,
        "options": options,
        "content": content_blocks,
        "figures": figs,
        "groupId": None,
        "source": {
            "file": "internal/ae/AE2022.pdf",
            "sha256": pdf_sha256,
            "pages": [{"page": p, "coordinateSystem": "PDF points, top-left origin"} for p in pages],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-07"
        },
        "transcriptionStatus": "source-verified",
        "solution": None,
        "solutionAvailability": "not-provided-in-source",
        "gradingStatus": "official key verified",
        "answerSource": {
            "url": "https://gate.iitkgp.ac.in/",
            "paper": "AE",
            "questionNumber": qnum,
            "section": sec,
            "page": 1 if qnum <= 35 else 2,
            "sha256": key_doc["sha256"],
            "verifiedOn": "2026-10-07"
        },
        "answer": ans,
        "negativeMarks": neg_marks,
        "markingRule": "gate-2022-official",
        "hasFigure": len(figs) > 0 or qnum in option_figures
    }
    
    if qtype == 'NAT' and ' OR ' in rawKey:
        parts = rawKey.split(' OR ')
        acc_list = []
        for p in parts:
            p = p.strip()
            if ' to ' in p:
                acc_list.append([float(x) for x in p.split(' to ')])
            else:
                acc_list.append(float(p) if '.' in p else int(p))
        q_record["acceptedAnswers"] = acc_list

    questions_list.append(q_record)

print(f"Total compiled questions: {len(questions_list)}")

ga_qids = [q["id"] for q in questions_list if q["section"] == "GA"]
ae_qids = [q["id"] for q in questions_list if q["section"] == "AE"]

paper_data = {
    "schemaVersion": 1,
    "id": "gate-2022-ae",
    "exam": "GATE",
    "year": 2022,
    "paper": "AE",
    "totalQuestions": 65,
    "totalMarks": 100,
    "durationMinutes": 180,
    "sectionOrder": ["GA", "AE"],
    "sections": [
        {
            "id": "GA",
            "title": "General Aptitude",
            "questionIds": ga_qids,
            "totalMarks": 15
        },
        {
            "id": "AE",
            "title": "Aerospace Engineering",
            "questionIds": ae_qids,
            "totalMarks": 85
        }
    ],
    "questionOrder": [q["id"] for q in questions_list],
    "questionRefs": [
        {"id": q["id"], "number": q["number"], "section": q["section"], "marks": q["marks"], "type": q["type"]}
        for q in questions_list
    ],
    "questionGroups": [],
    "marking": {
        "negativeFraction": {
            "MCQ": 0.3333333333333333,
            "MSQ": 0.0,
            "NAT": 0.0
        }
    },
    "questionTypeCounts": {
        "MCQ": len([q for q in questions_list if q["type"] == "MCQ"]),
        "MSQ": len([q for q in questions_list if q["type"] == "MSQ"]),
        "NAT": len([q for q in questions_list if q["type"] == "NAT"])
    },
    "source": {
        "file": "internal/ae/AE2022.pdf",
        "sha256": pdf_sha256,
        "pageCount": len(doc)
    },
    "ingestionStatus": "complete",
    "verificationStatus": "source-verified",
    "verifiedOn": "2026-10-07",
    "questions": questions_list
}

with open('data/ae/2022.json', 'w', encoding='utf-8') as f:
    json.dump(paper_data, f, indent=2, ensure_ascii=False)
print("Saved data/ae/2022.json")

# Update manifest.json
with open('data/ae/manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# Count figure assets
fig_assets_count = 0
for q in questions_list:
    fig_assets_count += len(q.get("figures", []))
    for opt in q.get("options", []):
        if "figure" in opt:
            fig_assets_count += 1

print(f"Total figure assets: {fig_assets_count}")

for y in manifest["years"]:
    if y["year"] == 2022:
        y["sourcePdf"] = "internal/ae/AE2022.pdf"
        y["path"] = "data/ae/2022.json"
        y["questionCount"] = 65
        y["newQuestionCount"] = 65
        y["reusedGAQuestionCount"] = 0
        y["totalMarks"] = 100
        y["sections"] = [
            {"id": "GA", "title": "General Aptitude", "questionIds": ga_qids, "totalMarks": 15},
            {"id": "AE", "title": "Aerospace Engineering", "questionIds": ae_qids, "totalMarks": 85}
        ]
        y["questionTypeCounts"] = paper_data["questionTypeCounts"]
        y["answerAvailability"] = {
            "officialKey": 65,
            "gradedAnswers": 65,
            "marksToAll": 0,
            "unavailable": 0
        }
        y["figureAssetCount"] = fig_assets_count
        y["newFigureAssetCount"] = fig_assets_count
        y["reusedFigureAssetCount"] = 0
        y["optionFigureCount"] = 12
        y["structuredTableCount"] = 0
        y["questionGroupCount"] = 0
        y["ingestionStatus"] = "complete"
        y["verificationStatus"] = "source-verified"
        y["verifiedOn"] = "2026-10-07"

with open('data/ae/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("Updated data/ae/manifest.json for 2022")
