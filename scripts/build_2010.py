import json

pdf_sha = '24017904cc0ced113e6235427670da59feb5a2f179a0930677966a0f72de30f3'
key_sha = 'f9c0cac1bcc8bd2dbe77ab1eb610f8d7a156dc1538637a0f56578fd4699db703'

raw_keys = {
    1: 'A', 2: 'B', 3: 'C', 4: 'B', 5: 'C', 6: 'C', 7: 'D', 8: 'C', 9: 'C', 10: 'C',
    11: 'A', 12: 'B', 13: 'A', 14: 'D', 15: 'B', 16: 'D', 17: 'D', 18: 'D', 19: 'A', 20: 'B',
    21: 'C', 22: 'D', 23: 'D', 24: 'D', 25: 'C', 26: 'D', 27: 'A', 28: 'D', 29: 'C', 30: 'B',
    31: 'B', 32: 'A', 33: 'A', 34: 'B', 35: 'B', 36: 'C', 37: 'A', 38: 'C', 39: 'A', 40: 'C',
    41: 'B', 42: 'D', 43: 'B', 44: 'B', 45: 'D', 46: 'A', 47: 'D', 48: 'C', 49: 'D', 50: 'A',
    51: 'A', 52: 'C', 53: 'D', 54: 'D', 55: 'C', 56: 'B', 57: 'A', 58: 'D', 59: 'C', 60: 'D',
    61: 'C', 62: 'C', 63: 'D', 64: 'B', 65: 'B'
}

