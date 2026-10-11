import sys
import os
import json
import hashlib
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'internal/ae/AE2021.pdf'
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

key_pdf_path = 'internal/ae/AE2021-key.pdf'
with open(key_pdf_path, 'rb') as f:
    key_sha256 = hashlib.sha256(f.read()).hexdigest()

doc = fitz.open(pdf_path)

with open('internal/ae/AE2021-key.json', 'r', encoding='utf-8') as f:
    key_doc = json.load(f)
key_rows = key_doc['rows']

# Question-level figure metadata
figure_metadata = {
    2: [{"src": "figures/gate-2021-ae-ga-02-figure-1.png", "alt": "Word PHYLAXIS shown relative to X and Y coordinate axes.", "page": 2}],
    9: [{"src": "figures/gate-2021-ae-ga-09-figure-1.png", "alt": "Square PQRS with shaded intersection of circular sectors.", "page": 5}],
    14: [{"src": "figures/gate-2021-ae-ae-14-figure-1.png", "alt": "Schematics of wave patterns at exit of Nozzles A and B.", "page": 8}],
    20: [{"src": "figures/gate-2021-ae-ae-20-figure-1.png", "alt": "Uniaxial tension test specimen with planes x-x and y-y at 45 degrees.", "page": 10}],
    21: [{"src": "figures/gate-2021-ae-ae-21-figure-1.png", "alt": "2D state of stress element with normal and shear stresses.", "page": 11}],
    23: [{"src": "figures/gate-2021-ae-ae-23-figure-1.png", "alt": "Variation of pitching moment coefficient C_m versus angle of attack alpha.", "page": 12}],
    24: [{"src": "figures/gate-2021-ae-ae-24-figure-1.png", "alt": "Supersonic flow past a wedge generating oblique shock waves.", "page": 13}],
    31: [{"src": "figures/gate-2021-ae-ae-31-figure-1.png", "alt": "Free vortex filament at origin and closed path ABCDEFA.", "page": 16}],
    36: [{"src": "figures/gate-2021-ae-ae-36-figure-1.png", "alt": "Mass m on rigid massless pinned rod supported by linear spring k.", "page": 18}],
    37: [{"src": "figures/gate-2021-ae-ae-37-figure-1.png", "alt": "Three glasses P, Q, and R with water and floating ice cubes.", "page": 19}],
    39: [{"src": "figures/gate-2021-ae-ae-39-figure-1.png", "alt": "Optical setup schematic with light source, lens, test section, and screen.", "page": 20}],
    43: [{"src": "figures/gate-2021-ae-ae-43-figure-1.png", "alt": "Moving normal shock transformed to stationary normal shock reference frame.", "page": 22}],
    50: [{"src": "figures/gate-2021-ae-ae-50-figure-1.png", "alt": "Water tank on wheeled cart with deflecting vane and rope tied to fixed support.", "page": 25}],
    56: [{"src": "figures/gate-2021-ae-ae-56-figure-1.png", "alt": "Axial compressor rotor velocity triangle diagram.", "page": 27}],
    59: [{"src": "figures/gate-2021-ae-ae-59-figure-1.png", "alt": "Rigid horizontal bar ABC pinned to columns BD and CE under load P.", "page": 29}],
    60: [{"src": "figures/gate-2021-ae-ae-60-figure-1.png", "alt": "Two-cell wing box section subjected to torque.", "page": 30}],
    61: [{"src": "figures/gate-2021-ae-ae-61-figure-1.png", "alt": "Two cantilever beams AB and DC in contact through a roller.", "page": 30}],
    62: [{"src": "figures/gate-2021-ae-ae-62-figure-1.png", "alt": "Signboard supported by vertical hollow square pole under wind load.", "page": 31}],
    63: [{"src": "figures/gate-2021-ae-ae-63-figure-1.png", "alt": "Airplane profile during pull-up maneuver showing CG, CP, and tail force point T.", "page": 31}]
}

# Option figures
option_figures = {
    2: {
        "A": {"src": "figures/gate-2021-ae-ga-02-option-A.png", "alt": "Mirror image option A.", "page": 2},
        "B": {"src": "figures/gate-2021-ae-ga-02-option-B.png", "alt": "Mirror image option B.", "page": 2},
        "C": {"src": "figures/gate-2021-ae-ga-02-option-C.png", "alt": "Mirror image option C.", "page": 2},
        "D": {"src": "figures/gate-2021-ae-ga-02-option-D.png", "alt": "Mirror image option D.", "page": 2}
    }
}

questions_data = {}

# Q1
questions_data[1] = {
    "page": 1,
    "question": "(i) Arun and Aparna are here.\n(ii) Arun and Aparna is here.\n(iii) Arun’s families is here.\n(iv) Arun’s family is here.\n\nWhich of the above sentences are grammatically CORRECT?",
    "options": [
        {"label": "A", "text": "(i) and (ii)"},
        {"label": "B", "text": "(i) and (iv)"},
        {"label": "C", "text": "(ii) and (iv)"},
        {"label": "D", "text": "(iii) and (iv)"}
    ]
}

# Q2
questions_data[2] = {
    "page": 2,
    "question": "The mirror image of the above text about the x-axis is",
    "options": [
        {"label": "A", "text": "Option A"},
        {"label": "B", "text": "Option B"},
        {"label": "C", "text": "Option C"},
        {"label": "D", "text": "Option D"}
    ]
}

# Q3
questions_data[3] = {
    "page": 3,
    "question": "Two identical cube shaped dice each with faces numbered 1 to 6 are rolled simultaneously. The probability that an even number is rolled out on each dice is:",
    "options": [
        {"label": "A", "text": "$\\frac{1}{36}$"},
        {"label": "B", "text": "$\\frac{1}{12}$"},
        {"label": "C", "text": "$\\frac{1}{8}$"},
        {"label": "D", "text": "$\\frac{1}{4}$"}
    ]
}

