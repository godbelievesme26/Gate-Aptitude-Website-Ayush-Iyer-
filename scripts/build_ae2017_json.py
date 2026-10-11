import json
import hashlib
import os

pdf_path = 'internal/ae/AE2017.pdf'
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

key_path = 'internal/ae/AE2017-key.json'
with open(key_path, 'r', encoding='utf-8') as f:
    key_data = json.load(f)

key_pdf_sha256 = "711b0d8d2da78a8ac7a65ff4f932b411d9f38d49b13fe44b474b95ddb57d8569"

# Build a lookup for key data by section and sectionQuestionNumber
key_lookup = {}
for r in key_data['rows']:
    sec = r['section']
    sqn = r['sectionQuestionNumber']
    key_lookup[(sec, sqn)] = r

# Map PDF question number to page number in AE2017.pdf
def get_pdf_page(sec, sqn):
    if sec == 'GA':
        if 56 <= sqn <= 59: return 19
        if 60 <= sqn <= 63: return 20
        if 64 <= sqn <= 65: return 21
    else:
        if 1 <= sqn <= 4: return 2
        if 5 <= sqn <= 8: return 3
        if 9 <= sqn <= 11: return 4
        if 12 <= sqn <= 14: return 5
        if 15 <= sqn <= 18: return 6
        if 19 <= sqn <= 22: return 7
        if 23 <= sqn <= 26: return 8
        if 27 <= sqn <= 29: return 9
        if 30 <= sqn <= 33: return 10
        if 34 <= sqn <= 35: return 11
        if 36 <= sqn <= 38: return 12
        if 39 <= sqn <= 42: return 13
        if 43 <= sqn <= 45: return 14
        if 46 <= sqn <= 48: return 15
        if 49 <= sqn <= 51: return 16
        if 52 <= sqn <= 53: return 17
        if 54 <= sqn <= 55: return 18
    return 1

def get_key_page(sec, sqn):
    if sec == 'AE' and sqn <= 36:
        return 1
    return 2

