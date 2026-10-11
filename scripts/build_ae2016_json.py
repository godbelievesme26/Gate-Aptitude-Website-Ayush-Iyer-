import json
import hashlib
import os

pdf_path = "internal/ae/AE2016.pdf"
with open(pdf_path, "rb") as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

key_pdf_path = "internal/ae/AE2016-key.pdf"
with open(key_pdf_path, "rb") as f:
    key_pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

with open("internal/ae/AE2016-key.json", "r", encoding="utf-8") as f:
    key_data = json.load(f)

key_map = {row["number"]: row for row in key_data["rows"]}

# Helper to compute SHA256 of figure assets
def get_fig_sha256(rel_path):
    with open(rel_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# Question definitions:
# (id, number, section, section_name, section_q_num, type, marks, negative_marks, text, figures, options)

raw_questions = [
    # GA Questions 1-10
    (
        "gate-2016-ae-ga-01", 1, "GA", "General Aptitude", 1, "MCQ", 1, 0.3333333333333333,
        "The chairman requested the aggrieved shareholders to _________________ him.",
        [],
        [
            {"label": "A", "text": "bare with"},
            {"label": "B", "text": "bore with"},
            {"label": "C", "text": "bear with"},
            {"label": "D", "text": "bare"}
        ]
    ),
    (
        "gate-2016-ae-ga-02", 2, "GA", "General Aptitude", 2, "MCQ", 1, 0.3333333333333333,
        "Identify the correct spelling out of the given options:",
        [],
        [
            {"label": "A", "text": "Managable"},
            {"label": "B", "text": "Manageable"},
            {"label": "C", "text": "Mangaeble"},
            {"label": "D", "text": "Managible"}
        ]
    ),
    (
        "gate-2016-ae-ga-03", 3, "GA", "General Aptitude", 3, "MCQ", 1, 0.3333333333333333,
        "Pick the odd one out in the following:\n\n13, 23, 33, 43, 53",
        [],
        [
            {"label": "A", "text": "23"},
            {"label": "B", "text": "33"},
            {"label": "C", "text": "43"},
            {"label": "D", "text": "53"}
        ]
    ),
    (
        "gate-2016-ae-ga-04", 4, "GA", "General Aptitude", 4, "MCQ", 1, 0.3333333333333333,
        "R2D2 is a robot. R2D2 can repair aeroplanes. No other robot can repair aeroplanes.\n\nWhich of the following can be logically inferred from the above statements?",
        [],
        [
            {"label": "A", "text": "R2D2 is a robot which can only repair aeroplanes."},
            {"label": "B", "text": "R2D2 is the only robot which can repair aeroplanes."},
            {"label": "C", "text": "R2D2 is a robot which can repair only aeroplanes."},
            {"label": "D", "text": "Only R2D2 is a robot."}
        ]
    ),
    (
        "gate-2016-ae-ga-05", 5, "GA", "General Aptitude", 5, "MCQ", 1, 0.3333333333333333,
        "If $|9y-6| = 3$, then $y^2 - 4y/3$ is ______.",
        [],
        [
            {"label": "A", "text": "0"},
            {"label": "B", "text": "+1/3"},
            {"label": "C", "text": "-1/3"},
            {"label": "D", "text": "undefined"}
        ]
    ),
    (
        "gate-2016-ae-ga-06", 6, "GA", "General Aptitude", 6, "NAT", 2, 0.0,
        "The following graph represents the installed capacity for cement production (in tonnes) and the actual production (in tonnes) of nine cement plants of a cement company. Capacity utilization of a plant is defined as ratio of actual production of cement to installed capacity. A plant with installed capacity of at least 200 tonnes is called a large plant and a plant with lesser capacity is called a small plant. The difference between total production of large plants and small plants, in tonnes is ______.",
        [{"src": "figures/gate-2016-ae-ga-06-figure-1.png", "alt": "Installed capacity and actual production bar graph for nine cement plants"}],
        []
    ),
    (
        "gate-2016-ae-ga-07", 7, "GA", "General Aptitude", 7, "MCQ", 2, 0.6666666666666666,
        "A poll of students appearing for masters in engineering indicated that 60 % of the students believed that mechanical engineering is a profession unsuitable for women. A research study on women with masters or higher degrees in mechanical engineering found that 99 % of such women were successful in their professions.\n\nWhich of the following can be logically inferred from the above paragraph?",
        [],
        [
            {"label": "A", "text": "Many students have misconceptions regarding various engineering disciplines."},
            {"label": "B", "text": "Men with advanced degrees in mechanical engineering believe women are well suited to be mechanical engineers."},
            {"label": "C", "text": "Mechanical engineering is a profession well suited for women with masters or higher degrees in mechanical engineering."},
            {"label": "D", "text": "The number of women pursuing higher degrees in mechanical engineering is small."}
        ]
    ),
    (
        "gate-2016-ae-ga-08", 8, "GA", "General Aptitude", 8, "MCQ", 2, 0.6666666666666666,
        "Sourya committee had proposed the establishment of Sourya Institutes of Technology (SITs) in line with Indian Institutes of Technology (IITs) to cater to the technological and industrial needs of a developing country.\n\nWhich of the following can be logically inferred from the above sentence?\n\nBased on the proposal,\n(i) In the initial years, SIT students will get degrees from IIT.\n(ii) SITs will have a distinct national objective.\n(iii) SIT like institutions can only be established in consultation with IIT.\n(iv) SITs will serve technological needs of a developing country.",
        [],
        [
            {"label": "A", "text": "(iii) and (iv) only."},
            {"label": "B", "text": "(i) and (iv) only."},
            {"label": "C", "text": "(ii) and (iv) only."},
            {"label": "D", "text": "(ii) and (iii) only."}
        ]
    ),
    (
        "gate-2016-ae-ga-09", 9, "GA", "General Aptitude", 9, "MCQ", 2, 0.6666666666666666,
        "Shaquille O’ Neal is a 60% career free throw shooter, meaning that he successfully makes 60 free throws out of 100 attempts on average. What is the probability that he will successfully make exactly 6 free throws in 10 attempts?",
        [],
        [
            {"label": "A", "text": "0.2508"},
            {"label": "B", "text": "0.2816"},
            {"label": "C", "text": "0.2934"},
            {"label": "D", "text": "0.6000"}
        ]
    ),
    (
        "gate-2016-ae-ga-10", 10, "GA", "General Aptitude", 10, "NAT", 2, 0.0,
        "The numeral in the units position of $211^{870} + 146^{127} \\times 3^{424}$ is ______.",
        [],
        []
    ),

    # AE Questions 1-25 (Numbers 11 to 35)
    (
        "gate-2016-ae-ae-11", 11, "AE", "Aerospace Engineering", 1, "MCQ", 1, 0.3333333333333333,
        "With increase in airfoil thickness, the critical Mach number for an airfoil is likely to",
        [],
        [
            {"label": "A", "text": "decrease."},
            {"label": "B", "text": "increase."},
            {"label": "C", "text": "remain unchanged."},
            {"label": "D", "text": "be undefined."}
        ]
    ),
    (
        "gate-2016-ae-ae-12", 12, "AE", "Aerospace Engineering", 2, "NAT", 1, 0.0,
        "Due to a body in potential flow, the velocity at a point A in the flow field is 20 m/s while the free stream velocity is only 10 m/s. The value of coefficient of pressure ($C_p$) at the point A is ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-13", 13, "AE", "Aerospace Engineering", 3, "MCQ", 1, 0.3333333333333333,
        "Which of the following airfoil will have location of the maximum camber at half chord length from the leading edge?",
        [],
        [
            {"label": "A", "text": "NACA 5212"},
            {"label": "B", "text": "NACA 1225"},
            {"label": "C", "text": "NACA 2215"},
            {"label": "D", "text": "NACA 2512"}
        ]
    ),
    (
        "gate-2016-ae-ae-14", 14, "AE", "Aerospace Engineering", 4, "MCQ", 1, 0.3333333333333333,
        "For a laminar incompressible flow past a flat plate at zero angle of attack, the variation of skin friction drag coefficient ($C_f$) with Reynolds number based on the chord length ($Re_c$) can be expressed as",
        [],
        [
            {"label": "A", "text": "$C_f \\propto \\sqrt{Re_c}$"},
            {"label": "B", "text": "$C_f \\propto Re_c$"},
            {"label": "C", "text": "$C_f \\propto 1/\\sqrt{Re_c}$"},
            {"label": "D", "text": "$C_f \\propto 1/Re_c$"}
        ]
    ),
    (
        "gate-2016-ae-ae-15", 15, "AE", "Aerospace Engineering", 5, "MCQ", 1, 0.3333333333333333,
        "Which of the following statement is NOT TRUE across an oblique shock wave?",
        [],
        [
            {"label": "A", "text": "Static temperature increases, total temperature remains constant."},
            {"label": "B", "text": "Static pressure increases, static temperature increases."},
            {"label": "C", "text": "Static temperature increases, total pressure decreases."},
            {"label": "D", "text": "Static pressure increases, total temperature decreases."}
        ]
    ),
    (
        "gate-2016-ae-ae-16", 16, "AE", "Aerospace Engineering", 6, "MCQ", 1, 0.3333333333333333,
        "For a completely subsonic isentropic flow through a convergent nozzle, which of the following statement is TRUE?",
        [],
        [
            {"label": "A", "text": "Pressure at the nozzle exit > back pressure."},
            {"label": "B", "text": "Pressure at the nozzle exit < back pressure."},
            {"label": "C", "text": "Pressure at the nozzle exit = back pressure."},
            {"label": "D", "text": "Pressure at the nozzle exit = total pressure."}
        ]
    ),
    (
        "gate-2016-ae-ae-17", 17, "AE", "Aerospace Engineering", 7, "MCQ", 1, 0.3333333333333333,
        "Which of the following aircraft engines has the highest propulsive efficiency at a cruising Mach number of less than 0.5?",
        [],
        [
            {"label": "A", "text": "Turbofan engine"},
            {"label": "B", "text": "Turbojet engine"},
            {"label": "C", "text": "Turboprop engine"},
            {"label": "D", "text": "Ramjet engine"}
        ]
    ),
    (
        "gate-2016-ae-ae-18", 18, "AE", "Aerospace Engineering", 8, "MCQ", 1, 0.3333333333333333,
        "Air, with a Prandtl number of 0.7, flows over a flat plate at a high Reynolds number. Which of the following statement is TRUE?",
        [],
        [
            {"label": "A", "text": "Thermal boundary layer is thicker than the velocity boundary layer."},
            {"label": "B", "text": "Thermal boundary layer is thinner than the velocity boundary layer."},
            {"label": "C", "text": "Thermal boundary layer is as thick as the velocity boundary layer."},
            {"label": "D", "text": "There is no relationship between the thicknesses of thermal and velocity boundary layers."}
        ]
    ),
    (
        "gate-2016-ae-ae-19", 19, "AE", "Aerospace Engineering", 9, "MCQ", 1, 0.3333333333333333,
        "Consider an eigenvalue problem given by $\\mathbf{A}\\mathbf{x}=\\lambda_i\\mathbf{x}$. If $\\lambda_i$ represent the eigenvalues of the non-singular square matrix $\\mathbf{A}$, then what will be the eigenvalues of matrix $\\mathbf{A}^2$?",
        [],
        [
            {"label": "A", "text": "$\\lambda_i^4$"},
            {"label": "B", "text": "$\\lambda_i^2$"},
            {"label": "C", "text": "$\\lambda_i^{1/2}$"},
            {"label": "D", "text": "$\\lambda_i^{1/4}$"}
        ]
    ),
    (
        "gate-2016-ae-ae-20", 20, "AE", "Aerospace Engineering", 10, "MCQ", 1, 0.3333333333333333,
        "If $\\mathbf{A}$ and $\\mathbf{B}$ are both non-singular $n\\times n$ matrices, then which of the following statement is NOT TRUE. Note: $\\det$ represents the determinant of a matrix.",
        [],
        [
            {"label": "A", "text": "$\\det(\\mathbf{AB}) = \\det(\\mathbf{A})\\det(\\mathbf{B})$"},
            {"label": "B", "text": "$\\det(\\mathbf{A}+\\mathbf{B}) = \\det(\\mathbf{A}) + \\det(\\mathbf{B})$"},
            {"label": "C", "text": "$\\det(\\mathbf{AA}^{-1}) = 1$"},
            {"label": "D", "text": "$\\det(\\mathbf{A}^T) = \\det(\\mathbf{A})$"}
        ]
    ),
    (
        "gate-2016-ae-ae-21", 21, "AE", "Aerospace Engineering", 11, "NAT", 1, 0.0,
        "The total number of material constants that are necessary and sufficient to describe the three dimensional Hooke’s law for an isotropic material is ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-22", 22, "AE", "Aerospace Engineering", 12, "MCQ", 1, 0.3333333333333333,
        "Determine the correctness or otherwise of the following statements, [a] and [r]:\n\n[a]: In a plane stress problem, the shear strains along the thickness direction of a body are zero but the normal strain along the thickness is not zero.\n\n[r]: In a plane stress problem, Poisson effect induces the normal strain along the thickness direction of the body.",
        [],
        [
            {"label": "A", "text": "Both [a] and [r] are true and [r] is the correct reason for [a]."},
            {"label": "B", "text": "Both [a] and [r] are true but [r] is not the correct reason for [a]."},
            {"label": "C", "text": "Both [a] and [r] are false."},
            {"label": "D", "text": "[a] is true but [r] is false."}
        ]
    ),
    (
        "gate-2016-ae-ae-23", 23, "AE", "Aerospace Engineering", 13, "MCQ", 1, 0.3333333333333333,
        "Consider four thin-walled beams of different open cross-sections, as shown in the cases (i-iv). A shear force of magnitude 'F' acts vertically downward at the location 'P' in all the beams. In which of the following case, does the shear force induce bending and twisting?",
        [{"src": "figures/gate-2016-ae-ae-23-figure-1.png", "alt": "Four thin-walled beam open cross-sections under shear force F at point P"}],
        [
            {"label": "A", "text": "(i)"},
            {"label": "B", "text": "(ii)"},
            {"label": "C", "text": "(iii)"},
            {"label": "D", "text": "(iv)"}
        ]
    ),
    (
        "gate-2016-ae-ae-24", 24, "AE", "Aerospace Engineering", 14, "NAT", 1, 0.0,
        "The effective stiffness of the spring-mass system as shown in the figure below is ______ N/mm.",
        [{"src": "figures/gate-2016-ae-ae-24-figure-1.png", "alt": "Spring-mass system with spring stiffnesses 4 N/mm, 2 N/mm, 2 N/mm and mass m"}],
        []
    ),
    (
        "gate-2016-ae-ae-25", 25, "AE", "Aerospace Engineering", 15, "MCQ", 1, 0.3333333333333333,
        "A structural member supports loads, which produce at a particular point, a state of pure shear stress of $50\\text{ N/mm}^2$. At what angles are the principal planes oriented with respect to the plane of pure shear?",
        [],
        [
            {"label": "A", "text": "$\\pi/6$ and $2\\pi/3$"},
            {"label": "B", "text": "$\\pi/4$ and $3\\pi/4$"},
            {"label": "C", "text": "$\\pi/4$ and $\\pi/2$"},
            {"label": "D", "text": "$\\pi/2$ and $\\pi$"}
        ]
    ),
    (
        "gate-2016-ae-ae-26", 26, "AE", "Aerospace Engineering", 16, "NAT", 1, 0.0,
        "Let $x$ be a positive real number. The function $f(x) = x^2 + 1/x^2$ has its minima at $x=$ ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-27", 27, "AE", "Aerospace Engineering", 17, "NAT", 1, 0.0,
        "The vector $\\vec{u}$ is defined as $\\vec{u} = y\\hat{e}_x - x\\hat{e}_y$, where $\\hat{e}_x$ and $\\hat{e}_y$ are the unit vectors along $x$ and $y$ directions, respectively. If the vector $\\vec{\\omega}$ is defined as $\\vec{\\omega} = \\vec{\\nabla} \\times \\vec{u}$, then $|(\\vec{\\omega} \\cdot \\vec{\\nabla})\\vec{u}| =$ ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-28", 28, "AE", "Aerospace Engineering", 18, "MCQ", 1, 0.3333333333333333,
        "The partial differential equation $\\frac{\\partial u}{\\partial t} = \\alpha \\frac{\\partial^2 u}{\\partial x^2}$, where $\\alpha$ is a positive constant, is",
        [],
        [
            {"label": "A", "text": "circular."},
            {"label": "B", "text": "elliptic."},
            {"label": "C", "text": "hyperbolic."},
            {"label": "D", "text": "parabolic."}
        ]
    ),
    (
        "gate-2016-ae-ae-29", 29, "AE", "Aerospace Engineering", 19, "MCQ", 1, 0.3333333333333333,
        "Combustion in gas turbine engines is ideally represented as the following process:",
        [],
        [
            {"label": "A", "text": "Adiabatic"},
            {"label": "B", "text": "Isentropic"},
            {"label": "C", "text": "Isobaric"},
            {"label": "D", "text": "Isochoric"}
        ]
    ),
    (
        "gate-2016-ae-ae-30", 30, "AE", "Aerospace Engineering", 20, "MCQ", 1, 0.3333333333333333,
        "For a given chamber pressure, the thrust of a rocket engine is highest when",
        [],
        [
            {"label": "A", "text": "the rocket is operating at its design altitude."},
            {"label": "B", "text": "the rocket is operating in vacuum."},
            {"label": "C", "text": "the rocket is operating at sea-level."},
            {"label": "D", "text": "there is a normal shock in the rocket nozzle."}
        ]
    ),
    (
        "gate-2016-ae-ae-31", 31, "AE", "Aerospace Engineering", 21, "MCQ", 1, 0.3333333333333333,
        "The damping ratio in phugoid motion for gliders is usually less compared to powered aircraft because",
        [],
        [
            {"label": "A", "text": "gliders are unpowered."},
            {"label": "B", "text": "gliders are light."},
            {"label": "C", "text": "lift to drag ratio is higher for gliders."},
            {"label": "D", "text": "gliders fly at low speed."}
        ]
    ),
    (
        "gate-2016-ae-ae-32", 32, "AE", "Aerospace Engineering", 22, "MCQ", 1, 0.3333333333333333,
        "During an aircraft cruising flight, the altitude above the ground is usually measured using",
        [],
        [
            {"label": "A", "text": "dynamic pressure."},
            {"label": "B", "text": "static pressure."},
            {"label": "C", "text": "radar."},
            {"label": "D", "text": "laser range finder."}
        ]
    ),
    (
        "gate-2016-ae-ae-33", 33, "AE", "Aerospace Engineering", 23, "MCQ", 1, 0.3333333333333333,
        "Indicated airspeed is used by a pilot during",
        [],
        [
            {"label": "A", "text": "take-off."},
            {"label": "B", "text": "navigation."},
            {"label": "C", "text": "setting the engine RPM."},
            {"label": "D", "text": "setting the elevator angle."}
        ]
    ),
    (
        "gate-2016-ae-ae-34", 34, "AE", "Aerospace Engineering", 24, "MCQ", 1, 0.3333333333333333,
        "The pitch angle and the angle of attack for a fixed wing aircraft are equal during",
        [],
        [
            {"label": "A", "text": "wings level constant altitude flight."},
            {"label": "B", "text": "unaccelerated climb."},
            {"label": "C", "text": "unaccelerated descent."},
            {"label": "D", "text": "landing."}
        ]
    ),
    (
        "gate-2016-ae-ae-35", 35, "AE", "Aerospace Engineering", 25, "MCQ", 1, 0.3333333333333333,
        "The load factor of an aircraft turning at a constant altitude is 2. The coefficient of lift required for turning flight as compared to level flight at the same speed will be",
        [],
        [
            {"label": "A", "text": "same"},
            {"label": "B", "text": "half"},
            {"label": "C", "text": "double"},
            {"label": "D", "text": "four times"}
        ]
    ),

    # AE Questions 26-55 (Numbers 36 to 65)
    (
        "gate-2016-ae-ae-36", 36, "AE", "Aerospace Engineering", 26, "NAT", 2, 0.0,
        "An un-mixed turbofan engine with a bypass ratio of 6.0, flies with a velocity of 200 m/s. The core and the bypass nozzles of the engine, that are both convergent nozzles, operate under choked condition and have exhaust static temperatures of 580 K and 295 K, respectively. The specific gas constant and the ratio of specific heats for both the streams are 287 J/kgK and 1.4, respectively. If the fuel-air ratio is negligible, the thrust per unit mass flow rate generated by the engine is _______ Ns/kg.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-37", 37, "AE", "Aerospace Engineering", 27, "MCQ", 2, 0.6666666666666666,
        "A single-stage gas turbine operates with an axial absolute flow at the entry and exit from the stage. The absolute flow angle at the nozzle exit is $70^\\circ$. The turbine stage generates a specific work of 228 kJ/kg when operating with a mean blade speed of 440 m/s. The absolute velocity at the rotor entry is",
        [],
        [
            {"label": "A", "text": "275.7 m/s"},
            {"label": "B", "text": "551.5 m/s"},
            {"label": "C", "text": "1103.0 m/s"},
            {"label": "D", "text": "1654.5 m/s"}
        ]
    ),
    (
        "gate-2016-ae-ae-38", 38, "AE", "Aerospace Engineering", 28, "NAT", 2, 0.0,
        "An axial compressor operates such that it has an inlet and an exit total temperature of 300 K and 430 K, respectively. The isentropic efficiency of the compressor is 85 %. If the ratio of specific heats is 1.4, then the total pressure ratio across the compressor is ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-39", 39, "AE", "Aerospace Engineering", 29, "MCQ", 2, 0.6666666666666666,
        "The maximum value of coefficient of lift ($C_l$) for a 2D circular cylinder, provided at least one stagnation point lies on the cylinder surface, is predicted by the potential flow theory to be",
        [],
        [
            {"label": "A", "text": "$\\pi/2$"},
            {"label": "B", "text": "$\\pi$"},
            {"label": "C", "text": "$2\\pi$"},
            {"label": "D", "text": "$4\\pi$"}
        ]
    ),
    (
        "gate-2016-ae-ae-40", 40, "AE", "Aerospace Engineering", 30, "NAT", 2, 0.0,
        "The nozzle AB, as shown below, leading to the test section of a low speed subsonic wind tunnel, has a contraction ratio of 10:1. The pressure difference across the nozzle is maintained at $1000\\text{ N/m}^2$ and the density of air is $1.23\\text{ kg/m}^3$. Assuming one-dimensional, steady, inviscid flow, the velocity in the test section as measured at point B is ______ m/s.",
        [{"src": "figures/gate-2016-ae-ae-40-figure-1.png", "alt": "Nozzle AB with 10 to 1 contraction ratio leading to test section"}],
        []
    ),
    (
        "gate-2016-ae-ae-41", 41, "AE", "Aerospace Engineering", 31, "MCQ", 2, 0.6666666666666666,
        "The rate of change of moment coefficient with respect to the angle of attack, $\\frac{dC_m}{d\\alpha}$, at half chord point of a thin airfoil, as per approximations from the thin airfoil theory is",
        [],
        [
            {"label": "A", "text": "$\\pi/4\\text{ radian}^{-1}$"},
            {"label": "B", "text": "$\\pi/2\\text{ radian}^{-1}$"},
            {"label": "C", "text": "$\\pi\\text{ radian}^{-1}$"},
            {"label": "D", "text": "$2\\pi\\text{ radian}^{-1}$"}
        ]
    ),
    (
        "gate-2016-ae-ae-42", 42, "AE", "Aerospace Engineering", 32, "MCQ", 2, 0.6666666666666666,
        "An untwisted wing of elliptic planform and aspect ratio 6 consists of thin symmetric airfoil sections. The coefficient of lift ($C_L$) at $10^\\circ$ angle of attack assuming inviscid incompressible flow is",
        [],
        [
            {"label": "A", "text": "$\\pi^2/16$"},
            {"label": "B", "text": "$\\pi^2/12$"},
            {"label": "C", "text": "$\\pi^2/8$"},
            {"label": "D", "text": "$\\pi/2$"}
        ]
    ),
    (
        "gate-2016-ae-ae-43", 43, "AE", "Aerospace Engineering", 33, "NAT", 2, 0.0,
        "A gaseous mixture of air and fuel enters a constant area combustion chamber at a velocity of 100 m/s and at a static temperature of 300 K. The heat release due to combustion is 1000 kJ/kg. The specific heat at constant pressure of the calorically perfect gas is 1000 J/kgK. The total temperature of air-fuel mixture after combustion is ______ K.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-44", 44, "AE", "Aerospace Engineering", 34, "MCQ", 2, 0.6666666666666666,
        "Consider 1-D, steady, inviscid, compressible flow through a convergent nozzle. The total temperature and total pressure are $T_o$, $P_o$ respectively. The flow through the nozzle is choked with a mass flow rate of $\\dot{m}_o$. If the total temperature is increased to $4T_o$, with total pressure remaining unchanged, then the mass flow rate through the nozzle",
        [],
        [
            {"label": "A", "text": "remains unchanged."},
            {"label": "B", "text": "becomes half of $\\dot{m}_o$."},
            {"label": "C", "text": "becomes twice of $\\dot{m}_o$."},
            {"label": "D", "text": "becomes four times of $\\dot{m}_o$."}
        ]
    ),
    (
        "gate-2016-ae-ae-45", 45, "AE", "Aerospace Engineering", 35, "MCQ", 2, 0.6666666666666666,
        "Consider a second order linear ordinary differential equation $\\frac{d^2 y}{dx^2} - 4\\frac{dy}{dx} + 4y = 0$, with the boundary conditions $y(0) = 1$; $\\left.\\frac{dy}{dx}\\right|_{x=0} = 1$. The value of $y$ at $x = 1$ is",
        [],
        [
            {"label": "A", "text": "0"},
            {"label": "B", "text": "1"},
            {"label": "C", "text": "e"},
            {"label": "D", "text": "$e^2$"}
        ]
    ),
    (
        "gate-2016-ae-ae-46", 46, "AE", "Aerospace Engineering", 36, "MCQ", 2, 0.6666666666666666,
        "Consider the following system of linear equations:\n$$2x - y + z = 1$$\n$$3x - 3y + 4z = 6$$\n$$x - 2y + 3z = 4$$\nThis system of linear equations has",
        [],
        [
            {"label": "A", "text": "no solution."},
            {"label": "B", "text": "one solution."},
            {"label": "C", "text": "two solutions."},
            {"label": "D", "text": "three solutions."}
        ]
    ),
    (
        "gate-2016-ae-ae-47", 47, "AE", "Aerospace Engineering", 37, "NAT", 2, 0.0,
        "A bar made of linear elastic isotropic material is fixed at one end and subjected to an axial force of 1 kN at the other end. The cross-sectional area of the bar is $100\\text{ mm}^2$, length is 100 mm and the Young’s Modulus is $1\\times 10^5\\text{ N/mm}^2$. The strain energy stored in the bar is ______ Nmm.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-48", 48, "AE", "Aerospace Engineering", 38, "NAT", 2, 0.0,
        "A cantilever beam-spring system is shown in the figure. The beam is made with a material of Young’s modulus $1\\times 10^5\\text{ N/mm}^2$ and geometry such that its moment of inertia is $100\\text{ mm}^4$ and length $l = 100\\text{ mm}$. It is supported by a spring of stiffness $K = 30\\text{ N/mm}$ and subjected to a load of $P = 100\\text{ N}$ at the point 'B'. The deflection at the point 'B' due to the load P is ______ mm.",
        [{"src": "figures/gate-2016-ae-ae-48-figure-1.png", "alt": "Cantilever beam AB of length l with spring K and load P at tip B"}],
        []
    ),
    (
        "gate-2016-ae-ae-49", 49, "AE", "Aerospace Engineering", 39, "MCQ", 2, 0.6666666666666666,
        "Determine the correctness or otherwise of the following statements, [a] and [r],\n\n[a]: Ribs, used in airplane wings, increase the column buckling strength of the longitudinal stiffeners.\n\n[r]: Ribs distribute concentrated loads into the structure and redistribute stresses around discontinuities.",
        [],
        [
            {"label": "A", "text": "Both [a] and [r] are true and [r] is the correct reason for [a]"},
            {"label": "B", "text": "Both [a] and [r] are true but [r] is not the correct reason for [a]"},
            {"label": "C", "text": "Both [a] and [r] are false"},
            {"label": "D", "text": "[a] is true but [r] is false"}
        ]
    ),
    (
        "gate-2016-ae-ae-50", 50, "AE", "Aerospace Engineering", 40, "NAT", 2, 0.0,
        "A channel section shown in the figure has uniform thickness. It is subjected to an anticlockwise torque of $62.5\\times 10^3\\text{ Nmm}$. The maximum possible thickness of the channel section, such that the shear stress induced in it does not exceed $100\\text{ N/mm}^2$, is ______ mm.",
        [{"src": "figures/gate-2016-ae-ae-50-figure-1.png", "alt": "Channel section with flange lengths 100 mm and web height 100 mm"}],
        []
    ),
    (
        "gate-2016-ae-ae-51", 51, "AE", "Aerospace Engineering", 41, "NAT", 2, 0.0,
        "The governing differential equation of motion of a damped system is given by $m\\frac{d^2 x}{dt^2} + c\\frac{dx}{dt} + kx = 0$. If $m = 1\\text{ kg}$, $c = 2\\text{ Ns/m}$ and $k = 2\\text{ N/m}$ then the frequency of the damped oscillation of this system is ______ rad/s.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-52", 52, "AE", "Aerospace Engineering", 42, "NAT", 2, 0.0,
        "The two dimensional state of stress in a body is described by the Airy’s stress function:\n$$\\phi = 5\\frac{x^4}{12} + \\frac{x^3 y}{6} + 3\\frac{x^2 y^2}{2} + 7\\frac{xy^3}{6} + E\\frac{y^4}{12}$$\nThe Airy’s stress function will satisfy the equilibrium and the compatibility requirements if and only if the value of the coefficient E is ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-53", 53, "AE", "Aerospace Engineering", 43, "NAT", 2, 0.0,
        "The value of definite integral $\\int_0^\\pi (x \\sin x)dx$ is ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-54", 54, "AE", "Aerospace Engineering", 44, "NAT", 2, 0.0,
        "Use Newton-Raphson method to solve the equation: $x e^x = 1$. Begin with the initial guess $x_0 = 0.5$. The solution after one step is $x = $ ______.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-55", 55, "AE", "Aerospace Engineering", 45, "NAT", 2, 0.0,
        "A wall of thickness 5 mm is heated by a hot gas flowing along the wall. The gas is at a temperature of 3000 K, and the convective heat transfer coefficient is $160\\text{ W/m}^2\\text{K}$. The wall thermal conductivity is $40\\text{ W/mK}$. If the colder side of the wall is held at 500 K, the temperature of the side exposed to the hot gas is _______ K.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-56", 56, "AE", "Aerospace Engineering", 46, "NAT", 2, 0.0,
        "A launch vehicle has a main rocket engine with two identical strap-on motors, all of which fire simultaneously during the operation. The main engine delivers a thrust of 6300 kN with a specific impulse of 428 s. Each strap-on motor delivers a thrust of 12000 kN with specific impulse of 292 s. The acceleration due to gravity is $9.81\\text{ m/s}^2$. The effective (combined) specific impulse of the vehicle is _______ s.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-57", 57, "AE", "Aerospace Engineering", 47, "MCQ", 2, 0.6666666666666666,
        "A substance experiences an entropy change of $\\Delta s > 0$ in a quasi-steady process. The rise in temperature (corresponding to the entropy change $\\Delta s$) is highest for the following process:",
        [],
        [
            {"label": "A", "text": "isenthalpic"},
            {"label": "B", "text": "isobaric"},
            {"label": "C", "text": "isochoric"},
            {"label": "D", "text": "isothermal"}
        ]
    ),
    (
        "gate-2016-ae-ae-58", 58, "AE", "Aerospace Engineering", 48, "NAT", 2, 0.0,
        "In a particular rocket engine, helium propellant is heated to 6000 K and 95% of its total enthalpy is recovered as kinetic energy of the nozzle exhaust. Consider helium to be a calorically perfect gas with specific heat at constant pressure of 5200 J/kgK. The exhaust velocity for such a rocket for an optimum expansion is _____ m/s.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-59", 59, "AE", "Aerospace Engineering", 49, "NAT", 2, 0.0,
        "An aircraft is flying level in the North direction at a velocity of 55 m/s under cross wind from East to West of 5 m/s. For the given aircraft $C_{n\\beta} = 0.012/\\text{deg}$ and $C_{n\\delta r} = -0.0072/\\text{deg}$, where $\\delta r$ is the rudder deflection and $\\beta$ is the side slip angle. The rudder deflection exerted by pilot is __________ degrees.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-60", 60, "AE", "Aerospace Engineering", 50, "NAT", 2, 0.0,
        "An aircraft weighing 10000 N is flying level at 100 m/s and it is powered by a jet engine. The thrust required for level flight is 1000 N. The maximum possible thrust produced by the jet engine is 5000 N. The minimum time required to climb 1000 m, when flight speed is 100 m/s, is ________s.",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-61", 61, "AE", "Aerospace Engineering", 51, "MCQ", 2, 0.6666666666666666,
        "The aircraft velocity (m/s) components in body axes are given as $[u, v, w] = [100, 10, 10]$. The air velocity (m/s), angle of attack (deg) and sideslip angle (deg) in that order are",
        [],
        [
            {"label": "A", "text": "[120, 0.1, 0.1]"},
            {"label": "B", "text": "[100, 0.1, 0.1]"},
            {"label": "C", "text": "[100.995, 0.1, 5.73]"},
            {"label": "D", "text": "[100.995, 5.71, 5.68]"}
        ]
    ),
    (
        "gate-2016-ae-ae-62", 62, "AE", "Aerospace Engineering", 52, "MCQ", 2, 0.6666666666666666,
        "The Dutch roll motion of the aircraft is described by following relationship:\n$$\\begin{bmatrix} \\Delta \\dot{\\beta} \\\\ \\Delta \\dot{r} \\end{bmatrix} = \\begin{bmatrix} -0.26 & -1 \\\\ 4.49 & -0.76 \\end{bmatrix} \\begin{bmatrix} \\Delta \\beta \\\\ \\Delta r \\end{bmatrix}$$\nThe undamped natural frequency (rad/s) and damping ratio for the Dutch roll motion in that order are:",
        [],
        [
            {"label": "A", "text": "4.68, 1.02"},
            {"label": "B", "text": "4.49, 1.02"},
            {"label": "C", "text": "2.165, 0.235"},
            {"label": "D", "text": "2.165, 1.02"}
        ]
    ),
    (
        "gate-2016-ae-ae-63", 63, "AE", "Aerospace Engineering", 53, "NAT", 2, 0.0,
        "A glider weighing 3300 N is flying at 1000 m above sea level. The wing area is $14.1\\text{ m}^2$ and the air density is $1.23\\text{ kg/m}^3$. Under zero wind conditions, the velocity for maximum range is __________ m/s.\n\n| $\\alpha$ (deg) | $C_L$ | $C_D$ | $C_L/C_D$ |\n| :---: | :---: | :---: | :---: |\n| 11 | 1.46 | 0.0865 | 16.9 |\n| 9 | 1.36 | 0.0675 | 20.1 |\n| 7 | 1.23 | 0.0535 | 22.9 |\n| 5 | 1.08 | 0.0440 | 24.5 |\n| 3 | 0.90 | 0.0350 | 25.7 |\n| 1 | 0.70 | 0.0275 | 25.4 |\n| -1 | 0.49 | 0.0220 | 22.2 |\n| -3 | 0.25 | 0.0180 | 13.8 |",
        [],
        []
    ),
    (
        "gate-2016-ae-ae-64", 64, "AE", "Aerospace Engineering", 54, "MCQ", 2, 0.6666666666666666,
        "A rocket, with a total lift-off mass of 10000 kg, moves vertically upward from rest under a constant gravitational acceleration of $9.81\\text{ m/s}^2$. The propellant mass of 8400 kg burns at a constant rate of 1200 kg/s. If the specific impulse of the rocket engine is 240 s, neglecting drag, the burnout velocity in m/s is",
        [],
        [
            {"label": "A", "text": "3933.7"},
            {"label": "B", "text": "4314.6"},
            {"label": "C", "text": "4245.9"},
            {"label": "D", "text": "4383.3"}
        ]
    ),
    (
        "gate-2016-ae-ae-65", 65, "AE", "Aerospace Engineering", 55, "MCQ", 2, 0.6666666666666666,
        "A satellite is injected at an altitude of 350 km above the Earth’s surface, with a velocity of 8.0 km/s parallel to the local horizon. (Earth radius = 6378 km, $\\mu_E$ ($GM = \\text{Gravitational constant} \\times \\text{Earth mass}$) = $3.986\\times 10^{14}\\text{ m}^3\\text{s}^{-2}$). The satellite",
        [],
        [
            {"label": "A", "text": "forms a circular orbit."},
            {"label": "B", "text": "forms an elliptic orbit."},
            {"label": "C", "text": "escapes from Earth’s gravitational field."},
            {"label": "D", "text": "falls back to earth."}
        ]
    ),
]

questions = []
question_refs = []

for item in raw_questions:
    qid, qnum, sec, sec_name, sec_q_num, qtype, marks, neg_marks, text, figs, opts = item
    
    key_info = key_map[qnum]
    raw_key = key_info["rawKey"]
    
    # Parse accepted answer according to schema
    if raw_key == "MTA*":
        answer = "MTA"
        accepted_answers = ["MTA"]
    elif qtype == "NAT":
        if " OR " in raw_key:
            parts = raw_key.split(" OR ")
            answer = []
            for p in parts:
                if " to " in p:
                    answer.append([float(x) for x in p.split(" to ")])
                else:
                    answer.append(float(p))
            accepted_answers = answer
        elif " to " in raw_key:
            answer = [float(x) for x in raw_key.split(" to ")]
            accepted_answers = [answer]
        else:
            answer = float(raw_key)
            accepted_answers = [answer]
    elif qtype == "MSQ" or ";" in raw_key or " OR " in raw_key or " or " in raw_key:
        if " OR " in raw_key or " or " in raw_key:
            parts = [s.strip() for s in (raw_key.split(" OR ") if " OR " in raw_key else raw_key.split(" or "))]
        else:
            parts = [s.strip() for s in raw_key.split(";")]
        answer = parts
        accepted_answers = parts
    else:
        answer = raw_key
        accepted_answers = [raw_key]
        
    formatted_figs = []
    for fig in figs:
        fsrc = fig["src"]
        formatted_figs.append({
            "src": fsrc,
            "alt": fig["alt"],
            "page": 2 if "ga-06" in fsrc else (5 if "ae-23" in fsrc else (6 if "ae-24" in fsrc else (8 if "ae-40" in fsrc else (9 if "ae-48" in fsrc else 10)))),
            "source": {
                "file": pdf_path,
                "sha256": pdf_sha256,
                "page": 2 if "ga-06" in fsrc else (5 if "ae-23" in fsrc else (6 if "ae-24" in fsrc else (8 if "ae-40" in fsrc else (9 if "ae-48" in fsrc else 10)))),
                "verificationStatus": "source-verified",
                "verifiedOn": "2026-10-07"
            }
        })
        
    if qnum <= 5:
        pdf_page = 1
    elif qnum <= 7:
        pdf_page = 2
    elif qnum <= 10:
        pdf_page = 3
    elif qnum <= 18:
        pdf_page = 4
    elif qnum <= 23:
        pdf_page = 5
    elif qnum <= 32:
        pdf_page = 6
    elif qnum <= 39:
        pdf_page = 7
    elif qnum <= 45:
        pdf_page = 8
    elif qnum <= 49:
        pdf_page = 9
    elif qnum <= 57:
        pdf_page = 10
    elif qnum <= 64:
        pdf_page = 11
    else:
        pdf_page = 12

    q_obj = {
        "id": qid,
        "number": qnum,
        "year": 2016,
        "paper": "AE",
        "section": sec,
        "subject": sec_name,
        "type": qtype,
        "marks": marks,
        "negativeMarks": neg_marks,
        "question": text,
        "options": opts,
        "answer": answer,
        "acceptedAnswers": accepted_answers,
        "markingRule": "gate-2016-official",
        "hasFigure": len(formatted_figs) > 0,
        "figures": formatted_figs,
        "groupId": None,
        "source": {
            "paper": "AE",
            "year": 2016,
            "questionNumber": sec_q_num,
            "section": sec,
            "file": pdf_path,
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
            "paper": "AE",
            "questionNumber": sec_q_num,
            "section": sec,
            "file": key_pdf_path,
            "sha256": key_pdf_sha256,
            "verifiedOn": "2026-10-07"
        }
    }
    questions.append(q_obj)
    
    question_refs.append({
        "id": qid,
        "number": qnum,
        "section": sec,
        "marks": marks,
        "type": qtype
    })

mcq_count = sum(1 for q in questions if q['type'] == 'MCQ')
msq_count = sum(1 for q in questions if q['type'] == 'MSQ')
nat_count = sum(1 for q in questions if q['type'] == 'NAT')
fig_count = sum(len(q['figures']) for q in questions)

paper_json = {
    "schemaVersion": 1,
    "id": "gate-2016-ae",
    "exam": "GATE",
    "year": 2016,
    "paper": "AE",
    "title": "GATE Aerospace Engineering 2016",
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
    "questionRefs": question_refs,
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
        "file": pdf_path,
        "sha256": pdf_sha256,
        "pageCount": 14
    },
    "ingestionStatus": "complete",
    "verificationStatus": "source-verified",
    "verifiedOn": "2026-10-07",
    "questions": questions
}

os.makedirs('data/ae', exist_ok=True)
with open('data/ae/2016.json', 'w', encoding='utf-8') as f:
    json.dump(paper_json, f, indent=2, ensure_ascii=False)

print(f"Generated data/ae/2016.json with {len(questions)} questions (MCQ: {mcq_count}, MSQ: {msq_count}, NAT: {nat_count}, Figures: {fig_count}).")

# Update manifest.json
manifest_path = 'data/ae/manifest.json'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

for row in manifest.get('years', []):
    if row.get('year') == 2016:
        row['sourcePdf'] = pdf_path
        row['ingestionStatus'] = "complete"
        row['verificationStatus'] = "source-verified"
        row['path'] = "data/ae/2016.json"
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