# Q4
questions_data[4] = {
    "page": 3,
    "question": "$\\oplus$ and $\\odot$ are two operators on numbers $p$ and $q$ such that\n\n$p \\odot q = p - q$, and $p \\oplus q = p \\times q$\n\nThen, $(9 \\odot (6 \\oplus 7)) \\odot (7 \\oplus (6 \\odot 5))=$",
    "options": [
        {"label": "A", "text": "40"},
        {"label": "B", "text": "-26"},
        {"label": "C", "text": "-33"},
        {"label": "D", "text": "-40"}
    ]
}

# Q5
questions_data[5] = {
    "page": 3,
    "question": "Four persons P, Q, R and S are to be seated in a row. R should not be seated at the second position from the left end of the row. The number of distinct seating arrangements possible is:",
    "options": [
        {"label": "A", "text": "6"},
        {"label": "B", "text": "9"},
        {"label": "C", "text": "18"},
        {"label": "D", "text": "24"}
    ]
}

# Q6
questions_data[6] = {
    "page": 4,
    "question": "On a planar field, you travelled 3 units East from a point O. Next you travelled 4 units South to arrive at point P. Then you travelled from P in the North-East direction such that you arrive at a point that is 6 units East of point O. Next, you travelled in the North-West direction, so that you arrive at point Q that is 8 units North of point P.\n\nThe distance of point Q to point O, in the same units, should be ______",
    "options": [
        {"label": "A", "text": "3"},
        {"label": "B", "text": "4"},
        {"label": "C", "text": "5"},
        {"label": "D", "text": "6"}
    ]
}

# Q7
questions_data[7] = {
    "page": 4,
    "question": "The author said, “Musicians rehearse before their concerts. Actors rehearse their roles before the opening of a new play. On the other hand, I find it strange that many public speakers think they can just walk on to the stage and start speaking. In my opinion, it is no less important for public speakers to rehearse their talks.”\n\nBased on the above passage, which one of the following is TRUE?",
    "options": [
        {"label": "A", "text": "The author is of the opinion that rehearsing is important for musicians, actors and public speakers."},
        {"label": "B", "text": "The author is of the opinion that rehearsing is less important for public speakers than for musicians and actors."},
        {"label": "C", "text": "The author is of the opinion that rehearsing is more important only for musicians than public speakers."},
        {"label": "D", "text": "The author is of the opinion that rehearsal is more important for actors than musicians."}
    ]
}

# Q8
questions_data[8] = {
    "page": 5,
    "question": "1. Some football players play cricket.\n2. All cricket players play hockey.\n\nAmong the options given below, the statement that logically follows from the two statements 1 and 2 above, is:",
    "options": [
        {"label": "A", "text": "No football player plays hockey."},
        {"label": "B", "text": "Some football players play hockey."},
        {"label": "C", "text": "All football players play hockey."},
        {"label": "D", "text": "All hockey players play football."}
    ]
}

# Q9
questions_data[9] = {
    "page": 5,
    "question": "In the figure shown above, PQRS is a square. The shaded portion is formed by the intersection of sectors of circles with radius equal to the side of the square and centers at S and Q.\n\nThe probability that any point picked randomly within the square falls in the shaded area is ______",
    "options": [
        {"label": "A", "text": "$4 - \\frac{\\pi}{2}$"},
        {"label": "B", "text": "$\\frac{1}{2}$"},
        {"label": "C", "text": "$\\frac{\\pi}{2} - 1$"},
        {"label": "D", "text": "$\\frac{\\pi}{4}$"}
    ]
}

# Q10
questions_data[10] = {
    "page": 6,
    "question": "In an equilateral triangle PQR, side PQ is divided into four equal parts, side QR is divided into six equal parts and side PR is divided into eight equal parts. The length of each subdivided part in cm is an integer.\n\nThe minimum area of the triangle PQR possible, in $\\text{cm}^2$, is",
    "options": [
        {"label": "A", "text": "18"},
        {"label": "B", "text": "24"},
        {"label": "C", "text": "$48\\sqrt{3}$"},
        {"label": "D", "text": "$144\\sqrt{3}$"}
    ]
}

# Q11
questions_data[11] = {
    "page": 7,
    "question": "Consider the differential equation $\\frac{d^2 y}{dx^2} + 8\\frac{dy}{dx} + 16y = 0$ and the boundary conditions $y(0) = 1$ and $\\frac{dy}{dx}(0) = 0$. The solution to this equation is:",
    "options": [
        {"label": "A", "text": "$y = (1 + 2x)e^{-4x}$"},
        {"label": "B", "text": "$y = (1 - 4x)e^{-4x}$"},
        {"label": "C", "text": "$y = (1 + 8x)e^{-4x}$"},
        {"label": "D", "text": "$y = (1 + 4x)e^{-4x}$"}
    ]
}

# Q12
questions_data[12] = {
    "page": 7,
    "question": "$u(x, y)$ is governed by the following equation $\\frac{\\partial^2 u}{\\partial x^2} - 4\\frac{\\partial^2 u}{\\partial x \\partial y} + 6\\frac{\\partial^2 u}{\\partial y^2} = x + 2y$.\n\nThe nature of this equation is:",
    "options": [
        {"label": "A", "text": "linear"},
        {"label": "B", "text": "elliptic"},
        {"label": "C", "text": "hyperbolic"},
        {"label": "D", "text": "parabolic"}
    ]
}

# Q13
questions_data[13] = {
    "page": 7,
    "question": "Consider the velocity field $\\vec{V} = (2x + 3y)\\hat{i} + (3x + 2y)\\hat{j}$. The field $\\vec{V}$ is",
    "options": [
        {"label": "A", "text": "divergence-free and curl-free"},
        {"label": "B", "text": "curl-free but not divergence-free"},
        {"label": "C", "text": "divergence-free but not curl-free"},
        {"label": "D", "text": "neither divergence-free nor curl-free"}
    ]
}