# Question definitions
# (id, number, section, subject, secQNum, type, marks, negMarks, question_text, figures, options)
q_defs = [
    # GA 1-5 (1M)
    (
        "gate-2017-ae-ga-01", 1, "GA", "General Aptitude", 56, "MCQ", 1, 0.3333333333333333,
        "The ninth and the tenth of this month are Monday and Tuesday ________.",
        [],
        [
            {"label": "A", "text": "figuratively"},
            {"label": "B", "text": "retrospectively"},
            {"label": "C", "text": "respectively"},
            {"label": "D", "text": "rightfully"}
        ]
    ),
    (
        "gate-2017-ae-ga-02", 2, "GA", "General Aptitude", 57, "MCQ", 1, 0.3333333333333333,
        "It is ________ to read this year’s textbook ________ the last year’s.",
        [],
        [
            {"label": "A", "text": "easier, than"},
            {"label": "B", "text": "most easy, than"},
            {"label": "C", "text": "easier, from"},
            {"label": "D", "text": "easiest, from"}
        ]
    ),
    (
        "gate-2017-ae-ga-03", 3, "GA", "General Aptitude", 58, "MCQ", 1, 0.3333333333333333,
        "A rule states that in order to drink beer, one must be over 18 years old. In a bar, there are 4 people. P is 16 years old, Q is 25 years old, R is drinking milkshake and S is drinking a beer. What must be checked to ensure that the rule is being followed?",
        [],
        [
            {"label": "A", "text": "Only P’s drink"},
            {"label": "B", "text": "Only P’s drink and S’s age"},
            {"label": "C", "text": "Only S’s age"},
            {"label": "D", "text": "Only P’s drink, Q’s drink and S’s age"}
        ]
    ),
    (
        "gate-2017-ae-ga-04", 4, "GA", "General Aptitude", 59, "MCQ", 1, 0.3333333333333333,
        "Fatima starts from point P, goes North for 3 km, and then East for 4 km to reach point Q. She then turns to face point P and goes 15 km in that direction. She then goes North for 6 km. How far is she from point P, and in which direction should she go to reach point P?",
        [],
        [
            {"label": "A", "text": "8 km, East"},
            {"label": "B", "text": "12 km, North"},
            {"label": "C", "text": "6 km, East"},
            {"label": "D", "text": "10 km, North"}
        ]
    ),
    (
        "gate-2017-ae-ga-05", 5, "GA", "General Aptitude", 60, "MCQ", 1, 0.3333333333333333,
        "500 students are taking one or more courses out of Chemistry, Physics, and Mathematics. Registration records indicate course enrolment as follows: Chemistry (329), Physics (186), Mathematics (295), Chemistry and Physics (83), Chemistry and Mathematics (217), and Physics and Mathematics (63). How many students are taking all 3 subjects?",
        [],
        [
            {"label": "A", "text": "37"},
            {"label": "B", "text": "43"},
            {"label": "C", "text": "47"},
            {"label": "D", "text": "53"}
        ]
    ),
    # GA 6-10 (2M)
    (
        "gate-2017-ae-ga-06", 6, "GA", "General Aptitude", 61, "MCQ", 2, 0.6666666666666666,
        "“If you are looking for a history of India, or for an account of the rise and fall of the British Raj, or for the reason of the cleaving of the subcontinent into two mutually antagonistic parts and the effects this mutilation will have in the respective sections, and ultimately on Asia, you will not find it in these pages; for though I have spent a lifetime in the country, I lived too near the seat of events, and was too intimately associated with the actors, to get the perspective needed for the impartial recording of these matters.”\n\nWhich of the following statements best reflects the author’s opinion?",
        [],
        [
            {"label": "A", "text": "An intimate association does not allow for the necessary perspective."},
            {"label": "B", "text": "Matters are recorded with an impartial perspective."},
            {"label": "C", "text": "An intimate association offers an impartial perspective."},
            {"label": "D", "text": "Actors are typically associated with the impartial recording of matters."}
        ]
    ),
    (
        "gate-2017-ae-ga-07", 7, "GA", "General Aptitude", 62, "MCQ", 2, 0.6666666666666666,
        "Each of P, Q, R, S, W, X, Y and Z has been married at most once. X and Y are married and have two children P and Q. Z is the grandfather of the daughter S of P. Further, Z and W are married and are parents of R. Which one of the following must necessarily be FALSE?",
        [],
        [
            {"label": "A", "text": "X is the mother-in-law of R"},
            {"label": "B", "text": "P and R are not married to each other"},
            {"label": "C", "text": "P is a son of X and Y"},
            {"label": "D", "text": "Q cannot be married to R"}
        ]
    ),
    (
        "gate-2017-ae-ga-08", 8, "GA", "General Aptitude", 63, "MCQ", 2, 0.6666666666666666,
        "1200 men and 500 women can build a bridge in 2 weeks. 900 men and 250 women will take 3 weeks to build the same bridge. How many men will be needed to build the bridge in one week?",
        [],
        [
            {"label": "A", "text": "3000"},
            {"label": "B", "text": "3300"},
            {"label": "C", "text": "3600"},
            {"label": "D", "text": "3900"}
        ]
    ),
    (
        "gate-2017-ae-ga-09", 9, "GA", "General Aptitude", 64, "MCQ", 2, 0.6666666666666666,
        "The number of 3-digit numbers such that the digit 1 is never to the immediate right of 2 is",
        [],
        [
            {"label": "A", "text": "781"},
            {"label": "B", "text": "791"},
            {"label": "C", "text": "881"},
            {"label": "D", "text": "891"}
        ]
    ),
    (
        "gate-2017-ae-ga-10", 10, "GA", "General Aptitude", 65, "MCQ", 2, 0.6666666666666666,
        "A contour line joins locations having the same height above the mean sea level. The following is a contour plot of a geographical region. Contour lines are shown at 25 m intervals in this plot.\n\nWhich of the following is the steepest path leaving from P?",
        [{"src": "figures/gate-2017-ae-ga-10-figure-1.png", "alt": "Contour plot of geographical region with marked points P, Q, R, S, T and scale"}],
        [
            {"label": "A", "text": "P to Q"},
            {"label": "B", "text": "P to R"},
            {"label": "C", "text": "P to S"},
            {"label": "D", "text": "P to T"}
        ]
    ),
    # AE 1-25 (1M)
    (
        "gate-2017-ae-ae-11", 11, "AE", "Aerospace Engineering", 1, "MCQ", 1, 0.3333333333333333,
        "Given the vectors $\\vec{v}_1 = \\hat{\\imath} + 3\\hat{\\jmath}$; $\\vec{v}_2 = 2\\hat{\\imath} - 4\\hat{\\jmath} + 3\\hat{k}$, the vector $\\vec{v}_3$ that is perpendicular to both $\\vec{v}_1$ and $\\vec{v}_2$ is given by:",
        [],
        [
            {"label": "A", "text": "$\\vec{v}_3 = \\vec{v}_1 - (\\vec{v}_1 \\cdot \\vec{v}_2)\\frac{\\vec{v}_2}{|\\vec{v}_2|}$"},
            {"label": "B", "text": "$\\vec{v}_3 = \\hat{k}$"},
            {"label": "C", "text": "$\\vec{v}_3 = \\vec{v}_2 - (\\vec{v}_1 \\cdot \\vec{v}_2)\\frac{\\vec{v}_1}{|\\vec{v}_1|}$"},
            {"label": "D", "text": "$\\vec{v}_3 = \\frac{\\vec{v}_1 \\times \\vec{v}_2}{|\\vec{v}_1 \\times \\vec{v}_2|}$"}
        ]
    ),
    (
        "gate-2017-ae-ae-12", 12, "AE", "Aerospace Engineering", 2, "NAT", 1, 0.0,
        "The value of the integral $I = \\int_C ((x-y)dx + x^2 dy)$, with C the boundary of the square $0 \\le x \\le 2; 0 \\le y \\le 2$, is ______",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-13", 13, "AE", "Aerospace Engineering", 3, "NAT", 1, 0.0,
        "Let $\\vec{v}(t)$ be a unit vector that is a function of the parameter $t$. Then $\\vec{v} \\cdot \\frac{d\\vec{v}}{dt} =$ ______",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-14", 14, "AE", "Aerospace Engineering", 4, "MCQ", 1, 0.3333333333333333,
        "The eigenvalues $\\lambda_n$ and eigenfunctions $u_n(x)$ of the Sturm-Liouville problem\n\n$$\\frac{d^2 y}{dx^2} + k^2\\lambda y = 0, \\quad 0 < x < 1; \\quad y(0) = 0, y(1) = 0$$\n\nare given by:",
        [],
        [
            {"label": "A", "text": "$\\lambda_n = n^2\\pi^2; \\quad u_n(x) = \\sin\\lambda_n x, \\quad n = 0, \\pm 1, \\pm 2, \\dots, \\infty$"},
            {"label": "B", "text": "$\\lambda_n = n^2\\pi^2/k^2; \\quad u_n(x) = \\sin kn\\pi x, \\quad n = 0, \\pm 1, \\pm 2, \\dots, \\infty$"},
            {"label": "C", "text": "$\\lambda_n = n^2\\pi^2/k^2; \\quad u_n(x) = \\sin n\\pi x, \\quad n = 0, \\pm 1, \\pm 2, \\dots, \\infty$"},
            {"label": "D", "text": "$\\lambda_n = n^2\\pi^2; \\quad u_n(x) = \\sin n\\pi x, \\quad n = 0, \\pm 1, \\pm 2, \\dots, \\infty$"}
        ]
    ),
    (
        "gate-2017-ae-ae-15", 15, "AE", "Aerospace Engineering", 5, "MCQ", 1, 0.3333333333333333,
        "3-point Gaussian integration formula is given by:\n\n$$\\int_{-1}^1 f(x)dx \\approx \\sum_{j=1}^3 A_j f(x_j) \\text{ with } x_1 = 0, x_2 = -x_3 = -\\sqrt{\\frac{3}{5}}; \\quad A_1 = \\frac{8}{9}, A_2 = A_3 = \\frac{5}{9}$$\n\nThis formula exactly integrates",
        [],
        [
            {"label": "A", "text": "$f(x) = 5 - x^7$"},
            {"label": "B", "text": "$f(x) = 2 + 3x + 6x^4$"},
            {"label": "C", "text": "$f(x) = 13 + 6x^3 + x^6$"},
            {"label": "D", "text": "$f(x) = e^{-x^2}$"}
        ]
    ),
    (
        "gate-2017-ae-ae-16", 16, "AE", "Aerospace Engineering", 6, "MCQ", 1, 0.3333333333333333,
        "Which one of the following statements is NOT true",
        [],
        [
            {"label": "A", "text": "The pitching moment of any airfoil at any angle of attack is always zero at the center of pressure"},
            {"label": "B", "text": "The pitching moment of any airfoil at any angle of attack is always zero at the aerodynamic center"},
            {"label": "C", "text": "The center of pressure and aerodynamic center coincide for a symmetric airfoil"},
            {"label": "D", "text": "The pitching moment about the aerodynamic center, for any airfoil, does not vary with angle of attack"}
        ]
    ),
    (
        "gate-2017-ae-ae-17", 17, "AE", "Aerospace Engineering", 7, "MCQ", 1, 0.3333333333333333,
        "Which one of the following statements is NOT true",
        [],
        [
            {"label": "A", "text": "Compared to a laminar boundary layer, a turbulent boundary layer is more desirable on a wing operating at large angle of attack"},
            {"label": "B", "text": "The skin friction drag for a turbulent boundary layer is larger than that for a laminar boundary layer"},
            {"label": "C", "text": "The location of transition from laminar to turbulent boundary layer depends only on the operating Reynolds number"},
            {"label": "D", "text": "A separated flow does not necessarily lead to a turbulent boundary layer"}
        ]
    ),
    (
        "gate-2017-ae-ae-18", 18, "AE", "Aerospace Engineering", 8, "NAT", 1, 0.0,
        "A De Laval nozzle is to be designed for an exit Mach number of 1.5. The reservoir conditions are given as $P_0=1\\text{ atm (gage)}$, $T_0=20^\\circ\\text{C}$, $\\gamma=1.4$. Assuming shock free flow in the nozzle, the exit absolute pressure (in atm) is ______ (in three decimal places)",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-19", 19, "AE", "Aerospace Engineering", 9, "MCQ", 1, 0.3333333333333333,
        "Consider a steady one dimensional flow of a perfect gas with heat transfer in a duct. The T-s diagram (shown below) shows both the static and the stagnation conditions at two locations, A and B, in the duct. $A_t$ and $B_t$ denote stagnation conditions for states A and B, respectively. It is known that $(\\Delta T)_A = (\\Delta T)_B$. $M_A$ and $M_B$ are the Mach numbers of the flow at locations A and B.\n\nWhich of the following statements is true about the flow.",
        [{"src": "figures/gate-2017-ae-ae-19-figure-1.png", "alt": "T-s diagram showing states A, At, B, Bt and temperature differences"}],
        [
            {"label": "A", "text": "Flow is subsonic and $M_A < M_B$."},
            {"label": "B", "text": "Flow is supersonic and $M_A > M_B$"},
            {"label": "C", "text": "Flow is subsonic and $M_A > M_B$"},
            {"label": "D", "text": "Flow is supersonic and $M_A < M_B$"}
        ]
    ),
    (
        "gate-2017-ae-ae-20", 20, "AE", "Aerospace Engineering", 10, "MCQ", 1, 0.3333333333333333,
        "To ensure only the longitudinal static stability (and not the condition for equilibrium) of a low speed aircraft, the aircraft components must be designed to satisfy which one of the following conditions:",
        [],
        [
            {"label": "A", "text": "$\\frac{\\partial C_m}{\\partial \\alpha} < 0$ and $C_{m0} > 0$"},
            {"label": "B", "text": "$\\frac{\\partial C_m}{\\partial \\alpha} < 0$"},
            {"label": "C", "text": "$\\frac{\\partial C_m}{\\partial C_L} < 0$ and $C_{m0} < 0$"},
            {"label": "D", "text": "$\\frac{\\partial C_m}{\\partial C_L} = 0.0$"}
        ]
    ),
    (
        "gate-2017-ae-ae-21", 21, "AE", "Aerospace Engineering", 11, "MCQ", 1, 0.3333333333333333,
        "Which of the following statement(s) is / are true about the shear centre of a cross-section:\nP: It is that point in the cross-section through which shear loads produce no twisting.\nQ: This point is also the centre of twist of sections subjected to pure torsion.\nR: The normal stress at this point is always zero.",
        [],
        [
            {"label": "A", "text": "P, Q and R"},
            {"label": "B", "text": "P only"},
            {"label": "C", "text": "P and Q only"},
            {"label": "D", "text": "P and R only"}
        ]
    ),
    (
        "gate-2017-ae-ae-22", 22, "AE", "Aerospace Engineering", 12, "MCQ", 1, 0.3333333333333333,
        "Let $\\bar{N}_m$ and $\\bar{N}_0$ be respectively the non-dimensional locations of the stick-fixed maneuver point and stick-fixed neutral point of a low speed conventional aircraft. These distances are measured with respect to the nose of the fuselage. The numerical value of $\\bar{N}_m - \\bar{N}_0$",
        [],
        [
            {"label": "A", "text": "will always be negative"},
            {"label": "B", "text": "will always be positive"},
            {"label": "C", "text": "will always be zero"},
            {"label": "D", "text": "can have any value depending on the location of the center of gravity of the aircraft"}
        ]
    ),
    (
        "gate-2017-ae-ae-23", 23, "AE", "Aerospace Engineering", 13, "MCQ", 1, 0.3333333333333333,
        "The phenomenon of rudder lock in conventional low speed aircraft is primarily due to",
        [],
        [
            {"label": "A", "text": "large value of directional derivative, $C_{n\\beta}$"},
            {"label": "B", "text": "the sidewash due to fuselage on the vertical stabilizer"},
            {"label": "C", "text": "the tendency of rudder to float rapidly at high angles of side-slip"},
            {"label": "D", "text": "the sidewash due to wing on the vertical stabilizer"}
        ]
    ),
    (
        "gate-2017-ae-ae-24", 24, "AE", "Aerospace Engineering", 14, "NAT", 1, 0.0,
        "The period of revolution of earth about the sun is 365.256 days, approximately. The semi-major axis of the earth’s orbit is close to $1.4953 \\times 10^{11}\\text{ m}$. The semi-major axis of the orbit of Mars is $2.2783 \\times 10^{11}\\text{ m}$. The period of revolution of Mars, about the sun, is ______ Earth days (in three decimal place)",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-25", 25, "AE", "Aerospace Engineering", 15, "MCQ", 1, 0.3333333333333333,
        "Consider a system consisting of certain amount of perfect gas enclosed in a cylinder fitted with a frictionless piston. This system can undergo following processes\n(i) Expansion with finite pressure difference with the surrounding.\n(ii) Compression with infinitesimal pressure difference with the surrounding.\n(iii) Heat transfer with finite temperature difference with the reservoir.\n(iv) Heat transfer with infinitesimal temperature difference with the reservoir.\n\nOut of these which processes are reversible?",
        [],
        [
            {"label": "A", "text": "(i) and (iii)"},
            {"label": "B", "text": "(i) and (iv)"},
            {"label": "C", "text": "(ii) and (iii)"},
            {"label": "D", "text": "(ii) and (iv)"}
        ]
    ),
    (
        "gate-2017-ae-ae-26", 26, "AE", "Aerospace Engineering", 16, "MCQ", 1, 0.3333333333333333,
        "Among the following engines, which one is expected to have the maximum Specific Impulse?",
        [],
        [
            {"label": "A", "text": "Cryogenic Rocket"},
            {"label": "B", "text": "Solid Propellant Rocket"},
            {"label": "C", "text": "Liquid Propellant Rocket"},
            {"label": "D", "text": "SCRAM Jet"}
        ]
    ),
    (
        "gate-2017-ae-ae-27", 27, "AE", "Aerospace Engineering", 17, "MCQ", 1, 0.3333333333333333,
        "The maximum gas flow rate that can be handled by a multistage axial compressor at a given rotational speed is dictated by",
        [],
        [
            {"label": "A", "text": "Compressor Surge"},
            {"label": "B", "text": "Rotating Stall"},
            {"label": "C", "text": "Choking"},
            {"label": "D", "text": "Optimum Design Pressure Ratio"}
        ]
    ),
    (
        "gate-2017-ae-ae-28", 28, "AE", "Aerospace Engineering", 18, "MCQ", 1, 0.3333333333333333,
        "For a turbine stage, which one of the following losses occurs due to the turning of the wall boundary layer through an angle due to curved surface?",
        [],
        [
            {"label": "A", "text": "Profile loss"},
            {"label": "B", "text": "Annulus loss"},
            {"label": "C", "text": "Tip clearance loss"},
            {"label": "D", "text": "Secondary flow loss"}
        ]
    ),
    (
        "gate-2017-ae-ae-29", 29, "AE", "Aerospace Engineering", 19, "MCQ", 1, 0.3333333333333333,
        "In the vane-less space between the impeller and the diffuser vanes in a Centrifugal Compressor, the angular momentum varies in the following manner in the radial direction",
        [],
        [
            {"label": "A", "text": "Increases"},
            {"label": "B", "text": "Remains constant"},
            {"label": "C", "text": "Decreases"},
            {"label": "D", "text": "First increases and then decreases"}
        ]
    ),
    (
        "gate-2017-ae-ae-30", 30, "AE", "Aerospace Engineering", 20, "MCQ", 1, 0.3333333333333333,
        "Which of the following statements about the neutral axis of a beam with unsymmetrical cross section is true:",
        [],
        [
            {"label": "A", "text": "The product of second moment of area about the neutral axis is always zero."},
            {"label": "B", "text": "The normal stress along the neutral axis is always zero."},
            {"label": "C", "text": "The shear stress along the neutral axis is always zero."},
            {"label": "D", "text": "The product of second moment of area about the neutral axis and the normal stress about the neutral axis are always zero."}
        ]
    ),
    (
        "gate-2017-ae-ae-31", 31, "AE", "Aerospace Engineering", 21, "MCQ", 1, 0.3333333333333333,
        "Assuming that the aircraft is flying straight, the top spar cap / flange of a wing is most likely to fail in:",
        [{"src": "figures/gate-2017-ae-ae-31-figure-1.png", "alt": "Airfoil cross section showing top spar cap / flange"}],
        [
            {"label": "A", "text": "Yielding"},
            {"label": "B", "text": "Buckling"},
            {"label": "C", "text": "Crushing"},
            {"label": "D", "text": "Creep"}
        ]
    ),
    (
        "gate-2017-ae-ae-32", 32, "AE", "Aerospace Engineering", 22, "NAT", 1, 0.0,
        "A 2-DOF undamped spring-mass system with two masses and two springs has natural frequencies $\\omega_1 = 0.79\\text{ rad/s}$ and $\\omega_2 = 1.538\\text{ rad/s}$. The mode shapes for the system are given by $\\phi_1 = [0.732\\ 1]^T$ and $\\phi_2 = [-2.73\\ 1]^T$. If the first mass is displaced by 1 cm, the minimum displacement in cms to be given to the second mass to make the system vibrate in first mode alone is = ______ (in three decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-33", 33, "AE", "Aerospace Engineering", 23, "MCQ", 1, 0.3333333333333333,
        "An aircraft landing gear can be idealized as a single degree of freedom spring-mass-damper system. The desirable damping characteristics of such a system is:",
        [],
        [
            {"label": "A", "text": "Under damped"},
            {"label": "B", "text": "Over damped"},
            {"label": "C", "text": "Critically damped"},
            {"label": "D", "text": "Undamped"}
        ]
    ),
    (
        "gate-2017-ae-ae-34", 34, "AE", "Aerospace Engineering", 24, "NAT", 1, 0.0,
        "A single degree of freedom spring-mass system of natural frequency 5 Hz is modified in the following manners:\nCase 1: Viscous damping with damping ratio $\\zeta = 0.2$ is introduced in parallel to the spring.\nCase 2: The original undamped spring-mass system is moved to a surface with coefficient of friction, $\\mu = 0.01$.\nThe ratio of the damped natural frequency for the cases 1 and 2 is given by ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-35", 35, "AE", "Aerospace Engineering", 25, "MCQ", 1, 0.3333333333333333,
        "Which of the following statements about the compatibility equations are true:\nP. Strain compatibility equations must be satisfied in the solution of three-dimensional problems in elasticity.\nQ. Six strains are defined in terms of three displacement functions and can have arbitrary values.\nR. Compatibility equations are an expression of the continuity of displacements.",
        [],
        [
            {"label": "A", "text": "P and Q"},
            {"label": "B", "text": "Q and R"},
            {"label": "C", "text": "P and R"},
            {"label": "D", "text": "P, Q and R"}
        ]
    ),
    # AE 26-55 (2M)
    (
        "gate-2017-ae-ae-36", 36, "AE", "Aerospace Engineering", 26, "MCQ", 2, 0.6666666666666666,
        "Matrix $[A] = \\begin{bmatrix} 2 & 0 & 2 \\\\ 3 & 2 & 7 \\\\ 3 & 1 & 5 \\end{bmatrix}$ and vector $\\{b\\} = \\begin{pmatrix} 4 \\\\ 4 \\\\ 5 \\end{pmatrix}$ are given. If vector $\\{x\\}$ is the solution to the system of equations $[A]\\{x\\} = \\{b\\}$, which of the following is true for $\\{x\\}$:",
        [],
        [
            {"label": "A", "text": "Solution does not exist"},
            {"label": "B", "text": "Infinite solutions exist"},
            {"label": "C", "text": "Unique solution exists"},
            {"label": "D", "text": "Five possible solutions exist"}
        ]
    ),
    (
        "gate-2017-ae-ae-37", 37, "AE", "Aerospace Engineering", 27, "MCQ", 2, 0.6666666666666666,
        "Let matrix $[A] = \\begin{bmatrix} 2 & -6 \\\\ 0 & 2 \\end{bmatrix}$. Then for any non-trivial vector $\\{x\\} = \\begin{pmatrix} x_1 \\\\ x_2 \\end{pmatrix}$, which of the following is true for the value of $K = \\{x\\}^T [A]\\{x\\}$:",
        [],
        [
            {"label": "A", "text": "K is always less than zero"},
            {"label": "B", "text": "K is always greater than zero"},
            {"label": "C", "text": "K is non-negative"},
            {"label": "D", "text": "K can be anything"}
        ]
    ),
    (
        "gate-2017-ae-ae-38", 38, "AE", "Aerospace Engineering", 28, "MCQ", 2, 0.6666666666666666,
        "Consider the initial value problem:\n\n$$\\frac{d^2 y}{dt^2} + 4\\frac{dy}{dt} + 6y = f(t); \\quad y(0) = 2, \\left(\\frac{dy}{dt}\\right)_{t=0} = 1$$\n\nIf $Y(s) = \\int_0^\\infty y(t)e^{-st}dt$ and $F(s) = \\int_0^\\infty f(t)e^{-st}dt$ are the Laplace transforms of $y(t)$ and $f(t)$ respectively, then $Y(s)$ is given by:",
        [],
        [
            {"label": "A", "text": "$\\frac{F(s)}{(s^2 + 4s + 6)}$"},
            {"label": "B", "text": "$\\frac{F(s)+2s+9}{(s^2+4s+6)}$"},
            {"label": "C", "text": "$\\frac{F(s)}{(-s^2+4s+6)}$"},
            {"label": "D", "text": "$\\frac{F(s)-2s+9}{(s^2+4s+6)}$"}
        ]
    ),
    (
        "gate-2017-ae-ae-39", 39, "AE", "Aerospace Engineering", 29, "NAT", 2, 0.0,
        "Let $u(x,t)$ denote the displacement of a point on a rod. The displacement satisfies the following equation of motion:\n\n$$\\frac{\\partial^2 u}{\\partial t^2} - 25 \\frac{\\partial^2 u}{\\partial x^2} = 0, \\quad 0 < x < 1$$\n\nwith $u(x,0) = 0.01\\sin(10\\pi x)$, $\\frac{\\partial u}{\\partial t}(x,0) = 0$; $u(0,t) = 0, u(1,t) = 0$. The value of $u(0.25, 1)$ is ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-40", 40, "AE", "Aerospace Engineering", 30, "MCQ", 2, 0.6666666666666666,
        "The equation $x^2 \\frac{d^2 y}{dx^2} + 5x \\frac{dy}{dx} + 4y = 0$ has a solution $y(x)$ that is:",
        [],
        [
            {"label": "A", "text": "A polynomial in $x$"},
            {"label": "B", "text": "Finite series in terms of non-integer fractional powers of $x$"},
            {"label": "C", "text": "Consists of negative integer powers of $x$ and logarithmic function of $x$"},
            {"label": "D", "text": "Consists of exponential functions of $x$."}
        ]
    ),
    (
        "gate-2017-ae-ae-41", 41, "AE", "Aerospace Engineering", 31, "NAT", 2, 0.0,
        "Consider a straight wing with rectangular planform of aspect ratio 10 and with a NACA 0012 airfoil. The span effectiveness factor for this wing is 0.95. Assume the flow to be incompressible and governed by thin airfoil theory. The lift coefficient of this wing, at an angle of attack of 6 deg, is ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-42", 42, "AE", "Aerospace Engineering", 32, "NAT", 2, 0.0,
        "Consider an incompressible flow over a flat plate with the following approximation to the velocity profile:\n\n$$\\frac{u(y)}{U} = \\begin{cases} \\frac{y}{\\delta} & \\text{for } y \\le \\delta \\\\ 1 & \\text{for } y > \\delta \\end{cases}$$\n\nwhere $\\delta$ is the boundary layer thickness and U the free-stream speed. The normalized momentum thickness $(\\theta/\\delta)$ for this profile is ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-43", 43, "AE", "Aerospace Engineering", 33, "NAT", 2, 0.0,
        "An idealized velocity field is given by $\\vec{V} = 4tx\\hat{\\imath} - 2t^2 y\\hat{\\jmath} + 4xz\\hat{k}$. At point (-1,1,0) and at t = 1, the magnitude of the material acceleration vector of the fluid element is ______",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-44", 44, "AE", "Aerospace Engineering", 34, "NAT", 2, 0.0,
        "A trace from the schlieren photograph of the flow around a corner reveals the edges of the expansion fan as shown below. The leading and trailing edges of the expansion fan make the angles as shown. Assuming $\\gamma = 1.4$, the angle of the expansion fan (in degrees) is ______ (in two decimal places)\n\nPrandtl Meyer function is given by\n$$\\nu(M) = \\sqrt{\\frac{\\gamma+1}{\\gamma-1}} \\tan^{-1}\\sqrt{\\frac{\\gamma-1}{\\gamma+1}(M^2-1)} - \\tan^{-1}\\sqrt{(M^2-1)}$$",
        [{"src": "figures/gate-2017-ae-ae-44-figure-1.png", "alt": "Expansion fan geometry around corner"}],
        []
    ),
    (
        "gate-2017-ae-ae-45", 45, "AE", "Aerospace Engineering", 35, "NAT", 2, 0.0,
        "A strong normal shock wave, with a pressure ratio of 29 across it, is travelling into stationary air ($\\gamma=1.4$) at $\\text{T} = 280\\text{ K}$ in a straight duct (see figure). The magnitude of the velocity of the air induced behind the shock wave is ______ m/s. (round to nearest integer)\n\n(Gas constant = $287\\text{ J/kg}\\cdot\\text{K}$; Shock wave relations:\nPressure ratio: $\\frac{p_2}{p_1} = 1 + \\frac{2\\gamma}{\\gamma+1}(M^2-1)$; Density ratio: $\\frac{\\rho_2}{\\rho_1} = \\frac{(\\gamma+1)M^2}{(\\gamma-1)M^2+2}$)",
        [{"src": "figures/gate-2017-ae-ae-45-figure-1.png", "alt": "Shock wave propagation in straight duct"}],
        []
    ),
    (
        "gate-2017-ae-ae-46", 46, "AE", "Aerospace Engineering", 36, "NAT", 2, 0.0,
        "In the figure below, water exits from a nozzle into atmospheric pressure of 101 kPa. If the exit velocity is $V_2 = 8\\text{ m/s}$ and friction is neglected, the magnitude of the axial force on the flange at location 1 required to keep the nozzle attached to the pipe is ______ N (round to nearest integer).",
        [{"src": "figures/gate-2017-ae-ae-46-figure-1.png", "alt": "Pipe, nozzle and flange assembly"}],
        []
    ),
    (
        "gate-2017-ae-ae-47", 47, "AE", "Aerospace Engineering", 37, "NAT", 2, 0.0,
        "A football, meant to be thrown at 100 km/h in sea level air ($\\rho = 1.22\\text{ kg/m}^3$, $\\mu = 1.78 \\times 10^{-5}\\text{ N-s/m}^2$), is to be tested using a one-quarter scale model in a water tunnel ($\\rho = 1000\\text{ kg/m}^3$, $\\mu = 10^{-3}\\text{ N-s/m}^2$). For dynamic similarity, the ratio of the model force to the prototype force is ______ (round to nearest integer).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-48", 48, "AE", "Aerospace Engineering", 38, "NAT", 2, 0.0,
        "An aircraft model was tested in a low speed wind-tunnel (Reynolds number = $2\\times 10^6$ based on wing mean chord). The variation of pitching moment coefficient ($C_m$) with angle of attack ($\\alpha$) for two elevator deflections ($\\delta_e$) as recorded during this test is presented below.\n\nBased on the result presented in the figure above, the value of elevator control power ($C_{m_{\\delta_e}}$) in per radian will be ______ (in three decimal place).",
        [{"src": "figures/gate-2017-ae-ae-48-figure-1.png", "alt": "Cm vs alpha graph for delta_e = 0 deg and -10 deg"}],
        []
    ),
    (
        "gate-2017-ae-ae-49", 49, "AE", "Aerospace Engineering", 39, "MCQ", 2, 0.6666666666666666,
        "A pilot was flying a single engine propeller aircraft and maintaining a steady level flight at a lift coefficient, $C_L=0.5$ at an altitude of 500 m. Due to some emergency, at the same altitude (500 m), the pilot had to fully deploy the landing gear. If the pilot wants to maintain steady level flight at the same $C_L=0.5$ and at the same altitude, which of the following control actions should the pilot undertake:",
        [],
        [
            {"label": "A", "text": "move the elevator up, and decrease the throttle"},
            {"label": "B", "text": "move the elevator up, and increase the throttle"},
            {"label": "C", "text": "move the elevator down, and decrease the throttle"},
            {"label": "D", "text": "move the elevator down, and increase the throttle"}
        ]
    ),
    (
        "gate-2017-ae-ae-50", 50, "AE", "Aerospace Engineering", 40, "NAT", 2, 0.0,
        "A conventional low speed aircraft had the following aerodynamic characteristics:\n$C_{D0}=0.020$, $e=1.0$ (Oswald efficiency).\nThe aircraft was flown to maintain a steady level flight and for minimum thrust required, at a lift coefficient of $C_L=0.8$. The numerical value of the aspect ratio of the wing is ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-51", 51, "AE", "Aerospace Engineering", 41, "NAT", 2, 0.0,
        "A batch of aluminium alloy yields in uniaxial tension at the stress of $330\\text{ MN/m}^2$. If this material is subjected to the following state of stress: $\\sigma_x = 140\\text{ MN/m}^2$, $\\sigma_y = -70\\text{ MN/m}^2$, $\\sigma_z = 0$, $\\tau_{xy} = x\\text{ MN/m}^2$, $\\tau_{yz} = 0$ and $\\tau_{zx} = 0$. The value of $x$ that would result in yielding according to the Von Mises failure criterion is ______ (in three decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-52", 52, "AE", "Aerospace Engineering", 42, "MCQ", 2, 0.6666666666666666,
        "The roots obtained by solving longitudinal characteristic equations of motion for a statically stable aircraft are given below:\n$$\\lambda_{1,2} = -0.02 \\pm 0.30i, \\quad \\lambda_{3,4} = -2.00 \\pm 2.50i, \\quad \\text{where } i = \\sqrt{-1}$$\nThe undamped short-period longitudinal natural frequency (radians/sec) and damping ratio, in that order, are close to",
        [],
        [
            {"label": "A", "text": "3.40, 0.73"},
            {"label": "B", "text": "3.36, 0.65"},
            {"label": "C", "text": "3.83, 0.56"},
            {"label": "D", "text": "3.20, 0.63"}
        ]
    ),
    (
        "gate-2017-ae-ae-53", 53, "AE", "Aerospace Engineering", 43, "NAT", 2, 0.0,
        "An aircraft is to be designed to ensure that it has enough excess power to achieve steady climb at flight path angle, $\\gamma=10\\text{ degrees}$, maintaining $\\frac{C_L}{C_D}=10.0$. The numerical value of the thrust to weight ratio of the complete aircraft to meet the above requirement under standard atmospheric condition will be ______ (in three decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-54", 54, "AE", "Aerospace Engineering", 44, "NAT", 2, 0.0,
        "A conventional aircraft was analyzed to estimate the contribution of wing towards $C_{m0}$ ($C_m$ at $\\alpha=0$) of the whole aircraft. The wing was installed with zero setting angle along the fuselage reference line. Further, the wing was laid such that $\\bar{X}_{ac,w}=0.3$, and $\\bar{X}_{cg,aircraft}=0.4$. $\\bar{X}_{ac,w}$ and $\\bar{X}_{cg,aircraft}$ are the non-dimensional distances, from the leading edge of the wing, of the aerodynamic center of the wing and center of gravity of the aircraft respectively. The wing had the following aerodynamic characteristics:\n$C_{L0}=0.20$, and $C_{mac,wing}=-0.02$.\nThe numerical value of $C_{m0,w}$ (contribution of the wing to $C_{m0}$) about the CG of the aircraft is ______ (in two decimal places).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-55", 55, "AE", "Aerospace Engineering", 45, "MCQ", 2, 0.6666666666666666,
        "In a combustor, gaseous Octane ($C_8H_{18}$) and air are to be burned in stoichiometric proportions. If the required flowrate of air is 1 kg/s, what should be the corresponding flow rate of Octane?",
        [],
        [
            {"label": "A", "text": "0.066 kg/s"},
            {"label": "B", "text": "15.15 kg/s"},
            {"label": "C", "text": "0.16 kg/s"},
            {"label": "D", "text": "6.25 kg/s"}
        ]
    ),
    (
        "gate-2017-ae-ae-56", 56, "AE", "Aerospace Engineering", 46, "NAT", 2, 0.0,
        "The given diagram represents the velocity triangles at the leading edge (1) and trailing edge (2) at the mean radius of a single stage axial compressor rotor. The stage efficiency of the compressor is 0.8. The stagnation temperature of air entering the stage is 298 K and the specific heat at constant pressure for air is 1.005 kJ/kgK. The ratio of specific heats for air is 1.4. Considering actual work in the rotor is equal to the ideal work, the pressure ratio for the stage is equal to ______ (in two decimal points).",
        [{"src": "figures/gate-2017-ae-ae-56-figure-1.png", "alt": "Velocity triangles at leading edge (1) and trailing edge (2) of axial compressor rotor"}],
        []
    ),
    (
        "gate-2017-ae-ae-57", 57, "AE", "Aerospace Engineering", 47, "NAT", 2, 0.0,
        "An aircraft with a turbojet engine, having an inlet area of $1\\text{ m}^2$, is flying at 270 m/s at an altitude where the atmospheric pressure is equal to 0.9 bar and the ambient temperature is equal to 290 K. The stagnation pressure and temperature at the exit of the turbine are equal to 1.6 bar and 774 K respectively. The specific heat at constant pressure of the burned gases is equal to 1.147 kJ/kgK and the ratio of specific heats is equal to 1.33. Considering ideal expansion in the nozzle with no losses, the specific thrust produced by the engine is ______ Ns/kg (in one decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-58", 58, "AE", "Aerospace Engineering", 48, "NAT", 2, 0.0,
        "Air, at 450 K stagnation temperature and at a rate of 50 kg/s, enters the combustor of a turbofan engine and is burned with 1 kg/s of Aviation Kerosene (Heating value 44 MJ/kg). The specific heat at constant pressure for the incoming air and the burned products are 1.005 kJ/kgK and 1.147 kJ/kgK respectively. Considering 100% burner efficiency, the stagnation temperature at the exit of the combustor is equal to ______ K. (in one decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-59", 59, "AE", "Aerospace Engineering", 49, "NAT", 2, 0.0,
        "A single stage chemical rocket, having an initial mass of 10,000 kg and specific impulse of 450 s, is launched from the surface of the earth and has to reach the escape velocity (11 km/s) at burn out. Consider $g_e = 9.8\\text{ m/s}^2$. If the atmospheric drag and the effect of gravity are to be neglected, the mass of propellant to be carried by the rocket is equal to ______ kg (in one decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-60", 60, "AE", "Aerospace Engineering", 50, "NAT", 2, 0.0,
        "A centrifugal compressor requires 1800 kW of power to compress 10 kg/s of air. Consider the whirl velocity component is equal to the impeller speed (ie., no slip) and no losses in the impeller. If the impeller has to rotate at 1900 rad/s, the diameter of the impeller is to be ______ m (in two decimal place).",
        [],
        []
    ),
    (
        "gate-2017-ae-ae-61", 61, "AE", "Aerospace Engineering", 51, "NAT", 2, 0.0,
        "An aircraft wing is idealized as a cantilever beam of constant width and length $l$ with a tip mass of weight $\\mathbf{W}$ (Newtons) and has a uniformly distributed loading of $\\mathbf{q_0}$ (Newtons/m) as shown in the figure. Flexural rigidity = $EI$ and $\\mathbf{q_0} l = 10\\ \\mathbf{W}$.\n\nThe upward deflection of the tip of the aircraft wing under the given loading can be expressed as:\n$$\\delta = k\\frac{W l^3}{EI}$$\nThe value of $k$ is ______ (in three decimal places).",
        [{"src": "figures/gate-2017-ae-ae-61-figure-1.png", "alt": "Idealized cantilever beam with tip mass and uniformly distributed upward loading"}],
        []
    ),
    (
        "gate-2017-ae-ae-62", 62, "AE", "Aerospace Engineering", 52, "NAT", 2, 0.0,
        "For the state of plane stress shown in the figure, the minimum principal stress is $-7\\text{ MN/m}^2$. The normal stress $\\sigma_x$ in $\\text{MN/m}^2$ is equal to ______ (round to nearest integer).",
        [{"src": "figures/gate-2017-ae-ae-62-figure-1.png", "alt": "State of plane stress element with normal and shear stresses"}],
        []
    ),
    (
        "gate-2017-ae-ae-63", 63, "AE", "Aerospace Engineering", 53, "NAT", 2, 0.0,
        "The maximum normal stress in $\\text{MN/m}^2$ for the thin walled beam of square cross section of outer dimension $120\\text{ mm} \\times 120\\text{ mm}$ and wall thickness $1\\text{ mm}$ under the action of moment $M_0 = 96\\text{ Nm}$ as shown in the figure is ______ (in three decimal places).",
        [{"src": "figures/gate-2017-ae-ae-63-figure-1.png", "alt": "Square cross section of thin-walled tube with inclined moment Mo at 45 deg"}],
        []
    ),
    (
        "gate-2017-ae-ae-64", 64, "AE", "Aerospace Engineering", 54, "NAT", 2, 0.0,
        "The idealized cross section of a thin-walled wing box structure shown in the figure is subjected to an anticlockwise torque of $10\\text{ kNm}$. The corresponding shear-flow distribution under this loading condition is shown in the figure. The area of each cell is $A_1 = 300 \\times 10^3\\text{ mm}^2$ and $A_2 = 250 \\times 10^3\\text{ mm}^2$. The ratio of the unknowns $\\frac{x}{y}$ is given by ______ (in three decimal places).",
        [{"src": "figures/gate-2017-ae-ae-64-figure-1.png", "alt": "Two-cell thin-walled wing box with shear flows and torque"}],
        []
    ),
    (
        "gate-2017-ae-ae-65", 65, "AE", "Aerospace Engineering", 55, "NAT", 2, 0.0,
        "The natural frequency of the system suspended by two identical springs of stiffness $k$ as shown in the figure is given by $\\omega_n = a\\sqrt{\\frac{k}{m}}$ for small displacement. Both the springs make an angle of $45^\\circ$ with the horizontal. The value of $a$ is ______ (in two decimal places).",
        [{"src": "figures/gate-2017-ae-ae-65-figure-1.png", "alt": "Spring-mass system suspended symmetrically by two springs at 45 deg"}],
        []
    )
]

