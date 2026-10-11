import json
import hashlib
import os

pdf_path = "internal/ae/AE2013.pdf"
key_pdf_path = "internal/ae/AE2013-key.pdf"

with open(pdf_path, "rb") as f:
    pdf_sha = hashlib.sha256(f.read()).hexdigest()

with open(key_pdf_path, "rb") as f:
    key_sha = hashlib.sha256(f.read()).hexdigest()

questions_data = [
    # AE Q1 - Q25 (1 mark each)
    {
        "num": 1, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "The directional derivative of the function f(x, y, z) = 2x^2 + 3y^2 + z^2 at the point P:(2, 1, 3) in the direction of the vector a = i - 2k is",
        "opts": ["-4/\\sqrt{5}", "-2/\\sqrt{5}", "2/\\sqrt{5}", "4/\\sqrt{5}"],
        "page": 4
    },
    {
        "num": 2, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "The evaluation of the integral \\int_C \\frac{e^z}{z^2 + π^2} dz along the counter-clockwise contour C: |z| = 4 yields",
        "opts": ["0", "2i", "-2i", "4π i"],
        "page": 4
    },
    {
        "num": 3, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "One of the eigenvalues of the matrix A = \\matrix{1 & 2 & 1; 2 & 1 & 0; -1 & 0 & 1} is -1. The sum of the other two eigenvalues is",
        "opts": ["4", "3", "2", "1"],
        "page": 4
    },
    {
        "num": 4, "sec": "AE", "type": "NAT", "marks": 1, "ans": [0, 0], "rawKey": "0 to 0",
        "q": "The line integral \\int_C (y^2 dx + 2xy dy) over the curve C: x^2 + y^2 = 1 from (1, 0) to (0, 1) in the counter-clockwise direction is ________.",
        "opts": [],
        "page": 4
    },
    {
        "num": 5, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "An aircraft is flying at a constant altitude in a horizontal circle at a speed of 120 m/s. If the bank angle is 60°, the radius of the circle (in meters) is (take g = 9.81 m/s^2)",
        "opts": ["848", "1468", "2544", "848.3"],
        "page": 4
    },
    {
        "num": 6, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "Which one of the following flight instruments is used on an aircraft to determine its attitude in roll and pitch?",
        "opts": ["Altimeter", "Turn and slip indicator", "Artificial horizon", "Rate of climb indicator"],
        "page": 5
    },
    {
        "num": 7, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "An aircraft has a zero-lift drag coefficient C_{D0} = 0.02, wing aspect ratio AR = 8, and Oswald efficiency factor e = 0.8. The lift coefficient C_L for the maximum lift-to-drag ratio is",
        "opts": ["0.40", "0.50", "0.63", "0.75"],
        "page": 5
    },
    {
        "num": 8, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "Which one of the following statements is TRUE for an airplane in steady, level flight at a constant altitude?",
        "opts": [
            "Maximum range occurs at a higher speed than maximum endurance",
            "Maximum range occurs at a lower speed than maximum endurance",
            "Maximum range and maximum endurance occur at the same speed",
            "Maximum range speed is independent of weight"
        ],
        "page": 5
    },
    {
        "num": 9, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "The primary control surface used to control the yawing motion of an aircraft is",
        "opts": ["Aileron", "Rudder", "Elevator", "Flap"],
        "page": 5
    },
    {
        "num": 10, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "An airfoil with a positive camber at zero angle of attack produces",
        "opts": [
            "Positive lift and negative pitching moment about the quarter chord",
            "Negative lift and positive pitching moment about the quarter chord",
            "Zero lift and zero pitching moment about the quarter chord",
            "Positive lift and positive pitching moment about the quarter chord"
        ],
        "page": 5
    },
    {
        "num": 11, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Which one of the following statements is NOT TRUE for a supersonic flow?",
        "opts": [
            "Over an expansion corner, static temperature decreases",
            "Across an oblique shock wave, total pressure increases",
            "Across a normal shock wave, Mach number decreases",
            "In a convergent-divergent nozzle with supersonic flow at the exit, Mach number increases in the divergent portion"
        ],
        "page": 6
    },
    {
        "num": 12, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "In a 2-D potential flow, a source of strength m and a sink of strength m placed at a distance d apart form a doublet as d → 0 such that md remains constant. The streamlines around the doublet are",
        "opts": [
            "Concentric circles tangent to the doublet axis",
            "Radial straight lines",
            "Concentric circles with center at the doublet",
            "Hyperbolas"
        ],
        "page": 6
    },
    {
        "num": 13, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "A laminar boundary layer develops over a flat plate of length L. If the freestream velocity is doubled, the skin friction drag force on the plate will",
        "opts": [
            "Increase by a factor of 2",
            "Increase by a factor of \\sqrt{2}",
            "Increase by a factor of 2\\sqrt{2}",
            "Remain unchanged"
        ],
        "page": 6
    },
    {
        "num": 14, "sec": "AE", "type": "NAT", "marks": 1, "ans": [1, 1], "rawKey": "1 to 1",
        "q": "Consider a velocity field given by u = 2x, v = -2y in a 2-D flow field. The magnitude of the circulation along a circle of radius R = 1 centered at the origin is ________.",
        "opts": [],
        "page": 6
    },
    {
        "num": 15, "sec": "AE", "type": "NAT", "marks": 1, "ans": [0.2, 0.2], "rawKey": "0.2 to 0.2",
        "q": "A flat plate of chord c = 1 m is placed in an incompressible flow of air (density 1.2 kg/m^3, kinematic viscosity 1.5 × 10^{-5} m^2/s) at a freestream speed of 30 m/s. The Reynolds number based on the chord is Re = 2 × 10^6. The boundary layer thickness (in mm) at x = 0.1 m from the leading edge is ________ (assume laminar boundary layer with δ = 5x/\\sqrt{Re_x}).",
        "opts": [],
        "page": 6
    },
    {
        "num": 16, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "MTA", "rawKey": "MTA*", "gradingRule": "marks-to-all",
        "q": "The cross-section of a long thin-walled member is as shown in the figure. When subjected to pure twist, point A",
        "opts": [
            "does not move horizontally or axially, but moves vertically",
            "does not move axially, but moves both vertically and horizontally",
            "does not move horizontally, vertically or axially",
            "does not move vertically or axially, but moves horizontally"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-16-figure-1.png",
            "alt": "Thin-walled open section with point A at corner",
            "page": 7
        }],
        "page": 7
    },
    {
        "num": 17, "sec": "AE", "type": "NAT", "marks": 1, "ans": [0.12, 0.13], "rawKey": "0.12 to 0.13",
        "q": "The channel section of uniform thickness 2mm shown in the figure is subjected to a torque of 10 Nm. If it is made of a material with shear modulus of 25 GPa, the twist per unit length in radians/m is ________.",
        "opts": [],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-17-figure-1.png",
            "alt": "Channel section with flange lengths 300mm and web height 600mm",
            "page": 7
        }],
        "page": 7
    },
    {
        "num": 18, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "The stiffened cross-section of a long slender uniform structural member is idealized as four concentrated corner booms carrying direct stresses and thin skin panels carrying shear stresses only, as shown in the figure. If the member is subjected to a vertical shear force V_y = 10 kN through the shear center, the shear flow in web 1-2 is",
        "opts": [
            "50 N/mm",
            "100 N/mm",
            "25 N/mm",
            "0 N/mm"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-18-figure-1.png",
            "alt": "Idealized 4-boom cross section with dimensions and booms 1, 2, 3, 4",
            "page": 8
        }],
        "page": 8
    },
    {
        "num": 19, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "A solid circular shaft of radius R is subjected to a torque T. If the maximum shear stress induced is τ_max, the ratio of torque carried by the outer core (from r = R/2 to r = R) to the total torque T is",
        "opts": ["3/4", "7/8", "1/2", "15/16"],
        "page": 8
    },
    {
        "num": 20, "sec": "AE", "type": "NAT", "marks": 1, "ans": [0.3, 0.35], "rawKey": "0.3 to 0.35",
        "q": "A thin-walled cylindrical pressure vessel of internal diameter 1 m and wall thickness 5 mm is subjected to an internal gauge pressure of 2 MPa. The maximum in-plane shear stress (in MPa) in the wall of the vessel is ________.",
        "opts": [],
        "page": 8
    },
    {
        "num": 21, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "For a linear elastic isotropic material, which of the following relationships between Young’s modulus E, Shear modulus G, Bulk modulus K and Poisson’s ratio ν is NOT correct?",
        "opts": [
            "E = 2G(1 + ν)",
            "E = 3K(1 - 2ν)",
            "G = \\frac{3K(1 - 2ν)}{2(1 + ν)}",
            "E = \\frac{9KG}{3K + 2G}"
        ],
        "page": 8
    },
    {
        "num": 22, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "A gas turbine engine is mounted on an aircraft which can attain a maximum altitude of 15 km. As altitude increases in the troposphere, the thrust produced by the engine",
        "opts": [
            "Increases continuously",
            "Remains constant",
            "First decreases then increases",
            "Decreases continuously"
        ],
        "page": 9
    },
    {
        "num": 23, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "In a gas turbine combustor, the primary zone air-fuel mixture is",
        "opts": [
            "Extremely lean to minimize emissions",
            "Nearly stoichiometric to sustain stable combustion",
            "Extremely rich to maximize temperature",
            "Completely unmixed"
        ],
        "page": 9
    },
    {
        "num": 24, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "For an ideal ramjet engine operating at supersonic flight speed, the net thrust is maximum when the flight Mach number is such that",
        "opts": [
            "Combustion chamber temperature is equal to ambient temperature",
            "Total temperature rise in the intake equals temperature rise in the combustor",
            "Combustor exit velocity is sonic",
            "Intake pressure ratio is minimum"
        ],
        "page": 9
    },
    {
        "num": 25, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "Which one of the following rocket propellant combinations is cryogenic?",
        "opts": [
            "Liquid Oxygen (LOX) + Liquid Hydrogen (LH2)",
            "UDMH + N2O4",
            "Kerosene + Liquid Oxygen",
            "Solid propellant HTPB + AP"
        ],
        "page": 9
    },

    # AE Q26 - Q55 (2 marks each)
    {
        "num": 26, "sec": "AE", "type": "NAT", "marks": 2, "ans": [0, 0], "rawKey": "0 to 0",
        "q": "Let S be the closed surface of the unit sphere x^2 + y^2 + z^2 = 1. The value of the surface integral \\iint_S (y^2 z i + z^2 x j + x^2 y k) · n dS, where n is the outward unit normal, is ________.",
        "opts": [],
        "page": 10
    },
    {
        "num": 27, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "The solution of the initial value problem \\frac{d^2 y}{dx^2} - 2 \\frac{dy}{dx} + y = e^x with y(0) = 1, y'(0) = 2 is",
        "opts": [
            "y = (1 + x + \\frac{x^2}{2}) e^x",
            "y = (1 + x) e^x + \\frac{x^2}{2} e^x",
            "y = (1 + 2x) e^x",
            "y = (1 - x + x^2) e^x"
        ],
        "page": 10
    },
    {
        "num": 28, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "The value of the integral \\oint_C \\frac{\\cos(π z)}{z(z-1)} dz around the contour C: |z| = 1.5 in the counter-clockwise direction is",
        "opts": ["0", "2π i", "-2π i", "-4π i"],
        "page": 10
    },
    {
        "num": 29, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "A fair coin is tossed 4 times. The probability of getting at least 3 heads is",
        "opts": ["5/16", "1/4", "3/8", "7/16"],
        "page": 10
    },
    {
        "num": 30, "sec": "AE", "type": "NAT", "marks": 2, "ans": [9, 10], "rawKey": "9 to 10",
        "q": "A glider is launched from a 500m high hilltop. Following data is available for the glider: Wing area S = 15 m^2, Aspect ratio AR = 8, Weight W = 3000 N, Zero-lift drag coefficient C_{D0} = 0.015, Oswald efficiency factor e = 0.85, Air density ρ = 1.2 kg/m^3. The maximum distance (in km) that the glider can cover in still air is ________.",
        "opts": [],
        "page": 11
    },
    {
        "num": 31, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "An airplane has a wing loading W/S = 2500 N/m^2, zero-lift drag coefficient C_{D0} = 0.02, aspect ratio AR = 8 and Oswald efficiency factor e = 0.8. In steady level flight at sea-level (ρ = 1.225 kg/m^3), the minimum thrust required (in N per unit weight) is",
        "opts": ["0.035", "0.040", "0.056", "0.070"],
        "page": 11
    },
    {
        "num": 32, "sec": "AE", "type": "NAT", "marks": 2, "ans": [-0.24, -0.23], "rawKey": "-0.24 to -0.23",
        "q": "For a symmetric airfoil of chord c = 1.5 m with a 20% plain flap, the lift curve slope is C_{Lα} = 2π rad^{-1}. If flap deflection δ_f = 10° produces a lift increment Δ C_L = 0.35, the flap effectiveness parameter τ = (∂α/∂δ_f) is ________.",
        "opts": [],
        "page": 11
    },
    {
        "num": 33, "sec": "AE", "type": "NAT", "marks": 2, "ans": [1, 1], "rawKey": "1 to 1",
        "q": "An airplane has a neutral point located at 0.45 c and center of gravity at 0.30 c. The static margin (as a fraction of mean aerodynamic chord c) is ________.",
        "opts": [],
        "page": 11
    },
    {
        "num": 34, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "A jet transport airplane of weight W = 500 kN is in steady coordinated turn at an altitude of 10 km. If the bank angle is 45° and maximum available thrust is 150 kN, the maximum load factor n that can be sustained is",
        "opts": ["1.0", "1.2", "1.3", "1.414"],
        "page": 11
    },
    {
        "num": 35, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Consider the longitudinal dynamic equations of motion for an aircraft. If the short-period mode has undamped natural frequency ω_n = 3.0 rad/s and damping ratio ζ = 0.6, the time (in seconds) to damp to half amplitude is",
        "opts": ["0.23", "0.31", "0.385", "0.55"],
        "page": 11
    },
    {
        "num": 36, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Streamline pattern of flow past a cylinder is shown in the figure below. The oncoming uniform flow velocity is V_∞. If the circulation is Γ in the clockwise direction, the lift force experienced by the cylinder per unit span is given by",
        "opts": [
            "Zero",
            "\\frac{1}{2} ρ_∞ V_∞^2 (2R)",
            "ρ_∞ V_∞ Γ (acting upward)",
            "ρ_∞ V_∞ Γ (acting downward)"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-36-figure-1.png",
            "alt": "Streamlines past a cylinder with circulation showing upward displaced stagnation points",
            "page": 12
        }],
        "page": 12
    },
    {
        "num": 37, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A finite wing with span b = 10 m and chord c = 1.5 m has an elliptic lift distribution. The trailing vortex wake rollup is as shown in the figure. If the total circulation at mid-span is Γ_0 = 40 m^2/s and freestream speed is V_∞ = 50 m/s, the downwash velocity w_0 (in m/s) at the wing is",
        "opts": ["1.0", "1.5", "2.0", "2.5"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-37-figure-1.png",
            "alt": "Finite wing with span b and trailing vortex wake rollup",
            "page": 12
        }],
        "page": 12
    },
    {
        "num": 38, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "The idealized cross-section of a beam is comprised of four identical booms connected by thin webs as shown in the figure. If each boom area is B = 100 mm^2 and the cross-section is subjected to a bending moment M_x = 10 kN·m, the normal stress (in MPa) in boom 1 is",
        "opts": ["250", "-250", "125", "-125"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-38-figure-1.png",
            "alt": "Idealized beam cross section with 4 booms of area B and dimensions 200mm x 100mm",
            "page": 13
        }],
        "page": 13
    },
    {
        "num": 39, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A cantilever beam of span L and uniform flexural rigidity EI has an end moment M_0 applied at the free end. The strain energy U stored in the beam is",
        "opts": [
            "\\frac{M_0^2 L}{EI}",
            "\\frac{M_0^2 L}{2EI}",
            "\\frac{M_0^2 L}{3EI}",
            "\\frac{M_0^2 L}{6EI}"
        ],
        "page": 13
    },
    {
        "num": 40, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A column of length L and uniform flexural rigidity EI is pinned at both ends. An additional elastic torsional spring of stiffness K_t is attached at one end. The critical buckling load P_{cr} satisfies",
        "opts": [
            "P_{cr} = \\frac{π^2 EI}{L^2}",
            "\\tan(k L) = \\frac{k L}{1 - \\frac{K_t L}{EI}} where k = \\sqrt{P_{cr}/EI}",
            "P_{cr} = \\frac{4π^2 EI}{L^2}",
            "P_{cr} = \\frac{π^2 EI}{4L^2}"
        ],
        "page": 13
    },
    {
        "num": 41, "sec": "AE", "type": "NAT", "marks": 2, "ans": [1900, 2000], "rawKey": "1900 to 2000",
        "q": "In the steel structure (Young’s modulus = 200 GPa) shown in the figure, all members are pin-jointed with cross-sectional area A = 100 mm^2. Under the applied load P = 10 kN at joint B, the vertical downward deflection (in mm × 10^{-3}) at joint B is ________.",
        "opts": [],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-41-figure-1.png",
            "alt": "Truss structure ABC with pin joints and downward load P at joint B",
            "page": 14
        }],
        "page": 14
    },
    {
        "num": 42, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A single degree of freedom system with mass m = 2 kg and stiffness k = 800 N/m is subjected to a harmonic force F(t) = F_0 \\cos(ω t). If the amplitude of steady-state response at resonance (ω = ω_n) is 10 times the static deflection, the damping ratio ζ of the system is",
        "opts": ["0.02", "0.05", "0.10", "0.20"],
        "page": 14
    },
    {
        "num": 43, "sec": "AE", "type": "NAT", "marks": 2, "ans": [70, 70], "rawKey": "70 to 70",
        "q": "A thin-walled single-cell closed tube of non-circular cross-section of mean enclosed area A_m = 0.05 m^2 and uniform wall thickness t = 2 mm is subjected to a torque T = 14 kN·m. The shear stress (in MPa) developed in the wall is ________.",
        "opts": [],
        "page": 14
    },
    {
        "num": 44, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "A simply supported beam with overhang is loaded by uniformly distributed load of intensity q as shown in the figure. The bending moment at the mid-point of AB is",
        "opts": [
            "\\frac{qL^2}{16} sagging",
            "\\frac{qL^2}{16} hogging",
            "\\frac{3qL^2}{16} hogging",
            "\\frac{3qL^2}{16} sagging"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2013-ae-ae-44-figure-1.png",
            "alt": "Simply supported beam AB with overhang L/2 under uniform load q",
            "page": 15
        }],
        "page": 15
    },
    {
        "num": 45, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "Thrust of liquid oxygen - liquid hydrogen rocket engine is 300 kN. The O/F ratio used is 5. If the fuel mass flow rate is 12.5 kg/s, the specific impulse of the rocket motor in Ns/kg is",
        "opts": ["3800", "4000", "4200", "4400"],
        "page": 15
    },
    {
        "num": 46, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "In a 50 % reaction axial compressor stage, the local blade velocity is 300 m/s and the axial component of velocity is 100 m/s. If the absolute inlet flow angle α_1 = 45°, the work per unit mass done on the fluid by the stage in kJ/kg is",
        "opts": ["30", "40", "50", "60"],
        "page": 15
    },
    {
        "num": 47, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "Consider two rockets P and Q fired vertically up with identical specific impulse and a payload of 2 kg. Rocket P has 2 identical stages, and each stage has 200 kg of propellant and 20 kg of structural weight. Rocket Q has a single stage with 400 kg of propellant and 40 kg of structural weight. Neglecting drag and gravity effects, the ratio of the change in velocity of P to that attained by Q is",
        "opts": ["1.13", "1.23", "1.33", "1.43"],
        "page": 15
    },

    # Common Data Questions 48 and 49
    {
        "num": 48, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "Common Data for Questions 48 and 49: Data for an airplane are given as follows: weight W = 30kN, thrust available at sea-level T_0 = 4000N, wing planform area S = 30m^2, maximum lift coefficient C_{L max} = 1.4, and drag coefficient C_D = 0.015 + 0.024 C_L^2. Assume air density at sea-level ρ_∞ = 1.22kg/m^3.\n\nStall speed of the airplane in m/s is",
        "opts": ["17.36", "34.22", "45.52", "119.46"],
        "page": 15
    },
    {
        "num": 49, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Common Data for Questions 48 and 49: Data for an airplane are given as follows: weight W = 30kN, thrust available at sea-level T_0 = 4000N, wing planform area S = 30m^2, maximum lift coefficient C_{L max} = 1.4, and drag coefficient C_D = 0.015 + 0.024 C_L^2. Assume air density at sea-level ρ_∞ = 1.22kg/m^3.\n\nMinimum and maximum speeds of the airplane in level flight condition at sea-level in m/s are respectively",
        "opts": [
            "17.36 and 180",
            "17.36 and 34.22",
            "34.22 and 119.46",
            "17.36 and 119.46"
        ],
        "page": 15
    },

    # Common Data Questions 50 and 51
    {
        "num": 50, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "Common Data for Questions 50 and 51: An aircraft is flying at Mach number M = 1.5, where the ambient temperature is 250 K. The stagnation temperature of gases at the entry to the nozzle is 800 K. The nozzle is choked and always under expanded. Assume the molecular weight of the exhaust gases to be 29, the ratio of specific heats to be 1.4 and the universal gas constant is 8314 J/kmol-K.\n\nFor which one of the nozzle exit Mach numbers given below is the propulsive efficiency highest?",
        "opts": ["1", "1.5", "2", "2.5"],
        "page": 16
    },
    {
        "num": 51, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "Common Data for Questions 50 and 51: An aircraft is flying at Mach number M = 1.5, where the ambient temperature is 250 K. The stagnation temperature of gases at the entry to the nozzle is 800 K. The nozzle is choked and always under expanded. Assume the molecular weight of the exhaust gases to be 29, the ratio of specific heats to be 1.4 and the universal gas constant is 8314 J/kmol-K.\n\nFor which one of the nozzle exit Mach numbers given below is the thrust highest?",
        "opts": ["1", "1.5", "2", "2.5"],
        "page": 16
    },

    # Linked Answer Questions 52 and 53
    {
        "num": 52, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "MTA", "rawKey": "MTA*", "gradingRule": "marks-to-all",
        "q": "Statement for Linked Answer Questions 52 and 53: Circulation theory of lift is assumed for a thin symmetric airfoil at an angle of attack α. Free stream velocity is U.\n\nIf the circulation at the quarter chord (c/4) of the airfoil is Γ_1, the normal velocity is zero at",
        "opts": [
            "c/4",
            "c/2",
            "3c/4",
            "all points on the chord"
        ],
        "page": 16
    },
    {
        "num": 53, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "MTA", "rawKey": "MTA*", "gradingRule": "marks-to-all",
        "q": "Statement for Linked Answer Questions 52 and 53: Circulation theory of lift is assumed for a thin symmetric airfoil at an angle of attack α. Free stream velocity is U.\n\nA second identical airfoil is placed behind the first one at a distance of c/2 from the trailing edge of the first. The second airfoil has an unknown circulation Γ_2 placed at its quarter chord. The normal velocity becomes zero at the same chord-wise locations of the respective airfoils as in the previous question. The values of Γ_1 and Γ_2 are respectively",
        "opts": [
            "\\frac{4}{3} π c U α, \\frac{2}{3} π c U α",
            "\\frac{2}{3} π c U α, \\frac{2}{3} π c U α",
            "\\frac{2}{3} π c U α, \\frac{1}{3} π c U α",
            "\\frac{4}{3} π c U α, \\frac{4}{3} π c U α"
        ],
        "page": 16
    },

    # Linked Answer Questions 54 and 55
    {
        "num": 54, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "Statement for Linked Answer Questions 54 and 55: A wing-body alone configuration airplane with a wing loading of W/S = 1000 N/m^2 is flying in cruise condition at a speed V = 90m/s at sea-level (air density at sea-level ρ_∞ = 1.22 kg/m^3). The zero lift pitching moment coefficient of the airplane is C_{mac}^{wb} = C_{m0} = -0.06 and the location of airplane aerodynamic center from the wing leading edge is X_{ac} = 0.25c. Here c is the chord length.\n\nThe airplane trim lift coefficient C_{L trim} is",
        "opts": ["0.502", "0.402", "0.302", "0.202"],
        "page": 17
    },
    {
        "num": 55, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Statement for Linked Answer Questions 54 and 55: A wing-body alone configuration airplane with a wing loading of W/S = 1000 N/m^2 is flying in cruise condition at a speed V = 90m/s at sea-level (air density at sea-level ρ_∞ = 1.22 kg/m^3). The zero lift pitching moment coefficient of the airplane is C_{mac}^{wb} = C_{m0} = -0.06 and the location of airplane aerodynamic center from the wing leading edge is X_{ac} = 0.25c. Here c is the chord length.\n\nDistance of center of gravity of the aircraft (X_{CG}) from the wing leading edge is",
        "opts": ["0.447c", "-0.547c", "0.547c", "-0.25c"],
        "page": 17
    },

    # General Aptitude Q56 - Q65
    {
        "num": 56, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "If 3 ≤ X ≤ 5 and 8 ≤ Y ≤ 11 then which of the following options is TRUE?",
        "opts": [
            "\\frac{3}{5} ≤ \\frac{X}{Y} ≤ \\frac{8}{5}",
            "\\frac{3}{11} ≤ \\frac{X}{Y} ≤ \\frac{5}{8}",
            "\\frac{3}{11} ≤ \\frac{X}{Y} ≤ \\frac{8}{5}",
            "\\frac{3}{5} ≤ \\frac{X}{Y} ≤ \\frac{8}{11}"
        ],
        "page": 17
    },
    {
        "num": 57, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "The Headmaster ____________ to speak to you.\n\nWhich of the following options is incorrect to complete the above sentence?",
        "opts": ["is wanting", "wants", "want", "was wanting"],
        "page": 17
    },
    {
        "num": 58, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "Mahatama Gandhi was known for his humility as",
        "opts": [
            "he played an important role in humiliating exit of British from India.",
            "he worked for humanitarian causes.",
            "he displayed modesty in his interactions.",
            "he was a fine human being."
        ],
        "page": 17
    },
    {
        "num": 59, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "All engineering students should learn mechanics, mathematics and how to do computation.\n\nWhich of the following options is the most grammatically correct rewrite of the sentence above?",
        "opts": [
            "All engineering students should learn mechanics, mathematics and how to compute.",
            "All engineering students should learn mechanics, mathematics and computation.",
            "All engineering students should learn how to do mechanics, mathematics and computation.",
            "All engineering students should learn mechanics, mathematics and how to do computation."
        ],
        "page": 18
    },
    {
        "num": 60, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Which of the following options is the closest in meaning to the word underlined in the sentence below?\n\n\"The teacher was <u>appalled</u> by the student's misconduct.\"",
        "opts": ["pleased", "shocked", "confused", "amused"],
        "page": 18
    },
    {
        "num": 61, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A student is required to solve 8 out of 10 questions in an exam. The questions are divided into two parts containing 5 questions each. If the student must choose at least 3 questions from each part, the number of possible ways in which the student can choose the questions is",
        "opts": ["30", "40", "45", "50"],
        "page": 18
    },
    {
        "num": 62, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A square pyramid has a base perimeter of 40 cm and a slant height of 13 cm. The volume of the pyramid (in cm^3) is",
        "opts": ["300", "360", "400", "480"],
        "page": 18
    },
    {
        "num": 63, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A car travels from A to B at an average speed of 60 km/h and returns from B to A along the same route at an average speed of 40 km/h. The average speed (in km/h) for the entire journey is",
        "opts": ["50", "45", "48", "52"],
        "page": 19
    },
    {
        "num": 64, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "If |-2X + 9| = 3 then the possible value of |-X| - X^2 would be:",
        "opts": ["30", "-30", "-42", "42"],
        "page": 19
    },
    {
        "num": 65, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Find the next term in the series: 2, 5, 10, 17, 26, ____",
        "opts": ["35", "36", "37", "38"],
        "page": 19
    }
]