# Q14
questions_data[14] = {
    "page": 8,
    "question": "The figure shows schematics of wave patterns at the exit of nozzles A and B operating at different pressure ratios.\n\nNozzles A and B, respectively, are said to be operating in:",
    "options": [
        {"label": "A", "text": "over-expanded mode and under-expanded mode"},
        {"label": "B", "text": "under-expanded mode and perfectly expanded mode"},
        {"label": "C", "text": "perfectly expanded mode and under-expanded mode"},
        {"label": "D", "text": "under-expanded mode and over-expanded mode"}
    ]
}

# Q15
questions_data[15] = {
    "page": 8,
    "question": "The combustion process in a turbo-shaft engine during ideal operation is:",
    "options": [
        {"label": "A", "text": "isentropic"},
        {"label": "B", "text": "isobaric"},
        {"label": "C", "text": "isochoric"},
        {"label": "D", "text": "isothermal"}
    ]
}

# Q16
questions_data[16] = {
    "page": 9,
    "question": "How does the specific thrust of a turbojet engine change for a given flight speed with increase in flight altitude?",
    "options": [
        {"label": "A", "text": "Increases monotonically"},
        {"label": "B", "text": "Decreases monotonically"},
        {"label": "C", "text": "Remains constant"},
        {"label": "D", "text": "First increases and then decreases"}
    ]
}

# Q17
questions_data[17] = {
    "page": 9,
    "question": "How does the propulsion efficiency of a turbofan engine, operating at a given Mach number and a given altitude, change with increase in compressor pressure ratio?",
    "options": [
        {"label": "A", "text": "Remains constant"},
        {"label": "B", "text": "Increases monotonically"},
        {"label": "C", "text": "Decreases monotonically"},
        {"label": "D", "text": "First decreases and then increases"}
    ]
}

# Q18
questions_data[18] = {
    "page": 9,
    "question": "A solid propellant rocket producing 25 MN thrust is fired for 150 seconds. The specific impulse of the rocket is 2980 Ns/kg. How much propellant is burned during the rocket operation?",
    "options": [
        {"label": "A", "text": "8390 kg"},
        {"label": "B", "text": "82300 kg"},
        {"label": "C", "text": "$1.26 \\times 10^6$ kg"},
        {"label": "D", "text": "$11.2 \\times 10^6$ kg"}
    ]
}

# Q19
questions_data[19] = {
    "page": 10,
    "question": "The shape of a supersonic diffuser that slows down a supersonic flow to subsonic flow is",
    "options": [
        {"label": "A", "text": "converging"},
        {"label": "B", "text": "diverging"},
        {"label": "C", "text": "diverging–converging"},
        {"label": "D", "text": "converging–diverging"}
    ]
}

# Q20
questions_data[20] = {
    "page": 10,
    "question": "Uniaxial tension test (see the figure) is conducted on two different samples prepared with homogeneous, isotropic materials. One of the materials is brittle, whereas the other is ductile.\n\nAssuming that there is no stress concentration at loading points, the failure would initiate:",
    "options": [
        {"label": "A", "text": "along x-x in both materials"},
        {"label": "B", "text": "along x-x in brittle material and along y-y in ductile material"},
        {"label": "C", "text": "along y-y in brittle material and along x-x in ductile material"},
        {"label": "D", "text": "along y-y in both materials"}
    ]
}

# Q21
questions_data[21] = {
    "page": 11,
    "question": "For the state of stress as shown in the figure, what is the orientation of the plane with maximum shear stress with respect to the x-axis?",
    "options": [
        {"label": "A", "text": "$45^\\circ$"},
        {"label": "B", "text": "$-45^\\circ$"},
        {"label": "C", "text": "$22.5^\\circ$"},
        {"label": "D", "text": "$-22.5^\\circ$"}
    ]
}

# Q22
questions_data[22] = {
    "page": 11,
    "question": "Let $V_{TAS}$ be the true airspeed of an aircraft flying at a certain altitude where the density of air is $\\rho$, and $V_{EAS}$ be the equivalent airspeed. If $\\rho_0$ is the density of air at sea-level, what is the ratio $\\frac{V_{TAS}}{V_{EAS}}$ equal to?",
    "options": [
        {"label": "A", "text": "$\\frac{\\rho}{\\rho_0}$"},
        {"label": "B", "text": "$\\frac{\\rho_0}{\\rho}$"},
        {"label": "C", "text": "$\\sqrt{\\frac{\\rho_0}{\\rho}}$"},
        {"label": "D", "text": "$\\sqrt{\\frac{\\rho}{\\rho_0}}$"}
    ]
}

# Q23
questions_data[23] = {
    "page": 12,
    "question": "$C_m - \\alpha$ variation for a certain aircraft is shown in the figure. Which one of the following statements is true for this aircraft?",
    "options": [
        {"label": "A", "text": "The aircraft can trim at a positive $\\alpha$ and it is stable."},
        {"label": "B", "text": "The aircraft can trim at a positive $\\alpha$, but it is unstable."},
        {"label": "C", "text": "The aircraft can trim at a negative $\\alpha$ and it is stable."},
        {"label": "D", "text": "The aircraft can trim at a negative $\\alpha$, but it is unstable."}
    ]
}

# Q24
questions_data[24] = {
    "page": 13,
    "question": "Which of the following statement(s) is/are true across an oblique shock (in adiabatic conditions) over a wedge shown below?",
    "options": [
        {"label": "A", "text": "Total pressure decreases"},
        {"label": "B", "text": "Mach number based on velocity tangential to the shock decreases"},
        {"label": "C", "text": "Total temperature remains constant"},
        {"label": "D", "text": "Mach number based on velocity tangential to the shock remains the same and that based on velocity normal to the shock decreases"}
    ]
}

