import json, hashlib

def get_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

paper_sha256 = get_sha256('internal/ae/AE2011.pdf')
key_sha256 = get_sha256('internal/ae/AE2011-key.pdf')

def build_paper():
    cd_48_49_ctx = "Common Data for Questions 48 and 49:\nThe partial differential equation (PDE) governing free vibrations of a uniform Euler-Bernoulli beam is given by\nEI \\frac{\\partial^{4}w}{\\partial x^{4}} + m \\frac{\\partial^{2}w}{\\partial t^{2}} = 0,\nwhere EI is the flexural stiffness, m is the mass per unit length, w(x, t) is the bending displacement, x is the coordinate along the beam length, t is time and L is the beam length."

    cd_50_51_ctx = "Common Data for Questions 50 and 51:\nConsider an inviscid, adiabatic flow of air at free stream Mach Number, M_{\\infty} = 2, across a compression corner (\\theta = 20^{\\circ}) as shown. The free stream total enthalpy is h_{0\\infty} = 810\\text{ kJ kg}^{-1}. Assume that air is calorically perfect with \\gamma = 1.4, R = 287\\text{ J kg}^{-1}\\text{ K}^{-1}."

    la_52_53_ctx = "Statement for Linked Answer Questions 52 and 53:\nA thin-walled (thickness << radius), hollow shaft of length 1 m and mean radius, R = 5 cm has to be designed such that it can transmit a torque, T = 7 kN-m. A survey of different commercially available materials was made and following data was obtained from the suppliers (E: Young’s modulus, \\tau_{y}: yield stress in shear, \\rho: density):\n\n| Material | E (GPa) | \\tau_{y} (MPa) | \\rho (kg/m^{3}) |\n| :--- | :--- | :--- | :--- |\n| X | 200 | 550 | 7700 |\n| Y | 70 | 225 | 2700 |\n| Z | 110 | 375 | 4875 |"

    la_54_55_ctx = "Statement for Linked Answer Questions 54 and 55:\nPrandtl’s lifting line equation for a general wing is given by\n\\alpha(y_{0}) = \\frac{\\Gamma(y_{0})}{\\pi U_{\\infty} c(y_{0})} + \\alpha_{L=0}(y_{0}) + \\frac{1}{4\\pi U_{\\infty}} \\int_{-b/2}^{b/2} \\frac{\\frac{\\partial \\Gamma}{\\partial y}}{y_{0} - y} dy,\nwhere U_{\\infty} is the free-stream velocity, \\alpha is the angle of attack, y_{0} is the spanwise location, \\alpha_{L=0}(y_{0}) gives the spanwise variation of zero-lift angle, c is the chord, b is the span, and \\Gamma(y_{0}) gives the spanwise variation of circulation."

    def make_fig(path, alt, page):
        return [{
            "src": path,
            "alt": alt,
            "source": {
                "file": "internal/ae/AE2011.pdf",
                "page": page,
                "sha256": paper_sha256
            },
            "verificationStatus": "source-verified"
        }]

    def q_src(q_num, section, page):
        return {
            "paper": "AE",
            "year": 2011,
            "questionNumber": q_num,
            "section": section,
            "file": "internal/ae/AE2011.pdf",
            "sha256": paper_sha256,
            "pages": [{"page": page, "coordinateSystem": "PDF points, top-left origin"}],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-08"
        }

    questions_raw = [
        # Q1
        {
            "num": 1, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "Consider x, y, z to be right-handed Cartesian coordinates. A vector function is defined in this coordinate system as v⃗ = (x^{3} + 3xy^{2})î + (y^{3} + 3x^{2}y)ĵ - (3x^{2}z + 3y^{2}z)k̂, where î, ĵ and k̂ are the unit vectors along x, y and z axes, respectively. The curl of v⃗ is given by",
            "opts": [
                {"label": "A", "text": "z^{2}î - 3yk̂"},
                {"label": "B", "text": "z^{2}ĵ + 3yk̂"},
                {"label": "C", "text": "z^{2}î + 3yĵ"},
                {"label": "D", "text": "-z^{2}î + 3yk̂"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q2
        {
            "num": 2, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "Which of the following functions is periodic?",
            "opts": [
                {"label": "A", "text": "f(x) = x^{2}"},
                {"label": "B", "text": "f(x) = \\log x"},
                {"label": "C", "text": "f(x) = e^{x}"},
                {"label": "D", "text": "f(x) = \\text{const.}"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q3
        {
            "num": 3, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "The function f(x_{1}, x_{2}, x_{3}) = x_{1}^{2} + x_{2}^{2} + x_{3}^{2} - 2x_{1} - 4x_{2} - 6x_{3} + 14 has its minimum value at",
            "opts": [
                {"label": "A", "text": "(1, 2, 3)"},
                {"label": "B", "text": "(0, 0, 0)"},
                {"label": "C", "text": "(3, 2, 1)"},
                {"label": "D", "text": "(1, 1, 3)"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q4
        {
            "num": 4, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "Consider the function f(x_{1}, x_{2}) = x_{1}^{2} + 2x_{2}^{2} + e^{-x_{1} - x_{2}}. The vector pointing in the direction of maximum increase of the function at the point (1, -1) is",
            "opts": [
                {"label": "A", "text": "\\begin{pmatrix} 2 \\\\ -5 \\end{pmatrix}"},
                {"label": "B", "text": "\\begin{pmatrix} 1 \\\\ -5 \\end{pmatrix}"},
                {"label": "C", "text": "\\begin{pmatrix} -0.73 \\\\ -6.73 \\end{pmatrix}"},
                {"label": "D", "text": "\\begin{pmatrix} 2 \\\\ -4 \\end{pmatrix}"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q5
        {
            "num": 5, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "Two simultaneous equations given by y = \\pi + x and y = x - \\pi have",
            "opts": [
                {"label": "A", "text": "a unique solution"},
                {"label": "B", "text": "infinitely many solutions"},
                {"label": "C", "text": "no solution"},
                {"label": "D", "text": "a finite number of multiple solutions"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q6
        {
            "num": 6, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "In three-dimensional linear elastic solids, the number of non-trivial stress-strain relations, strain-displacement equations and equations of equilibrium are, respectively,",
            "opts": [
                {"label": "A", "text": "3, 3 and 3"},
                {"label": "B", "text": "6, 3 and 3"},
                {"label": "C", "text": "6, 6 and 3"},
                {"label": "D", "text": "6, 3 and 6"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q7
        {
            "num": 7, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "An Euler-Bernoulli beam in bending is assumed to satisfy",
            "opts": [
                {"label": "A", "text": "both plane stress as well as plane strain conditions"},
                {"label": "B", "text": "plane strain condition but not plane stress condition"},
                {"label": "C", "text": "plane stress condition but not plane strain condition"},
                {"label": "D", "text": "neither plane strain condition nor plane stress condition"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q8
        {
            "num": 8, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "A statically indeterminate frame structure has",
            "opts": [
                {"label": "A", "text": "same number of joint degrees of freedom as the number of equilibrium equations"},
                {"label": "B", "text": "number of joint degrees of freedom greater than the number of equilibrium equations"},
                {"label": "C", "text": "number of joint degrees of freedom less than the number of equilibrium equations"},
                {"label": "D", "text": "unknown number of joint degrees of freedom, which cannot be solved using laws of mechanics"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q9
        {
            "num": 9, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 2,
            "q": "Consider a single degree of freedom spring-mass-damper system with mass, damping and stiffness of m, c and k, respectively. The logarithmic decrement of this system can be calculated using",
            "opts": [
                {"label": "A", "text": "\\frac{2\\pi c}{\\sqrt{4mk - c^{2}}}"},
                {"label": "B", "text": "\\frac{\\pi c}{\\sqrt{4mk - c^{2}}}"},
                {"label": "C", "text": "\\frac{2\\pi c}{\\sqrt{mk - c^{2}}}"},
                {"label": "D", "text": "\\frac{2\\pi c}{\\sqrt{mk - 4c^{2}}}"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q10
        {
            "num": 10, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "Consider a single degree of freedom spring-mass system of spring stiffness k_{1} and mass m which has a natural frequency of 10 rad/s. Consider another single degree of freedom spring-mass system of spring stiffness k_{2} and mass m which has a natural frequency of 20 rad/s. The spring stiffness k_{1} is equal to",
            "opts": [
                {"label": "A", "text": "k_{2}"},
                {"label": "B", "text": "\\frac{1}{2} k_{2}"},
                {"label": "C", "text": "4 k_{2}"},
                {"label": "D", "text": "\\frac{1}{4} k_{2}"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q11
        {
            "num": 11, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "Consider a simply supported two-dimensional beam shown below:\n\nIf the beam is converted into a fixed-fixed beam as shown below:\n\nthen the degree of static indeterminacy will",
            "fig": make_fig("figures/gate-2011-ae-ae-11-figure-1.png", "GATE 2011 Aerospace Engineering Question 11 figure", 3),
            "opts": [
                {"label": "A", "text": "increase by 3"},
                {"label": "B", "text": "increase by 2"},
                {"label": "C", "text": "decrease by 1"},
                {"label": "D", "text": "decrease by 3"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q12
        {
            "num": 12, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "An impulsive launch of a rocket minimizes the loss of burn-out velocity due to",
            "opts": [
                {"label": "A", "text": "aerodynamic drag force only"},
                {"label": "B", "text": "gravitational force only"},
                {"label": "C", "text": "both aerodynamic drag and gravitational forces"},
                {"label": "D", "text": "reaction jet control force"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q13
        {
            "num": 13, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "Multi-staging in rockets improves the burn-out performance by increasing mainly stage-wise",
            "opts": [
                {"label": "A", "text": "payload mass ratios"},
                {"label": "B", "text": "structural mass efficiencies"},
                {"label": "C", "text": "propellant masses"},
                {"label": "D", "text": "control system masses"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q14
        {
            "num": 14, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "In an un-powered glide of an aircraft having weight W, lift L and drag D, the equilibrium glide angle is defined as",
            "opts": [
                {"label": "A", "text": "\\tan^{-1}\\left(\\frac{L}{D}\\right)"},
                {"label": "B", "text": "\\tan^{-1}\\left(\\frac{D}{L}\\right)"},
                {"label": "C", "text": "\\tan^{-1}\\left(\\frac{L}{W}\\right)"},
                {"label": "D", "text": "\\tan^{-1}\\left(\\frac{W}{L}\\right)"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q15
        {
            "num": 15, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "Lift on an aircraft climbing vertically up is",
            "opts": [
                {"label": "A", "text": "equal to its weight"},
                {"label": "B", "text": "zero"},
                {"label": "C", "text": "equal to the drag"},
                {"label": "D", "text": "equal to the thrust"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q16
        {
            "num": 16, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "If an aircraft is performing a positive yawing manoeuvre, the side slip angle",
            "opts": [
                {"label": "A", "text": "is always zero"},
                {"label": "B", "text": "is never zero"},
                {"label": "C", "text": "is always negative"},
                {"label": "D", "text": "could be any value"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q17
        {
            "num": 17, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "For an airplane to be statically stable, its centre of gravity must always be",
            "opts": [
                {"label": "A", "text": "ahead of wing aerodynamic centre"},
                {"label": "B", "text": "aft of the wing aerodynamic centre"},
                {"label": "C", "text": "ahead of neutral point"},
                {"label": "D", "text": "aft of neutral point"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q18
        {
            "num": 18, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 3,
            "q": "It is seen that the drag polar of a certain aerofoil is symmetric about the C_{d} axis. This drag polar could refer to",
            "opts": [
                {"label": "A", "text": "NACA 0012"},
                {"label": "B", "text": "NACA 4415"},
                {"label": "C", "text": "NACA 23012"},
                {"label": "D", "text": "None of the above"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q19
        {
            "num": 19, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "The aerodynamic centre of a supersonic aerofoil, with chord c, is located at",
            "opts": [
                {"label": "A", "text": "the leading edge"},
                {"label": "B", "text": "0.25c"},
                {"label": "C", "text": "0.5c"},
                {"label": "D", "text": "0.75c"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q20
        {
            "num": 20, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "Winglets are used on wings to minimize",
            "opts": [
                {"label": "A", "text": "skin friction drag"},
                {"label": "B", "text": "profile drag"},
                {"label": "C", "text": "wave drag"},
                {"label": "D", "text": "induced drag"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q21
        {
            "num": 21, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "Consider a potential flow with free stream velocity V_{\\infty}, over a spinning circular cylinder of radius R and circulation \\Gamma. The stream function, \\psi, where \\psi = 0 on the cylinder surface, in cylindrical coordinates (r, \\theta) is given by",
            "opts": [
                {"label": "A", "text": "V_{\\infty} r \\cos\\theta \\left(1 - \\frac{R^{2}}{r^{2}}\\right) + \\frac{\\Gamma}{2\\pi} \\ln\\left(\\frac{r}{R}\\right)"},
                {"label": "B", "text": "V_{\\infty} r \\cos\\theta \\left(1 + \\frac{R^{2}}{r^{2}}\\right) + \\frac{\\Gamma}{2\\pi} \\ln\\left(\\frac{r}{R}\\right)"},
                {"label": "C", "text": "V_{\\infty} r \\sin\\theta \\left(1 - \\frac{R^{2}}{r^{2}}\\right) + \\frac{\\Gamma}{2\\pi} \\ln\\left(\\frac{r}{R}\\right)"},
                {"label": "D", "text": "V_{\\infty} r \\sin\\theta \\left(1 + \\frac{R^{2}}{r^{2}}\\right) + \\frac{\\Gamma}{2\\pi} \\ln\\left(\\frac{r}{R}\\right)"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q22
        {
            "num": 22, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "A main objective of by-pass in a turbo-fan engine is to increase",
            "opts": [
                {"label": "A", "text": "mass flow rate through engine inlet"},
                {"label": "B", "text": "turbine inlet temperature"},
                {"label": "C", "text": "mass flow rate through exhaust nozzle"},
                {"label": "D", "text": "compressor pressure ratio"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q23
        {
            "num": 23, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "The pressure ratio in any one stage of a jet engine compressor is limited by",
            "opts": [
                {"label": "A", "text": "entry stagnation temperature in that stage"},
                {"label": "B", "text": "entry Mach number in that stage"},
                {"label": "C", "text": "pressure gradient induced separation in that stage"},
                {"label": "D", "text": "mass flow rate in that stage"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q24
        {
            "num": 24, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "Thermodynamic cycle on which the jet engine operates can be",
            "opts": [
                {"label": "A", "text": "open Rankine cycle only"},
                {"label": "B", "text": "either open or closed Rankine cycle"},
                {"label": "C", "text": "open Brayton cycle only"},
                {"label": "D", "text": "either open or closed Brayton cycle"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q25
        {
            "num": 25, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 4,
            "q": "Propulsion efficiency of a jet engine is",
            "opts": [
                {"label": "A", "text": "directly proportional to both the thrust power and the air mass flow rate"},
                {"label": "B", "text": "inversely proportional to both the thrust power and the air mass flow rate"},
                {"label": "C", "text": "directly proportional to the thrust power and inversely proportional to the air mass flow rate"},
                {"label": "D", "text": "inversely proportional to the thrust power and directly proportional to the air mass flow rate"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q26 (NAT)
        {
            "num": 26, "sec": "AE", "subj": "Aerospace Engineering", "type": "NAT", "marks": 2, "neg": 0, "page": 4,
            "q": "Consider a cantilever beam having length L=1 m, square cross-section (width = depth = 0.01 m) and Young’s modulus 50 GPa. The beam is subjected to a transverse load P = 1 N at the mid-span (L/2) at the center of the cross-section. Under the small deformation theory, the transverse deflection of the beam (in mm) at its free-end is",
            "fig": make_fig("figures/gate-2011-ae-ae-26-figure-1.png", "GATE 2011 Aerospace Engineering Question 26 figure", 4),
            "opts": [],
            "ans": [2.45, 2.55], "rule": "gate-2011-official"
        },
        # Q27 (NAT)
        {
            "num": 27, "sec": "AE", "subj": "Aerospace Engineering", "type": "NAT", "marks": 2, "neg": 0, "page": 5,
            "q": "Consider a beam in bending with a solid circular cross-section of 1 mm^{2}, which is subjected to a transverse shear force of 1 N. The shear stress at the center of the cross-section (in N/mm^{2}) is",
            "opts": [],
            "ans": [1.30, 1.35], "rule": "gate-2011-official"
        },
        # Q28 (NAT)
        {
            "num": 28, "sec": "AE", "subj": "Aerospace Engineering", "type": "NAT", "marks": 2, "neg": 0, "page": 5,
            "q": "A simply supported slender column of square cross section (width=depth=d) has to be designed such that it buckles at the same instant as it yields. Length of the column is given to be 1.57 m and it is made of a material whose Young’s modulus is 200 GPa and yield stress is 240 MPa. The width, d, of the column (in cm) should be",
            "opts": [],
            "ans": [5.95, 6.05], "rule": "gate-2011-official"
        },
        # Q29 (NAT)
        {
            "num": 29, "sec": "AE", "subj": "Aerospace Engineering", "type": "NAT", "marks": 2, "neg": 0, "page": 5,
            "q": "A turbojet powered aircraft is flying at Mach number 0.8 at an altitude of 10 km. The inlet and exit areas of the engine are 0.7 m^{2} and 0.4 m^{2} respectively. The exhaust gases have velocity of 500 m/s and pressure of 60 kPa. The free stream pressure, density and speed of sound are 26.5 kPa, 0.413 kg/m^{3} and 299.5 m/s respectively. The thrust of the engine (in kN) is",
            "opts": [],
            "ans": [29.0, 32.0], "rule": "gate-2011-official"
        },
        # Q30 (NAT)
        {
            "num": 30, "sec": "AE", "subj": "Aerospace Engineering", "type": "NAT", "marks": 2, "neg": 0, "page": 5,
            "q": "A low speed wind tunnel has a contraction ratio of 14:1 and the cross-sectional area of the test section is 1 m^{2}. The static pressure difference between the settling chamber and the test section is 40 cm of water column. Assume g = 9.81\\text{ m/s}^{2}, \\rho_{\\text{air}} = 1.2\\text{ kg/m}^{3} and \\rho_{\\text{water}} = 1000\\text{ kg/m}^{3}. The speed of air in the test section (in m/s) is",
            "opts": [],
            "ans": [80.0, 82.0], "rule": "gate-2011-official"
        },
        # Q31
        {
            "num": 31, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 5,
            "q": "Consider the function f(x) = x - \\sin(x). The Newton-Raphson iteration formula to find the root of the function starting from an initial guess x^{(0)} at iteration k is",
            "opts": [
                {"label": "A", "text": "x^{(k+1)} = \\frac{\\sin(x^{(k)}) - x^{(k)}\\cos(x^{(k)})}{1 - \\cos(x^{(k)})}"},
                {"label": "B", "text": "x^{(k+1)} = \\frac{\\sin(x^{(k)}) - x^{(k)}\\cos(x^{(k)})}{1 + \\cos(x^{(k)})}"},
                {"label": "C", "text": "x^{(k+1)} = \\frac{\\sin(x^{(k)}) + x^{(k)}\\cos(x^{(k)})}{1 - \\cos(x^{(k)})}"},
                {"label": "D", "text": "x^{(k+1)} = \\frac{\\sin(x^{(k)}) + x^{(k)}\\cos(x^{(k)})}{1 + \\cos(x^{(k)})}"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q32
        {
            "num": 32, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 5,
            "q": "Consider the matrix \\begin{bmatrix} a & 2 \\\\ 2 & b \\end{bmatrix} where a and b are real numbers. The two eigenvalues of this matrix \\lambda_{1} and \\lambda_{2} are real and distinct (\\lambda_{1} \\neq \\lambda_{2}) when",
            "opts": [
                {"label": "A", "text": "a < 0\\text{ and }b > 0"},
                {"label": "B", "text": "a > 0\\text{ and }b < 0"},
                {"label": "C", "text": "a < 0\\text{ and }b < 0"},
                {"label": "D", "text": "a = 0\\text{ and }b = 0"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q33
        {
            "num": 33, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 5,
            "q": "The solution of \\frac{dy}{dt} = y^{3} e^{t} t^{2} with initial condition y(0) = 1 is given by",
            "opts": [
                {"label": "A", "text": "\\frac{1}{9} [e^{t} (t + 3)]^{2}"},
                {"label": "B", "text": "\\left[ \\frac{5}{2} + 2e^{t}(t^{2} - 2t + 2) \\right]^{9/2}"},
                {"label": "C", "text": "\\frac{1}{4} [e^{t} (t + 2)]^{2}"},
                {"label": "D", "text": "\\left[ 5 - 2e^{t}(t^{2} - 2t + 2) \\right]^{-1/2}"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q34
        {
            "num": 34, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "A jet engine is operating at a Mach number of 0.8 at an altitude of 10 km. The efficiency of the air intake is 0.8 and that of the compressor is 0.87. The total temperatures (in K) at the exits of the air intake and the compressor respectively are\n(Ambient pressure = 26.5 kPa; Ambient temperature = 223.3 K; Gas constant, \\gamma = 1.4; r_{c} = 8, c_{p} = 1005\\text{ J/kg}\\cdot\\text{K})",
            "opts": [
                {"label": "A", "text": "251.9 and 458.2"},
                {"label": "B", "text": "234.9 and 486.8"},
                {"label": "C", "text": "251.9 and 486.8"},
                {"label": "D", "text": "234.9 and 458.2"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q35
        {
            "num": 35, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "A rocket engine is tested on a test bed under the ideal condition of fully expanded jet. The exhaust velocity is 2 km/s through a nozzle of area 2.5 m^{2}. The mass flow rate is 200 kg/s. The specific impulse of the propellant and the thrust developed respectively are (assume g = 9.81 m/s^{2})",
            "opts": [
                {"label": "A", "text": "175.87 s and 200 kN"},
                {"label": "B", "text": "203.87 s and 400 kN"},
                {"label": "C", "text": "231.87 s and 200 kN"},
                {"label": "D", "text": "280.87 s and 400 kN"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q36
        {
            "num": 36, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "A body undergoes deformation under plane strain conditions when subjected to the following stresses (in MPa): \\sigma_{xx} = 450, \\sigma_{yy} = 450, \\tau_{xy} = 75, \\tau_{xz} = 0, \\tau_{yz} = 0. What are the remaining components of stresses (in MPa) and strains? Assume the material to be isotropic and linear-elastic with Young’s modulus E = 200 GPa and Poisson’s ratio \\nu = 1/3.",
            "opts": [
                {"label": "A", "text": "\\sigma_{zz} = 0, \\epsilon_{xx} = 0.00225, \\epsilon_{yy} = 0.00225, \\gamma_{xy} = 0.002, \\gamma_{xz} = 0, \\gamma_{yz} = 0"},
                {"label": "B", "text": "\\sigma_{zz} = 300, \\epsilon_{xx} = 0.001, \\epsilon_{yy} = 0.001, \\gamma_{xy} = 0.001, \\gamma_{xz} = 0, \\gamma_{yz} = 0"},
                {"label": "C", "text": "\\sigma_{zz} = 300, \\epsilon_{xx} = 0.00225, \\epsilon_{yy} = 0.00225, \\gamma_{xy} = 0.001, \\gamma_{xz} = 0, \\gamma_{yz} = 0"},
                {"label": "D", "text": "\\sigma_{zz} = 0, \\epsilon_{xx} = 0.001, \\epsilon_{yy} = 0.001, \\gamma_{xy} = 0.002, \\gamma_{xz} = 0, \\gamma_{yz} = 0"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q37
        {
            "num": 37, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "Which of the following Airy’s stress functions could satisfy the given boundary conditions, assuming constant values of σ_{xx} = P, σ_{yy} = Q and τ_{xy} = R, along the boundary?",
            "fig": make_fig("figures/gate-2011-ae-ae-37-figure-1.png", "GATE 2011 Aerospace Engineering Question 37 figure", 6),
            "opts": [
                {"label": "A", "text": "\\phi = \\frac{P x^{2}}{2} + \\frac{Q y^{2}}{2} - Rxy"},
                {"label": "B", "text": "\\phi = \\frac{P y^{2}}{2} + \\frac{Q x^{2}}{2} + Rxy"},
                {"label": "C", "text": "\\phi = \\frac{P y^{2}}{2} + \\frac{Q x^{2}}{2} - Rxy"},
                {"label": "D", "text": "\\phi = \\frac{P x^{2}}{2} + \\frac{Q y^{2}}{2} + Rxy"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q38
        {
            "num": 38, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "An aircraft is performing a coordinated turn manoeuvre at a bank angle of 30^{\\circ} and forward speed of 100 m/s. Assume g = 9.81 ms^{-2}. The load factor and turn radius respectively are",
            "opts": [
                {"label": "A", "text": "(2/\\sqrt{3}) and 1.76 km"},
                {"label": "B", "text": "\\sqrt{3} and 17.6 km"},
                {"label": "C", "text": "2 and 0.18 km"},
                {"label": "D", "text": "(2/\\sqrt{3}) and 17.6 km"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q39
        {
            "num": 39, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 6,
            "q": "An aircraft in a steady level flight at forward speed of 50 m/s suddenly rolls by 180^{\\circ} and becomes inverted. If no other changes are made to the configuration or controls of the aircraft, the nature of the subsequent flight path taken by the aircraft and its characteristic parameter(s) (assume g = 9.81 ms^{-2}) are",
            "opts": [
                {"label": "A", "text": "straight line path with a speed of 50 m/s"},
                {"label": "B", "text": "upward circular path with a speed of 50 m/s and radius of 127.4 m"},
                {"label": "C", "text": "downward circular path with a speed of 50 m/s and radius of 127.4 m"},
                {"label": "D", "text": "downward circular path with a speed of 25 m/s and radius of 254.8 m"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q40
        {
            "num": 40, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "An aircraft with a mass of 5000 kg takes off from sea level with a forward speed of 50 m/s and starts to climb with a climb angle of 15^{\\circ}. The rate of climb and excess thrust available at the start of the climb respectively (assume g = 9.81 ms^{-2}) are",
            "opts": [
                {"label": "A", "text": "13.40 m/s and 13146.0 N"},
                {"label": "B", "text": "12.94 m/s and 12694.1 N"},
                {"label": "C", "text": "13.40 m/s and 12694.1 N"},
                {"label": "D", "text": "12.94 m/s and 13146.0 N"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q41
        {
            "num": 41, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "A glider having a mass of 500 kg is taken to an altitude of 1000 m with a jeep moving on ground at 54 kmph. Upon reaching the required altitude in 50 s, the glider is released and starts its descent. Under the assumption of equilibrium glide, the range and endurance of the glider for a constant lift-to-drag ratio of 15 are",
            "opts": [
                {"label": "A", "text": "15.0 km and 1002.2 s respectively"},
                {"label": "B", "text": "15.0 km and 601.3 s respectively"},
                {"label": "C", "text": "1.0 km and 601.3 s respectively"},
                {"label": "D", "text": "1.0 km and 50 s respectively"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q42
        {
            "num": 42, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "An elliptic orbit has its perigee at 400 km above the Earth’s surface and apogee at 3400 km above the Earth’s surface. For this orbit, the eccentricity and semi-major axis respectively are (assume radius of Earth = 6400 km)",
            "opts": [
                {"label": "A", "text": "0.18 and 8300 km"},
                {"label": "B", "text": "0.18 and 1900 km"},
                {"label": "C", "text": "0.22 and 8300 km"},
                {"label": "D", "text": "0.22 and 1900 km"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q43
        {
            "num": 43, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "An aircraft in level flight encounters a vertical gust, which excites the phugoid mode. The phugoid motion completes 10 cycles in 50 s and its amplitude reduces to half of its maximum value in 25 s. The eigenvalues of the phugoid mode are",
            "opts": [
                {"label": "A", "text": "-0.05 \\pm 0.02i"},
                {"label": "B", "text": "-0.5 \\pm 0.2i"},
                {"label": "C", "text": "-0.028 \\pm 1.26i"},
                {"label": "D", "text": "0.028 \\pm 1.26i"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q44
        {
            "num": 44, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "Consider the inviscid, adiabatic flow of air at free stream conditions, M_{1} = 2, p_{1} = 1 atm and T_{1} = 288 K around a sharp expansion corner (θ = 20°) as shown below. The Prandtl-Meyer function, ν, is given as a function of Mach number, M, as\n\nν(M) = \\sqrt{\\frac{\\gamma+1}{\\gamma-1}} \\tan^{-1}\\sqrt{\\frac{\\gamma-1}{\\gamma+1}(M^{2}-1)} - \\tan^{-1}\\sqrt{M^{2}-1}.\n\nAssume air to be calorically perfect with γ = 1.4. The Mach number, M_{2}, downstream of the expansion corner is approximately",
            "fig": make_fig("figures/gate-2011-ae-ae-44-figure-1.png", "GATE 2011 Aerospace Engineering Question 44 figure", 7),
            "opts": [
                {"label": "A", "text": "2.00"},
                {"label": "B", "text": "1.76"},
                {"label": "C", "text": "2.83"},
                {"label": "D", "text": "3.14"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q45
        {
            "num": 45, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 7,
            "q": "Consider a steady two dimensional zero-pressure gradient laminar flow of air over a flat plate as shown below. The free stream conditions are U_{\\infty} = 100\\text{ ms}^{-1}, \\rho_{\\infty} = 1.2\\text{ kg m}^{-3}, p_{\\infty} = 1\\text{ atm} and \\mu_{\\infty} = 1.8 \\times 10^{-5}\\text{ kg m}^{-1}\\text{s}^{-1}. The ratio of displacement thickness to momentum thickness of the boundary layer at a distance of 2 m from the leading edge is",
            "fig": make_fig("figures/gate-2011-ae-ae-45-figure-1.png", "GATE 2011 Aerospace Engineering Question 45 figure", 7),
            "opts": [
                {"label": "A", "text": "7.53"},
                {"label": "B", "text": "2.59"},
                {"label": "C", "text": "2.91"},
                {"label": "D", "text": "0.39"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q46
        {
            "num": 46, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "q": "In the context of Prandtl’s lifting line theory for a finite wing, which of the following combinations of statements is TRUE?\nP: The bound vortex is responsible for the lift force\nQ: The trailing vortices are responsible for the induced drag\nR: The bound vortex is responsible for the induced drag\nS: The trailing vortices are responsible for the lift force",
            "opts": [
                {"label": "A", "text": "P, Q"},
                {"label": "B", "text": "Q, R"},
                {"label": "C", "text": "R, S"},
                {"label": "D", "text": "P, S"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q47
        {
            "num": 47, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "q": "Consider flow over a thin aerofoil at Mach number, M_{\\infty} = 0.5 at an angle of attack, \\alpha. Using the Prandtl-Glauert rule for compressibility correction, the formula for lift coefficient, c_{l}, can be written as",
            "opts": [
                {"label": "A", "text": "5.44\\alpha"},
                {"label": "B", "text": "6.28\\alpha"},
                {"label": "C", "text": "7.26\\alpha"},
                {"label": "D", "text": "14.52\\alpha"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q48 (Common Data 48 & 49)
        {
            "num": 48, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "groupId": "common-data-48-49",
            "q": "To solve the PDE, the number of boundary conditions (BC) and initial conditions (IC) needed are",
            "opts": [
                {"label": "A", "text": "4 BC, 3 IC"},
                {"label": "B", "text": "2 BC, 2 IC"},
                {"label": "C", "text": "2 BC, 4 IC"},
                {"label": "D", "text": "4 BC, 2 IC"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q49 (Common Data 48 & 49)
        {
            "num": 49, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "groupId": "common-data-48-49",
            "q": "For the cantilever beam shown in the figure, which of the following CANNOT be a possible boundary condition?",
            "fig": make_fig("figures/gate-2011-ae-ae-49-figure-1.png", "GATE 2011 Aerospace Engineering Question 49 figure", 8),
            "opts": [
                {"label": "A", "text": "w(0, t) = 0"},
                {"label": "B", "text": "\\frac{\\partial^{2}w}{\\partial x^{2}}(L, t) = 0"},
                {"label": "C", "text": "\\frac{\\partial^{2}w}{\\partial x^{2}}(0, t) = 0"},
                {"label": "D", "text": "\\frac{\\partial^{3}w}{\\partial x^{3}}(L, t) = 0"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q50 (Common Data 50 & 51)
        {
            "num": 50, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "groupId": "common-data-50-51",
            "q": "The shock angle \\beta is",
            "fig": make_fig("figures/gate-2011-ae-ae-50-figure-1.png", "GATE 2011 Aerospace Engineering Question 50 figure", 8),
            "opts": [
                {"label": "A", "text": "= 20^{\\circ}"},
                {"label": "B", "text": "> 20^{\\circ}\\text{ and }< 30^{\\circ}"},
                {"label": "C", "text": "= 30^{\\circ}"},
                {"label": "D", "text": "> 30^{\\circ}"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q51 (Common Data 50 & 51)
        {
            "num": 51, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 8,
            "groupId": "common-data-50-51",
            "q": "The total temperature at point P is",
            "opts": [
                {"label": "A", "text": "806.37 K"},
                {"label": "B", "text": "1128.92 K"},
                {"label": "C", "text": "1612.74 K"},
                {"label": "D", "text": "2257.84 K"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q52 (Linked Answer 52 & 53)
        {
            "num": 52, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 9,
            "groupId": "linked-answer-52-53",
            "q": "Which of the above materials would you choose such that weight of the shaft is minimum?",
            "opts": [
                {"label": "A", "text": "X only"},
                {"label": "B", "text": "Y only"},
                {"label": "C", "text": "Z only"},
                {"label": "D", "text": "X or Y"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q53 (Linked Answer 52 & 53)
        {
            "num": 53, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 9,
            "groupId": "linked-answer-52-53",
            "q": "If you assume a factor of safety of 2, what should be the approximate thickness of such a shaft?",
            "opts": [
                {"label": "A", "text": "0.5 mm"},
                {"label": "B", "text": "1 mm"},
                {"label": "C", "text": "2 mm"},
                {"label": "D", "text": "4 mm"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q54 (Linked Answer 54 & 55)
        {
            "num": 54, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 9,
            "groupId": "linked-answer-54-55",
            "q": "The rate of change of circulation with angle of attack \\Gamma_{\\alpha} = \\frac{\\partial \\Gamma}{\\partial \\alpha} is",
            "opts": [
                {"label": "A", "text": "inversely proportional to \\alpha"},
                {"label": "B", "text": "independent of \\alpha"},
                {"label": "C", "text": "a linear function of \\alpha"},
                {"label": "D", "text": "a quadratic function of \\alpha"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q55 (Linked Answer 54 & 55)
        {
            "num": 55, "sec": "AE", "subj": "Aerospace Engineering", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 9,
            "groupId": "linked-answer-54-55",
            "q": "Given that C_{L} \\propto \\int_{-b/2}^{b/2} \\Gamma(y) dy, the corresponding lift curve-slope \\frac{\\partial C_{L}}{\\partial \\alpha} is",
            "opts": [
                {"label": "A", "text": "independent of \\alpha"},
                {"label": "B", "text": "a linear function of \\alpha"},
                {"label": "C", "text": "a quadratic function of \\alpha"},
                {"label": "D", "text": "a cubic function of \\alpha"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q56
        {
            "num": 56, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 10,
            "q": "Choose the word from the options given below that is most nearly opposite in meaning to the given word:\n\n**Deference**",
            "opts": [
                {"label": "A", "text": "aversion"},
                {"label": "B", "text": "resignation"},
                {"label": "C", "text": "suspicion"},
                {"label": "D", "text": "contempt"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        },
        # Q57
        {
            "num": 57, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 10,
            "q": "Choose the most appropriate word(s) from the options given below to complete the following sentence.\n\nWe lost confidence in him because he never __________ the grandiose promises he had made.",
            "opts": [
                {"label": "A", "text": "delivered"},
                {"label": "B", "text": "delivered on"},
                {"label": "C", "text": "forgot"},
                {"label": "D", "text": "reneged on"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q58
        {
            "num": 58, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 10,
            "q": "Choose the word or phrase that best completes the sentence below.\n\n______________ in the frozen wastes of Arctic takes special equipment.",
            "opts": [
                {"label": "A", "text": "To survive"},
                {"label": "B", "text": "Surviving"},
                {"label": "C", "text": "Survival"},
                {"label": "D", "text": "That survival"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q59
        {
            "num": 59, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 10,
            "q": "In how many ways 3 scholarships can be awarded to 4 applicants, when each applicant can receive any number of scholarships?",
            "opts": [
                {"label": "A", "text": "4"},
                {"label": "B", "text": "12"},
                {"label": "C", "text": "64"},
                {"label": "D", "text": "81"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q60
        {
            "num": 60, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 1, "neg": 0.3333333333333333, "page": 10,
            "q": "Choose the most appropriate word from the options given below to complete the following sentence.\n\nThe _________ of evidence was on the side of the plaintiff since all but one witness testified that his story was correct.",
            "opts": [
                {"label": "A", "text": "paucity"},
                {"label": "B", "text": "propensity"},
                {"label": "C", "text": "preponderance"},
                {"label": "D", "text": "accuracy"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q61
        {
            "num": 61, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 10,
            "q": "If \\frac{2y+1}{y+2} < 1, then which of the following alternatives gives the CORRECT range of y?",
            "opts": [
                {"label": "A", "text": "-2 < y < 2"},
                {"label": "B", "text": "-2 < y < 1"},
                {"label": "C", "text": "-3 < y < 1"},
                {"label": "D", "text": "-4 < y < 1"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q62
        {
            "num": 62, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 10,
            "q": "A student attempted to solve a quadratic equation in x twice. However, in the first attempt, he incorrectly wrote the constant term and ended up with the roots as (4, 3). In the second attempt, he incorrectly wrote down the coefficient of x and got the roots as (3, 2). Based on the above information, the roots of the correct quadratic equation are",
            "opts": [
                {"label": "A", "text": "(-3, 4)"},
                {"label": "B", "text": "(3, -4)"},
                {"label": "C", "text": "(6, 1)"},
                {"label": "D", "text": "(4, 2)"}
            ],
            "ans": "C", "rule": "gate-2011-official"
        },
        # Q63
        {
            "num": 63, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 11,
            "q": "L, M and N are waiting in a queue meant for children to enter the zoo. There are 5 children between L and M, and 8 children between M and N. If there are 3 children ahead of N and 21 children behind L, then what is the minimum number of children in the queue?",
            "opts": [
                {"label": "A", "text": "28"},
                {"label": "B", "text": "27"},
                {"label": "C", "text": "41"},
                {"label": "D", "text": "40"}
            ],
            "ans": "A", "rule": "gate-2011-official"
        },
        # Q64
        {
            "num": 64, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 11,
            "q": "Four archers P, Q, R and S try to hit a bull’s eye during a tournament consisting of seven rounds. As illustrated in the figure below, a player receives 10 points for hitting the bull’s eye, 5 points for hitting within the inner circle and 1 point for hitting within the outer circle.\n\nThe final scores received by the players during the tournament are listed in the table below:\n\n| Round | P | Q | R | S |\n| :--- | :--- | :--- | :--- | :--- |\n| 1 | 1 | 5 | 1 | 10 |\n| 2 | 5 | 10 | 10 | 1 |\n| 3 | 1 | 1 | 1 | 5 |\n| 4 | 10 | 10 | 1 | 1 |\n| 5 | 1 | 5 | 5 | 10 |\n| 6 | 10 | 5 | 1 | 1 |\n| 7 | 5 | 10 | 1 | 1 |\n\nThe most accurate and the most consistent players during the tournament are respectively",
            "fig": make_fig("figures/gate-2011-ae-ga-64-figure-1.png", "GATE 2011 Aerospace Engineering Question 64 figure", 11),
            "opts": [
                {"label": "A", "text": "P and S"},
                {"label": "B", "text": "Q and R"},
                {"label": "C", "text": "Q and Q"},
                {"label": "D", "text": "R and Q"}
            ],
            "ans": "B", "rule": "gate-2011-official"
        },
        # Q65
        {
            "num": 65, "sec": "GA", "subj": "General Aptitude", "type": "MCQ", "marks": 2, "neg": 0.6666666666666666, "page": 11,
            "q": "Nimbus clouds are dark and ragged, stratus clouds appear dull in colour and cover the entire sky. Cirrus clouds are thin and delicate, whereas cumulus clouds look like cotton balls.\n\nIt can be inferred from the passage that",
            "opts": [
                {"label": "A", "text": "A cumulus cloud on the ground is called fog"},
                {"label": "B", "text": "It is easy to predict the weather by studying clouds"},
                {"label": "C", "text": "Clouds are generally of very different shapes, sizes and mass"},
                {"label": "D", "text": "There are four basic cloud types: stratus, nimbus, cumulus and cirrus"}
            ],
            "ans": "D", "rule": "gate-2011-official"
        }
    ]

    q_list = []
    question_refs = []
    ae_q_ids = []
    ga_q_ids = []
    all_q_ids = []

    for item in questions_raw:
        sec_prefix = item['sec'].lower()
        qid = f"gate-2011-ae-{sec_prefix}-{item['num']:02d}"
        all_q_ids.append(qid)
        if item['sec'] == 'AE':
            ae_q_ids.append(qid)
        else:
            ga_q_ids.append(qid)

        question_refs.append({
            "id": qid,
            "number": item['num'],
            "section": item['sec']
        })

        has_fig = bool(item.get('fig'))
        figs = item.get('fig', [])

        q_obj = {
            "id": qid,
            "number": item['num'],
            "year": 2011,
            "paper": "AE",
            "section": item['sec'],
            "subject": item['subj'],
            "type": item['type'],
            "marks": item['marks'],
            "negativeMarks": item['neg'],
            "question": item['q'],
            "options": item['opts'],
            "answer": item['ans'],
            "acceptedAnswers": [item['ans']] if isinstance(item['ans'], str) else item['ans'],
            "markingRule": item['rule'],
            "hasFigure": has_fig,
            "figures": figs,
            "groupId": item.get('groupId', None),
            "source": q_src(item['num'], item['sec'], item['page']),
            "transcriptionStatus": "source-verified",
            "solution": None,
            "solutionAvailability": "not-provided-in-source",
            "gradingStatus": "official key verified"
        }
        q_list.append(q_obj)

    question_groups = [
        {
            "id": "common-data-48-49",
            "type": "common-data",
            "title": "Common Data for Questions 48 and 49",
            "content": [
                {
                    "type": "text",
                    "text": cd_48_49_ctx
                }
            ],
            "questionIds": ["gate-2011-ae-ae-48", "gate-2011-ae-ae-49"]
        },
        {
            "id": "common-data-50-51",
            "type": "common-data",
            "title": "Common Data for Questions 50 and 51",
            "content": [
                {
                    "type": "text",
                    "text": cd_50_51_ctx
                }
            ],
            "questionIds": ["gate-2011-ae-ae-50", "gate-2011-ae-ae-51"]
        },
        {
            "id": "linked-answer-52-53",
            "type": "linked-answer",
            "title": "Statement for Linked Answer Questions 52 and 53",
            "content": [
                {
                    "type": "text",
                    "text": la_52_53_ctx
                }
            ],
            "questionIds": ["gate-2011-ae-ae-52", "gate-2011-ae-ae-53"],
            "dependencies": [
                {
                    "questionId": "gate-2011-ae-ae-53",
                    "dependsOn": "gate-2011-ae-ae-52"
                }
            ]
        },
        {
            "id": "linked-answer-54-55",
            "type": "linked-answer",
            "title": "Statement for Linked Answer Questions 54 and 55",
            "content": [
                {
                    "type": "text",
                    "text": la_54_55_ctx
                }
            ],
            "questionIds": ["gate-2011-ae-ae-54", "gate-2011-ae-ae-55"],
            "dependencies": [
                {
                    "questionId": "gate-2011-ae-ae-55",
                    "dependsOn": "gate-2011-ae-ae-54"
                }
            ]
        }
    ]

    paper = {
        "schemaVersion": 1,
        "id": "gate-2011-ae",
        "exam": "GATE",
        "year": 2011,
        "paper": "AE",
        "title": "GATE Aerospace Engineering 2011",
        "durationMinutes": 180,
        "totalMarks": 100,
        "totalQuestions": 65,
        "sectionOrder": ["AE", "GA"],
        "sections": [
            {
                "id": "AE",
                "title": "Aerospace Engineering",
                "questionIds": ae_q_ids,
                "totalMarks": 85
            },
            {
                "id": "GA",
                "title": "General Aptitude",
                "questionIds": ga_q_ids,
                "totalMarks": 15
            }
        ],
        "questionOrder": all_q_ids,
        "questionRefs": question_refs,
        "questionGroups": question_groups,
        "marking": {
            "negativeFraction": {
                "MCQ": 0.3333333333333333,
                "MSQ": 0,
                "NAT": 0
            }
        },
        "source": {
            "file": "internal/ae/AE2011.pdf",
            "sha256": paper_sha256,
            "pageCount": 11
        },
        "questions": q_list
    }

    with open('data/ae/2011.json', 'w', encoding='utf-8') as f:
        json.dump(paper, f, indent=2, ensure_ascii=False)

    print("Successfully built data/ae/2011.json")

if __name__ == '__main__':
    build_paper()