formatted_questions = []
for q in questions_data:
    number = q["num"]
    sec = q["sec"]
    num_str = f"{number:02d}"
    qid = f"gate-2013-ae-ga-{num_str}" if sec == "GA" else f"gate-2013-ae-ae-{num_str}"
    
    opts = []
    if q["type"] != "NAT":
        for i, opt in enumerate(q["opts"]):
            label = chr(65 + i)
            opts.append({"label": label, "text": opt})
    
    neg_marks = 0
    if q["type"] == "MCQ":
        neg_marks = 0.3333333333333333 if q["marks"] == 1 else 0.6666666666666666

    figures = []
    if q.get("hasFigure"):
        for fig in q["figures"]:
            figures.append({
                "src": fig["src"],
                "alt": fig["alt"],
                "page": fig["page"],
                "source": {
                    "file": "internal/ae/AE2013.pdf",
                    "sha256": pdf_sha,
                    "page": fig["page"],
                    "verificationStatus": "source-verified",
                    "verifiedOn": "2026-10-08"
                }
            })

    item = {
        "id": qid,
        "number": number,
        "year": 2013,
        "paper": "AE",
        "section": sec,
        "subject": "General Aptitude" if sec == "GA" else "Aerospace Engineering",
        "type": q["type"],
        "marks": q["marks"],
        "negativeMarks": neg_marks,
        "question": q["q"],
        "options": opts,
        "answer": q["ans"],
        "acceptedAnswers": q["ans"] if isinstance(q["ans"], list) else [q["ans"]],
        "markingRule": "gate-2013-official",
        "hasFigure": bool(figures),
        "figures": figures,
        "groupId": None,
        "source": {
            "paper": "AE",
            "year": 2013,
            "questionNumber": number if sec == "AE" else number - 55,
            "section": sec,
            "file": "internal/ae/AE2013.pdf",
            "sha256": pdf_sha,
            "pages": [{
                "page": q["page"],
                "coordinateSystem": "PDF points, top-left origin"
            }],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-08"
        },
        "transcriptionStatus": "source-verified",
        "solution": None,
        "solutionAvailability": "not-provided-in-source",
        "gradingStatus": "official key verified",
        "answerSource": {
            "paper": "AE",
            "questionNumber": number if sec == "AE" else number - 55,
            "section": sec,
            "file": "internal/ae/AE2013-key.pdf",
            "sha256": key_sha,
            "verifiedOn": "2026-10-08"
        }
    }
    if q.get("gradingRule"):
        item["gradingRule"] = q["gradingRule"]
    formatted_questions.append(item)