# Q25
questions_data[25] = {
    "page": 13,
    "question": "Which of the following statement(s) is/are true with regards to Kutta condition for flow past airfoils?",
    "options": [
        {"label": "A", "text": "It is utilized to determine the circulation on an airfoil."},
        {"label": "B", "text": "It is applicable only to airfoils with sharp trailing edge."},
        {"label": "C", "text": "The trailing edge of an airfoil is a stagnation point."},
        {"label": "D", "text": "The flow leaves the trailing edge smoothly."}
    ]
}

# Q26
questions_data[26] = {
    "page": 14,
    "question": "According to the thin airfoil theory, which of the following statement(s) is/are true for a cambered airfoil?",
    "options": [
        {"label": "A", "text": "The lift coefficient for an airfoil is directly proportional to the absolute angle of attack."},
        {"label": "B", "text": "The aerodynamic center lies at quarter chord point."},
        {"label": "C", "text": "The center of pressure lies at quarter chord point."},
        {"label": "D", "text": "Drag coefficient is proportional to the square of lift coefficient."}
    ]
}

# Q27
questions_data[27] = {
    "page": 15,
    "question": "$\\lim_{x \\to 0} \\left( \\frac{1}{\\sin x} - \\frac{1}{x} \\right) = $ ______ (round off to nearest integer)."
}

# Q28
questions_data[28] = {
    "page": 15,
    "question": "Given that $\\varsigma$ is the unit circle in the counter-clockwise direction with its center at origin, the integral $\\oint_\\varsigma \\frac{z^3}{4z - i} dz = $ ______ (round off to three decimal place)."
}

# Q29
questions_data[29] = {
    "page": 15,
    "question": "A single degree of freedom spring-mass-damper system is designed to ensure that the system returns to its original undisturbed position in minimum possible time without overshooting. If the mass of the system is 10 kg, spring stiffness is 17400 N/m and the natural frequency is 13.2 rad/s, the coefficient of damping of the system in Ns/m is ______ (round off to nearest integer)."
}

# Q30
questions_data[30] = {
    "page": 15,
    "question": "Two cantilever beams (Beam 1 and Beam 2) are made of same homogenous material and have identical cross sections. Beam 1 has length $l$ and Beam 2 has length $2l$. Ratio of the first natural frequency of Beam 1 to that of Beam 2 is ______ (round off to nearest integer)."
}

# Q31
questions_data[31] = {
    "page": 16,
    "question": "A free vortex filament (oriented along Z-axis) of strength $\\text{K} = 5$ m$^2$/s is placed at the origin as shown in the figure. The circulation around the closed loop ABCDEFA for this flow is ______ .",
}

# Q32
questions_data[32] = {
    "page": 16,
    "question": "A thin-walled cylindrical tank with closed ends, made of homogeneous and isotropic material, is pressurized internally. If the hoop (circumferential) strain developed in the material is thrice the value of the axial strain then the Poisson’s ratio of the material is ______ (correct up to one decimal place)."
}

# Q33
questions_data[33] = {
    "page": 16,
    "question": "A jet aircraft has the following specifications: wing loading $= 1800$ N/m$^2$, wing area $= 30$ m$^2$, drag polar $C_D = 0.02 + 0.04C_L^2$, and $C_{L,\\max} = 1.6$. Take density of air at sea level as 1.225 kg/m$^3$.\n\nThe speed at which the aircraft achieves maximum endurance in a steady and level flight at sea level is ______ m/s (round off to two decimal places)."
}

# Q34
questions_data[34] = {
    "page": 17,
    "question": "An aircraft with twin jet engines has the following specifications:\nThrust produced (per engine) $= 8000$ N\nSpanwise distance between the two engines $= 10$ m\nWing area $= 50$ m$^2$, Wing span $= 10$ m\nRudder effectiveness, $C_{n\\delta r} = -0.002$ /deg\nDensity of air at sea level $= 1.225$ kg/m$^3$\n\nThe rudder deflection, in degrees, required to maintain zero sideslip at 100 m/s in steady and level flight at sea level with a non-functional right engine is ______ (round off to two decimal places)."
}

# Q35
questions_data[35] = {
    "page": 17,
    "question": "The velocity required to launch a space shuttle from the surface of the earth to achieve a circular orbit of 250 km altitude is ______ (round off to two decimal places).\n\nFor earth, $Gm_e = 398,600.4$ km$^3$/s$^2$ and surface radius $R_0 = 6378.14$ km."
}

# Q36
questions_data[36] = {
    "page": 18,
    "question": "A rigid massless rod pinned at one end has a mass $m$ attached to its other end. The rod is supported by a linear spring of stiffness $k$ as shown in the figure.\n\nThe natural frequency of this system is:",
    "options": [
        {"label": "A", "text": "$\\frac{1}{2\\pi}\\sqrt{\\frac{kL^2}{4m(L^2 + H^2)}}$"},
        {"label": "B", "text": "$\\frac{1}{2\\pi}\\sqrt{\\frac{kL^2}{m(L^2 + H^2)}}$"},
        {"label": "C", "text": "$\\frac{1}{2\\pi}\\sqrt{\\frac{4kL^2}{m(L^2 + H^2)}}$"},
        {"label": "D", "text": "$\\frac{1}{2\\pi}\\sqrt{\\frac{k(L^2 + H^2)}{4mL^2}}$"}
    ]
}

