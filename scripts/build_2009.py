import json

paper = {
  "id": "gate-2009-ae",
  "year": 2009,
  "paperCode": "AE",
  "title": "GATE 2009 Aerospace Engineering (AE)",
  "durationMinutes": 180,
  "totalMarks": 100,
  "schemaVersion": 1,
  "marking": {
    "correctMarks": {
      "1": 1,
      "2": 2
    },
    "negativeMarks": {
      "1": 0.3333333333333333,
      "2": 0.6666666666666666
    },
    "negativeFraction": {
      "MCQ": 0.3333333333333333,
      "MSQ": 0,
      "NAT": 0
    }
  },
  "sections": [
    {
      "id": "ae",
      "name": "Aerospace Engineering",
      "startQuestion": 1,
      "endQuestion": 60,
      "totalMarks": 100,
      "totalQuestions": 60
    }
  ],
  "questions": []
}

questions = [
  # Q1
  {
    "id": "gate-2009-ae-ae-01",
    "questionNumber": 1,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "For a flow through a Prandtl-Meyer expansion wave",
    "options": [
      "Mach number stays constant.",
      "Entropy stays constant.",
      "Temperature stays constant.",
      "Density stays constant."
    ],
    "correctOption": "B"
  },
  # Q2
  {
    "id": "gate-2009-ae-ae-02",
    "questionNumber": 2,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "For two-dimensional irrotational and incompressible flows",
    "options": [
      "Both potential and stream functions satisfy the Laplace equation.",
      "Potential function must satisfy the Laplace equation but the stream function need not.",
      "Stream function must satisfy the Laplace equation but the potential function need not.",
      "Neither the stream function nor the potential function need to satisfy the Laplace equation."
    ],
    "correctOption": "A"
  },
  # Q3
  {
    "id": "gate-2009-ae-ae-03",
    "questionNumber": 3,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "A trailing edge plain flap deflected downward increases the lift coefficient of an airfoil by",
    "options": [
      "Increasing the effective camber of the airfoil.",
      "Delaying the separation of the flow from the airfoil surface.",
      "Increasing the local airspeed near the trailing edge.",
      "Controlling the growth of the boundary layer thickness along the airfoil surface."
    ],
    "correctOption": "A"
  },
  # Q4
  {
    "id": "gate-2009-ae-ae-04",
    "questionNumber": 4,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "Thin airfoil theory predicts that the lift slope is $\\frac{dc_l}{d\\alpha} = 2\\pi$ for",
    "options": [
      "Symmetric airfoils only.",
      "Cambered airfoils only.",
      "Any airfoil shape.",
      "Joukowski airfoils only."
    ],
    "correctOption": "C"
  },
  # Q5
  {
    "id": "gate-2009-ae-ae-05",
    "questionNumber": 5,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "The ordinary differential equation $\\frac{d^2 y}{dx^2} + ky = 0$ where $k$ is real and positive",
    "options": [
      "is non-linear",
      "has a characteristic equation with one real and one complex root",
      "has a characteristic equation with two real roots",
      "has a complementary function that is simple harmonic"
    ],
    "correctOption": "D"
  },
  # Q6
  {
    "id": "gate-2009-ae-ae-06",
    "questionNumber": 6,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "A non-trivial solution to the $(n \\times n)$ system of equations $[A]\\{x\\} = \\{0\\}$, where $\\{0\\}$ is the null vector",
    "options": [
      "can never be found",
      "may be found only if $[A]$ is not singular",
      "may be found only if $[A]$ is an orthogonal matrix",
      "may be found only if $[A]$ has at least one eigenvalue equal to zero"
    ],
    "correctOption": "D"
  },
  # Q7
  {
    "id": "gate-2009-ae-ae-07",
    "questionNumber": 7,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "For a plane strain problem, the stresses satisfy the condition",
    "options": [
      "\\(\\tau_{xz} = \\tau_{yz} = \\sigma_z = 0\\)",
      "\\(\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu(\\sigma_x + \\sigma_y)\\)",
      "\\(\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu\\tau_{xy}\\)",
      "\\(\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu(\\sigma_x + \\sigma_y) + (1-\\nu)\\tau_{xy}\\)"
    ],
    "correctOption": "B"
  },
  # Q8
  {
    "id": "gate-2009-ae-ae-08",
    "questionNumber": 8,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "The propulsive efficiency of a turbo-jet engine moving at velocity $U_\\infty$ and having exhaust velocity $U_e$ with respect to the engine is given by",
    "options": [
      "\\(\\frac{2}{U_\\infty / U_e + 1}\\)",
      "\\(1 - \\frac{U_\\infty}{U_e}\\)",
      "\\(\\frac{2 U_\\infty U_e}{U_e^2 + U_\\infty^2}\\)",
      "\\(\\frac{2 U_\\infty}{U_e + U_\\infty}\\)"
    ],
    "correctOption": "D"
  },
  # Q9
  {
    "id": "gate-2009-ae-ae-09",
    "questionNumber": 9,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "An aircraft is flying at $M = 2$ where the ambient temperature around the aircraft is $250\\text{ K}$. If the specific heat ratio for air $\\gamma = 1.4$, the stagnation temperature on the surface of the aircraft is",
    "options": [
      "$200\\text{ K}$",
      "$450\\text{ K}$",
      "$350\\text{ K}$",
      "$1450\\text{ K}$"
    ],
    "correctOption": "B"
  },
  # Q10
  {
    "id": "gate-2009-ae-ae-10",
    "questionNumber": 10,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "The division of feed air to an aircraft gas-turbine combustor into primary and secondary streams serves which of the following purposes ?\n\nP. a flammable mixture can be formed\nQ. cooling of combustor liner and flame tube can be accomplished\nR. specific fuel consumption can be reduced",
    "options": [
      "P and R",
      "Q and R",
      "P and Q",
      "P, Q and R"
    ],
    "correctOption": "C"
  },
  # Q11
  {
    "id": "gate-2009-ae-ae-11",
    "questionNumber": 11,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "Classify the following propellants as: cryogenic (C) , semi-cryogenic (SC), compressed gas (CG) and earth storable (ES)\n\n$\\text{N}_2\\text{O}_4\\text{-UDMH}$ (nitrogen tetra oxide and unsymmetrical di-methyl hydrazine)\nLOX-RP1 (liquid oxygen and kerosene)\n$\\text{LOX-LH}_2$ (liquid oxygen and liquid hydrogen)\n$\\text{N}_2$ (nitrogen gas)",
    "options": [
      "$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (C)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (C)}$",
      "$\\text{N}_2\\text{O}_4\\text{-UDMH (SC)}, \\quad \\text{LOX-RP1 (SC)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (C)}$",
      "$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (SC)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (CG)}$",
      "$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (C)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (CG)}$"
    ],
    "correctOption": "C"
  },
  # Q12
  {
    "id": "gate-2009-ae-ae-12",
    "questionNumber": 12,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "A conventional altimeter is a",
    "options": [
      "Pressure transducer",
      "Temperature transducer",
      "Density transducer",
      "Velocity transducer"
    ],
    "correctOption": "A"
  },
  # Q13
  {
    "id": "gate-2009-ae-ae-13",
    "questionNumber": 13,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "The relation between an airplane's true airspeed $V_{\\text{TAS}}$ and equivalent airspeed $V_{\\text{EAS}}$ in terms of the density ratio ($\\sigma = \\frac{\\rho}{\\rho_0}$), where $\\rho_0$ is the air density at sea-level and $\\rho$ is the air density at the altitude at which the airplane is flying, is given by the formula:",
    "options": [
      "\\(\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sigma\\)",
      "\\(\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sigma^2\\)",
      "\\(\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sqrt{\\sigma}\\)",
      "\\(\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\frac{1}{\\sqrt{\\sigma}}\\)"
    ],
    "correctOption": "C"
  },
  # Q14
  {
    "id": "gate-2009-ae-ae-14",
    "questionNumber": 14,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "An unswept fixed-winged aircraft has a large roll stability if the wing is placed",
    "options": [
      "low on the fuselage and has negative dihedral angle",
      "low on the fuselage and has positive dihedral angle",
      "high on the fuselage and has negative dihedral angle",
      "high on the fuselage and has positive dihedral angle"
    ],
    "correctOption": "B"
  },
  # Q15
  {
    "id": "gate-2009-ae-ae-15",
    "questionNumber": 15,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "Thrust available from a turbojet engine",
    "options": [
      "increases as altitude increases",
      "increases up to the tropopause and then decreases",
      "remains constant at all altitudes",
      "decreases as altitude increases"
    ],
    "correctOption": "D"
  },
  # Q16
  {
    "id": "gate-2009-ae-ae-16",
    "questionNumber": 16,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "If $C_{m_{\\text{CG}}}$ is the pitching moment coefficient about the center of gravity of an aircraft, and $\\alpha$ is the angle of attack, then $\\frac{dC_{m_{\\text{CG}}}}{d\\alpha}$ is",
    "options": [
      "a stability derivative which represents stiffness in pitch",
      "a stability derivative which represents damping in pitch",
      "a control derivative in pitch",
      "positive for an aircraft that is stable in pitch"
    ],
    "correctOption": "A"
  },
  # Q17
  {
    "id": "gate-2009-ae-ae-17",
    "questionNumber": 17,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "The life of a geo-stationary communications satellite is limited by",
    "options": [
      "the working life of the on-board electronic circuitry",
      "the time it takes for its orbit to decay due to atmospheric drag",
      "the quantity of on-board fuel available for station-keeping",
      "the number of meteorite impacts that the satellite structure can withstand before breaking up"
    ],
    "correctOption": "C"
  },
  # Q18
  {
    "id": "gate-2009-ae-ae-18",
    "questionNumber": 18,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "For a critically damped single degree of freedom spring - mass - damper system with a damping constant $c$ of $4\\text{ Ns/m}$ and spring constant $k$ of $16\\text{ N/m}$, the system mass $m$ is",
    "options": [
      "$0.5\\text{ kg}$",
      "$0.25\\text{ kg}$",
      "$2\\text{ kg}$",
      "$4\\text{ kg}$"
    ],
    "correctOption": "B"
  },
  # Q19
  {
    "id": "gate-2009-ae-ae-19",
    "questionNumber": 19,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "In a thin walled rectangular tube subjected to equal and opposite forces $P$ as shown in the figure, the shear stress along leg AB is\n\n<img src=\"figures/gate-2009-ae-ae-19-figure-1.png\" alt=\"Thin walled rectangular tube\" />",
    "options": [
      "zero",
      "constant non-zero",
      "varies linearly",
      "varies parabolically"
    ],
    "correctOption": "B"
  },
  # Q20
  {
    "id": "gate-2009-ae-ae-20",
    "questionNumber": 20,
    "section": "ae",
    "type": "MCQ",
    "marks": 1,
    "negativeMarks": 0.3333333333333333,
    "question": "For the thin walled beam cross section as shown in the figure, the shear centre lies at\n\n<img src=\"figures/gate-2009-ae-ae-20-figure-1.png\" alt=\"Thin walled beam cross section\" />",
    "options": [
      "Mid point of AB, i.e. at point $E$",
      "Mid point of BD, i.e. at point $F$",
      "Junction point $B$",
      "at a point $G$ lying within the area $ABC$"
    ],
    "correctOption": "C"
  },
  # Q21
  {
    "id": "gate-2009-ae-ae-21",
    "questionNumber": 21,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "Let $M_0$ be the total mass of a single stage rocket, $M_p$ be the total mass of propellant, $M_L$ be the mass of payload carried by the rocket and $M_S$ be the mass of inert structural components. If $I_{sp}$ is the specific impulse of the propulsion system (in seconds) and $g$ is the acceleration due to gravity, then the maximum velocity that can be attained by the rocket vehicle in the absence of gravity and atmospheric drag is given by",
    "options": [
      "\\(g I_{sp} \\ln \\left( \\frac{M_0}{M_p} \\right)\\)",
      "\\(g I_{sp} \\ln \\left( \\frac{M_0}{M_L + M_S} - 1 \\right)\\)",
      "\\(g I_{sp} \\ln \\left( \\frac{M_0}{M_S} \\right)\\)",
      "\\(g I_{sp} \\ln \\left( \\frac{M_0}{M_0 - M_p} \\right)\\)"
    ],
    "correctOption": "D"
  },
  # Q22
  {
    "id": "gate-2009-ae-ae-22",
    "questionNumber": 22,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "An ideal axial compressor is driven by an ideal turbine across which the total temperature ratio is $0.667$. If the total temperature at turbine inlet is $T_0 = 1500\\text{ K}$ and specific heat of gas $c_p = 1\\text{ kJ/kg/K}$, the power drawn by the compressor per unit mass flow rate of air is approximately",
    "options": [
      "$300\\text{ kW/kg/s}$",
      "$1000\\text{ kW/kg/s}$",
      "$600\\text{ kW/kg/s}$",
      "$500\\text{ kW/kg/s}$"
    ],
    "correctOption": "D"
  },
  # Q23
  {
    "id": "gate-2009-ae-ae-23",
    "questionNumber": 23,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The performance of a solid rocket motor is improved by replacing the old propellant with a new one. The new propellant gives a combustion temperature $40\\%$ higher than the previous propellant without appreciable change in molecular weight of combustion products and other operating parameters. By approximately what percentage is the specific impulse of the new motor higher than the old one ?",
    "options": [
      "$18\\%$",
      "$96\\%$",
      "$42\\%$",
      "$112\\%$"
    ],
    "correctOption": "A"
  },
  # Q24
  {
    "id": "gate-2009-ae-ae-24",
    "questionNumber": 24,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A solid rocket motor has an end burning grain of cross-sectional area $A_{cs} = 0.4\\text{ m}^2$. The density of propellant is $\\rho_p = 1500\\text{ kg/m}^3$ and has linear regression rate $\\dot{r} = 5\\text{ mm/s}$. If the specific impulse of the propulsion system is $I_{sp} = 200\\text{ seconds}$, the thrust produced by the motor is approximately",
    "options": [
      "$3\\text{ kN}$",
      "$6\\text{ kN}$",
      "$1.5\\text{ kN}$",
      "$12\\text{ kN}$"
    ],
    "correctOption": "B"
  },
  # Q25
  {
    "id": "gate-2009-ae-ae-25",
    "questionNumber": 25,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "An ideal ramjet is flying at an altitude of $10\\text{ km}$ with a velocity of $1\\text{ km/s}$. The ambient pressure is $0.25\\text{ bar}$ and temperature is $225\\text{ K}$. The exhaust gases from the engine are optimally expanded and leave the nozzle at $900\\text{ K}$. If the specific heat ratio ($\\gamma$) remains constant, the specific thrust developed by the engine is approximately",
    "options": [
      "$1000\\text{ N-s/kg}$",
      "$2000\\text{ N-s/kg}$",
      "$500\\text{ N-s/kg}$",
      "$4000\\text{ N-s/kg}$"
    ],
    "correctOption": "A"
  },
  # Q26
  {
    "id": "gate-2009-ae-ae-26",
    "questionNumber": 26,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A combat aircraft engine is equipped with an afterburner followed by a variable area convergent nozzle (operating with the nozzle choked). The exhaust gas temperature is $750\\text{ K}$ when afterburner is off and $3000\\text{ K}$ when it is on. When the afterburner is turned on, (assuming the total pressure remains the same, the mass of fuel added in the afterburner is negligible i.e., the mass flow rate remains the same, and the specific heat ratio ($\\gamma$) remains constant), approximately by what factor must the nozzle area be changed ?",
    "options": [
      "$0.5$",
      "$4$",
      "$1$",
      "$2$"
    ],
    "correctOption": "D"
  },
  # Q27
  {
    "id": "gate-2009-ae-ae-27",
    "questionNumber": 27,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "An airplane flying at $100\\text{ m/s}$ is pitching at the rate of $0.2\\text{ deg/s}$. Due to this pitching, the horizontal tail surface located $4\\text{ metres}$ behind the centre-of-mass of the airplane will experience a change in angle of attack, which is",
    "options": [
      "$0.01\\text{ deg}$",
      "$0.008\\text{ deg}$",
      "$0.04\\text{ deg}$",
      "$0.004\\text{ deg}$"
    ],
    "correctOption": "B"
  },
  # Q28
  {
    "id": "gate-2009-ae-ae-28",
    "questionNumber": 28,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The contribution of the horizontal tail to the pitching moment coefficient about the center of gravity ($C_{m_{\\text{CG}}}$) of an aircraft is given by $C_{m_{\\text{tail}}} = 0.2 - 0.0215\\,\\alpha$, where $\\alpha$ is the angle of attack of the aircraft. The contribution of the tail to the aircraft longitudinal stability",
    "options": [
      "is stabilizing",
      "is destabilizing",
      "is nil",
      "cannot be determined from the given information"
    ],
    "correctOption": "A"
  },
  # Q29
  {
    "id": "gate-2009-ae-ae-29",
    "questionNumber": 29,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The linearized dynamics of an aircraft (which has no large rotating components) in straight and level flight is governed by the equations\n\n$$\\frac{d\\vec{x}}{dt} = \\begin{bmatrix} [A] & [B] \\\\ [C] & [D] \\end{bmatrix} \\vec{x}$$\n\nwhere $\\vec{x} = \\begin{bmatrix} u & w & q & \\theta & v & p & r & \\phi \\end{bmatrix}^T$, $[\\;]^T$ represents the transpose of a matrix, $[A], [B], [C]$ and $[D]$ are $4\\times 4$ matrices and $[0]$ is the $4\\times 4$ null matrix. Which of the following is true ?",
    "options": [
      "$[A] \\neq [0];\\; [B] \\neq [0];\\; [C] = [0];\\; [D] \\neq [0]$",
      "$[A] = [0];\\; [B] \\neq [0];\\; [C] \\neq [0];\\; [D] = [0]$",
      "$[A] \\neq [0];\\; [B] = [0];\\; [C] = [0];\\; [D] \\neq [0]$",
      "$[A] \\neq [0];\\; [B] = [0];\\; [C] \\neq [0];\\; [D] = [0]$"
    ],
    "correctOption": "C"
  },
  # Q30
  {
    "id": "gate-2009-ae-ae-30",
    "questionNumber": 30,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The velocity vector of an aircraft along its body-fixed axis is given by $\\vec{V} = \\begin{Bmatrix} u \\\\ v \\\\ w \\end{Bmatrix}$. If $V$ is the magnitude of $\\vec{V}$, $\\alpha$ is the angle of attack and $\\beta$ is the angle of sideslip, which of the following set of relations is correct ?",
    "options": [
      "$u = V\\sin\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$",
      "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\cos\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$",
      "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\sin\\beta\\sin\\alpha$",
      "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$"
    ],
    "correctOption": "D"
  },
  # Q31
  {
    "id": "gate-2009-ae-ae-31",
    "questionNumber": 31,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "An aircraft of mass $2500\\text{ kg}$ in straight and level flight at a constant speed of $100\\text{ m/s}$ has available excess power of $1.0 \\times 10^6\\text{ W}$. The steady rate of climb it can attain at that speed is",
    "options": [
      "$100\\text{ m/s}$",
      "$60\\text{ m/s}$",
      "$40\\text{ m/s}$",
      "$20\\text{ m/s}$"
    ],
    "correctOption": "C"
  },
  # Q32
  {
    "id": "gate-2009-ae-ae-32",
    "questionNumber": 32,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The acceleration due to gravity on the surface of Mars is $0.385$ times that on earth, and the diameter of Mars is $0.532$ times that of earth. The ratio of the escape velocity from the surface of Mars to the escape velocity from the surface of earth is approximately",
    "options": [
      "$0.453$",
      "$0.205$",
      "$0.851$",
      "$0.724$"
    ],
    "correctOption": "A"
  },
  # Q33
  {
    "id": "gate-2009-ae-ae-33",
    "questionNumber": 33,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "Which of the following statements are true for flow across a stationary normal shock ?\n\nP. Stagnation temperature stays constant.\nQ. Stagnation pressure decreases.\nR. Entropy increases.\nS. Stagnation pressure increases.\nT. Stagnation temperature increases.",
    "options": [
      "P, Q, R",
      "Q, R, S",
      "R, S, T",
      "S, T, P"
    ],
    "correctOption": "A"
  },
  # Q34
  {
    "id": "gate-2009-ae-ae-34",
    "questionNumber": 34,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A model airfoil in a wind tunnel that is operating at $50\\text{ m/s}$ develops a minimum pressure co-efficient of $-6.29$ at some point on its upper surface. The local airspeed at that point is",
    "options": [
      "$50\\text{ m/s}$",
      "$125\\text{ m/s}$",
      "$135\\text{ m/s}$",
      "$150\\text{ m/s}$"
    ],
    "correctOption": "C"
  },
  # Q35
  {
    "id": "gate-2009-ae-ae-35",
    "questionNumber": 35,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A symmetrical airfoil section produces a lift coefficient of $0.53$ at an angle of attack of $5\\text{ degrees}$ measured from its chord line. An untwisted wing of elliptical planform and aspect ratio $6$ is made of this airfoil. At an angle of attack of $5\\text{ degrees}$ relative to its chordal plane, this wing would produce a lift coefficient of",
    "options": [
      "$0.53$",
      "$0.48$",
      "$0.40$",
      "$0.36$"
    ],
    "correctOption": "C"
  },
  # Q36
  {
    "id": "gate-2009-ae-ae-36",
    "questionNumber": 36,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "Consider an ideal flow of density $\\rho$ through a variable area duct as shown in the figure below :\n\n<img src=\"figures/gate-2009-ae-ae-36-figure-1.png\" alt=\"Variable area duct with Pitot static probe\" />\n\nLet the cross-sectional areas at sections (1) and (2) be $A_1$ and $A_2$ respectively. The velocity measured at section (1) using a Pitot static probe is $V_1$. Then the static pressure drop $p_2 - p_1$ is",
    "options": [
      "\\(-\\frac{1}{2}\\rho\\left(1 - \\frac{A_1^2}{A_2^2}\\right)V_1^2\\)",
      "\\(\\frac{1}{2}\\rho\\left(1 - \\frac{A_1^2}{A_2^2}\\right)V_1^2\\)",
      "\\(\\frac{1}{2}\\rho\\left(1 + \\frac{A_1^2}{A_2^2}\\right)V_1^2\\)",
      "\\(-\\frac{1}{2}\\rho\\left(1 + \\frac{A_1^2}{A_2^2}\\right)V_1^2\\)"
    ],
    "correctOption": "B"
  },
  # Q37
  {
    "id": "gate-2009-ae-ae-37",
    "questionNumber": 37,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "Two vortices of the same strength and sign are placed a distance $d$ apart as shown below. Assume that the vortices are free to move and the fluid is ideal.\n\n<img src=\"figures/gate-2009-ae-ae-37-figure-1.png\" alt=\"Two vortices separated by distance d\" />\n\nWhich of the following statements is true ?",
    "options": [
      "Vortices 1 and 2 spiral inwards with an initial angular speed $\\frac{\\Gamma}{2\\pi d^2}$ to finally merge and form one vortex of twice the strength.",
      "Vortices 1 and 2 spiral inwards with an initial angular speed $\\frac{\\Gamma}{\\pi d^2}$ to finally merge and form one vortex of twice the strength.",
      "Vortices 1 and 2 perpetually revolve about the midpoint $P$ with radius of revolution $\\frac{d}{2}$ and angular speed $\\frac{\\Gamma}{2\\pi d^2}$.",
      "Vortices 1 and 2 perpetually revolve about the midpoint $P$ with radius of revolution $\\frac{d}{2}$ and angular speed $\\frac{\\Gamma}{\\pi d^2}$."
    ],
    "correctOption": "D"
  },
  # Q38
  {
    "id": "gate-2009-ae-ae-38",
    "questionNumber": 38,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The laminar boundary layer over a large flat plate held parallel to the flow is $7.2\\text{ mm}$ thick at a point $0.33\\text{ m}$ downstream of the leading edge. If the free stream speed is increased by $50\\%$, then the new boundary layer thickness at this location will be approximately",
    "options": [
      "$10.8\\text{ mm}$",
      "$8.8\\text{ mm}$",
      "$5.9\\text{ mm}$",
      "$4.8\\text{ mm}$"
    ],
    "correctOption": "C"
  },
  # Q39
  {
    "id": "gate-2009-ae-ae-39",
    "questionNumber": 39,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "Consider a simply supported beam of length $2L$ with an overhang of length $L$, loaded by an end moment $M$, as shown below.\n\n<img src=\"figures/gate-2009-ae-ae-39-figure-1.png\" alt=\"Overhang beam loaded by end moment M\" />\n\nThe bending moment distribution for this beam is shown in options (A) to (D) below:\n\n<img src=\"figures/gate-2009-ae-ae-39-figure-2.png\" alt=\"Bending moment distribution diagrams\" />",
    "options": [
      "Diagram (A)",
      "Diagram (B)",
      "Diagram (C)",
      "Diagram (D)"
    ],
    "correctOption": "B"
  },
  # Q40
  {
    "id": "gate-2009-ae-ae-40",
    "questionNumber": 40,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "For the spring-mass system shown below, the natural frequencies are\n\n<img src=\"figures/gate-2009-ae-ae-40-figure-1.png\" alt=\"Spring-mass system\" />",
    "options": [
      "$0\\text{ and }\\sqrt{\\frac{k(m_1 + m_2)}{m_1 m_2}}$",
      "$0\\text{ and }\\sqrt{\\frac{k(m_1 + m_2)}{2m_1 m_2}}$",
      "$0\\text{ and }\\sqrt{\\frac{k}{(m_1 + m_2)}}$",
      "$0\\text{ and }\\sqrt{\\frac{k}{2(m_1 + m_2)}}$"
    ],
    "correctOption": "A"
  },
  # Q41
  {
    "id": "gate-2009-ae-ae-41",
    "questionNumber": 41,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The buckling load for a simply supported column of rectangular cross section of dimensions $1\\text{ cm} \\times 1.5\\text{ cm}$ and length $0.5\\text{ m}$ made of steel ($E = 210 \\times 10^9\\text{ N/m}^2$) is approximately",
    "options": [
      "$10\\text{ kN}$",
      "$4\\text{ kN}$",
      "$23\\text{ kN}$",
      "$46\\text{ kN}$"
    ],
    "correctOption": "A"
  },
  # Q42
  {
    "id": "gate-2009-ae-ae-42",
    "questionNumber": 42,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A wing root cross section is idealized using lumped areas (booms) as shown below.\n\n<img src=\"figures/gate-2009-ae-ae-42-figure-1.png\" alt=\"Wing root cross section idealized using booms\" />\n\nThe wing root bending moment in steady level flight is $M_y = 10\\text{ N-m}$. If the airplane flies at a load factor $n = 3.5$, the maximum bending stress at the root is",
    "options": [
      "$1 \\times 10^6\\text{ N/m}^2$",
      "$3.5 \\times 10^6\\text{ N/m}^2$",
      "$7 \\times 10^6\\text{ N/m}^2$",
      "$0.286 \\times 10^6\\text{ N/m}^2$"
    ],
    "correctOption": "B"
  },
  # Q43
  {
    "id": "gate-2009-ae-ae-43",
    "questionNumber": 43,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A uniform rigid bar of mass $m = 1\\text{ kg}$ and length $L = 1\\text{ m}$ is pivoted at $A$. It is supported by a spring of stiffness $k = 1\\text{ N/m}$ and a viscous damper of damping constant $C = 1\\text{ N-s/m}$, with $a = 1/\\sqrt{3}\\text{ m}$ as shown below. The moment of inertia of the rigid bar is $I_A = \\frac{m L^2}{3}$.\n\n<img src=\"figures/gate-2009-ae-ae-43-figure-1.png\" alt=\"Pivoted rigid bar with spring and damper\" />\n\nThe system is",
    "options": [
      "overdamped",
      "underdamped with natural frequency $\\omega_n = 1\\text{ rad/s}$",
      "critically damped",
      "underdamped with natural frequency $\\omega_n = 2\\text{ rad/s}$"
    ],
    "correctOption": "B"
  },
  # Q44
  {
    "id": "gate-2009-ae-ae-44",
    "questionNumber": 44,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "A 2-celled tube with wall thickness $0.5\\text{ mm}$ is subjected to a torque of $10\\text{ N-m}$. The resulting shear flows in the two cells are $q_1$ and $q_2$ as shown below.\n\n<img src=\"figures/gate-2009-ae-ae-44-figure-1.png\" alt=\"2-celled tube with shear flows q1 and q2\" />\n\nThe torque balance equation (Bredt-Batho formula) for this section leads to",
    "options": [
      "$q_1 - q_2 = 2000\\text{ N/m}$",
      "$q_1 + 2q_2 = 2000\\text{ N/m}$",
      "$q_1 + q_2 = 2000\\text{ N/m}$",
      "$2q_1 + q_2 = 2000\\text{ N/m}$"
    ],
    "correctOption": "C"
  },
  # Q45
  {
    "id": "gate-2009-ae-ae-45",
    "questionNumber": 45,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The value of the integral $\\int_0^\\pi \\frac{dx}{1 + x + \\sin x}$ evaluated using the trapezoidal rule with two equal intervals is approximately",
    "options": [
      "$1.27$",
      "$1.81$",
      "$1.41$",
      "$0.71$"
    ],
    "correctOption": "C"
  },
  # Q46
  {
    "id": "gate-2009-ae-ae-46",
    "questionNumber": 46,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The product of the eigenvalues of the matrix $\\begin{bmatrix} 2 & 1 & 1 \\\\ 1 & 3 & 1 \\\\ 1 & 1 & 4 \\end{bmatrix}$ is",
    "options": [
      "$20$",
      "$24$",
      "$9$",
      "$17$"
    ],
    "correctOption": "D"
  },
  # Q47
  {
    "id": "gate-2009-ae-ae-47",
    "questionNumber": 47,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "In the interval $1 \\le x \\le 2$, the function $f(x) = e^{\\pi x} + \\sin\\pi x$ is",
    "options": [
      "maximum at $x = 1$",
      "maximum at $x = 2$",
      "maximum at $x = 1.5$",
      "monotonically decreasing"
    ],
    "correctOption": "B"
  },
  # Q48
  {
    "id": "gate-2009-ae-ae-48",
    "questionNumber": 48,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The inverse Laplace transform of $F(s) = \\frac{(s+1)}{(s+4)(s-3)}$ is",
    "options": [
      "\\(\\frac{3}{7} e^{4t} + \\frac{4}{7} e^{-3t}\\)",
      "\\(\\frac{3}{7} e^{-4t} + \\frac{4}{7} e^{3t}\\)",
      "\\(\\frac{5}{7} e^{-4t} + \\frac{6}{7} e^{3t}\\)",
      "\\(\\frac{5}{7} e^{4t} + \\frac{6}{7} e^{-3t}\\)"
    ],
    "correctOption": "B"
  },
  # Q49
  {
    "id": "gate-2009-ae-ae-49",
    "questionNumber": 49,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The linear system of equations $\\mathbf{Ax} = \\mathbf{b}$ where $\\mathbf{A} = \\begin{bmatrix} 1 & 2 \\\\ 2 & 4 \\end{bmatrix}$ and $\\mathbf{b} = \\begin{Bmatrix} 3 \\\\ 3 \\end{Bmatrix}$ has",
    "options": [
      "no solution",
      "infinitely many solutions",
      "a unique solution $\\mathbf{x} = \\begin{Bmatrix} 1 \\\\ 1 \\end{Bmatrix}$",
      "a unique solution $\\mathbf{x} = \\begin{Bmatrix} 0.5 \\\\ 0.5 \\end{Bmatrix}$"
    ],
    "correctOption": "A"
  },
  # Q50
  {
    "id": "gate-2009-ae-ae-50",
    "questionNumber": 50,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "question": "The correct iterative scheme for finding the square root of a positive real number $R$ using the Newton Raphson method is",
    "options": [
      "$x_{n+1} = \\sqrt{R}$",
      "$x_{n+1} = \\frac{1}{2} \\left( x_n + \\frac{R}{x_n} \\right)$",
      "$x_{n+1} = \\frac{1}{2} \\left( \\sqrt{x_n} + \\sqrt{x_{n-1}} \\right)$",
      "$x_{n+1} = \\frac{1}{2} (\\sqrt{R} + x_n)$"
    ],
    "correctOption": "B"
  },
  # Q51
  {
    "id": "gate-2009-ae-ae-51",
    "questionNumber": 51,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "The roots of the characteristic equation for the longitudinal dynamics of a certain aircraft are: $\\lambda_1 = -0.02 + 0.2i;\\; \\lambda_2 = -0.02 - 0.2i;\\; \\lambda_3 = -2.5 + 2.6i;\\; \\lambda_4 = -2.5 - 2.6i$, where $i = \\sqrt{-1}$.",
    "question": "The pair of eigenvalues that represent the phugoid mode is",
    "options": [
      "$\\lambda_1$ and $\\lambda_3$",
      "$\\lambda_2$ and $\\lambda_4$",
      "$\\lambda_3$ and $\\lambda_4$",
      "$\\lambda_1$ and $\\lambda_2$"
    ],
    "correctOption": "D"
  },
  # Q52
  {
    "id": "gate-2009-ae-ae-52",
    "questionNumber": 52,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "The roots of the characteristic equation for the longitudinal dynamics of a certain aircraft are: $\\lambda_1 = -0.02 + 0.2i;\\; \\lambda_2 = -0.02 - 0.2i;\\; \\lambda_3 = -2.5 + 2.6i;\\; \\lambda_4 = -2.5 - 2.6i$, where $i = \\sqrt{-1}$.",
    "question": "The short period damped frequency is",
    "options": [
      "$2.6\\text{ rad/s}$",
      "$0.2\\text{ rad/s}$",
      "$2.5\\text{ rad/s}$",
      "$0.02\\text{ rad/s}$"
    ],
    "correctOption": "A"
  },
  # Q53
  {
    "id": "gate-2009-ae-ae-53",
    "questionNumber": 53,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "Consider the vector field $\\vec{A} = (y^3 + z^3)\\hat{i} + (x^3 + z^3)\\hat{j} + (x^3 + y^3)\\hat{k}$ defined over the unit sphere $x^2 + y^2 + z^2 = 1$.",
    "question": "The surface integral (taken over the unit sphere) of the component of $\\vec{A}$ normal to the surface is",
    "options": [
      "$\\pi$",
      "$1$",
      "$0$",
      "$4\\pi$"
    ],
    "correctOption": "C"
  },
  # Q54
  {
    "id": "gate-2009-ae-ae-54",
    "questionNumber": 54,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "Consider the vector field $\\vec{A} = (y^3 + z^3)\\hat{i} + (x^3 + z^3)\\hat{j} + (x^3 + y^3)\\hat{k}$ defined over the unit sphere $x^2 + y^2 + z^2 = 1$.",
    "question": "The magnitude of the component of $\\vec{A}$ normal to the spherical surface at the point $\\left( \\frac{1}{\\sqrt{3}}, \\frac{1}{\\sqrt{3}}, \\frac{1}{\\sqrt{3}} \\right)$ is",
    "options": [
      "\\(\\frac{1}{3}\\)",
      "\\(\\frac{2}{3}\\)",
      "\\(\\frac{3}{3}\\)",
      "\\(\\frac{4}{3}\\)"
    ],
    "correctOption": "B"
  },
  # Q55
  {
    "id": "gate-2009-ae-ae-55",
    "questionNumber": 55,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "The partial differential equation for the torsional vibration of a shaft of length $L$, torsional rigidity $GJ$, and mass polar moment of inertia per unit length $I$, is $I \\frac{\\partial^2 \\theta}{\\partial t^2} = GJ \\frac{\\partial^2 \\theta}{\\partial x^2}$, where $\\theta$ is the twist.",
    "question": "If the shaft is fixed at both ends, the boundary conditions are:",
    "options": [
      "\\(\\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=0} = 0 \\text{ and } \\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=L} = 0\\)",
      "\\(\\theta(0) = 0 \\text{ and } \\theta(L) = 0\\)",
      "\\(\\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=0} = 0 \\text{ and } \\theta(L) = 0\\)",
      "\\(\\theta(0) = 0 \\text{ and } \\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=L} = 0\\)"
    ],
    "correctOption": "B"
  },
  # Q56
  {
    "id": "gate-2009-ae-ae-56",
    "questionNumber": 56,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "commonData": "The partial differential equation for the torsional vibration of a shaft of length $L$, torsional rigidity $GJ$, and mass polar moment of inertia per unit length $I$, is $I \\frac{\\partial^2 \\theta}{\\partial t^2} = GJ \\frac{\\partial^2 \\theta}{\\partial x^2}$, where $\\theta$ is the twist.",
    "question": "If the $n^{\\text{th}}$ mode shape of torsional vibration of the above shaft is $\\sin\\left(\\frac{n\\pi x}{L}\\right)$ then the $n^{\\text{th}}$ natural frequency of vibration, i.e., $\\omega_n$, is given by",
    "options": [
      "\\(\\omega_n = \\frac{n\\pi}{L} \\sqrt{\\frac{GJ}{I}}\\)",
      "\\(\\omega_n = \\frac{(2n+1)\\pi}{2L} \\sqrt{\\frac{GJ}{I}}\\)",
      "\\(\\omega_n = \\frac{n\\pi}{2L} \\sqrt{\\frac{GJ}{I}}\\)",
      "\\(\\omega_n = \\frac{(2n+1)\\pi}{L} \\sqrt{\\frac{GJ}{I}}\\)"
    ],
    "correctOption": "A"
  },
  # Q57
  {
    "id": "gate-2009-ae-ae-57",
    "questionNumber": 57,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "linkedStatement": "Air enters the combustor of a gas-turbine engine at a total temperature $T_0$ of $500\\text{ K}$. The air stream is split into two parts: primary and secondary streams. The primary stream reacts with fuel supplied at a fuel-air ratio of $0.05$. The resulting combustion products are then mixed with the secondary air stream to obtain gas with total temperature of $1550\\text{ K}$ at the turbine inlet. The fuel has a heating value of $42\\text{ MJ/kg}$. The specific heats of air and combustion products are taken as $c_p = 1\\text{ kJ/kg/K}$.",
    "question": "If the sensible enthalpy of fuel is neglected, the temperature of combustion products from the reaction of primary air stream with fuel is approximately",
    "options": [
      "$2100\\text{ K}$",
      "$3200\\text{ K}$",
      "$2600\\text{ K}$",
      "$1800\\text{ K}$"
    ],
    "correctOption": "C"
  },
  # Q58
  {
    "id": "gate-2009-ae-ae-58",
    "questionNumber": 58,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0,
    "dependsOn": "gate-2009-ae-ae-57",
    "linkedStatement": "Air enters the combustor of a gas-turbine engine at a total temperature $T_0$ of $500\\text{ K}$. The air stream is split into two parts: primary and secondary streams. The primary stream reacts with fuel supplied at a fuel-air ratio of $0.05$. The resulting combustion products are then mixed with the secondary air stream to obtain gas with total temperature of $1550\\text{ K}$ at the turbine inlet. The fuel has a heating value of $42\\text{ MJ/kg}$. The specific heats of air and combustion products are taken as $c_p = 1\\text{ kJ/kg/K}$.",
    "question": "The approximate ratio of mass flow rates of the primary air stream to the secondary air stream required to achieve the turbine inlet total temperature of $1550\\text{ K}$ is",
    "options": [
      "$2:1$",
      "$1:2$",
      "$1:1.5$",
      "$1:1$"
    ],
    "correctOption": "D"
  },
  # Q59
  {
    "id": "gate-2009-ae-ae-59",
    "questionNumber": 59,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0.6666666666666666,
    "linkedStatement": "A piston compresses $1\\text{ kg}$ of air inside a cylinder as shown\n\n<img src=\"figures/gate-2009-ae-ae-59-figure-1.png\" alt=\"Piston compresses air inside cylinder\" />\n\nThe rate at which the piston does work on the air is $3000\\text{ W}$. At the same time, heat is being lost through the walls of the cylinder at a rate of $847.5\\text{ W}$.",
    "question": "After 10 seconds, the change in specific internal energy of the air is",
    "options": [
      "$21,525\\text{ J/kg}$",
      "$-21,525\\text{ J/kg}$",
      "$30,000\\text{ J/kg}$",
      "$-8,475\\text{ J/kg}$"
    ],
    "correctOption": "A"
  },
  # Q60
  {
    "id": "gate-2009-ae-ae-60",
    "questionNumber": 60,
    "section": "ae",
    "type": "MCQ",
    "marks": 2,
    "negativeMarks": 0,
    "dependsOn": "gate-2009-ae-ae-59",
    "linkedStatement": "A piston compresses $1\\text{ kg}$ of air inside a cylinder as shown\n\n<img src=\"figures/gate-2009-ae-ae-59-figure-1.png\" alt=\"Piston compresses air inside cylinder\" />\n\nThe rate at which the piston does work on the air is $3000\\text{ W}$. At the same time, heat is being lost through the walls of the cylinder at a rate of $847.5\\text{ W}$.",
    "question": "Given that the specific heats of air at constant pressure and volume are $c_p = 1004.5\\text{ J/kg-K}$ and $c_v = 717.5\\text{ J/kg-K}$ respectively, the corresponding change in the temperature of the air is",
    "options": [
      "$21.4\\text{ K}$",
      "$-21.4\\text{ K}$",
      "$30\\text{ K}$",
      "$-30\\text{ K}$"
    ],
    "correctOption": "C"
  }
]

paper["questions"] = questions

with open("data/ae/2009.json", "w", encoding="utf-8") as f:
    json.dump(paper, f, indent=2)

print(f"data/ae/2009.json successfully created with {len(questions)} questions.")