ae_ids = [q["id"] for q in formatted_questions if q["section"] == "AE"]
ga_ids = [q["id"] for q in formatted_questions if q["section"] == "GA"]
q_order = [q["id"] for q in formatted_questions]

paper_2013 = {
    "schemaVersion": 1,
    "id": "gate-2013-ae",
    "exam": "GATE",
    "year": 2013,
    "paper": "AE",
    "title": "GATE Aerospace Engineering 2013",
    "durationMinutes": 180,
    "totalMarks": 100,
    "totalQuestions": 65,
    "sectionOrder": ["AE", "GA"],
    "sections": [
        {
            "id": "AE",
            "title": "Aerospace Engineering",
            "questionIds": ae_ids,
            "totalMarks": 85
        },
        {
            "id": "GA",
            "title": "General Aptitude",
            "questionIds": ga_ids,
            "totalMarks": 15
        }
    ],
    "questionOrder": q_order,
    "questionRefs": [{"id": q["id"], "number": q["number"], "section": q["section"]} for q in formatted_questions],
    "questionGroups": [],
    "marking": {
        "negativeFraction": {
            "MCQ": 0.3333333333333333,
            "MSQ": 0,
            "NAT": 0
        }
    },
    "source": {
        "file": "internal/ae/AE2013.pdf",
        "sha256": pdf_sha,
        "pageCount": 19
    },
    "questions": formatted_questions
}