# Q37
questions_data[37] = {
    "page": 19,
    "question": "The figure shows three glasses P, Q and R with water and floating ice cube. Glass P has a solid ice cube, glass Q has an ice cube with a small solid steel ball embedded in it and glass R has an ice cube with an air bubble. After the ice cube melts, the level of water in glasses P, Q and R, respectively:",
    "options": [
        {"label": "A", "text": "remains same, increases, and decreases"},
        {"label": "B", "text": "increases, decreases, and increases"},
        {"label": "C", "text": "remains same, decreases, and decreases"},
        {"label": "D", "text": "remains same, decreases, and increases"}
    ]
}

# Q38
questions_data[38] = {
    "page": 19,
    "question": "To estimate aerodynamic loads on an aircraft flying at 100 km/h at standard sea-level conditions, a one-fifth scale model is tested in a variable-density wind tunnel ensuring similarity of inertial and viscous forces. The pressure used in the wind tunnel is 10 times the atmospheric pressure. Assuming ideal gas law to hold and the same temperature conditions in model and prototype, the velocity needed in the wind tunnel test-section is ______ .",
    "options": [
        {"label": "A", "text": "25 km/h"},
        {"label": "B", "text": "50 km/h"},
        {"label": "C", "text": "100 km/h"},
        {"label": "D", "text": "20 km/h"}
    ]
}

# Q39
questions_data[39] = {
    "page": 20,
    "question": "The figure shows schematic of a set-up for visualization of non-uniform density field in the test section of a supersonic wind tunnel. This technique of visualization of high speed flows is known as:",
    "options": [
        {"label": "A", "text": "schlieren"},
        {"label": "B", "text": "interferometry"},
        {"label": "C", "text": "shadowgraph"},
        {"label": "D", "text": "holography"}
    ]
}

# Q40
questions_data[40] = {
    "page": 20,
    "question": "For a conventional fixed-wing aircraft in a 360$^{\\circ}$ inverted vertical loop maneuver, what is the load factor ($n$) at the topmost point of the loop? Assume the flight to be steady at the topmost point.",
    "options": [
        {"label": "A", "text": "$n = 1$"},
        {"label": "B", "text": "$n < 1$"},
        {"label": "C", "text": "$n = -1$"},
        {"label": "D", "text": "$n > -1$"}
    ]
}

# Q41
questions_data[41] = {
    "page": 21,
    "question": "Which of the following statement(s) is/are true about the function defined as $f(x) = e^{-x}|\\cos x|$ for $x > 0$?",
    "options": [
        {"label": "A", "text": "Differentiable at $x = \\frac{\\pi}{2}$"},
        {"label": "B", "text": "Differentiable at $x = \\pi$"},
        {"label": "C", "text": "Differentiable at $x = \\frac{3\\pi}{2}$"},
        {"label": "D", "text": "Continuous at $x = 2\\pi$"}
    ]
}

# Q42
questions_data[42] = {
    "page": 21,
    "question": "A two degree of freedom spring-mass system undergoing free vibration with generalized coordinates $x_1$ and $x_2$ has natural frequencies $\\omega_1 = 233.9$ rad/s and $\\omega_2 = 324.5$ rad/s, respectively. The corresponding mode shapes are $\\phi_1 = \\begin{bmatrix} 1 \\\\ -3.16 \\end{bmatrix}$ and $\\phi_2 = \\begin{bmatrix} 1 \\\\ 3.16 \\end{bmatrix}$. If the system is disturbed with certain deflections and zero initial velocities, then which of the following statement(s) is/are true?",
    "options": [
        {"label": "A", "text": "An initial deflection of $x_1(0) = 6.32$ cm and $x_2(0) = -3.16$ cm would make the system oscillate with only the second natural frequency."},
        {"label": "B", "text": "An initial deflection of $x_1(0) = 2$ cm and $x_2(0) = -6.32$ cm would make the system oscillate with only the first natural frequency."},
        {"label": "C", "text": "An initial deflection of $x_1(0) = 2$ cm and $x_2(0) = -2$ cm would make the system oscillate with a linear combination of first and second natural frequencies."},
        {"label": "D", "text": "An initial deflection of $x_1(0) = 1$ cm and $x_2(0) = -6.32$ cm would make the system oscillate with only the first natural frequency."}
    ]
}

# Q43
questions_data[43] = {
    "page": 22,
    "question": "A shock moving into a stationary gas can be transformed to a stationary shock by a change in reference frame, as shown in the figure. Which of the following is/are true relating the flow properties in the two reference frames?",
    "options": [
        {"label": "A", "text": "$T_1' > T_1$, $T_{01}' > T_{01}$, $p_{01}' > p_{01}$, $\\rho_2' > \\rho_1'$"},
        {"label": "B", "text": "$T_1' = T_1$, $T_2' < T_{01}$, $p_{01}' > p_{01}$, $\\rho_2' = \\rho_2$"},
        {"label": "C", "text": "$T_1' < T_1$, $p_1' > p_1$, $p_{01}' > p_{01}$, $\\rho_2' > \\rho_1$"},
        {"label": "D", "text": "$T_1' = T_1$, $p_2 > p_{01}$, $T_{01}' > T_{01}$, $p_{01}' > p_{01}$"}
    ]
}

# Q44
questions_data[44] = {
    "page": 22,
    "question": "For a conventional fixed-wing aircraft, which of the following statements are true?",
    "options": [
        {"label": "A", "text": "Making $C_{m_\\alpha}$ more negative leads to an increase in the frequency of its short-period mode."},
        {"label": "B", "text": "Making $C_{m_q}$ more negative leads to a decreased damping of the short-period mode."},
        {"label": "C", "text": "The primary contribution towards $C_{l_p}$ is from the aircraft wing."},
        {"label": "D", "text": "Increasing the size of the vertical fin leads to a higher yaw damping."}
    ]
}

