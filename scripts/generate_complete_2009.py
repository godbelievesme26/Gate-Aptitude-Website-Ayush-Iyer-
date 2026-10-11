import json
import hashlib

def get_sha256(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

paper_sha = get_sha256('internal/ae/AE2009.pdf')
key_sha = get_sha256('internal/ae/AE2009-key.pdf')

q_order = [f"gate-2009-ae-ae-{i:02d}" for i in range(1, 61)]
q_refs = [{"id": f"gate-2009-ae-ae-{i:02d}", "number": i, "section": "AE", "type": "MCQ"} for i in range(1, 61)]

groups = [
    {
        "id": "common-data-51-52",
        "type": "common-data",
        "title": "Common Data for Questions 51 and 52",
        "content": [
            {
                "type": "text",
                "text": "Common Data for Questions 51 and 52:\nThe roots of the characteristic equation for the longitudinal dynamics of a certain aircraft are: $\\lambda_1 = -0.02 + 0.2i;\\; \\lambda_2 = -0.02 - 0.2i;\\; \\lambda_3 = -2.5 + 2.6i;\\; \\lambda_4 = -2.5 - 2.6i$, where $i = \\sqrt{-1}$."
            }
        ],
        "questionIds": [
            "gate-2009-ae-ae-51",
            "gate-2009-ae-ae-52"
        ]
    },
    {
        "id": "common-data-53-54",
        "type": "common-data",
        "title": "Common Data for Questions 53 and 54",
        "content": [
            {
                "type": "text",
                "text": "Common Data for Questions 53 and 54:\nConsider the vector field $\\vec{A} = (y^3 + z^3)\\hat{i} + (x^3 + z^3)\\hat{j} + (x^3 + y^3)\\hat{k}$ defined over the unit sphere $x^2 + y^2 + z^2 = 1$."
            }
        ],
        "questionIds": [
            "gate-2009-ae-ae-53",
            "gate-2009-ae-ae-54"
        ]
    },
    {
        "id": "common-data-55-56",
        "type": "common-data",
        "title": "Common Data for Questions 55 and 56",
        "content": [
            {
                "type": "text",
                "text": "Common Data for Questions 55 and 56:\nThe partial differential equation for the torsional vibration of a shaft of length $L$, torsional rigidity $GJ$, and mass polar moment of inertia per unit length $I$, is $I \\frac{\\partial^2 \\theta}{\\partial t^2} = GJ \\frac{\\partial^2 \\theta}{\\partial x^2}$, where $\\theta$ is the twist."
            }
        ],
        "questionIds": [
            "gate-2009-ae-ae-55",
            "gate-2009-ae-ae-56"
        ]
    },
    {
        "id": "linked-answer-57-58",
        "type": "linked-answer",
        "title": "Statement for Linked Answer Questions 57 and 58",
        "content": [
            {
                "type": "text",
                "text": "Statement for Linked Answer Questions 57 and 58:\nAir enters the combustor of a gas-turbine engine at a total temperature $T_0$ of $500\\text{ K}$. The air stream is split into two parts: primary and secondary streams. The primary stream reacts with fuel supplied at a fuel-air ratio of $0.05$. The resulting combustion products are then mixed with the secondary air stream to obtain gas with total temperature of $1550\\text{ K}$ at the turbine inlet. The fuel has a heating value of $42\\text{ MJ/kg}$. The specific heats of air and combustion products are taken as $c_p = 1\\text{ kJ/kg/K}$."
            }
        ],
        "questionIds": [
            "gate-2009-ae-ae-57",
            "gate-2009-ae-ae-58"
        ],
        "dependencies": [
            {
                "questionId": "gate-2009-ae-ae-58",
                "dependsOn": "gate-2009-ae-ae-57"
            }
        ]
    },
    {
        "id": "linked-answer-59-60",
        "type": "linked-answer",
        "title": "Statement for Linked Answer Questions 59 and 60",
        "content": [
            {
                "type": "text",
                "text": "Statement for Linked Answer Questions 59 and 60:\nA piston compresses $1\\text{ kg}$ of air inside a cylinder as shown below.\nThe rate at which the piston does work on the air is $3000\\text{ W}$. At the same time, heat is being lost through the walls of the cylinder at a rate of $847.5\\text{ W}$."
            }
        ],
        "questionIds": [
            "gate-2009-ae-ae-59",
            "gate-2009-ae-ae-60"
        ],
        "dependencies": [
            {
                "questionId": "gate-2009-ae-ae-60",
                "dependsOn": "gate-2009-ae-ae-59"
            }
        ]
    }
]

paper_data = {
    "schemaVersion": 1,
    "id": "gate-2009-ae",
    "exam": "GATE",
    "year": 2009,
    "paper": "AE",
    "title": "GATE 2009 Aerospace Engineering (AE)",
    "durationMinutes": 180,
    "totalMarks": 100,
    "totalQuestions": 60,
    "sectionOrder": ["AE"],
    "sections": [
        {
            "id": "AE",
            "title": "Aerospace Engineering",
            "totalQuestions": 60,
            "totalMarks": 100,
            "questionIds": q_order
        }
    ],
    "questionOrder": q_order,
    "questionRefs": q_refs,
    "questionGroups": groups,
    "marking": {
        "negativeFraction": {
            "MCQ": 0.3333333333333333,
            "MSQ": 0,
            "NAT": 0
        }
    },
    "source": {
        "paper": "AE",
        "year": 2009,
        "file": "internal/ae/AE2009.pdf",
        "sha256": paper_sha,
        "keyFile": "internal/ae/AE2009-key.pdf",
        "keySha256": key_sha
    },
    "questions": []
}

raw_questions = [
  # 1
  (1, 1, "For a flow through a Prandtl-Meyer expansion wave",
   ["Mach number stays constant.", "Entropy stays constant.", "Temperature stays constant.", "Density stays constant."],
   "B", 2, None, []),
  # 2
  (2, 1, "For two-dimensional irrotational and incompressible flows",
   ["Both potential and stream functions satisfy the Laplace equation.", "Potential function must satisfy the Laplace equation but the stream function need not.", "Stream function must satisfy the Laplace equation but the potential function need not.", "Neither the stream function nor the potential function need to satisfy the Laplace equation."],
   "A", 2, None, []),
  # 3
  (3, 1, "A trailing edge plain flap deflected downward increases the lift coefficient of an airfoil by",
   ["Increasing the effective camber of the airfoil.", "Delaying the separation of the flow from the airfoil surface.", "Increasing the local airspeed near the trailing edge.", "Controlling the growth of the boundary layer thickness along the airfoil surface."],
   "A", 2, None, []),
  # 4
  (4, 1, "Thin airfoil theory predicts that the lift slope is $\\frac{dc_l}{d\\alpha} = 2\\pi$ for",
   ["Symmetric airfoils only.", "Cambered airfoils only.", "Any airfoil shape.", "Joukowski airfoils only."],
   "C", 2, None, []),
  # 5
  (5, 1, "The ordinary differential equation $\\frac{d^2 y}{dx^2} + ky = 0$ where $k$ is real and positive",
   ["is non-linear", "has a characteristic equation with one real and one complex root", "has a characteristic equation with two real roots", "has a complementary function that is simple harmonic"],
   "D", 2, None, []),
  # 6
  (6, 1, "A non-trivial solution to the $(n \\times n)$ system of equations $[A]\\{x\\} = \\{0\\}$, where $\\{0\\}$ is the null vector",
   ["can never be found", "may be found only if $[A]$ is not singular", "may be found only if $[A]$ is an orthogonal matrix", "may be found only if $[A]$ has at least one eigenvalue equal to zero"],
   "D", 2, None, []),
  # 7
  (7, 1, "For a plane strain problem, the stresses satisfy the condition",
   ["$\\tau_{xz} = \\tau_{yz} = \\sigma_z = 0$", "$\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu(\\sigma_x + \\sigma_y)$", "$\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu\\tau_{xy}$", "$\\tau_{xz} = \\tau_{yz} = 0,\\; \\sigma_z = \\nu(\\sigma_x + \\sigma_y) + (1-\\nu)\\tau_{xy}$"],
   "B", 2, None, []),
  # 8
  (8, 1, "The propulsive efficiency of a turbo-jet engine moving at velocity $U_\\infty$ and having exhaust velocity $U_e$ with respect to the engine is given by",
   ["$\\frac{2}{U_\\infty / U_e + 1}$", "$1 - \\frac{U_\\infty}{U_e}$", "$\\frac{2 U_\\infty U_e}{U_e^2 + U_\\infty^2}$", "$\\frac{2 U_\\infty}{U_e + U_\\infty}$"],
   "D", 3, None, []),
  # 9
  (9, 1, "An aircraft is flying at $M = 2$ where the ambient temperature around the aircraft is $250\\text{ K}$. If the specific heat ratio for air $\\gamma = 1.4$, the stagnation temperature on the surface of the aircraft is",
   ["$200\\text{ K}$", "$450\\text{ K}$", "$350\\text{ K}$", "$1450\\text{ K}$"],
   "B", 3, None, []),
  # 10
  (10, 1, "The division of feed air to an aircraft gas-turbine combustor into primary and secondary streams serves which of the following purposes ?\n\nP. a flammable mixture can be formed\nQ. cooling of combustor liner and flame tube can be accomplished\nR. specific fuel consumption can be reduced",
   ["P and R", "Q and R", "P and Q", "P, Q and R"],
   "C", 3, None, []),
  # 11
  (11, 1, "Classify the following propellants as: cryogenic (C) , semi-cryogenic (SC), compressed gas (CG) and earth storable (ES)\n\n$\\text{N}_2\\text{O}_4\\text{-UDMH}$ (nitrogen tetra oxide and unsymmetrical di-methyl hydrazine)\nLOX-RP1 (liquid oxygen and kerosene)\n$\\text{LOX-LH}_2$ (liquid oxygen and liquid hydrogen)\n$\\text{N}_2$ (nitrogen gas)",
   ["$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (C)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (C)}$",
    "$\\text{N}_2\\text{O}_4\\text{-UDMH (SC)}, \\quad \\text{LOX-RP1 (SC)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (C)}$",
    "$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (SC)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (CG)}$",
    "$\\text{N}_2\\text{O}_4\\text{-UDMH (ES)}, \\quad \\text{LOX-RP1 (C)}, \\quad \\text{LOX-LH}_2\\text{ (C)}, \\quad \\text{N}_2\\text{ (CG)}$"],
   "C", 3, None, []),
  # 12
  (12, 1, "A conventional altimeter is a",
   ["Pressure transducer", "Temperature transducer", "Density transducer", "Velocity transducer"],
   "A", 3, None, []),
  # 13
  (13, 1, "The relation between an airplane's true airspeed $V_{\\text{TAS}}$ and equivalent airspeed $V_{\\text{EAS}}$ in terms of the density ratio ($\\sigma = \\frac{\\rho}{\\rho_0}$), where $\\rho_0$ is the air density at sea-level and $\\rho$ is the air density at the altitude at which the airplane is flying, is given by the formula:",
   ["$\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sigma$", "$\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sigma^2$", "$\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\sqrt{\\sigma}$", "$\\frac{V_{\\text{EAS}}}{V_{\\text{TAS}}} = \\frac{1}{\\sqrt{\\sigma}}$"],
   "C", 3, None, []),
  # 14
  (14, 1, "An unswept fixed-winged aircraft has a large roll stability if the wing is placed",
   ["low on the fuselage and has negative dihedral angle", "low on the fuselage and has positive dihedral angle", "high on the fuselage and has negative dihedral angle", "high on the fuselage and has positive dihedral angle"],
   "B", 4, None, []),
  # 15
  (15, 1, "Thrust available from a turbojet engine",
   ["increases as altitude increases", "increases up to the tropopause and then decreases", "remains constant at all altitudes", "decreases as altitude increases"],
   "D", 4, None, []),
  # 16
  (16, 1, "If $C_{m_{\\text{CG}}}$ is the pitching moment coefficient about the center of gravity of an aircraft, and $\\alpha$ is the angle of attack, then $\\frac{dC_{m_{\\text{CG}}}}{d\\alpha}$ is",
   ["a stability derivative which represents stiffness in pitch", "a stability derivative which represents damping in pitch", "a control derivative in pitch", "positive for an aircraft that is stable in pitch"],
   "A", 4, None, []),
  # 17
  (17, 1, "The life of a geo-stationary communications satellite is limited by",
   ["the working life of the on-board electronic circuitry", "the time it takes for its orbit to decay due to atmospheric drag", "the quantity of on-board fuel available for station-keeping", "the number of meteorite impacts that the satellite structure can withstand before breaking up"],
   "C", 4, None, []),
  # 18
  (18, 1, "For a critically damped single degree of freedom spring - mass - damper system with a damping constant $c$ of $4\\text{ Ns/m}$ and spring constant $k$ of $16\\text{ N/m}$, the system mass $m$ is",
   ["$0.5\\text{ kg}$", "$0.25\\text{ kg}$", "$2\\text{ kg}$", "$4\\text{ kg}$"],
   "B", 4, None, []),
  # 19
  (19, 1, "In a thin walled rectangular tube subjected to equal and opposite forces $P$ as shown in the figure, the shear stress along leg AB is",
   ["zero", "constant non-zero", "varies linearly", "varies parabolically"],
   "B", 4, None, ["figures/gate-2009-ae-ae-19-figure-1.png"]),
  # 20
  (20, 1, "For the thin walled beam cross section as shown in the figure, the shear centre lies at",
   ["Mid point of AB, i.e. at point $E$", "Mid point of BD, i.e. at point $F$", "Junction point $B$", "at a point $G$ lying within the area $ABC$"],
   "C", 5, None, ["figures/gate-2009-ae-ae-20-figure-1.png"]),
  # 21
  (21, 2, "Let $M_0$ be the total mass of a single stage rocket, $M_p$ be the total mass of propellant, $M_L$ be the mass of payload carried by the rocket and $M_S$ be the mass of inert structural components. If $I_{sp}$ is the specific impulse of the propulsion system (in seconds) and $g$ is the acceleration due to gravity, then the maximum velocity that can be attained by the rocket vehicle in the absence of gravity and atmospheric drag is given by",
   ["$g I_{sp} \\ln \\left( \\frac{M_0}{M_p} \\right)$", "$g I_{sp} \\ln \\left( \\frac{M_0}{M_L + M_S} - 1 \\right)$", "$g I_{sp} \\ln \\left( \\frac{M_0}{M_S} \\right)$", "$g I_{sp} \\ln \\left( \\frac{M_0}{M_0 - M_p} \\right)$"],
   "D", 5, None, []),
  # 22
  (22, 2, "An ideal axial compressor is driven by an ideal turbine across which the total temperature ratio is $0.667$. If the total temperature at turbine inlet is $T_0 = 1500\\text{ K}$ and specific heat of gas $c_p = 1\\text{ kJ/kg/K}$, the power drawn by the compressor per unit mass flow rate of air is approximately",
   ["$300\\text{ kW/kg/s}$", "$1000\\text{ kW/kg/s}$", "$600\\text{ kW/kg/s}$", "$500\\text{ kW/kg/s}$"],
   "D", 5, None, []),
  # 23
  (23, 2, "The performance of a solid rocket motor is improved by replacing the old propellant with a new one. The new propellant gives a combustion temperature $40\\%$ higher than the previous propellant without appreciable change in molecular weight of combustion products and other operating parameters. By approximately what percentage is the specific impulse of the new motor higher than the old one ?",
   ["$18\\%$", "$96\\%$", "$42\\%$", "$112\\%$"],
   "A", 5, None, []),
  # 24
  (24, 2, "A solid rocket motor has an end burning grain of cross-sectional area $A_{cs} = 0.4\\text{ m}^2$. The density of propellant is $\\rho_p = 1500\\text{ kg/m}^3$ and has linear regression rate $\\dot{r} = 5\\text{ mm/s}$. If the specific impulse of the propulsion system is $I_{sp} = 200\\text{ seconds}$, the thrust produced by the motor is approximately",
   ["$3\\text{ kN}$", "$6\\text{ kN}$", "$1.5\\text{ kN}$", "$12\\text{ kN}$"],
   "B", 5, None, []),
  # 25
  (25, 2, "An ideal ramjet is flying at an altitude of $10\\text{ km}$ with a velocity of $1\\text{ km/s}$. The ambient pressure is $0.25\\text{ bar}$ and temperature is $225\\text{ K}$. The exhaust gases from the engine are optimally expanded and leave the nozzle at $900\\text{ K}$. If the specific heat ratio ($\\gamma$) remains constant, the specific thrust developed by the engine is approximately",
   ["$1000\\text{ N-s/kg}$", "$2000\\text{ N-s/kg}$", "$500\\text{ N-s/kg}$", "$4000\\text{ N-s/kg}$"],
   "A", 6, None, []),
  # 26
  (26, 2, "A combat aircraft engine is equipped with an afterburner followed by a variable area convergent nozzle (operating with the nozzle choked). The exhaust gas temperature is $750\\text{ K}$ when afterburner is off and $3000\\text{ K}$ when it is on. When the afterburner is turned on, (assuming the total pressure remains the same, the mass of fuel added in the afterburner is negligible i.e., the mass flow rate remains the same, and the specific heat ratio ($\\gamma$) remains constant), approximately by what factor must the nozzle area be changed ?",
   ["$0.5$", "$4$", "$1$", "$2$"],
   "D", 6, None, []),
  # 27
  (27, 2, "An airplane flying at $100\\text{ m/s}$ is pitching at the rate of $0.2\\text{ deg/s}$. Due to this pitching, the horizontal tail surface located $4\\text{ metres}$ behind the centre-of-mass of the airplane will experience a change in angle of attack, which is",
   ["$0.01\\text{ deg}$", "$0.008\\text{ deg}$", "$0.04\\text{ deg}$", "$0.004\\text{ deg}$"],
   "B", 6, None, []),
  # 28
  (28, 2, "The contribution of the horizontal tail to the pitching moment coefficient about the center of gravity ($C_{m_{\\text{CG}}}$) of an aircraft is given by $C_{m_{\\text{tail}}} = 0.2 - 0.0215\\,\\alpha$, where $\\alpha$ is the angle of attack of the aircraft. The contribution of the tail to the aircraft longitudinal stability",
   ["is stabilizing", "is destabilizing", "is nil", "cannot be determined from the given information"],
   "A", 6, None, []),
  # 29
  (29, 2, "The linearized dynamics of an aircraft (which has no large rotating components) in straight and level flight is governed by the equations\n\n$$\\frac{d\\vec{x}}{dt} = \\begin{bmatrix} [A] & [B] \\\\ [C] & [D] \\end{bmatrix} \\vec{x}$$\n\nwhere $\\vec{x} = \\begin{bmatrix} u & w & q & \\theta & v & p & r & \\phi \\end{bmatrix}^T$, $[\\;]^T$ represents the transpose of a matrix, $[A], [B], [C]$ and $[D]$ are $4\\times 4$ matrices and $[0]$ is the $4\\times 4$ null matrix. Which of the following is true ?",
   ["$[A] \\neq [0];\\; [B] \\neq [0];\\; [C] = [0];\\; [D] \\neq [0]$", "$[A] = [0];\\; [B] \\neq [0];\\; [C] \\neq [0];\\; [D] = [0]$", "$[A] \\neq [0];\\; [B] = [0];\\; [C] = [0];\\; [D] \\neq [0]$", "$[A] \\neq [0];\\; [B] = [0];\\; [C] \\neq [0];\\; [D] = [0]$"],
   "C", 6, None, []),
  # 30
  (30, 2, "The velocity vector of an aircraft along its body-fixed axis is given by $\\vec{V} = \\begin{Bmatrix} u \\\\ v \\\\ w \\end{Bmatrix}$. If $V$ is the magnitude of $\\vec{V}$, $\\alpha$ is the angle of attack and $\\beta$ is the angle of sideslip, which of the following set of relations is correct ?",
   ["$u = V\\sin\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$", "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\cos\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$", "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\sin\\beta\\sin\\alpha$", "$u = V\\cos\\beta\\cos\\alpha;\\quad v = V\\sin\\beta;\\quad w = V\\cos\\beta\\sin\\alpha$"],
   "D", 7, None, []),
  # 31
  (31, 2, "An aircraft of mass $2500\\text{ kg}$ in straight and level flight at a constant speed of $100\\text{ m/s}$ has available excess power of $1.0 \\times 10^6\\text{ W}$. The steady rate of climb it can attain at that speed is",
   ["$100\\text{ m/s}$", "$60\\text{ m/s}$", "$40\\text{ m/s}$", "$20\\text{ m/s}$"],
   "C", 7, None, []),
  # 32
  (32, 2, "The acceleration due to gravity on the surface of Mars is $0.385$ times that on earth, and the diameter of Mars is $0.532$ times that of earth. The ratio of the escape velocity from the surface of Mars to the escape velocity from the surface of earth is approximately",
   ["$0.453$", "$0.205$", "$0.851$", "$0.724$"],
   "A", 7, None, []),
  # 33
  (33, 2, "Which of the following statements are true for flow across a stationary normal shock ?\n\nP. Stagnation temperature stays constant.\nQ. Stagnation pressure decreases.\nR. Entropy increases.\nS. Stagnation pressure increases.\nT. Stagnation temperature increases.",
   ["P, Q, R", "Q, R, S", "R, S, T", "S, T, P"],
   "A", 7, None, []),
  # 34
  (34, 2, "A model airfoil in a wind tunnel that is operating at $50\\text{ m/s}$ develops a minimum pressure co-efficient of $-6.29$ at some point on its upper surface. The local airspeed at that point is",
   ["$50\\text{ m/s}$", "$125\\text{ m/s}$", "$135\\text{ m/s}$", "$150\\text{ m/s}$"],
   "C", 7, None, []),
  # 35
  (35, 2, "A symmetrical airfoil section produces a lift coefficient of $0.53$ at an angle of attack of $5\\text{ degrees}$ measured from its chord line. An untwisted wing of elliptical planform and aspect ratio $6$ is made of this airfoil. At an angle of attack of $5\\text{ degrees}$ relative to its chordal plane, this wing would produce a lift coefficient of",
   ["$0.53$", "$0.48$", "$0.40$", "$0.36$"],
   "C", 7, None, []),
  # 36
  (36, 2, "Consider an ideal flow of density $\\rho$ through a variable area duct as shown in the figure below :\n\nLet the cross-sectional areas at sections (1) and (2) be $A_1$ and $A_2$ respectively. The velocity measured at section (1) using a Pitot static probe is $V_1$. Then the static pressure drop $p_2 - p_1$ is",
   ["$-\\frac{1}{2}\\rho\\left(1 - \\frac{A_1^2}{A_2^2}\\right)V_1^2$", "$\\frac{1}{2}\\rho\\left(1 - \\frac{A_1^2}{A_2^2}\\right)V_1^2$", "$\\frac{1}{2}\\rho\\left(1 + \\frac{A_1^2}{A_2^2}\\right)V_1^2$", "$-\\frac{1}{2}\\rho\\left(1 + \\frac{A_1^2}{A_2^2}\\right)V_1^2$"],
   "B", 8, None, ["figures/gate-2009-ae-ae-36-figure-1.png"]),
  # 37
  (37, 2, "Two vortices of the same strength and sign are placed a distance $d$ apart as shown below. Assume that the vortices are free to move and the fluid is ideal.\n\nWhich of the following statements is true ?",
   ["Vortices 1 and 2 spiral inwards with an initial angular speed $\\frac{\\Gamma}{2\\pi d^2}$ to finally merge and form one vortex of twice the strength.", "Vortices 1 and 2 spiral inwards with an initial angular speed $\\frac{\\Gamma}{\\pi d^2}$ to finally merge and form one vortex of twice the strength.", "Vortices 1 and 2 perpetually revolve about the midpoint $P$ with radius of revolution $\\frac{d}{2}$ and angular speed $\\frac{\\Gamma}{2\\pi d^2}$.", "Vortices 1 and 2 perpetually revolve about the midpoint $P$ with radius of revolution $\\frac{d}{2}$ and angular speed $\\frac{\\Gamma}{\\pi d^2}$."],
   "D", 8, None, ["figures/gate-2009-ae-ae-37-figure-1.png"]),
  # 38
  (38, 2, "The laminar boundary layer over a large flat plate held parallel to the flow is $7.2\\text{ mm}$ thick at a point $0.33\\text{ m}$ downstream of the leading edge. If the free stream speed is increased by $50\\%$, then the new boundary layer thickness at this location will be approximately",
   ["$10.8\\text{ mm}$", "$8.8\\text{ mm}$", "$5.9\\text{ mm}$", "$4.8\\text{ mm}$"],
   "C", 8, None, []),
  # 39
  (39, 2, "Consider a simply supported beam of length $2L$ with an overhang of length $L$, loaded by an end moment $M$, as shown below.\n\nThe bending moment distribution for this beam is shown in options (A) to (D) below:",
   ["Diagram (A)", "Diagram (B)", "Diagram (C)", "Diagram (D)"],
   "B", 9, None, ["figures/gate-2009-ae-ae-39-figure-1.png", "figures/gate-2009-ae-ae-39-figure-2.png"]),
  # 40
  (40, 2, "For the spring-mass system shown below, the natural frequencies are",
   ["$0\\text{ and }\\sqrt{\\frac{k(m_1 + m_2)}{m_1 m_2}}$", "$0\\text{ and }\\sqrt{\\frac{k(m_1 + m_2)}{2m_1 m_2}}$", "$0\\text{ and }\\sqrt{\\frac{k}{(m_1 + m_2)}}$", "$0\\text{ and }\\sqrt{\\frac{k}{2(m_1 + m_2)}}$"],
   "A", 9, None, ["figures/gate-2009-ae-ae-40-figure-1.png"]),
  # 41
  (41, 2, "The buckling load for a simply supported column of rectangular cross section of dimensions $1\\text{ cm} \\times 1.5\\text{ cm}$ and length $0.5\\text{ m}$ made of steel ($E = 210 \\times 10^9\\text{ N/m}^2$) is approximately",
   ["$10\\text{ kN}$", "$4\\text{ kN}$", "$23\\text{ kN}$", "$46\\text{ kN}$"],
   "A", 9, None, []),
  # 42
  (42, 2, "A wing root cross section is idealized using lumped areas (booms) as shown below.\n\nThe wing root bending moment in steady level flight is $M_y = 10\\text{ N-m}$. If the airplane flies at a load factor $n = 3.5$, the maximum bending stress at the root is",
   ["$1 \\times 10^6\\text{ N/m}^2$", "$3.5 \\times 10^6\\text{ N/m}^2$", "$7 \\times 10^6\\text{ N/m}^2$", "$0.286 \\times 10^6\\text{ N/m}^2$"],
   "B", 10, None, ["figures/gate-2009-ae-ae-42-figure-1.png"]),
  # 43
  (43, 2, "A uniform rigid bar of mass $m = 1\\text{ kg}$ and length $L = 1\\text{ m}$ is pivoted at $A$. It is supported by a spring of stiffness $k = 1\\text{ N/m}$ and a viscous damper of damping constant $C = 1\\text{ N-s/m}$, with $a = 1/\\sqrt{3}\\text{ m}$ as shown below. The moment of inertia of the rigid bar is $I_A = \\frac{m L^2}{3}$.\n\nThe system is",
   ["overdamped", "underdamped with natural frequency $\\omega_n = 1\\text{ rad/s}$", "critically damped", "underdamped with natural frequency $\\omega_n = 2\\text{ rad/s}$"],
   "B", 10, None, ["figures/gate-2009-ae-ae-43-figure-1.png"]),
  # 44
  (44, 2, "A 2-celled tube with wall thickness $0.5\\text{ mm}$ is subjected to a torque of $10\\text{ N-m}$. The resulting shear flows in the two cells are $q_1$ and $q_2$ as shown below.\n\nThe torque balance equation (Bredt-Batho formula) for this section leads to",
   ["$q_1 - q_2 = 2000\\text{ N/m}$", "$q_1 + 2q_2 = 2000\\text{ N/m}$", "$q_1 + q_2 = 2000\\text{ N/m}$", "$2q_1 + q_2 = 2000\\text{ N/m}$"],
   "C", 10, None, ["figures/gate-2009-ae-ae-44-figure-1.png"]),
  # 45
  (45, 2, "The value of the integral $\\int_0^\\pi \\frac{dx}{1 + x + \\sin x}$ evaluated using the trapezoidal rule with two equal intervals is approximately",
   ["$1.27$", "$1.81$", "$1.41$", "$0.71$"],
   "C", 11, None, []),
  # 46
  (46, 2, "The product of the eigenvalues of the matrix $\\begin{bmatrix} 2 & 1 & 1 \\\\ 1 & 3 & 1 \\\\ 1 & 1 & 4 \\end{bmatrix}$ is",
   ["$20$", "$24$", "$9$", "$17$"],
   "D", 11, None, []),
  # 47
  (47, 2, "In the interval $1 \\le x \\le 2$, the function $f(x) = e^{\\pi x} + \\sin\\pi x$ is",
   ["maximum at $x = 1$", "maximum at $x = 2$", "maximum at $x = 1.5$", "monotonically decreasing"],
   "B", 11, None, []),
  # 48
  (48, 2, "The inverse Laplace transform of $F(s) = \\frac{(s+1)}{(s+4)(s-3)}$ is",
   ["$\\frac{3}{7} e^{4t} + \\frac{4}{7} e^{-3t}$", "$\\frac{3}{7} e^{-4t} + \\frac{4}{7} e^{3t}$", "$\\frac{5}{7} e^{-4t} + \\frac{6}{7} e^{3t}$", "$\\frac{5}{7} e^{4t} + \\frac{6}{7} e^{-3t}$"],
   "B", 11, None, []),
  # 49
  (49, 2, "The linear system of equations $\\mathbf{Ax} = \\mathbf{b}$ where $\\mathbf{A} = \\begin{bmatrix} 1 & 2 \\\\ 2 & 4 \\end{bmatrix}$ and $\\mathbf{b} = \\begin{Bmatrix} 3 \\\\ 3 \\end{Bmatrix}$ has",
   ["no solution", "infinitely many solutions", "a unique solution $\\mathbf{x} = \\begin{Bmatrix} 1 \\\\ 1 \\end{Bmatrix}$", "a unique solution $\\mathbf{x} = \\begin{Bmatrix} 0.5 \\\\ 0.5 \\end{Bmatrix}$"],
   "A", 11, None, []),
  # 50
  (50, 2, "The correct iterative scheme for finding the square root of a positive real number $R$ using the Newton Raphson method is",
   ["$x_{n+1} = \\sqrt{R}$", "$x_{n+1} = \\frac{1}{2} \\left( x_n + \\frac{R}{x_n} \\right)$", "$x_{n+1} = \\frac{1}{2} \\left( \\sqrt{x_n} + \\sqrt{x_{n-1}} \\right)$", "$x_{n+1} = \\frac{1}{2} (\\sqrt{R} + x_n)$"],
   "B", 11, None, []),
  # 51
  (51, 2, "The pair of eigenvalues that represent the phugoid mode is",
   ["$\\lambda_1$ and $\\lambda_3$", "$\\lambda_2$ and $\\lambda_4$", "$\\lambda_3$ and $\\lambda_4$", "$\\lambda_1$ and $\\lambda_2$"],
   "D", 12, "common-data-51-52", []),
  # 52
  (52, 2, "The short period damped frequency is",
   ["$2.6\\text{ rad/s}$", "$0.2\\text{ rad/s}$", "$2.5\\text{ rad/s}$", "$0.02\\text{ rad/s}$"],
   "A", 12, "common-data-51-52", []),
  # 53
  (53, 2, "The surface integral (taken over the unit sphere) of the component of $\\vec{A}$ normal to the surface is",
   ["$\\pi$", "$1$", "$0$", "$4\\pi$"],
   "C", 12, "common-data-53-54", []),
  # 54
  (54, 2, "The magnitude of the component of $\\vec{A}$ normal to the spherical surface at the point $\\left( \\frac{1}{\\sqrt{3}}, \\frac{1}{\\sqrt{3}}, \\frac{1}{\\sqrt{3}} \\right)$ is",
   ["$\\frac{1}{3}$", "$\\frac{2}{3}$", "$\\frac{3}{3}$", "$\\frac{4}{3}$"],
   "B", 12, "common-data-53-54", []),
  # 55
  (55, 2, "If the shaft is fixed at both ends, the boundary conditions are:",
   ["$\\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=0} = 0 \\text{ and } \\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=L} = 0$", "$\\theta(0) = 0 \\text{ and } \\theta(L) = 0$", "$\\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=0} = 0 \\text{ and } \\theta(L) = 0$", "$\\theta(0) = 0 \\text{ and } \\left.\\frac{\\partial \\theta}{\\partial x}\\right|_{x=L} = 0$"],
   "B", 12, "common-data-55-56", []),
  # 56
  (56, 2, "If the $n^{\\text{th}}$ mode shape of torsional vibration of the above shaft is $\\sin\\left(\\frac{n\\pi x}{L}\\right)$ then the $n^{\\text{th}}$ natural frequency of vibration, i.e., $\\omega_n$, is given by",
   ["$\\omega_n = \\frac{n\\pi}{L} \\sqrt{\\frac{GJ}{I}}$", "$\\omega_n = \\frac{(2n+1)\\pi}{2L} \\sqrt{\\frac{GJ}{I}}$", "$\\omega_n = \\frac{n\\pi}{2L} \\sqrt{\\frac{GJ}{I}}$", "$\\omega_n = \\frac{(2n+1)\\pi}{L} \\sqrt{\\frac{GJ}{I}}$"],
   "A", 13, "common-data-55-56", []),
  # 57
  (57, 2, "If the sensible enthalpy of fuel is neglected, the temperature of combustion products from the reaction of primary air stream with fuel is approximately",
   ["$2100\\text{ K}$", "$3200\\text{ K}$", "$2600\\text{ K}$", "$1800\\text{ K}$"],
   "C", 13, "linked-answer-57-58", []),
  # 58
  (58, 2, "The approximate ratio of mass flow rates of the primary air stream to the secondary air stream required to achieve the turbine inlet total temperature of $1550\\text{ K}$ is",
   ["$2:1$", "$1:2$", "$1:1.5$", "$1:1$"],
   "D", 13, "linked-answer-57-58", []),
  # 59
  (59, 2, "After 10 seconds, the change in specific internal energy of the air is",
   ["$21,525\\text{ J/kg}$", "$-21,525\\text{ J/kg}$", "$30,000\\text{ J/kg}$", "$-8,475\\text{ J/kg}$"],
   "A", 13, "linked-answer-59-60", ["figures/gate-2009-ae-ae-59-figure-1.png"]),
  # 60
  (60, 2, "Given that the specific heats of air at constant pressure and volume are $c_p = 1004.5\\text{ J/kg-K}$ and $c_v = 717.5\\text{ J/kg-K}$ respectively, the corresponding change in the temperature of the air is",
   ["$21.4\\text{ K}$", "$-21.4\\text{ K}$", "$30\\text{ K}$", "$-30\\text{ K}$"],
   "C", 13, "linked-answer-59-60", [])
]

for num, marks, q_text, opts, ans, page_num, group_id, fig_paths in raw_questions:
    q_id = f"gate-2009-ae-ae-{num:02d}"
    neg_marks = 0.3333333333333333 if marks == 1 else (0.6666666666666666 if num not in [58, 60] else 0)
    
    option_objs = [
        {"label": chr(65 + i), "text": opts[i]} for i in range(len(opts))
    ]
    
    fig_objs = []
    for fpath in fig_paths:
        fig_objs.append({
            "src": fpath,
            "alt": f"GATE 2009 Aerospace Engineering Question {num} figure",
            "source": {
                "file": "internal/ae/AE2009.pdf",
                "page": page_num,
                "sha256": paper_sha
            },
            "verificationStatus": "source-verified"
        })
        
    q_entry = {
        "id": q_id,
        "number": num,
        "year": 2009,
        "paper": "AE",
        "section": "AE",
        "subject": "Aerospace Engineering",
        "type": "MCQ",
        "marks": marks,
        "negativeMarks": neg_marks,
        "question": q_text,
        "options": option_objs,
        "answer": ans,
        "acceptedAnswers": [ans],
        "markingRule": "gate-2009-official",
        "hasFigure": len(fig_objs) > 0,
        "figures": fig_objs,
        "groupId": group_id,
        "source": {
            "paper": "AE",
            "year": 2009,
            "questionNumber": num,
            "section": "AE",
            "file": "internal/ae/AE2009.pdf",
            "sha256": paper_sha,
            "pages": [
                {
                    "page": page_num,
                    "coordinateSystem": "PDF points, top-left origin"
                }
            ],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-08"
        },
        "transcriptionStatus": "source-verified",
        "solution": None,
        "solutionAvailability": "not-provided-in-source",
        "gradingStatus": "official key verified"
    }
    
    paper_data["questions"].append(q_entry)

with open("data/ae/2009.json", "w", encoding="utf-8") as f:
    json.dump(paper_data, f, indent=2)

print("data/ae/2009.json built with complete schema!")