questions_data = [
    # Q1
    {
        'num': 1, 'page': 2,
        'q': "Isentropic efficiency $\\eta_d$ of a subsonic diffuser is defined as\n(Note: 'a' represents the ambient, '2' represents the exit of the diffuser and 's' represents an isentropic process)",
        'opts': [
            '$\\frac{T_{02s} - T_a}{T_{02} - T_a}$',
            '$\\frac{T_{02s} + T_a}{T_{02} + T_a}$',
            '$\\frac{P_{02s} - P_a}{P_{02} - P_a}$',
            '$\\frac{P_a - P_{02s}}{P_a - P_{02}}$'
        ]
    },
    # Q2
    {
        'num': 2, 'page': 2,
        'q': "Two position vectors are indicated by $\\vec{V}_1 = \\begin{Bmatrix} x_1 \\\\ y_1 \\end{Bmatrix}$ and $\\vec{V}_2 = \\begin{Bmatrix} x_2 \\\\ y_2 \\end{Bmatrix}$. If $a^2 + b^2 = 1$, then the operation $\\vec{V}_2 = \\begin{bmatrix} a & -b \\\\ b & a \\end{bmatrix} \\vec{V}_1$ amounts to obtaining the position vector $\\vec{V}_2$ from $\\vec{V}_1$ by",
        'opts': [
            'translation',
            'rotation',
            'magnification',
            'combination of translation, rotation, and magnification.'
        ]
    },
    # Q3
    {
        'num': 3, 'page': 2,
        'q': 'An aircraft is climbing at a constant speed in a straight line at a steep angle of climb. The load factor it sustains during the climb is:',
        'opts': [
            'equal to 1.0',
            'greater than 1.0',
            'positive but less than 1.0',
            'dependant on the weight of the aircraft'
        ]
    },
    # Q4
    {
        'num': 4, 'page': 2,
        'q': 'In a general case of a homogeneous material under thermo-mechanical loading the number of distinct components of the state of stress is',
        'opts': ['3', '4', '5', '6']
    },
    # Q5
    {
        'num': 5, 'page': 2,
        'q': 'The linear second order partial differential equation $5\\frac{\\partial^2 \\phi}{\\partial x^2} + 3\\frac{\\partial^2 \\phi}{\\partial x \\partial y} + 2\\frac{\\partial^2 \\phi}{\\partial y^2} + 9 = 0$ is',
        'opts': [
            'Parabolic',
            'Hyperbolic',
            'Elliptic',
            'None of the above'
        ]
    },
    # Q6
    {
        'num': 6, 'page': 2,
        'q': 'All other factors remaining constant, if the weight of an aircraft increases by 30% then the takeoff distance increases by approximately:',
        'opts': ['15%', '30%', '70%', '105%']
    },
    # Q7
    {
        'num': 7, 'page': 2,
        'q': 'A vertical slender rod is suspended by a hinge at the top and hangs freely. It is heated until it attains a uniform temperature, $T$. Neglecting the effect of gravity, the rod has',
        'opts': [
            'Stress but no strain',
            'Strain but no stress',
            'Both stress and strain',
            'Neither stress nor strain'
        ]
    },
    # Q8
    {
        'num': 8, 'page': 2,
        'q': 'An aircraft stalls at a speed of $40\\text{ m/s}$ in straight and level flight. The slowest speed at which this aircraft can execute a level turn at a bank angle of 60 degrees is:',
        'opts': ['$28.3\\text{ m/s}$', '$40.0\\text{ m/s}$', '$56.6\\text{ m/s}$', '$80.0\\text{ m/s}$']
    },
    # Q9
    {
        'num': 9, 'page': 2,
        'q': 'The eigen-values of a real symmetric matrix are always',
        'opts': ['positive', 'imaginary', 'real', 'complex conjugate pairs']
    },
    # Q10
    {
        'num': 10, 'page': 3,
        'q': 'The concentration $x$ of a certain chemical species at time $t$ in a chemical reaction is described by the differential equation $\\frac{dx}{dt} + kx = 0$, with $x(t = 0) = x_0$. Given that $e$ is the base of the natural logarithms, the concentration $x$ at $t = \\frac{1}{k}$',
        'opts': [
            'falls to the value $0.5x_0$',
            'rises to the value $2x_0$',
            'falls to the value $\\frac{x_0}{e}$',
            'rises to the value $ex_0$'
        ]
    },
    # Q11
    {
        'num': 11, 'page': 3,
        'q': 'The definite integral $\\int_{-1}^{+1} \\frac{dx}{x^2}$',
        'opts': [
            'does not exist',
            'is equal to 2',
            'is equal to 0',
            'is equal to -2'
        ]
    },
    # Q12
    {
        'num': 12, 'page': 3,
        'q': 'The absolute ceiling of an aircraft is the altitude above which it:',
        'opts': [
            'can never reach',
            'cannot sustain level flight at a constant speed',
            'can perform accelerated flight as well as straight and level flight at a constant speed',
            'can perform straight and level flight at a constant speed only'
        ]
    },
    # Q13
    {
        'num': 13, 'page': 3,
        'q': 'A thin rectangular plate made of isotropic material which satisfies the octahedral (i.e., Von Mises/Distortion energy) failure criterion has yield strength of $200\\text{ MPa}$ under uniaxial tension. As shown in the figure, if it is loaded with uniform tension of $150\\text{ MPa}$ along the $x$-direction, the maximum uniform tensile stress that can be applied along the $y$-direction before the plate starts yielding is about',
        'opts': ['$227\\text{ MPa}$', '$77\\text{ MPa}$', '$87\\text{ MPa}$', '$114\\text{ MPa}$'],
        'fig': 'figures/gate-2010-ae-ae-13-figure-1.png'
    },
    # Q14
    {
        'num': 14, 'page': 3,
        'q': 'Consider an incompressible 2-D Couette flow of water between two walls spaced $1\\text{ m}$ apart. The lower wall is kept stationary. What is the shear stress acting on the lower wall if the upper wall is moving at a constant speed of $2\\text{ m/s}$? ($\\mu_{\\text{water}} = 7 \\times 10^{-3}\\text{ N}\\cdot\\text{s/m}^2$)',
        'opts': [
            '$3.5 \\times 10^{-3}\\text{ N/m}^2$',
            '$7 \\times 10^{-3}\\text{ N/m}^2$',
            '$10.5 \\times 10^{-3}\\text{ N/m}^2$',
            '$14 \\times 10^{-3}\\text{ N/m}^2$'
        ],
        'fig': 'figures/gate-2010-ae-ae-14-figure-1.png'
    },
    # Q15
    {
        'num': 15, 'page': 3,
        'q': 'The angular momentum, about the centre of mass of the earth, of an artificial satellite in a highly elliptical orbit is :',
        'opts': [
            'a maximum when the satellite is farthest from the earth',
            'a constant',
            'proportional to the speed of the satellite',
            'proportional to the square of the speed of the satellite'
        ]
    },
    # Q16
    {
        'num': 16, 'page': 4,
        'q': 'A column of length $l$ and flexural rigidity $EI$, has one end fixed and the other end hinged. The critical buckling load for the column is',
        'opts': [
            '$\\frac{\\pi^2 EI}{(0.5l)^2}$',
            '$\\frac{\\pi^2 EI}{(0.7l)^2}$',
            '$\\frac{\\pi^2 EI}{l^2}$',
            '$\\frac{\\pi^2 EI}{(2l)^2}$'
        ]
    },
    # Q17
    {
        'num': 17, 'page': 4,
        'q': 'A horizontal cantilevered steel beam of rectangular cross-section having width $b$ and depth $d$ is vibrating in the vertical plane. The natural frequency of bending vibration is highest when',
        'opts': [
            '$b = 10, d = 10$',
            '$b = 20, d = 5$',
            '$b = 5, d = 20$',
            '$b = 25, d = 4$'
        ],
        'fig': 'figures/gate-2010-ae-ae-17-figure-1.png'
    },
    # Q18
    {
        'num': 18, 'page': 4,
        'q': 'Consider an incompressible 2-D viscous flow over a curved surface. Let the pressure distribution on the surface be $p(s) = 2 + \\sin\\left(\\frac{\\pi}{2} + s\\right)\\text{ N/m}^2$, where $s$ is the distance along the curved surface from the leading edge. The flow separates at',
        'opts': [
            '$s = (2/3)\\pi\\text{ m}$',
            '$s = (3/2)\\pi\\text{ m}$',
            '$s = (\\pi/2)\\text{ m}$',
            '$s = \\pi\\text{ m}$'
        ]
    },
    # Q19
    {
        'num': 19, 'page': 4,
        'q': 'For a multi-stage axial compressor with constant diameter hub',
        'opts': [
            'Blade height decreases in the flow direction',
            'Blade height increases in the flow direction',
            'Blade height remains constant',
            'Blade height first increases and then decreases in the flow direction'
        ]
    },
    # Q20
    {
        'num': 20, 'page': 4,
        'q': 'In a 2-D, steady, fully developed, laminar boundary layer over a flat plate, if $x$ is the stream-wise coordinate, $y$ is the wall normal coordinate and $u$ is the stream-wise velocity component, which of the following is true:',
        'opts': [
            '$\\frac{\\partial u}{\\partial x} \\gg \\frac{\\partial u}{\\partial y}$',
            '$\\frac{\\partial u}{\\partial y} \\gg \\frac{\\partial u}{\\partial x}$',
            '$\\frac{\\partial u}{\\partial x} = \\frac{\\partial u}{\\partial y}$',
            '$\\frac{\\partial u}{\\partial x} = -\\frac{\\partial u}{\\partial y}$'
        ]
    },
    # Q21
    {
        'num': 21, 'page': 4,
        'q': 'How does the specific thrust, at constant turbine inlet temperature, produced by a turbofan engine change with an increase in compressor pressure ratio?',
        'opts': [
            'Increases',
            'Decreases',
            'First increases and then decreases',
            'First decreases and then increases'
        ]
    },
    # Q22
    {
        'num': 22, 'page': 4,
        'q': 'If $\\phi$ is the potential function for an incompressible irrotational flow, and $u$ and $v$ are the Cartesian velocity components, then which one of the following combinations is correct?',
        'opts': [
            '$u = \\frac{\\partial \\phi}{\\partial x},\\; v = \\frac{\\partial \\phi}{\\partial x}$',
            '$u = -\\frac{\\partial \\phi}{\\partial y},\\; v = \\frac{\\partial \\phi}{\\partial x}$',
            '$u = -\\frac{\\partial \\phi}{\\partial y},\\; v = \\frac{\\partial \\phi}{\\partial y}$',
            '$u = \\frac{\\partial \\phi}{\\partial x},\\; v = \\frac{\\partial \\phi}{\\partial y}$'
        ]
    },
    # Q23
    {
        'num': 23, 'page': 4,
        'q': 'Among the choices given below, the Specific Impulse is maximum for a',
        'opts': [
            'Cryogenic Rocket',
            'Solid Rocket',
            'Liquid Rocket',
            'Ramjet'
        ]
    },
    # Q24
    {
        'num': 24, 'page': 5,
        'q': 'For a flow across an oblique shock which of the following statements is true?',
        'opts': [
            'Component of velocity normal to shock decreases while tangential component increases.',
            'Component of velocity normal to shock increases while tangential component decreases.',
            'Component of velocity normal to shock is unchanged while tangential component decreases.',
            'Component of velocity normal to shock decreases while tangential component is unchanged.'
        ]
    },
    # Q25
    {
        'num': 25, 'page': 5,
        'q': 'The maximum operating flow rate through a centrifugal compressor at a given RPM is limited by',
        'opts': [
            'Impellor stall',
            'Surge',
            'Choking of diffuser throat',
            'Inlet flow distortion'
        ]
    },
    # Q26
    {
        'num': 26, 'page': 5,
        'q': 'A spacecraft of mass $100\\text{ kg}$, moving at an instantaneous speed of $1.8 \\times 10^4\\text{ m/s}$, picks up interstellar dust at the rate of $3.2 \\times 10^{-8}\\text{ kg/s}$. Assuming that the dust was initially at rest, the instantaneous rate of retardation of the spacecraft is:',
        'opts': [
            '$7.9 \\times 10^{-8}\\text{ m/s}^2$',
            '$2.3 \\times 10^{-3}\\text{ m/s}^2$',
            'zero',
            '$5.8 \\times 10^{-6}\\text{ m/s}^2$'
        ]
    },
    # Q27
    {
        'num': 27, 'page': 5,
        'q': 'Following stress state is proposed for a 2-D problem with no body forces: $\\sigma_{xx} = 3x^2 y + 4y^2$, $\\sigma_{yy} = y^3 + 14xy$, $\\tau_{xy} = -3xy^2 - 7x^2$. It satisfies',
        'opts': [
            'Equilibrium equations but not compatibility equation',
            'Compatibility equation but not equilibrium equations',
            'Neither equilibrium equations nor compatibility equation',
            'Both equilibrium equations and compatibility equation'
        ]
    },
    # Q28
    {
        'num': 28, 'page': 5,
        'q': 'A uniform cross-section rigid rod of mass $m$ and length $l$ is hinged at its upper end and suspended like a pendulum. Its natural frequency for small oscillations is',
        'opts': [
            '$\\sqrt{\\frac{g}{2l}}$',
            '$\\sqrt{\\frac{g}{l}}$',
            '$\\sqrt{\\frac{2g}{l}}$',
            '$\\sqrt{\\frac{3g}{2l}}$'
        ],
        'fig': 'figures/gate-2010-ae-ae-28-figure-1.png'
    },
    # Q29
    {
        'num': 29, 'page': 5,
        'q': "The thin rectangular plate shown in the figure is loaded with uniform shear, $\\tau_0$, along all edges and uniform uniaxial tension in the $y$-direction. The appropriate Airy's stress function to solve for stresses is given by",
        'opts': [
            '$-\\tau_0 xy - \\sigma_0 \\frac{x^2}{2} + \\sigma_0(x^4 - y^4)$',
            '$\\tau_0 xy - \\sigma_0 \\frac{x^2}{2}$',
            '$-\\tau_0 xy + \\sigma_0 \\frac{x^2}{2}$',
            '$\\tau_0 xy + \\sigma_0 \\frac{x^2}{2} + \\sigma_0(x^4 - y^4)$'
        ],
        'fig': 'figures/gate-2010-ae-ae-29-figure-1.png'
    },
    # Q30
    {
        'num': 30, 'page': 6,
        'q': 'A propeller powered aircraft, trimmed to attain maximum range and flying in a straight line, travels a distance $R$ from its take-off point when it has consumed a weight of fuel equal to 20% of its take-off weight. If the aircraft continues to fly and consumes a total weight of fuel equal to 50% of its take-off weight, the distance between it and its take-off point becomes:',
        'opts': ['$2.5\\text{ R}$', '$3.1\\text{ R}$', '$2.1\\text{ R}$', '$3.9\\text{ R}$']
    },
    # Q31
    {
        'num': 31, 'page': 6,
        'q': 'The given thin wall section of uniform thickness, $t$, is symmetric about $x$-axis. Moment of inertia is given to be $I_{xx} = \\frac{35}{12}th^3$. Shear center for this section is located at',
        'opts': [
            '$x = -\\frac{3}{8}h$',
            '$x = -\\frac{9}{28}h$',
            '$x = -\\frac{35}{36}h$',
            '$x = -\\frac{17}{35}h$'
        ],
        'fig': 'figures/gate-2010-ae-ae-31-figure-1.png'
    },
    # Q32
    {
        'num': 32, 'page': 6,
        'q': 'During an under-damped oscillation of a single degree of freedom system, in the time-displacement plot the third peak is of magnitude 100 and the tenth peak is of magnitude 10. The damping ratio $\\zeta$ is approximately:',
        'opts': ['0.052', '0.023', '0.366', '0.159']
    },
    # Q33
    {
        'num': 33, 'page': 6,
        'q': 'Given that the Laplace transform of $y(t) = e^{-t}(2\\cos 2t - \\sin 2t)$ is $Y(s) = \\frac{2s}{(s+1)^2 + 4}$, the Laplace transform of $y_1(t) = e^t(2\\cos 2t - \\sin 2t)$ is',
        'opts': [
            '$\\frac{2(s-2)}{(s-1)^2 + 4}$',
            '$\\frac{2(s+2)}{(s+3)^2 + 4}$',
            '$\\frac{2(s+2)}{(s+1)^2 + 4}$',
            '$\\frac{2(s-1)}{(s-1)^2 + 4}$'
        ]
    },
    # Q34
    {
        'num': 34, 'page': 6,
        'q': 'In a certain region a hill is described by the shape $z(x, y) = \\frac{1}{50}x^4 + y^2 - xy - 3y$, where the axes $x$ and $y$ are in the horizontal plane and axis $z$ points vertically upward. If $\\hat{i}$, $\\hat{j}$ and $\\hat{k}$ are unit vectors along $x$, $y$ and $z$, respectively, then at the point $x = 5, y = 10$ the unit vector in the direction of the steepest slope of the hill will be:',
        'opts': ['$\\hat{i}$', '$\\hat{j}$', '$\\hat{k}$', '$\\hat{i} + \\hat{j} + \\hat{k}$']
    },
    # Q35
    {
        'num': 35, 'page': 6,
        'q': 'An aircraft is cruising at an altitude of $9\\text{ km}$. The free-stream static pressure and density at this altitude are $3.08 \\times 10^4\\text{ N/m}^2$ and $0.467\\text{ kg/m}^3$ respectively. A Pitot tube mounted on the wing senses a pressure of $3.31 \\times 10^4\\text{ N/m}^2$. Ignoring compressibility effects, the cruising speed of the aircraft is approximately',
        'opts': ['$50\\text{ m/s}$', '$100\\text{ m/s}$', '$150\\text{ m/s}$', '$200\\text{ m/s}$']
    },
    # Q36
    {
        'num': 36, 'page': 7,
        'q': 'The trim curves of an aircraft are of the form $C_{m_{cg}} = (0.05 - 0.2\\delta_e) - 0.1C_L$ where the elevator deflection angle, $\\delta_e$, is in radians. The static margin of the aircraft is :',
        'opts': ['0.5', '0.2', '0.1', '0.05']
    },
    # Q37
    {
        'num': 37, 'page': 7,
        'q': 'The function $f(x, y) = x^2 + y^2 - xy - 3y$ has an extremum at the point',
        'opts': ['(1, 2)', '(3, 0)', '(2, 2)', '(1, 1)']
    },
    # Q38
    {
        'num': 38, 'page': 7,
        'q': 'Consider the flow of air ($\\rho = 1.23\\text{ kg/m}^3$) over a wing of chord length $0.5\\text{ m}$ and span $3\\text{ m}$. Let the free stream velocity be $U = 100\\text{ m/s}$ and the average circulation around the wing be $\\Gamma = 10\\text{ m}^2/\\text{s}$ per unit span. The lift force acting on the wing is',
        'opts': ['$615\\text{ N}$', '$1845\\text{ N}$', '$3690\\text{ N}$', '$4920\\text{ N}$']
    },
    # Q39
    {
        'num': 39, 'page': 7,
        'q': 'The stagnation pressure and stagnation temperature inside the combustion chamber of a liquid rocket engine are $1.5\\text{ MPa}$ and $2500\\text{ K}$ respectively. The burned gases have $\\gamma = 1.2$ and $R = 692.83\\text{ J/kgK}$. The rocket has a converging - diverging nozzle with a throat area of $0.025\\text{ m}^2$ and the flow at the exit of the nozzle is supersonic. If the flow through the nozzle is isentropic, what is the mass flow rate of the gases out of the nozzle?',
        'opts': ['$18.5\\text{ kg/s}$', '$31.2\\text{ kg/s}$', '$29.7\\text{ kg/s}$', '$19.4\\text{ kg/s}$']
    },
    # Q40
    {
        'num': 40, 'page': 7,
        'q': 'In finding a root of the equation: $x^2 - 6x + 5 = 0$ the Newton-Raphson method achieves an order of convergence equal to:',
        'opts': ['1.0', '1.67', '2.0', '2.5']
    },
    # Q41
    {
        'num': 41, 'page': 7,
        'q': 'Consider a 1-D adiabatic, inviscid, compressible flow of air ($R = 287\\text{ J/Kg}\\cdot\\text{K}$, $c_v = 718\\text{ J/Kg}\\cdot\\text{K}$) through a duct of constant cross-sectional area $A = 1\\text{ m}^2$. If the volumetric flow rate is $Q = 680\\text{ m}^3/\\text{s}$ and stagnation temperature is $T_0 = 580.05\\text{ K}$, then the air temperature inside the duct is',
        'opts': ['$300\\text{ K}$', '$350\\text{ K}$', '$400\\text{ K}$', '$450\\text{ K}$']
    },
    # Q42
    {
        'num': 42, 'page': 7,
        'q': 'A two stage chemical rocket, having the same specific impulse ($I_{sp}$) of $300\\text{ s}$ for both the stages is designed in such a way that the payload ratio and the structural ratio are same for both the stages. The second stage of the rocket has following mass distribution :\nPropellant Mass $= 10208\\text{ kg}$\nStructural Mass $= 1134\\text{ kg}$\nPayload Mass $= 1700\\text{ kg}$\n$g_e = 9.8\\text{ m/s}^2$\n\nIf the rocket is fired from rest and it flies in a zero gravity field and a drag free environment, the final velocity attained by the payload is',
        'opts': ['$9729.3\\text{ m/s}$', '$897.3\\text{ m/s}$', '$9360.2\\text{ m/s}$', '$8973.2\\text{ m/s}$']
    },
    # Q43
    {
        'num': 43, 'page': 7,
        'q': 'A missile with a Ramjet engine is flying in air. The temperature at the inlet and the outlet of the combustor are $1200\\text{ K}$ and $2500\\text{ K}$ respectively. The heating value of the fuel is $43\\text{ MJ/kg}$ and the burner efficiency is 90%. Considering the working fluid to be air ($C_p = 1005\\text{ J/kgK}$ and $\\gamma = 1.4$), the fuel/air ratio ($f = \\frac{\\dot{m}_f}{\\dot{m}_a}$) for this engine is equal to:',
        'opts': ['0.032', '0.036', '0.042', '0.026']
    },
    # Q44
    {
        'num': 44, 'page': 8,
        'q': 'The trim curves of an aircraft are of the form $C_{m_{cg}} = (0.05 - 0.2\\delta_e) - 0.1C_L$ where the elevator deflection angle, $\\delta_e$, is in radians. The change in elevator deflection needed to increase the lift coefficient from 0.4 to 0.9 is :',
        'opts': ['-0.5 radians', '-0.25 radians', '0.25 radians', '0.5 radians']
    },
    # Q45
    {
        'num': 45, 'page': 8,
        'q': 'If $e$ is the base of the natural logarithms then the equation of the tangent from the origin to the curve $y = e^x$ is',
        'opts': ['$y = x$', '$y = \\pi x$', '$y = \\frac{x}{e}$', '$y = ex$']
    },
    # Q46
    {
        'num': 46, 'page': 8,
        'q': 'Consider a potential flow over a finite wing with the following circulation distribution\n$$\\Gamma(y) = 100 \\sqrt{1 - \\left(\\frac{2y}{4}\\right)^2}\\text{ m}^2/\\text{s}$$\nIf the free stream velocity is $100\\text{ m/s}$, the induced angle of attack is',
        'opts': [
            '0.125 radians',
            '-0.125 radians',
            '$0.125\\sqrt{1 - \\left(\\frac{y}{2}\\right)^2}\\text{ radians}$',
            '$-0.125\\sqrt{1 - \\left(\\frac{y}{2}\\right)^2}\\text{ radians}$'
        ],
        'fig': 'figures/gate-2010-ae-ae-46-figure-1.png'
    },
    # Q47
    {
        'num': 47, 'page': 8,
        'q': 'The inlet stagnation temperature for a single stage axial compressor is $300\\text{ K}$ and the stage efficiency is 0.80. Following conditions exist at the mean radius of the rotor blade:\nBlade speed $= 200\\text{ m/s}$\nAxial flow velocity $= 160\\text{ m/s}$\nInlet blade angle $\\beta_1 = 44^\\circ$\nOutlet blade angle $\\beta_2 = 14^\\circ$\n$C_p = 1005\\text{ J/kgK}$ and $\\gamma = 1.4$\n\nWhat is the stagnation pressure ratio ($P_{RS}$) for this compressor?',
        'opts': ['1.41', '1.37', '1.51', '1.23']
    },
    # Q48
    {
        'num': 48, 'page': 9, 'group': 'common-data-48-49',
        'q': 'Bending moment diagram is given by',
        'opts': ['(A)', '(B)', '(C)', '(D)'],
        'fig': 'figures/gate-2010-ae-ae-48-figure-2.png'
    },
    # Q49
    {
        'num': 49, 'page': 9, 'group': 'common-data-48-49',
        'q': 'Maximum value of shear stress is',
        'opts': [
            '$0.67\\text{ P}/h^2$',
            '$1.33\\text{ P}/h^2$',
            '$1.5\\text{ P}/h^2$',
            '$0.9\\text{ P}/h^2$'
        ]
    },
    # Q50
    {
        'num': 50, 'page': 10, 'group': 'common-data-50-51',
        'q': 'The radial and azimuthal velocities on the cylinder surface at $\\theta = \\pi/2$ are',
        'opts': [
            '$V_r = 0\\text{ m/s},\\; V_\\theta = -75\\text{ m/s}$',
            '$V_r = 0\\text{ m/s},\\; V_\\theta = 75\\text{ m/s}$',
            '$V_r = 0\\text{ m/s},\\; V_\\theta = -25\\text{ m/s}$',
            '$V_r = 0\\text{ m/s},\\; V_\\theta = 25\\text{ m/s}$'
        ],
        'fig': 'figures/gate-2010-ae-ae-50-figure-1.png'
    },
    # Q51
    {
        'num': 51, 'page': 10, 'group': 'common-data-50-51',
        'q': 'The stagnation points are located at',
        'opts': [
            '$210^\\circ\\text{ and } 330^\\circ$',
            '$240^\\circ\\text{ and } 300^\\circ$',
            '$30^\\circ\\text{ and } 150^\\circ$',
            '$60^\\circ\\text{ and } 120^\\circ$'
        ]
    },
    # Q52
    {
        'num': 52, 'page': 10, 'group': 'linked-answer-52-53',
        'q': 'What is the stagnation pressure at the inlet of the nozzle?',
        'opts': ['2.8 bar', '5.7 bar', '2.1 bar', '6.3 bar']
    },
    # Q53
    {
        'num': 53, 'page': 10, 'group': 'linked-answer-52-53',
        'q': 'What is the specific thrust produced by this engine under the given conditions?',
        'opts': ['586 Ns/kg', '745 Ns/kg', '686 Ns/kg', '500 Ns/kg']
    },
    # Q54
    {
        'num': 54, 'page': 10, 'group': 'linked-answer-54-55',
        'q': 'Assuming that $g$ is the acceleration due to gravity, $T$ is given approximately by:',
        'opts': [
            '$\\frac{v}{\\pi g}$',
            '$\\frac{\\pi v}{g}$',
            '$\\frac{v}{\\sqrt{2}\\pi g}$',
            '$\\frac{\\sqrt{2}\\pi v}{g}$'
        ]
    },
    # Q55
    {
        'num': 55, 'page': 10, 'group': 'linked-answer-54-55',
        'q': 'If $v = 200\\text{ m/s}$ then the wavelength of the phugoid oscillations, assuming $g = 9.81\\text{ m/s}^2$, is, approximately:',
        'opts': [
            '$1.28 \\times 10^4\\text{ m}$',
            '$1.30 \\times 10^3\\text{ m}$',
            '$1.81 \\times 10^4\\text{ m}$',
            '$918\\text{ m}$'
        ]
    },
    # Q56
    {
        'num': 56, 'page': 11,
        'q': 'Which of the following options is the closest in meaning to the word below:\nCircuitous',
        'opts': ['cyclic', 'indirect', 'confusing', 'crooked']
    },
    # Q57
    {
        'num': 57, 'page': 11,
        'q': 'The question below consists of a pair of related words followed by four pairs of words. Select the pair that best expresses the relation in the original pair.\nUnemployed : Worker',
        'opts': [
            'fallow : land',
            'unaware : sleeper',
            'wit : jester',
            'renovated : house'
        ]
    },
    # Q58
    {
        'num': 58, 'page': 11,
        'q': 'Choose the most appropriate word from the options given below to complete the following sentence:\nIf we manage to ____________ our natural resources, we would leave a better planet for our children.',
        'opts': ['uphold', 'restrain', 'cherish', 'conserve']
    },
    # Q59
    {
        'num': 59, 'page': 11,
        'q': 'Choose the most appropriate word from the options given below to complete the following sentence:\nHis rather casual remarks on politics ____________ his lack of seriousness about the subject.',
        'opts': ['masked', 'belied', 'betrayed', 'suppressed']
    },
    # Q60
    {
        'num': 60, 'page': 11,
        'q': '25 persons are in a room. 15 of them play hockey, 17 of them play football and 10 of them play both hockey and football. Then the number of persons playing neither hockey nor football is:',
        'opts': ['2', '17', '13', '3']
    },
    # Q61
    {
        'num': 61, 'page': 11,
        'q': 'Modern warfare has changed from large scale clashes of armies to suppression of civilian populations. Chemical agents that do their work silently appear to be suited to such warfare; and regretfully, there exist people in military establishments who think that chemical agents are useful tools for their cause.\n\nWhich of the following statements best sums up the meaning of the above passage?',
        'opts': [
            'Modern warfare has resulted in civil strife.',
            'Chemical agents are useful in modern warfare.',
            'Use of chemical agents in warfare would be undesirable.',
            'People in military establishments like to use chemical agents in war.'
        ]
    },
    # Q62
    {
        'num': 62, 'page': 12,
        'q': 'If $137 + 276 = 435$ how much is $731 + 672$?',
        'opts': ['534', '1403', '1623', '1513']
    },
    # Q63
    {
        'num': 63, 'page': 12,
        'q': '5 skilled workers can build a wall in 20 days; 8 semi-skilled workers can build a wall in 25 days; 10 unskilled workers can build a wall in 30 days. If a team has 2 skilled, 6 semi-skilled and 5 unskilled workers, how long will it take to build the wall?',
        'opts': ['20 days', '18 days', '16 days', '15 days']
    },
    # Q64
    {
        'num': 64, 'page': 12,
        'q': 'Given digits 2, 2, 3, 3, 3, 4, 4, 4, 4 how many distinct 4 digit numbers greater than 3000 can be formed?',
        'opts': ['50', '51', '52', '54']
    },
    # Q65
    {
        'num': 65, 'page': 12,
        'q': "Hari (H), Gita (G), Irfan (I) and Saira (S) are siblings (i.e. brothers and sisters). All were born on $1^{\\text{st}}$ January. The age difference between any two successive siblings (that is born one after another) is less than 3 years. Given the following facts:\ni. Hari's age + Gita's age > Irfan's age + Saira's age.\nii. The age difference between Gita and Saira is 1 year. However, Gita is not the oldest and Saira is not the youngest.\niii. There are no twins.\n\nIn what order were they born (oldest first)?",
        'opts': ['HSIG', 'SGHI', 'IGSH', 'IHSG']
    }
]