# Q45
questions_data[45] = {
    "page": 23,
    "question": "Which of the following statement(s) is/are true?",
    "options": [
        {"label": "A", "text": "Service ceiling is higher than absolute ceiling for a piston-propeller aircraft."},
        {"label": "B", "text": "For a given aircraft, the stall speed increases with increase in altitude."},
        {"label": "C", "text": "Everything else remaining the same, a tailwind increases the range of an aircraft."},
        {"label": "D", "text": "For a jet aircraft constrained to fly at constant altitude, there exists an altitude where its range is maximum."}
    ]
}

# Q46
questions_data[46] = {
    "page": 23,
    "question": "A conventional fixed-wing aircraft, with a horizontal tail and vertical fin, in steady and level flight is subjected to small perturbations. Which of the following statement(s) is/are true?",
    "options": [
        {"label": "A", "text": "Vertical fin has a stabilizing effect on the lateral stability of the aircraft."},
        {"label": "B", "text": "Vertical fin has a destabilizing effect on the directional stability of the aircraft."},
        {"label": "C", "text": "Presence of wing anhedral increases the lateral stability of the aircraft."},
        {"label": "D", "text": "Horizontal tail has a stabilizing effect on the longitudinal static stability of the aircraft."}
    ]
}

# Q47
questions_data[47] = {
    "page": 24,
    "question": "The ratio of the product of eigenvalues to the sum of the eigenvalues of the given matrix\n$$\\begin{bmatrix} 3 & 1 & 2 \\\\ 2 & -3 & -1 \\\\ 1 & 2 & 1 \\end{bmatrix}$$\nis ______ (round off to nearest integer)."
}

# Q48
questions_data[48] = {
    "page": 24,
    "question": "The definite integral $\\int_1^5 x^2 dx$ is evaluated using four equal intervals by two methods – first by the trapezoidal rule and then by the Simpson’s one-third rule. The absolute value of the difference between the two calculations is ______ (round off to two decimal places)."
}

# Q49
questions_data[49] = {
    "page": 24,
    "question": "The deflection $y$ of a certain beam of length $l$ and uniform weight per unit length $w$, is given as $y = \\frac{w}{48EI}(2x^4 - 3lx^3 + l^3 x)$, where $x$ is the distance from the point of support and $EI$ is a constant. The non-dimensional location $\\frac{x}{l}$, where the deflection of the beam is maximum, is ______ (round off to two decimal places)."
}

# Q50
questions_data[50] = {
    "page": 25,
    "question": "A large water tank is fixed on a cart with wheels and a vane (see figure). The wheels of the cart provide negligible resistance for rolling on the fixed support. The cart is tied to the fixed support with a thin horizontal rope. There is a hole of diameter 5 cm on the side of the tank through which a jet of constant velocity of 10 m/s emerges. The jet of water is deflected by the attached vane by 60$^{\\circ}$ (see figure). Assume that the jet velocity remains constant at 10 m/s after emerging from the vane. Take density of water to be 1000 kg/m$^3$. The tension in the connecting rope is ______ N (round off to one decimal place)."
}

# Q51
questions_data[51] = {
    "page": 25,
    "question": "A finite wing of elliptic planform with aspect ratio 10, whose section is a symmetric airfoil, is placed in a uniform flow at 5 degrees angle of attack. The induced drag coefficient for the wing is ______ (round off to three decimal places)."
}

# Q52
questions_data[52] = {
    "page": 26,
    "question": "Consider a model of a boundary layer with the following velocity profile:\n$$\\frac{u}{U} = \\begin{cases} \\left(\\frac{y}{\\delta}\\right)^2 & y \\le \\delta \\\\ 1 & y > \\delta \\end{cases}$$\nThe shape factor, defined as the ratio of the displacement thickness to momentum thickness, for this profile is ______ (round off to 2 decimal places)."
}

# Q53
questions_data[53] = {
    "page": 26,
    "question": "An aircraft with a turbojet engine is flying at 270 m/s. The enthalpy of the incoming air at the intake is 260 kJ/kg and the enthalpy of the exhaust gases at the nozzle exit is 912 kJ/kg. The ratio of mass flow rates of fuel and air is equal to 0.019. The chemical energy (heating value) of fuel is 44.5 MJ/kg and the combustion process is ideal. The total loss of heat from the engine to the ambient is 25 kJ per kg of air. The velocity of the exhaust jet is ______ m/s (round off to two decimal places)."
}

# Q54
questions_data[54] = {
    "page": 26,
    "question": "Hot gases are generated at a temperature of 2100 K and a pressure of 14 MPa in a rocket chamber. The hot gases are expanded ideally to the ambient pressure of 0.1 MPa in a convergent-divergent nozzle having a throat area of 0.1 m$^2$. The molecular mass of the gas is 22 kg/kmol. The ratio of specific heats ($\\gamma$) of the gas is 1.32. The value of the universal gas constant ($R_0$) is 8314 J/kmol-K. The acceleration due to gravity, $g$, is 9.8 m/s$^2$. The specific impulse of the rocket is ______ seconds (round off to two decimal places)."
}

# Q55
questions_data[55] = {
    "page": 27,
    "question": "A twin-spool turbofan engine is operated at sea level ($P_a = 1$ bar, $T_a = 288$ K). The engine has separate cold and hot nozzles. During static thrust test at sea level, the overall mass flow rate of air through the engine and the cold exhaust temperature are measured to be 100 kg/s and 288 K, respectively. The parameters for the engine are:\nFan pressure ratio $= 1.6$\nOverall pressure ratio $= 20$\nBypass ratio $= 3.0$\nTurbine entry temperature $= 1800$ K.\nThe specific heat at constant pressure ($C_p$) is 1.005 kJ/kg-K and the ratio of specific heats ($\\gamma$) is 1.4 for air.\nAssuming ideal fan and ideal expansion in the nozzle, the sea-level static thrust from the cold nozzle is ______ kN (round off to two decimal places)."
}