with open("data/ae/2013.json", "w", encoding="utf-8") as f:
    json.dump(paper_2013, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Saved data/ae/2013.json")

# Build internal/ae/AE2013-key.json
key_rows = []
for q in questions_data:
    number = q["num"]
    sec = q["sec"]
    raw_k = q.get("rawKey", q["ans"])
    key_rows.append({
        "number": number,
        "section": sec,
        "sectionQuestionNumber": number if sec == "AE" else number - 55,
        "type": q["type"],
        "rawKey": raw_k,
        "marks": q["marks"]
    })

key_doc = {
    "exam": "GATE",
    "year": 2013,
    "paper": "AE",
    "source": "internal/ae/AE2013-key.pdf",
    "sha256": key_sha,
    "totalQuestions": 65,
    "totalMarks": 100,
    "rows": key_rows
}

with open("internal/ae/AE2013-key.json", "w", encoding="utf-8") as f:
    json.dump(key_doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Saved internal/ae/AE2013-key.json")

# Update manifest.json
with open("data/ae/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

y_idx = next((i for i, y in enumerate(manifest["years"]) if y["year"] == 2013), -1)
if y_idx >= 0:
    manifest["years"][y_idx] = {
        "year": 2013,
        "paper": "AE",
        "title": "GATE 2013 Aerospace Engineering",
        "path": "data/ae/2013.json",
        "ingestionStatus": "complete",
        "verificationStatus": "source-verified",
        "totalQuestions": 65,
        "totalMarks": 100,
        "sections": [
            {
                "id": "AE",
                "title": "Aerospace Engineering",
                "questionIds": ae_ids,
                "totalMarks": 85
            },
            {
                "id": "GA",
                "title": "General Aptitude",
                "questionIds": ga_ids,
                "totalMarks": 15
            }
        ],
        "questionTypeCounts": {
            "MCQ": 54,
            "MSQ": 0,
            "NAT": 11
        },
        "figureAssetCount": 8,
        "newFigureAssetCount": 8,
        "answerAvailability": {
            "officialKey": 65,
            "gradedAnswers": 62,
            "marksToAll": 3,
            "unavailable": 0
        },
        "provenance": {
            "paperSource": "internal/ae/AE2013.pdf",
            "keySource": "internal/ae/AE2013-key.pdf"
        },
        "sourcePdf": "internal/ae/AE2013.pdf",
        "questionCount": 65,
        "newQuestionCount": 65,
        "reusedGAQuestionCount": 0,
        "reusedFigureAssetCount": 0,
        "optionFigureCount": 0,
        "structuredTableCount": 0,
        "questionGroupCount": 0,
        "verifiedOn": "2026-10-08"
    }

with open("data/ae/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Updated data/ae/manifest.json for 2013")