question_groups = [
    {
        'id': 'common-data-48-49',
        'type': 'common-data',
        'title': 'Common Data for Questions 48 and 49',
        'content': [
            {
                'type': 'text',
                'text': 'Common Data for Questions 48 and 49:\nConsider a simply supported beam of length $L$, carrying a bracket welded at its center. The bracket carries a vertical load, $P$, as shown in the figure. Dimensions of bracket are $a = 0.1L$. The beam has a square cross section of dimension $h \\times h$.'
            }
        ],
        'questionIds': [
            'gate-2010-ae-ae-48',
            'gate-2010-ae-ae-49'
        ]
    },
    {
        'id': 'common-data-50-51',
        'type': 'common-data',
        'title': 'Common Data for Questions 50 and 51',
        'content': [
            {
                'type': 'text',
                'text': 'Common Data for Questions 50 and 51:\nConsider a potential flow over a spinning cylinder. The stream function is given as\n$$\\psi = (V_\\infty r \\sin\\theta)\\left(1 - \\frac{R^2}{r^2}\\right) + \\frac{\\Gamma}{2\\pi}\\ln\\frac{r}{R}$$\nwhere\nFree stream velocity, $V_\\infty = 25\\text{ m/s}$\nCylinder radius, $R = 1\\text{ m}$\nCirculation, $\\Gamma = 50\\pi\\text{ m}^2/\\text{s}$'
            }
        ],
        'questionIds': [
            'gate-2010-ae-ae-50',
            'gate-2010-ae-ae-51'
        ]
    },
    {
        'id': 'linked-answer-52-53',
        'type': 'linked-answer',
        'title': 'Statement for Linked Answer Questions 52 and 53',
        'content': [
            {
                'type': 'text',
                'text': 'Statement for Linked Answer Questions 52 and 53:\nAn aircraft with an IDEAL Turbojet engine is flying at $200\\text{ m/s}$ at an altitude where the ambient pressure is equal to $0.8\\text{ bar}$. The stagnation pressure and temperature at the inlet of the turbine are $6\\text{ bar}$ and $1400\\text{ K}$ respectively. The change in specific enthalpy across the compressor is $335\\text{ kJ/kg}$. Assume the fuel flow rate to be very small in comparison to the air flow rate and consider $C_p = 1117\\text{ J/kgK}$ and $\\gamma = 1.3$.'
            }
        ],
        'questionIds': [
            'gate-2010-ae-ae-52',
            'gate-2010-ae-ae-53'
        ],
        'dependencies': [
            {
                'questionId': 'gate-2010-ae-ae-53',
                'dependsOn': 'gate-2010-ae-ae-52'
            }
        ]
    },
    {
        'id': 'linked-answer-54-55',
        'type': 'linked-answer',
        'title': 'Statement for Linked Answer Questions 54 and 55',
        'content': [
            {
                'type': 'text',
                'text': 'Statement for Linked Answer Questions 54 and 55:\nAn aircraft is in straight and level flight at a constant speed $v$. It is disturbed by a symmetric vertical gust, resulting in a phugoid oscillation of time period $T$.'
            }
        ],
        'questionIds': [
            'gate-2010-ae-ae-54',
            'gate-2010-ae-ae-55'
        ],
        'dependencies': [
            {
                'questionId': 'gate-2010-ae-ae-55',
                'dependsOn': 'gate-2010-ae-ae-54'
            }
        ]
    }
]