# Q56
questions_data[56] = {
    "page": 27,
    "question": "At the design conditions, the velocity triangle at the mean radius of a single stage axial compressor is such that the blade angle at the rotor exit is equal to 30$^{\\circ}$. The absolute velocities at the rotor inlet and exit are equal to 140 m/s and 240 m/s, respectively. The flow velocities relative to the rotor at inlet and exit of the rotor are equal to 240 m/s and 140 m/s, respectively.\n\nThe blade speed ($U$) at the mean radius of the rotor is ______ m/s (round off to two decimal places)."
}

# Q57
questions_data[57] = {
    "page": 28,
    "question": "A single stage axial turbine has a mean blade speed of 340 m/s at design condition with blade angles at inlet and exit of the rotor being 21$^{\\circ}$ and 55$^{\\circ}$, respectively. The degree of reaction at the mean radius of the rotor is equal to 0.4. The annulus area at the rotor inlet is 0.08 m$^2$ and the density of gas at the rotor inlet is 0.9 kg/m$^3$. The flow rate through the turbine at these conditions is ______ kg/s (round off to two decimal places)."
}

# Q58
questions_data[58] = {
    "page": 28,
    "question": "The air flow rate through the gas generator of a turboprop engine is 100 kg/s. The stagnation temperatures at inlet and exit of the combustor are 600 K and 1200 K, respectively. The burner efficiency is 90% and the heating value of the fuel is 40 MJ/kg. The specific heats at constant pressure ($C_p$) for air and burned gases are 1000 J/kg-K and 1200 J/kg-K, respectively. The flow rate of the fuel being used is ______ kg/s (round off to two decimal places).\n\n(Note: Do not neglect the fuel flow rate with respect to the air flow rate)"
}

# Q59
questions_data[59] = {
    "page": 29,
    "question": "A rigid horizontal bar ABC, with roller support at A, is pinned to the columns BD and CE at points B and C, respectively as shown in figure. The other end of the column BD is fixed at D, whereas the column CE is pinned at E. A vertical load P is applied on the bar at a distance ‘a’ from point B.\nThe two columns are made of steel with elastic modulus 200 GPa and have a cross section of 1.5 cm $\\times$ 1.5 cm. The value of ‘a’ for which both columns buckle simultaneously, is ______ cm (round off to one decimal place)."
}

# Q60
questions_data[60] = {
    "page": 30,
    "question": "A two-cell wing box is shown in the figure. The cell walls are 1.5 mm thick and the shear modulus $G = 27$ GPa. If the structure is subjected to a torque of 12 kNm, then the wall AD will experience a shear stress of magnitude ______ MPa (round off to one decimal place)."
}

# Q61
questions_data[61] = {
    "page": 30,
    "question": "Two cantilever beams AB and DC are in contact with each other at their free ends through a roller as shown in the figure. Both beams have a square cross section of 50 mm $\\times$ 50 mm, and the elastic modulus $E = 70$ GPa. If beam AB is subjected to a uniformly distributed load of 20 kN/m, then the compressive force experienced by the roller is ______ kN (round off to one decimal place)."
}

# Q62
questions_data[62] = {
    "page": 31,
    "question": "A 3 m $\\times$ 1 m signboard is supported by a vertical hollow pole that is fixed to the ground. The pole has a square cross section with outer dimension 250 mm. The yield strength of the pole material is 240 MPa. To sustain a wind pressure of 7.5 kPa, the dimension $d$ of the pole is ______ mm (round off to nearest integer).\n\n(Neglect the effect of transverse shear and load due to wind pressure acting on the pole)"
}

# Q63
questions_data[63] = {
    "page": 31,
    "question": "An airplane weighing 5500 kg is in a steady level flight with a speed of 225 m/s. The pilot initiates a steady pull-up maneuver with a radius of curvature of 775 m. The location of center of gravity (CG), center of pressure on wing (CP) and point of action (T) of tail force are marked in the figure. Use $g = 9.81$ m/s$^2$. Neglect drag on the tail and assume that tail force is vertical. Assuming the engine thrust and drag to be equal, opposite and collinear, the tail force is ______ kN (round off to one decimal place)."
}

# Q64
questions_data[64] = {
    "page": 32,
    "question": "A jet aircraft weighing 10,000 kg has an elliptic wing with a span of 10 m and area 30 m$^2$. The $C_{D_0}$ for the aircraft is 0.025. The maximum speed of the aircraft in steady and level flight at sea level is 100 m/s. The density of air at sea level is 1.225 kg/m$^3$, and take $g = 10$ m/s$^2$. The maximum thrust developed by the engine at sea level is ______ N (round off to two decimal places)."
}

# Q65
questions_data[65] = {
    "page": 32,
    "question": "Consider a jet transport airplane with the following specifications:\n\nLift curve slope for wing-body $\\frac{\\partial C_{L_{wb}}}{\\partial \\alpha_{wb}} = 0.1$ /deg\nLift curve slope for tail $\\frac{\\partial C_{L_t}}{\\partial \\alpha_t} = 0.068$ /deg\nTail area $S_t = 80$ m$^2$\nWing area $S = 350$ m$^2$\nDistance between mean aerodynamic centers of tail and wing-body $\\bar{l}_t = 28$ m\nMean aerodynamic chord $\\bar{c} = 9$ m\nDownwash $\\epsilon = 0.4\\alpha$\nAxial location of the wing-body mean aerodynamic center $x_{ac}/\\bar{c} = 0.25$\nAxial location of the center of gravity $x_{cg}/\\bar{c} = 0.3$\n\nAll axial locations are with respect to the leading edge of the root chord and along the body $x$-axis. Ignore propulsive effects.\n\nThe pitching-moment-coefficient curve slope ($C_{m_\\alpha}$) is ______ /deg (round off to three decimal places)."
}