questions = []
for q_id, num, sec, subj, sqn, qtype, marks, neg_marks, q_text, raw_figs, opts in q_defs:
    k_row = key_lookup[(sec, sqn)]
    raw_key = k_row['rawKey']
    pdf_page = get_pdf_page(sec, sqn)
    key_page = get_key_page(sec, sqn)
    
    # Process acceptedAnswers & answer field
    if qtype == 'MCQ':
        if ' or ' in raw_key.lower():
            accepted = [x.strip() for x in raw_key.upper().split('OR')]
            ans_val = accepted
        else:
            accepted = [raw_key.strip()]
            ans_val = raw_key.strip()
    elif qtype == 'NAT':
        # parse range from rawKey e.g. "11.9 to 12.1"
        parts = [float(x.strip()) for x in raw_key.split('to')]
        accepted = [parts]
        ans_val = parts

    # Process figures
    figs = []
    content_blocks = [{"type": "text", "text": q_text}]
    for rf in raw_figs:
        fig_asset = {
            "src": rf["src"],
            "alt": rf["alt"],
            "page": pdf_page,
            "source": {
                "file": "internal/ae/AE2017.pdf",
                "sha256": pdf_sha256,
                "page": pdf_page,
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            },
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-07"
        }
        figs.append(fig_asset)
        content_blocks.append({"type": "figure", "asset": fig_asset})

    q_obj = {
        "id": q_id,
        "exam": "GATE",
        "year": 2017,
        "paper": "AE",
        "number": num,
        "section": sec,
        "subject": subj,
        "type": qtype,
        "marks": marks,
        "question": q_text,
        "content": content_blocks,
        "figures": figs,
        "groupId": None,
        "source": {
            "file": "internal/ae/AE2017.pdf",
            "sha256": pdf_sha256,
            "pages": [
                {
                    "page": pdf_page,
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
            "url": "http://gate.iitg.ac.in/",
            "paper": "AE",
            "questionNumber": sqn,
            "section": sec,
            "page": key_page,
            "sha256": key_pdf_sha256,
            "verifiedOn": "2026-10-07"
        },
        "answer": ans_val,
        "negativeMarks": neg_marks,
        "markingRule": "gate-2017-official",
        "hasFigure": len(figs) > 0,
        "options": opts,
        "acceptedAnswers": accepted
    }
    questions.append(q_obj)

# Calculate type counts
mcq_count = sum(1 for q in questions if q['type'] == 'MCQ')
msq_count = sum(1 for q in questions if q['type'] == 'MSQ')
nat_count = sum(1 for q in questions if q['type'] == 'NAT')
fig_count = sum(len(q['figures']) for q in questions)

paper_json = {
    "schemaVersion": 1,
    "id": "gate-2017-ae",
    "exam": "GATE",
    "year": 2017,
    "paper": "AE",
    "title": "GATE Aerospace Engineering 2017",
    "durationMinutes": 180,
    "totalMarks": 100,
    "totalQuestions": 65,
    "sectionOrder": ["GA", "AE"],
    "sections": [
        {
            "id": "GA",
            "title": "General Aptitude",
            "questionIds": [q['id'] for q in questions if q['section'] == 'GA'],
            "totalMarks": sum(q['marks'] for q in questions if q['section'] == 'GA')
        },
        {
            "id": "AE",
            "title": "Aerospace Engineering",
            "questionIds": [q['id'] for q in questions if q['section'] == 'AE'],
            "totalMarks": sum(q['marks'] for q in questions if q['section'] == 'AE')
        }
    ],
    "questionOrder": [q['id'] for q in questions],
    "questionRefs": [
        {
            "id": q['id'],
            "number": q['number'],
            "section": q['section'],
            "marks": q['marks'],
            "type": q['type']
        }
        for q in questions
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
        "MCQ": mcq_count,
        "MSQ": msq_count,
        "NAT": nat_count
    },
    "source": {
        "file": "internal/ae/AE2017.pdf",
        "sha256": pdf_sha256,
        "pageCount": 23
    },
    "ingestionStatus": "complete",
    "verificationStatus": "source-verified",
    "verifiedOn": "2026-10-07",
    "questions": questions
}

os.makedirs('data/ae', exist_ok=True)
with open('data/ae/2017.json', 'w', encoding='utf-8') as f:
    json.dump(paper_json, f, indent=2, ensure_ascii=False)

print(f"Generated data/ae/2017.json with {len(questions)} questions (MCQ: {mcq_count}, MSQ: {msq_count}, NAT: {nat_count}, Figures: {fig_count}).")

# Update manifest.json
manifest_path = 'data/ae/manifest.json'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# Update the 2017 record in manifest['years']
for row in manifest.get('years', []):
    if row.get('year') == 2017:
        row['sourcePdf'] = "internal/ae/AE2017.pdf"
        row['ingestionStatus'] = "complete"
        row['verificationStatus'] = "source-verified"
        row['path'] = "data/ae/2017.json"
        row['questionCount'] = 65
        row['newQuestionCount'] = 65
        row['reusedGAQuestionCount'] = 0
        row['totalMarks'] = 100
        row['sections'] = [
            {
                "id": "GA",
                "title": "General Aptitude",
                "questionIds": [q['id'] for q in questions if q['section'] == 'GA'],
                "totalMarks": 15
            },
            {
                "id": "AE",
                "title": "Aerospace Engineering",
                "questionIds": [q['id'] for q in questions if q['section'] == 'AE'],
                "totalMarks": 85
            }
        ]
        row['questionTypeCounts'] = {
            "MCQ": mcq_count,
            "MSQ": msq_count,
            "NAT": nat_count
        }
        row['answerAvailability'] = {
            "officialKey": 65,
            "gradedAnswers": 65,
            "marksToAll": 0,
            "unavailable": 0
        }
        row['figureAssetCount'] = fig_count
        row['newFigureAssetCount'] = fig_count
        row['reusedFigureAssetCount'] = 0
        row['optionFigureCount'] = 0
        row['structuredTableCount'] = 0
        row['questionGroupCount'] = 0
        row['verifiedOn'] = "2026-10-07"
        break

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("Updated data/ae/manifest.json successfully.")
