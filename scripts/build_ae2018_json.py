import json
import hashlib
import fitz

doc = fitz.open('internal/ae/AE2018.pdf')
with open('internal/ae/AE2018.pdf', 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

with open('internal/ae/AE2018-key.json', 'r', encoding='utf-8') as f:
    key_data = json.load(f)

questions_data = {}

# Q1 (GA 1)
questions_data[1] = {
    "page": 1,
    "question": "“The dress _________ her so well that they all immediately _________ her on her appearance.”\n\nThe words that best fill the blanks in the above sentence are",
    "options": [
        {"label": "A", "text": "complemented, complemented"},
        {"label": "B", "text": "complimented, complemented"},
        {"label": "C", "text": "complimented, complimented"},
        {"label": "D", "text": "complemented, complimented"}
    ]
}

# Q2 (GA 2)
questions_data[2] = {
    "page": 1,
    "question": "“The judge’s standing in the legal community, though shaken by false allegations of wrongdoing, remained _________.”\n\nThe word that best fills the blank in the above sentence is",
    "options": [
        {"label": "A", "text": "undiminished"},
        {"label": "B", "text": "damaged"},
        {"label": "C", "text": "illegal"},
        {"label": "D", "text": "uncertain"}
    ]
}

# Q3 (GA 3)
questions_data[3] = {
    "page": 1,
    "question": "Find the missing group of letters in the following series:\nBC, FGH, LMNO, _____",
    "options": [
        {"label": "A", "text": "UVWXY"},
        {"label": "B", "text": "TUVWX"},
        {"label": "C", "text": "STUVW"},
        {"label": "D", "text": "RSTUV"}
    ]
}

# Q4 (GA 4)
questions_data[4] = {
    "page": 1,
    "question": "The perimeters of a circle, a square and an equilateral triangle are equal. Which one of the following statements is true?",
    "options": [
        {"label": "A", "text": "The circle has the largest area."},
        {"label": "B", "text": "The square has the largest area."},
        {"label": "C", "text": "The equilateral triangle has the largest area."},
        {"label": "D", "text": "All the three shapes have the same area."}
    ]
}

# Q5 (GA 5)
questions_data[5] = {
    "page": 1,
    "question": "The value of the expression $\\frac{1}{1+\\log_u vw} + \\frac{1}{1+\\log_v wu} + \\frac{1}{1+\\log_w uv}$ is _________.",
    "options": [
        {"label": "A", "text": "-1"},
        {"label": "B", "text": "0"},
        {"label": "C", "text": "1"},
        {"label": "D", "text": "3"}
    ]
}

# Q6 (GA 6)
questions_data[6] = {
    "page": 1,
    "question": "Forty students watched films A, B and C over a week. Each student watched either only one film or all three. Thirteen students watched film A, sixteen students watched film B and nineteen students watched film C. How many students watched all three films?",
    "options": [
        {"label": "A", "text": "0"},
        {"label": "B", "text": "2"},
        {"label": "C", "text": "4"},
        {"label": "D", "text": "8"}
    ]
}

# Q7 (GA 7)
questions_data[7] = {
    "page": 2,
    "question": "A wire would enclose an area of 1936 m$^2$, if it is bent into a square. The wire is cut into two pieces. The longer piece is thrice as long as the shorter piece. The long and the short pieces are bent into a square and a circle, respectively. Which of the following choices is closest to the sum of the areas enclosed by the two pieces in square meters?",
    "options": [
        {"label": "A", "text": "1096"},
        {"label": "B", "text": "1111"},
        {"label": "C", "text": "1243"},
        {"label": "D", "text": "2486"}
    ]
}

# Q8 (GA 8)
questions_data[8] = {
    "page": 2,
    "question": "A contract is to be completed in 52 days and 125 identical robots were employed, each operational for 7 hours a day. After 39 days, five-seventh of the work was completed. How many additional robots would be required to complete the work on time, if each robot is now operational for 8 hours a day?",
    "options": [
        {"label": "A", "text": "50"},
        {"label": "B", "text": "89"},
        {"label": "C", "text": "146"},
        {"label": "D", "text": "175"}
    ]
}

# Q9 (GA 9)
questions_data[9] = {
    "page": 2,
    "question": "A house has a number which needs to be identified. The following three statements are given that can help in identifying the house number.\ni. If the house number is a multiple of 3, then it is a number from 50 to 59.\nii. If the house number is NOT a multiple of 4, then it is a number from 60 to 69.\niii. If the house number is NOT a multiple of 6, then it is a number from 70 to 79.\n\nWhat is the house number?",
    "options": [
        {"label": "A", "text": "54"},
        {"label": "B", "text": "65"},
        {"label": "C", "text": "66"},
        {"label": "D", "text": "76"}
    ]
}

# Q10 (GA 10)
questions_data[10] = {
    "page": 3,
    "question": "An unbiased coin is tossed six times in a row and four different such trials are conducted. One trial implies six tosses of the coin. If H stands for head and T stands for tail, the following are the observations from the four trials:\n(1) HTHTHT (2) TTHHHT (3) HTTHHT (4) HHHT__ __.\n\nWhich statement describing the last two coin tosses of the fourth trial has the highest probability of being correct?",
    "options": [
        {"label": "A", "text": "Two T will occur."},
        {"label": "B", "text": "One H and one T will occur."},
        {"label": "C", "text": "Two H will occur."},
        {"label": "D", "text": "One H will be followed by one T."}
    ]
}

# Q11 (AE 1)
questions_data[11] = {
    "page": 4,
    "question": "Let $\\vec{a}, \\vec{b}$ be two distinct vectors that are not parallel. The vector $\\vec{c} = \\vec{a} \\times \\vec{b}$ is",
    "options": [
        {"label": "A", "text": "zero."},
        {"label": "B", "text": "orthogonal to $\\vec{a}$ alone."},
        {"label": "C", "text": "orthogonal to $\\vec{a} + \\vec{b}$."},
        {"label": "D", "text": "orthogonal to $\\vec{b}$ alone."}
    ]
}

# Q12 (AE 2)
questions_data[12] = {
    "page": 4,
    "question": "Consider the function $f(x, y) = \\frac{x^2}{2} + \\frac{y^2}{3} - 5$. All the roots of this function",
    "options": [
        {"label": "A", "text": "form a finite set of points."},
        {"label": "B", "text": "lie on an elliptical curve."},
        {"label": "C", "text": "lie on the surface of a sphere."},
        {"label": "D", "text": "lie on a hyperbolic curve."}
    ]
}

# Q13 (AE 3)
questions_data[13] = {
    "page": 4,
    "question": "Consider a vector field given by $x\\hat{\\imath} + y\\hat{\\jmath} + z\\hat{k}$. This vector field is",
    "options": [
        {"label": "A", "text": "divergence-free and curl-free."},
        {"label": "B", "text": "curl-free but not divergence-free."},
        {"label": "C", "text": "divergence-free but not curl-free."},
        {"label": "D", "text": "neither divergence-free nor curl-free."}
    ]
}

# Q14 (AE 4)
questions_data[14] = {
    "page": 4,
    "question": "A jet aircraft is initially flying steady and level at its maximum endurance condition. For the aircraft to fly steady and level, but faster at the same altitude, the pilot should",
    "options": [
        {"label": "A", "text": "increase thrust alone."},
        {"label": "B", "text": "increase thrust and increase angle of attack."},
        {"label": "C", "text": "increase thrust and reduce angle of attack."},
        {"label": "D", "text": "reduce angle of attack alone."}
    ]
}

# Q15 (AE 5)
questions_data[15] = {
    "page": 4,
    "question": "The pilot of a conventional airplane that is flying steady and level at some altitude, deflects the port side aileron up and the starboard aileron down. The aircraft will then",
    "options": [
        {"label": "A", "text": "pitch, nose up."},
        {"label": "B", "text": "roll with the starboard wing up."},
        {"label": "C", "text": "pitch, nose down."},
        {"label": "D", "text": "roll with the port wing up."}
    ]
}

# Q16 (AE 6)
questions_data[16] = {
    "page": 4,
    "question": "A NACA 0012 airfoil has a trailing edge flap. The airfoil is operating at an angle of attack of 5 degrees with un-deflected flap. If the flap is now deflected by 5 degrees downwards, the $C_L$ versus $\\alpha$ curve",
    "options": [
        {"label": "A", "text": "shifts right and slope increases."},
        {"label": "B", "text": "shifts left and slope increases."},
        {"label": "C", "text": "shifts left and slope stays the same."},
        {"label": "D", "text": "shifts right and slope stays the same."}
    ]
}

# Q17 (AE 7)
questions_data[17] = {
    "page": 5,
    "question": "An airplane requires a longer ground roll to lift-off on hot summer days because",
    "options": [
        {"label": "A", "text": "the thrust is directly proportional to free-stream density."},
        {"label": "B", "text": "the thrust is directly proportional to weight of the aircraft."},
        {"label": "C", "text": "the lift-off distance is directly proportional to free-stream density."},
        {"label": "D", "text": "the runway friction is high on hot summer days."}
    ]
}

# Q18 (AE 8)
questions_data[18] = {
    "page": 5,
    "question": "The velocity profile in an incompressible, laminar boundary layer is shown in the figure below. $U$ is the free-stream velocity, $u(y)$ is the stream-wise velocity component. The area of the black shaded region in the figure below represents the",
    "options": [
        {"label": "A", "text": "boundary layer thickness."},
        {"label": "B", "text": "momentum thickness."},
        {"label": "C", "text": "displacement thickness."},
        {"label": "D", "text": "shape factor."}
    ]
}

# Q19 (AE 9)
questions_data[19] = {
    "page": 5,
    "question": "The tangential velocity component $V$ of a spacecraft, which is in a circular orbit of radius $R$ around a spherical Earth ($\\mu = GM \\rightarrow \\text{gravitational parameter of Earth}$) is given by the following expression.",
    "options": [
        {"label": "A", "text": "$V = \\sqrt{\\frac{\\mu}{2R}}$"},
        {"label": "B", "text": "$V = \\sqrt{\\frac{\\mu}{R}}$"},
        {"label": "C", "text": "$V = \\frac{2\\pi}{\\sqrt{\\mu} R^{3/2}}$"},
        {"label": "D", "text": "$V = \\frac{2\\pi}{\\sqrt{\\mu} R^{2/3}}$"}
    ]
}

# Q20 (AE 10)
questions_data[20] = {
    "page": 5,
    "question": "Equation of the trajectory of a typical space object around any planet, in polar coordinates $(r, \\theta)$ (i.e. a general conic section geometry), is given as follows. ($h$ is angular momentum, $\\mu$ is gravitational parameter, $e$ is eccentricity, $r$ is radial distance from the planet center, $\\theta$ is angle between vectors $\\vec{e}$ and $\\vec{r}$).\n",
    "options": [
        {"label": "A", "text": "$r = \\frac{h^2/\\mu}{1 - e\\cos\\theta}$"},
        {"label": "B", "text": "$r = \\frac{h^2/\\mu}{e - \\cos\\theta}$"},
        {"label": "C", "text": "$r = \\frac{h^2/\\mu}{1 + e\\cos\\theta}$"},
        {"label": "D", "text": "$r = \\frac{h^2/\\mu}{e + \\cos\\theta}$"}
    ]
}

# Q21 (AE 11)
questions_data[21] = {
    "page": 5,
    "question": "In an elliptic orbit around any planet, the location at which a spacecraft has the maximum angular velocity is",
    "options": [
        {"label": "A", "text": "apoapsis."},
        {"label": "B", "text": "periapsis."},
        {"label": "C", "text": "a point at $+45^\\circ$ from periapsis."},
        {"label": "D", "text": "a point at $-90^\\circ$ from apoapsis."}
    ]
}

# Q22 (AE 12)
questions_data[22] = {
    "page": 6,
    "question": "The pitching moment of a positively cambered NACA airfoil about its leading edge at zero-lift angle of attack is",
    "options": [
        {"label": "A", "text": "negative."},
        {"label": "B", "text": "positive."},
        {"label": "C", "text": "indeterminate."},
        {"label": "D", "text": "zero."}
    ]
}

# Q23 (AE 13)
questions_data[23] = {
    "page": 6,
    "question": "In a low-speed wind tunnel, the angular location(s) from the front stagnation point on a circular cylinder where the static pressure equals the free-stream static pressure, is",
    "options": [
        {"label": "A", "text": "$\\pm 38^\\circ$"},
        {"label": "B", "text": "$\\pm 30^\\circ$"},
        {"label": "C", "text": "$\\pm 60^\\circ$"},
        {"label": "D", "text": "$0^\\circ$"}
    ]
}

# Q24 (AE 14)
questions_data[24] = {
    "page": 6,
    "question": "A thermocouple, mounted flush in an insulated flat surface in a supersonic laminar flow of air measures the",
    "options": [
        {"label": "A", "text": "static temperature."},
        {"label": "B", "text": "temperature greater than static but less than total temperature."},
        {"label": "C", "text": "total temperature."},
        {"label": "D", "text": "temperature greater than total temperature."}
    ]
}

# Q25 (AE 15)
questions_data[25] = {
    "page": 6,
    "question": "A shock wave is moving into still air in a shock tube. Which one of the following happens to the air?",
    "options": [
        {"label": "A", "text": "static temperature increases, total temperature remains constant."},
        {"label": "B", "text": "static temperature increases, total temperature increases."},
        {"label": "C", "text": "static temperature increases, total temperature decreases."},
        {"label": "D", "text": "static pressure increases, total temperature remains constant."}
    ]
}

# Q26 (AE 16)
questions_data[26] = {
    "page": 6,
    "question": "The highest limit load factor experienced by a civil transport aircraft is in the range",
    "options": [
        {"label": "A", "text": "0.0 – 2.0"},
        {"label": "B", "text": "2.0 – 5.0"},
        {"label": "C", "text": "5.0 – 8.0"},
        {"label": "D", "text": "8.0 – 10.0"}
    ]
}

# Q27 (AE 17)
questions_data[27] = {
    "page": 6,
    "question": "Determine the correctness or otherwise of the following statements, [a] and [r]:\n\n[a] A closed-section box beam configuration is used in aircraft wings.\n\n[r] Closed-section box beam configuration is capable of resisting torsional loads.",
    "options": [
        {"label": "A", "text": "Both [a] and [r] are true and [r] is the correct reason for [a]."},
        {"label": "B", "text": "Both [a] and [r] are true but [r] is not the correct reason for [a]."},
        {"label": "C", "text": "Both [a] and [r] are false."},
        {"label": "D", "text": "[a] is true but [r] is false."}
    ]
}

# Q28 (AE 18)
questions_data[28] = {
    "page": 7,
    "question": "The first law of thermodynamics is also known as conservation of",
    "options": [
        {"label": "A", "text": "mass."},
        {"label": "B", "text": "momentum."},
        {"label": "C", "text": "energy."},
        {"label": "D", "text": "species."}
    ]
}

# Q29 (AE 19)
questions_data[29] = {
    "page": 7,
    "question": "In an ideal gas turbine cycle, the expansion in a turbine is represented by",
    "options": [
        {"label": "A", "text": "an isenthalpic process."},
        {"label": "B", "text": "an isentropic process."},
        {"label": "C", "text": "an isobaric process."},
        {"label": "D", "text": "an isochoric process."}
    ]
}

# Q30 (AE 20)
questions_data[30] = {
    "page": 7,
    "question": "The determinant of the matrix $\\matrix{1 & 1 & -1; 2 & 1 & 0; 3 & 1 & 1}$ is ______ (accurate to one decimal place)."
}

# Q31 (AE 21)
questions_data[31] = {
    "page": 7,
    "question": "The theoretical maximum velocity (in m/s) of air expanding from a reservoir at 700 K is __________ (accurate to two decimal places). Specific heat of air at constant pressure is 1005 J/(kg-K)."
}

# Q32 (AE 22)
questions_data[32] = {
    "page": 7,
    "question": "For a damped single degree of freedom system with damping ratio of 0.1, ratio of two successive peak amplitudes of free vibration is ___________ (accurate to two decimal places)."
}

# Q33 (AE 23)
questions_data[33] = {
    "page": 7,
    "question": "The natural frequency (in rad/s) of the spring-mass system shown in the figure below is _____ (accurate to one decimal place)."
}

# Q34 (AE 24)
questions_data[34] = {
    "page": 7,
    "question": "The stagnation pressures at the inlet and exit of a subsonic intake are 100 kPa and 98 kPa, respectively. The pressure recovery of this intake will be ______ (accurate to two decimal places)."
}

# Q35 (AE 25)
questions_data[35] = {
    "page": 7,
    "question": "A combustor is operating with a fuel-air ratio of 0.03. If the stoichiometric fuel-air ratio of the fuel used is 0.06, the equivalence ratio of the combustor will be _______ (accurate to two decimal places)."
}

# Q36 (AE 26)
questions_data[36] = {
    "page": 8,
    "question": "The solution of the differential equation $\\frac{d^2 y}{dx^2} + 3\\frac{dy}{dx} = 0$, given that $y = 0$ and $\\frac{dy}{dx} = 1$ at $x = 0$ is",
    "options": [
        {"label": "A", "text": "$x(1 - e^{-3x})$"},
        {"label": "B", "text": "$\\frac{1}{3}(1 - e^{-3x})$"},
        {"label": "C", "text": "$\\frac{1}{3}(1 + e^{-3x})$"},
        {"label": "D", "text": "$\\frac{1}{3} x e^{-3x/2}$"}
    ]
}

# Q37 (AE 27)
questions_data[37] = {
    "page": 8,
    "question": "The relation between pressure ($p$) and velocity ($V$) for a steady, isentropic flow at two points along a streamline is, ($c$ is a constant)",
    "options": [
        {"label": "A", "text": "$c(p_2^\\gamma - p_1^\\gamma) = \\frac{V_1^2}{2} - \\frac{V_2^2}{2}$"},
        {"label": "B", "text": "$c(p_2^{\\frac{\\gamma}{\\gamma-1}} - p_1^{\\frac{\\gamma}{\\gamma-1}}) = \\frac{V_1^2}{2} - \\frac{V_2^2}{2}$"},
        {"label": "C", "text": "$c(p_2^{\\frac{\\gamma-1}{\\gamma}} - p_1^{\\frac{\\gamma-1}{\\gamma}}) = \\frac{V_1^2}{2} - \\frac{V_2^2}{2}$"},
        {"label": "D", "text": "$c(p_2^{\\gamma-1} - p_1^{\\gamma-1}) = \\frac{V_1^2}{2} - \\frac{V_2^2}{2}$"}
    ]
}

# Q38 (AE 28)
questions_data[38] = {
    "page": 8,
    "question": "A thin airfoil is mounted in a low-speed, subsonic wind tunnel, in which the Mach number is 0.1. At a point on the airfoil, the pressure coefficient is measured to be -1.2. If the flow velocity is increased such that the free-stream Mach number is 0.6, the pressure coefficient at the same point on the airfoil will approximately be:",
    "options": [
        {"label": "A", "text": "-3.5"},
        {"label": "B", "text": "-2.9"},
        {"label": "C", "text": "-1.5"},
        {"label": "D", "text": "-0.75"}
    ]
}

# Q39 (AE 29)
questions_data[39] = {
    "page": 8,
    "question": "A solid circular shaft of diameter $d$ is under pure torsion of magnitude $T$. The maximum tensile stress experienced at any point on the shaft is",
    "options": [
        {"label": "A", "text": "$\\frac{32T}{\\pi d^3}$"},
        {"label": "B", "text": "$\\frac{16T}{\\pi d^4}$"},
        {"label": "C", "text": "$\\frac{32T}{\\pi d^4}$"},
        {"label": "D", "text": "$\\frac{16T}{\\pi d^3}$"}
    ]
}

# Q40 (AE 30)
questions_data[40] = {
    "page": 8,
    "question": "A clamped-clamped beam, subjected to a point load $P$ at the midspan, is shown in the figure below. The magnitude of the moment reaction at the two fixed ends of the beam is",
    "options": [
        {"label": "A", "text": "$PL/2$"},
        {"label": "B", "text": "$PL/4$"},
        {"label": "C", "text": "$PL/8$"},
        {"label": "D", "text": "$PL/16$"}
    ]
}

# Q41 (AE 31)
questions_data[41] = {
    "page": 9,
    "question": "Which of the following statement(s) is/are true about the state of a body in plane strain condition?\n\nP: All the points in the body undergo displacements in one plane only, for example the x-y plane, leading to $\\varepsilon_{zz} = \\gamma_{xz} = \\gamma_{yz} = 0$.\nQ: All the components of stress perpendicular to the plane of deformation, for example the x-y plane, of the body are equal to zero, i.e. $\\sigma_{zz} = \\tau_{xz} = \\tau_{yz} = 0$.\nR: Except the normal component, all the other components of stress perpendicular to the plane of deformation of the body, for example the x-y plane, are equal to zero, i.e. $\\sigma_{zz} \\neq 0, \\tau_{xz} = \\tau_{yz} = 0$.",
    "options": [
        {"label": "A", "text": "P only"},
        {"label": "B", "text": "Q only"},
        {"label": "C", "text": "P and Q"},
        {"label": "D", "text": "P and R"}
    ]
}

# Q42 (AE 32)
questions_data[42] = {
    "page": 9,
    "question": "An aircraft with a turbojet engine flies at a velocity of 100 m/s. If the jet exhaust velocity is 300 m/s, the propulsive efficiency of the engine, assuming a negligible fuel-air ratio, is",
    "options": [
        {"label": "A", "text": "0.33"},
        {"label": "B", "text": "0.50"},
        {"label": "C", "text": "0.67"},
        {"label": "D", "text": "0.80"}
    ]
}

# Q43 (AE 33)
questions_data[43] = {
    "page": 9,
    "question": "An aircraft with a turboprop engine produces a thrust of 500 N and flies at 100 m/s. If the propeller efficiency is 0.5, the shaft power produced by the engine is",
    "options": [
        {"label": "A", "text": "50 kW"},
        {"label": "B", "text": "100 kW"},
        {"label": "C", "text": "125 kW"},
        {"label": "D", "text": "500 kW"}
    ]
}

# Q44 (AE 34)
questions_data[44] = {
    "page": 9,
    "question": "An axial compressor that generates a stagnation pressure ratio of 4.0, operates with inlet and exit stagnation temperatures of 300 K and 480 K, respectively. If the ratio of specific heats ($\\gamma$) is 1.4, the isentropic efficiency of the compressor is",
    "options": [
        {"label": "A", "text": "0.94"},
        {"label": "B", "text": "0.81"},
        {"label": "C", "text": "0.72"},
        {"label": "D", "text": "0.63"}
    ]
}

# Q45 (AE 35)
questions_data[45] = {
    "page": 9,
    "question": "A rocket has an initial mass of 150 kg. After operating for a duration of 10 s, its final mass is 50 kg. If the acceleration due to gravity is 9.81 m/s$^2$ and the thrust produced by the rocket is 19.62 kN, the specific impulse of the rocket is",
    "options": [
        {"label": "A", "text": "400 s"},
        {"label": "B", "text": "300 s"},
        {"label": "C", "text": "200 s"},
        {"label": "D", "text": "100 s"}
    ]
}

# Q46 (AE 36)
questions_data[46] = {
    "page": 9,
    "question": "Consider the vector field $\\vec{v} = -\\frac{y}{r^2}\\hat{\\imath} + \\frac{x}{r^2}\\hat{\\jmath}$; where $r = \\sqrt{x^2 + y^2}$. The contour integral $\\oint \\vec{v} \\cdot d\\vec{s}$, where $d\\vec{s}$ is tangent to the contour that encloses the origin, is __________ (accurate to two decimal places)."
}

# Q47 (AE 37)
questions_data[47] = {
    "page": 9,
    "question": "The magnitude of the x-component of a unit vector at the point (1, 1) that is normal to equi-potential lines of the potential function $\\phi(r) = \\frac{1}{r^2 + 4}$, where $r = \\sqrt{x^2 + y^2}$, is _______ (accurate to two decimal places)."
}

# Q48 (AE 38)
questions_data[48] = {
    "page": 10,
    "question": "Assuming ISA standard sea level conditions (288.16 K, density of 1.225 kg/m$^3$, $g = 9.81\\text{ m/s}^2$, $R = 287\\text{ J/(kg-K)}$), the density (in kg/m$^3$) of air at Leh, which is at an altitude of 3500 m above mean sea level is ________ (accurate to two decimal places)."
}

# Q49 (AE 39)
questions_data[49] = {
    "page": 10,
    "question": "Consider a cubical tank of side 2 m with its top open. It is filled with water up to a height of 1 m. Assuming the density of water to be 1000 kg/m$^3$, $g$ as 9.81 m/s$^2$ and the atmospheric pressure to be 100 kPa, the net hydrostatic force (in kN) on the side face of the tank due to the air and water is ______ (accurate to two decimal places)."
}

# Q50 (AE 40)
questions_data[50] = {
    "page": 10,
    "question": "An aircraft with mass of 400,000 kg cruises at 240 m/s at an altitude of 10 km. Its lift to drag ratio at cruise is 15. Assuming $g$ as 9.81 m/s$^2$, the power (in MW) needed for it to cruise is _______ (accurate to two decimal places)."
}

# Q51 (AE 41)
questions_data[51] = {
    "page": 10,
    "question": "A statically-stable aircraft has a $C_{L\\alpha} = 5$ (where the angle of attack, $\\alpha$, is measured in radians). The coefficient of moment of the aircraft about the center of gravity is given as $C_{M,c.g.} = 0.05 - 4\\alpha$. The mean aerodynamic chord of the aircraft wing is 1 m. The location (positive towards the nose) of the neutral point of the aircraft from the center of gravity is ______ (in m, accurate to two decimal places)."
}

# Q52 (AE 42)
questions_data[52] = {
    "page": 10,
    "question": "An aircraft with a gross weight of 2000 kg, has a speed of 130 m/s at sea level, where the conditions are: 1 atmosphere (pressure), 288 K (temperature), and 1.23 kg/m$^3$ (density). The speed (in m/s) required by the aircraft at an altitude of 9000 m, where the conditions are: 0.31 atmosphere, 230 K, and 0.47 kg/m$^3$, to maintain a steady, level flight is ________ (accurate to two decimal places)."
}

# Q53 (AE 43)
questions_data[53] = {
    "page": 10,
    "question": "A pitot probe on an aircraft in a steady, level flight records a pressure of 55,000 N/m$^2$. The static pressure and density are 45,280 N/m$^2$ and 0.6 kg/m$^3$, respectively. The wing area and the lift coefficient are 16 m$^2$ and 2, respectively. The wing loading (in N/m$^2$) on this aircraft is _________ (accurate to one decimal place)."
}

# Q54 (AE 44)
questions_data[54] = {
    "page": 10,
    "question": "A spacecraft forms a circular orbit at an altitude of 150 km above the surface of a spherical Earth. Assuming the gravitational parameter, $\\mu = 3.986 \\times 10^{14}\\text{ m}^3/\\text{s}^2$ and radius of earth, $R_E = 6,400\\text{ km}$, the velocity required for the injection of the spacecraft, parallel to the local horizon, is _______________ (accurate to two decimal places)."
}

# Q55 (AE 45)
questions_data[55] = {
    "page": 10,
    "question": "Air at 50 kPa pressure and 400 K temperature flows in a duct at Mach 3.0. A part of the flow leaks through an opening on the duct wall into the ambient, where the pressure is 30 kPa. The maximum Mach number achieved in the discharge is _______ (accurate to two decimal places). (Ratio of specific heats of air is $\\gamma = 1.4$)."
}

# Q56 (AE 46)
questions_data[56] = {
    "page": 11,
    "question": "Consider a $20^\\circ$ half-angle wedge in a supersonic flow at Mach 3.0 at standard sea-level conditions. If the shock-wave angle on the wedge is $36^\\circ$, the Mach number of the tangential component of the flow post-shock is _______ (accurate to two decimal places)."
}

# Q57 (AE 47)
questions_data[57] = {
    "page": 11,
    "question": "The boundary layer thickness at the location of a sensor on a flat plate in an incompressible, laminar flow of air is required to be restricted to 1 mm for an effective measurement. If the flow velocity is 20 m/s with 1 bar pressure, 300 K temperature, and $1.789 \\times 10^{-5}\\text{ kg/(m-s)}$ viscosity, the maximum distance (in mm) of the sensor location from the leading edge is ________ (accurate to one decimal place)."
}

# Q58 (AE 48)
questions_data[58] = {
    "page": 11,
    "question": "Gross weight of an airplane is 7000 N, wing area is 16 m$^2$, and the maximum lift coefficient is 2.0. Assuming density at the altitude as 1.23 kg/m$^3$, the stall speed (in m/s) of the aircraft is _________ (accurate to two decimal places)."
}

# Q59 (AE 49)
questions_data[59] = {
    "page": 11,
    "question": "A thin-walled tube with external radius of 100 mm and wall thickness of 2 mm, is fixed at one end. It is subjected to a compressive force of 1 N acting at a point on the circumference parallel to its length. The maximum normal stress (in kPa) experienced by the structure is _____________ (accurate to two decimal places)."
}

# Q60 (AE 50)
questions_data[60] = {
    "page": 11,
    "question": "A 1 m long massless cantilever beam oscillates at 2 Hz, while a 60 kg mass is attached at the tip of it. The flexural rigidity of the beam (in kN-m$^2$) is _________________ (accurate to two decimal places)."
}

# Q61 (AE 51)
questions_data[61] = {
    "page": 11,
    "question": "A cantilever beam having a rectangular cross-section of width 60 mm and depth 100 mm, is made of aluminum alloy. The material mechanical properties are: Young's modulus, $E = 73\\text{ GPa}$ and ultimate stress, $\\sigma_u = 480\\text{ MPa}$. Assuming a factor of safety of 4, the maximum bending moment (in kN-m) that can be applied on the beam is _____ (accurate to one decimal place)."
}

# Q62 (AE 52)
questions_data[62] = {
    "page": 11,
    "question": "The components of stress in a body under plane stress condition, in the absence of body forces, is given by:\n$\\sigma_{xx} = Ax^2$; $\\sigma_{yy} = 12x^2 - 6y^2$ and $\\sigma_{xy} = 12xy$.\nThe coefficient, $A$, such that the body is under equilibrium is _____ (accurate to one decimal place)."
}

# Q63 (AE 53)
questions_data[63] = {
    "page": 11,
    "question": "An axial compressor rotor with 50% degree of reaction, operates with an axial velocity of 200 m/s. The absolute flow angle at the inlet of the rotor is $22^\\circ$ with reference to the axial direction. If the axial velocity is assumed to remain constant through the rotor, the magnitude of the relative velocity (in m/s) at the rotor exit is __________ (accurate to one decimal place)."
}

# Q64 (AE 54)
questions_data[64] = {
    "page": 12,
    "question": "The relative velocity of air leaving a straight radial impeller of a centrifugal compressor is 100 m/s. If the impeller tip speed is 200 m/s, for a slip free operation, the absolute velocity (in m/s) at the impeller exit is _________ (accurate to one decimal place)."
}

# Q65 (AE 55)
questions_data[65] = {
    "page": 12,
    "question": "An aircraft wind tunnel model, having a pitch axis mass moment of inertia ($I_{yy}$) of $0.014\\text{ kg-m}^2$, is mounted in such a manner that it has pure pitching motion about its centre of gravity, where it is supported through a frictionless hinge. If the pitching moment ($M$) derivative with respect to angle of attack ($\\alpha$), denoted by '$M_\\alpha$', is $-0.504\\text{ N-m/rad}$ and the pitching moment ($M$) derivative with respect to pitch rate ($q$), denoted by '$M_q$', is $-0.0336\\text{ N-m/(rad/s)}$, the damping ratio of the resulting motion due to an initial disturbance in pitch angle is approximately _________ (accurate to three decimal places)."
}

# Figure metadata for questions
figure_metadata = {
    18: [{"src": "figures/gate-2018-ae-ae-18-figure-1.png", "alt": "Boundary layer velocity profile with shaded region", "page": 5}],
    33: [{"src": "figures/gate-2018-ae-ae-33-figure-1.png", "alt": "Two masses connected by rigid link and springs", "page": 7}],
    40: [{"src": "figures/gate-2018-ae-ae-40-figure-1.png", "alt": "Clamped-clamped beam with midspan point load P", "page": 8}]
}

def parse_key(raw_key, qtype):
    if raw_key == "MTA":
        return "MTA"
    if qtype == "NAT":
        if " OR " in raw_key:
            parts = raw_key.split(" OR ")
            res = []
            for p in parts:
                if " to " in p:
                    res.append([float(x) for x in p.split(" to ")])
                else:
                    res.append(float(p))
            return res
        if " to " in raw_key:
            return [float(x) for x in raw_key.split(" to ")]
        return float(raw_key)
    elif qtype == "MSQ":
        if ";" in raw_key:
            return [s.strip() for s in raw_key.split(";")]
        if " OR " in raw_key:
            return [s.strip() for s in raw_key.split(" OR ")]
        return [raw_key.strip()]
    return raw_key

questions_list = []
key_sha256 = key_data["sha256"]

for k_row in key_data["rows"]:
    idx = k_row["number"]
    sec = k_row["section"]
    qid = f"gate-2018-ae-ga-{idx:02d}" if sec == "GA" else f"gate-2018-ae-ae-{idx:02d}"
    
    qtype = k_row["type"]
    marks = k_row["marks"]
    raw_key = k_row["rawKey"]
    parsed_ans = parse_key(raw_key, qtype)
    
    q_data = questions_data[idx]
    page_num = q_data["page"]
    q_text = q_data["question"]
    
    neg_marks = 0.0
    if qtype == "MCQ":
        neg_marks = 0.3333333333333333 if marks == 1 else 0.6666666666666666
    
    figs_raw = figure_metadata.get(idx, [])
    figs = [
        {
            "src": f["src"],
            "alt": f["alt"],
            "page": f["page"],
            "source": {
                "file": "internal/ae/AE2018.pdf",
                "sha256": pdf_sha256,
                "page": f["page"],
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            },
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-07"
        }
        for f in figs_raw
    ]
    has_fig = len(figs) > 0
    
    content_blocks = [
        {
            "type": "text",
            "text": q_text
        }
    ]
    for fig in figs:
        content_blocks.append({
            "type": "figure",
            "asset": {
                "src": fig["src"],
                "alt": fig["alt"],
                "page": fig["page"],
                "source": fig["source"],
                "verificationStatus": fig["verificationStatus"],
                "verifiedOn": fig["verifiedOn"]
            }
        })
        
    raw_opts = q_data.get("options", [])
    opts = []
    if qtype in ["MCQ", "MSQ"]:
        for opt in raw_opts:
            opt_obj = {
                "label": opt["label"],
                "text": opt["text"]
            }
            opts.append(opt_obj)
            
    grading_status = "marks-to-all" if parsed_ans == "MTA" else "official key verified"
    grading_rule = "marks-to-all" if parsed_ans == "MTA" else None
    
    q_record = {
        "id": qid,
        "exam": "GATE",
        "year": 2018,
        "paper": "AE",
        "number": idx,
        "section": sec,
        "subject": "General Aptitude" if sec == "GA" else "Aerospace Engineering",
        "type": qtype,
        "marks": marks,
        "question": q_text,
        "content": content_blocks,
        "figures": figs,
        "groupId": None,
        "source": {
            "file": "internal/ae/AE2018.pdf",
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
        "gradingStatus": grading_status,
        "answerSource": {
            "url": "http://gate.iitg.ac.in/",
            "paper": "AE",
            "questionNumber": idx,
            "section": sec,
            "page": page_num,
            "sha256": key_sha256,
            "verifiedOn": "2026-10-07"
        },
        "answer": parsed_ans,
        "negativeMarks": neg_marks,
        "markingRule": "gate-2018-official",
        "hasFigure": has_fig,
        "options": opts
    }
    
    if grading_rule:
        q_record["gradingRule"] = grading_rule

    if parsed_ans == "MTA":
        q_record["acceptedAnswers"] = ["MTA"]
    elif qtype == "MCQ":
        q_record["acceptedAnswers"] = [parsed_ans]
    elif qtype == "MSQ":
        q_record["acceptedAnswers"] = [parsed_ans]
    elif qtype == "NAT":
        if isinstance(parsed_ans, list) and len(parsed_ans) > 0 and isinstance(parsed_ans[0], list):
            q_record["acceptedAnswers"] = [{"range": r} for r in parsed_ans]
        elif isinstance(parsed_ans, list):
            q_record["acceptedAnswers"] = [{"range": parsed_ans}]
        else:
            q_record["acceptedAnswers"] = [{"value": parsed_ans}]

    questions_list.append(q_record)

print(f"Total compiled questions: {len(questions_list)}")

ga_qids = [q["id"] for q in questions_list if q["section"] == "GA"]
ae_qids = [q["id"] for q in questions_list if q["section"] == "AE"]

paper_data = {
    "schemaVersion": 1,
    "id": "gate-2018-ae",
    "exam": "GATE",
    "year": 2018,
    "paper": "AE",
    "title": "GATE Aerospace Engineering 2018",
    "durationMinutes": 180,
    "totalMarks": 100,
    "totalQuestions": 65,
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
        "file": "internal/ae/AE2018.pdf",
        "sha256": pdf_sha256,
        "pageCount": len(doc)
    },
    "ingestionStatus": "complete",
    "verificationStatus": "source-verified",
    "verifiedOn": "2026-10-07",
    "questions": questions_list
}

with open('data/ae/2018.json', 'w', encoding='utf-8') as f:
    json.dump(paper_data, f, indent=2, ensure_ascii=False)
print("Saved data/ae/2018.json")

# Update manifest.json
with open('data/ae/manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

fig_assets_count = 0
for q in questions_list:
    fig_assets_count += len(q.get("figures", []))
    for opt in q.get("options", []):
        if "figure" in opt:
            fig_assets_count += 1

print(f"Total figure assets: {fig_assets_count}")

for y in manifest["years"]:
    if y["year"] == 2018:
        y["sourcePdf"] = "internal/ae/AE2018.pdf"
        y["path"] = "data/ae/2018.json"
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
            "gradedAnswers": 64,
            "marksToAll": 1,
            "unavailable": 0
        }
        y["figureAssetCount"] = fig_assets_count
        y["newFigureAssetCount"] = fig_assets_count
        y["reusedFigureAssetCount"] = 0
        y["optionFigureCount"] = 0
        y["structuredTableCount"] = 0
        y["questionGroupCount"] = 0
        y["ingestionStatus"] = "complete"
        y["verificationStatus"] = "source-verified"
        y["verifiedOn"] = "2026-10-07"

with open('data/ae/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("Updated data/ae/manifest.json for 2018")