questions_list = []
question_order = []
question_refs = []

for qentry in questions_data:
    qnum = qentry['num']
    sec = 'AE' if qnum <= 55 else 'GA'
    sec_lower = sec.lower()
    qid = f'gate-2010-ae-{sec_lower}-{qnum:02d}'
    question_order.append(qid)
    question_refs.append({
        'id': qid,
        'number': qnum,
        'section': sec,
        'type': 'MCQ'
    })
    
    marks = 1 if (qnum <= 25 or (56 <= qnum <= 60)) else 2
    neg_marks = 1.0/3.0 if marks == 1 else 2.0/3.0
    ans = raw_keys[qnum]
    
    opts = []
    labels = ['A', 'B', 'C', 'D']
    for idx, opt_text in enumerate(qentry['opts']):
        opts.append({
            'label': labels[idx],
            'text': opt_text
        })
        
    figures = []
    has_fig = False
    if 'fig' in qentry:
        has_fig = True
        figures.append({
            'src': qentry['fig'],
            'alt': f'GATE 2010 Aerospace Engineering Question {qnum} figure',
            'source': {
                'file': 'internal/ae/AE2010.pdf',
                'page': qentry['page'],
                'sha256': pdf_sha
            },
            'verificationStatus': 'source-verified'
        })
    elif qnum == 49:
        # Common data 48-49 beam figure
        has_fig = True
        figures.append({
            'src': 'figures/gate-2010-ae-ae-48-figure-1.png',
            'alt': f'GATE 2010 Aerospace Engineering Question {qnum} figure',
            'source': {
                'file': 'internal/ae/AE2010.pdf',
                'page': 9,
                'sha256': pdf_sha
            },
            'verificationStatus': 'source-verified'
        })
        
    q_obj = {
        'id': qid,
        'number': qnum,
        'year': 2010,
        'paper': 'AE',
        'section': sec,
        'subject': 'Aerospace Engineering' if sec == 'AE' else 'General Aptitude',
        'type': 'MCQ',
        'marks': marks,
        'negativeMarks': neg_marks,
        'question': qentry['q'],
        'options': opts,
        'answer': ans,
        'acceptedAnswers': [ans],
        'markingRule': 'gate-2010-official',
        'hasFigure': has_fig,
        'figures': figures,
        'groupId': qentry.get('group', None),
        'source': {
            'paper': 'AE',
            'year': 2010,
            'questionNumber': qnum,
            'section': sec,
            'file': 'internal/ae/AE2010.pdf',
            'sha256': pdf_sha,
            'pages': [
                {
                    'page': qentry['page'],
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
    questions_list.append(q_obj)

paper_data = {
    'schemaVersion': 1,
    'id': 'gate-2010-ae',
    'exam': 'GATE',
    'year': 2010,
    'paper': 'AE',
    'title': 'GATE 2010 Aerospace Engineering (AE)',
    'durationMinutes': 180,
    'totalMarks': 100,
    'totalQuestions': 65,
    'sectionOrder': ['AE', 'GA'],
    'sections': [
        {
            'id': 'AE',
            'title': 'Aerospace Engineering',
            'totalQuestions': 55,
            'totalMarks': 85,
            'questionIds': [q['id'] for q in questions_list if q['section'] == 'AE']
        },
        {
            'id': 'GA',
            'title': 'General Aptitude',
            'totalQuestions': 10,
            'totalMarks': 15,
            'questionIds': [q['id'] for q in questions_list if q['section'] == 'GA']
        }
    ],
    'questionOrder': question_order,
    'questionRefs': question_refs,
    'questionGroups': question_groups,
    'marking': {
        'negativeFraction': {
            'MCQ': 0.3333333333333333,
            'MSQ': 0,
            'NAT': 0
        }
    },
    'source': {
        'paper': 'AE',
        'year': 2010,
        'file': 'internal/ae/AE2010.pdf',
        'sha256': pdf_sha,
        'keyFile': 'internal/ae/AE2010-key.pdf',
        'keySha256': 'f9c0cac1bcc8bd2dbe77ab1eb610f8d7a156dc1538637a0f56578fd4699db703'
    },
    'questions': questions_list
}

with open('data/ae/2010.json', 'w', encoding='utf-8') as f:
    json.dump(paper_data, f, indent=2)

print('Successfully generated data/ae/2010.json with all 65 questions.')