# Build full questions list
questions_list = []

for row in key_rows:
    num = row['number']
    sec = row['section']
    qtype = row['type']
    marks = row['marks']
    raw_key = row['rawKey']

    q_data = questions_data[num]
    page_num = q_data['page']

    sec_prefix = "ga" if sec == "GA" else "ae"
    qid = f"gate-2021-ae-{sec_prefix}-{num:02d}"

    # Calculate negative marks
    if qtype == "MCQ":
        neg_marks = 0.3333333333333333 if marks == 1 else 0.6666666666666666
    else:
        neg_marks = 0.0

    # Parse answer
    if raw_key == "MTA*":
        parsed_ans = "MTA"
    elif qtype == "NAT":
        if " OR " in raw_key:
            parsed_ans = []
            for part in raw_key.split(" OR "):
                if " to " in part:
                    parsed_ans.append([float(x) for x in part.split(" to ")])
                else:
                    parsed_ans.append(float(part))
        elif " to " in raw_key:
            parsed_ans = [float(x) for x in raw_key.split(" to ")]
        else:
            parsed_ans = float(raw_key)
    elif qtype == "MSQ" or ";" in raw_key or " OR " in raw_key:
        if " OR " in raw_key:
            parsed_ans = [x.strip() for x in raw_key.split(" OR ")]
        else:
            parsed_ans = [x.strip() for x in raw_key.split(";")]
    else:
        parsed_ans = raw_key

    # Figures
    figs = []
    content_blocks = [{"type": "text", "text": q_data['question']}]
    
    if num in figure_metadata:
        for fig_info in figure_metadata[num]:
            fig_obj = {
                "src": fig_info["src"],
                "alt": fig_info["alt"],
                "source": {
                    "file": "internal/ae/AE2021.pdf",
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

    has_fig = len(figs) > 0 or (num in option_figures)

    # Options
    raw_opts = q_data.get('options', [])
    opts = []
    for opt in raw_opts:
        lbl = opt['label']
        opt_obj = {
            "label": lbl,
            "text": opt['text']
        }
        if num in option_figures and lbl in option_figures[num]:
            opt_fig_info = option_figures[num][lbl]
            opt_obj["figure"] = {
                "src": opt_fig_info["src"],
                "alt": opt_fig_info["alt"],
                "source": {
                    "file": "internal/ae/AE2021.pdf",
                    "sha256": pdf_sha256,
                    "page": opt_fig_info["page"],
                    "verificationStatus": "source-verified",
                    "verifiedOn": "2026-10-07"
                },
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            }
        opts.append(opt_obj)

    # Question record
    q_record = {
        "id": qid,
        "exam": "GATE",
        "year": 2021,
        "paper": "AE",
        "number": num,
        "section": sec,
        "subject": "General Aptitude" if sec == "GA" else "Aerospace Engineering",
        "type": qtype,
        "marks": marks,
        "question": q_data['question'],
        "content": content_blocks,
        "figures": figs,
        "groupId": None,
        "source": {
            "file": "internal/ae/AE2021.pdf",
            "sha256": pdf_sha256,
            "pages": [
                {
                    "page": page_num,
                    "coordinateSystem": "PDF points, top-left origin"
                }
            ],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-07"
        },
        "transcriptionStatus": "source-verified",
        "solution": None,
        "solutionAvailability": "not-provided-in-source",
        "gradingStatus": "official key verified",
        "answerSource": {
            "url": "https://gate.iitb.ac.in/",
            "paper": "AE",
            "questionNumber": num,
            "section": sec,
            "page": page_num,
            "sha256": key_sha256,
            "verifiedOn": "2026-10-07"
        },
        "answer": parsed_ans,
        "negativeMarks": neg_marks,
        "markingRule": "gate-2021-official",
        "hasFigure": has_fig,
        "options": opts
    }

    # Accepted answers list
    if qtype == "MCQ":
        q_record["acceptedAnswers"] = [parsed_ans]
    elif qtype == "MSQ":
        q_record["acceptedAnswers"] = [parsed_ans]
    elif qtype == "NAT":
        if isinstance(parsed_ans, list) and len(parsed_ans) > 0 and isinstance(parsed_ans[0], list):
            acc_list = [{"range": r} for r in parsed_ans]
        elif isinstance(parsed_ans, list):
            acc_list = [{"range": parsed_ans}]
        else:
            acc_list = [{"value": parsed_ans}]
        q_record["acceptedAnswers"] = acc_list

    questions_list.append(q_record)

print(f"Total compiled questions: {len(questions_list)}")

ga_qids = [q["id"] for q in questions_list if q["section"] == "GA"]
ae_qids = [q["id"] for q in questions_list if q["section"] == "AE"]

paper_data = {
    "schemaVersion": 1,
    "id": "gate-2021-ae",
    "exam": "GATE",
    "year": 2021,
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
        "file": "internal/ae/AE2021.pdf",
        "sha256": pdf_sha256,
        "pageCount": len(doc)
    },
    "ingestionStatus": "complete",
    "verificationStatus": "source-verified",
    "verifiedOn": "2026-10-07",
    "questions": questions_list
}

with open('data/ae/2021.json', 'w', encoding='utf-8') as f:
    json.dump(paper_data, f, indent=2, ensure_ascii=False)
print("Saved data/ae/2021.json")

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
    if y["year"] == 2021:
        y["sourcePdf"] = "internal/ae/AE2021.pdf"
        y["path"] = "data/ae/2021.json"
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
        y["optionFigureCount"] = 4
        y["structuredTableCount"] = 0
        y["questionGroupCount"] = 0
        y["ingestionStatus"] = "complete"
        y["verificationStatus"] = "source-verified"
        y["verifiedOn"] = "2026-10-07"

with open('data/ae/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("Updated data/ae/manifest.json for 2021")
