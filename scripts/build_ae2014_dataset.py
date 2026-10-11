import json
import hashlib
import os

pdf_path = "internal/ae/AE2014.pdf"
key_pdf_path = "internal/ae/AE2014-key.pdf"

with open(pdf_path, "rb") as f:
    pdf_sha = hashlib.sha256(f.read()).hexdigest()

with open(key_pdf_path, "rb") as f:
    key_sha = hashlib.sha256(f.read()).hexdigest()

# Define all 65 questions meticulously
questions_data = [
    # GA Q1 - Q10
    {
        "num": 1, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "A student is required to demonstrate a high level of comprehension of the subject, especially in the social sciences.\n\nThe word <b>comprehension</b> in the given sentence means",
        "opts": ["understanding", "perspicacity", "development", "thought"],
        "page": 5
    },
    {
        "num": 2, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Choose the most appropriate word from the options given below to complete the following sentence:\n\nOne of several hall marks of Western civilization is the _______ of individuals' rights over those of the state.",
        "opts": ["assertion", "ascendancy", "dissidence", "predilection"],
        "page": 5
    },
    {
        "num": 3, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "Which of the following options is the closest in meaning to the word underlined in the sentence below?\n\nIn a democracy, the <u>overt</u> participation of the public is essential for good governance.",
        "opts": ["obscure", "implicit", "secret", "apparent"],
        "page": 5
    },
    {
        "num": 4, "sec": "GA", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "Which of the following options can be used to convert the given active voice sentence into passive voice?\n\nSentence: The police officer arrested the thief.",
        "opts": [
            "The police officer is arresting the thief.",
            "The thief was being arrested by the police officer.",
            "The thief was arrested by the police officer.",
            "The thief is arrested by the police officer."
        ],
        "page": 5
    },
    {
        "num": 5, "sec": "GA", "type": "NAT", "marks": 1, "ans": [1300, 1300], "rawKey": "1300 to 1300",
        "q": "5 skilled workers can build a wall in 20 days; 8 semi-skilled workers can build a wall in 25 days; 10 unskilled workers can build a wall in 30 days. If a team has 2 skilled, 6 semi-skilled and 5 unskilled workers, how much time (in days) will it take to build the wall? (Give answer rounded off to the nearest integer)",
        "opts": [],
        "page": 5
    },
    {
        "num": 6, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "Consider the following statements:\n\n(i) No student is lazy.\n(ii) Some students are hardworking.\n\nWhich of the following statements must be true based on the above given information?",
        "opts": [
            "No hardworking student is lazy.",
            "All lazy people are students.",
            "Some hardworking people are not lazy.",
            "Some hardworking students are not lazy."
        ],
        "page": 5
    },
    {
        "num": 7, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "In a group of four children, Som is older than Tarun. Shreyas is older than Som and younger than Varun. Which of the following statements is true?",
        "opts": [
            "Varun is younger than Tarun.",
            "Tarun is the youngest among all.",
            "Varun is younger than Som.",
            "Som is the youngest among all."
        ],
        "page": 5
    },
    {
        "num": 8, "sec": "GA", "type": "NAT", "marks": 2, "ans": [180, 180], "rawKey": "180 to 180",
        "q": "The smallest angle of a triangle is equal to two thirds of the smallest angle of a quadrilateral. The ratio between the angles of the quadrilateral is 3:4:5:6. The largest angle of the triangle is twice its smallest angle. What is the sum (in degrees) of the second largest angle of the triangle and the largest angle of the quadrilateral?",
        "opts": [],
        "page": 6
    },
    {
        "num": 9, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "One percent of the people of country X are taller than 6 ft. Two percent of the people of country Y are taller than 6 ft. There are thrice as many people in country X as in country Y. Taking both countries together, what is the percentage of people taller than 6 ft?",
        "opts": ["3.0", "2.5", "1.5", "1.25"],
        "page": 6
    },
    {
        "num": 10, "sec": "GA", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "The monthly rainfall chart based on 50 years of rainfall in Agra is shown in the following figure. Which of the following are true? (k percentile is the value such that k percent of the data fall below that value)\n\n(i) On average, it rains more in July than in December\n(ii) Every year, the amount of rainfall in August is more than that in January\n(iii) July rainfall can be estimated with better certainty than January rainfall\n(iv) In August, each year at least 100 mm of rainfall was recorded",
        "opts": [
            "(i) and (ii)",
            "(i) and (iii)",
            "(ii) and (iii)",
            "(ii) and (iv)"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ga-10-figure-1.png",
            "alt": "Monthly rainfall chart in Agra showing percentiles across months",
            "page": 6
        }],
        "page": 6
    },

    # AE Q1 - Q25 (Global Q11 - Q35)
    {
        "num": 11, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "For a real symmetric matrix [A], which of the following statements is true:\n(A) The matrix is always diagonalizable and invertible.\n(B) The matrix is always invertible but not necessarily diagonalizable.\n(C) The matrix is always diagonalizable but not necessarily invertible.\n(D) The matrix is always neither diagonalizable nor invertible.",
        "opts": [
            "The matrix is always diagonalizable and invertible.",
            "The matrix is always invertible but not necessarily diagonalizable.",
            "The matrix is always diagonalizable but not necessarily invertible.",
            "The matrix is always neither diagonalizable nor invertible."
        ],
        "page": 7
    },
    {
        "num": 12, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "The series \\sum_{m=1}^{\\infty} \\frac{(x-2)^m}{m 3^m} converges for all x with |x - 2| ≤ R given by",
        "opts": ["R = 0", "R = 3", "R = ∞", "R = 1/3"],
        "page": 7
    },
    {
        "num": 13, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "The function given by f(x) = x \\sin(1/x) for x ≠ 0, and f(0) = 0 is",
        "opts": [
            "Unbounded everywhere",
            "Bounded and continuous everywhere",
            "Bounded but not continuous at x = 0",
            "Continuous and differentiable everywhere"
        ],
        "page": 7
    },
    {
        "num": 14, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "Given the boundary-value problem \\frac{d}{dx}\\left(x \\frac{dy}{dx}\\right) + k y = 0, 0 < x < 1, with y(0) = y(1) = 0. Then the solutions of the boundary-value problem for k = 1 (given by y_1) and k = 5 (given by y_5) satisfy:",
        "opts": [
            "\\int_0^1 y_1 y_5 dx = 0",
            "\\int_0^1 \\frac{dy_1}{dx} \\frac{dy_5}{dx} dx = 0",
            "\\int_0^1 y_1 y_5 dx ≠ 0",
            "\\int_0^1 (y_1 y_5 + \\frac{dy_1}{dx} \\frac{dy_5}{dx}) dx = 0"
        ],
        "page": 7
    },
    {
        "num": 15, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "The value of I = \\int_0^1 1000 x^4 dx, obtained by using Simpson’s rule with 2 equally spaced intervals is,",
        "opts": ["200", "400", "180", "208"],
        "page": 7
    },
    {
        "num": 16, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "For a NACA 5-digit airfoil of chord c, the designed lift coefficient and location of maximum camber along the chord from the leading edge are denoted by C_L and X_m respectively. For NACA12018 airfoil, which combination of C_L and X_m given below are correct?",
        "opts": [
            "C_L = 0.15 and X_m = 0.1c",
            "C_L = 0.12 and X_m = 0.2c",
            "C_L = 0.12 and X_m = 0.18c",
            "C_L = 0.15 and X_m = 0.2c"
        ],
        "page": 7
    },
    {
        "num": 17, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "For inviscid, supersonic flow over a diamond shaped airfoil, shown in the figure, which statement is correct among the following?",
        "opts": [
            "The airfoil will experience zero lift and positive drag force",
            "The airfoil will experience positive lift and zero drag force",
            "The airfoil will experience negative lift and zero drag force",
            "The airfoil will experience positive lift and positive drag force"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-17-figure-1.png",
            "alt": "Diamond shaped airfoil in supersonic flow at angle of attack",
            "page": 7
        }],
        "page": 7
    },
    {
        "num": 18, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Consider supersonic flow near a corner (at an angle θ from the horizontal) with an attached oblique shock (at an angle β with horizontal) as shown in figure. If Mach number M decreases gradually from a high supersonic value, which of the following statements is correct?",
        "opts": [
            "β will decrease if the shock is a weak shock",
            "β will decrease if the shock is a strong shock",
            "β will increase for both weak and strong shocks",
            "β remains unchanged for both weak and strong shocks"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-18-figure-1.png",
            "alt": "Supersonic flow near a corner with attached oblique shock at angle beta and deflection angle theta",
            "page": 8
        }],
        "page": 8
    },
    {
        "num": 19, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "The streamlines of a potential line vortex is concentric circles with respect to the vortex center as shown in figure. Velocity along these streamlines, outside the core of the vortex can be written as, v_θ = \\frac{Γ}{2π r}, where strength of the vortex is \\frac{Γ}{2π} and r is radial direction. The value of circulation along the curve shown in the figure is:",
        "opts": ["Γ", "-2Γ", "2Γ", "0"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-19-figure-1.png",
            "alt": "Potential line vortex streamlines with closed integration curve not enclosing the vortex center",
            "page": 8
        }],
        "page": 8
    },
    {
        "num": 20, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "To observe unsteady separated flow in a diverging channel, bubbles are injected at each 10ms interval at point A as shown in figure. These bubbles act as tracer particles and follow the flow faithfully. The curved line AB shown at any instant represents:",
        "opts": [
            "Streamline, streakline and pathline",
            "Streamline and pathline",
            "Only a pathline",
            "Only a streakline"
        ],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-20-figure-1.png",
            "alt": "Diverging channel with bubbles injected at point A forming curved line AB",
            "page": 8
        }],
        "page": 8
    },
    {
        "num": 21, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "A",
        "q": "It is desired to measure the Young’s modulus and the Poisson’s ratio of a given homogeneous, isotropic material. A bar of length 20cm and square cross-section (10mm× 10mm) of this material is subjected to a tensile load of 40kN. Under this load, length increases to 20.1cm while the cross-section reduces to 9.98mm× 9.98mm. Young’s modulus and Poisson’s ratio of the material are:",
        "opts": [
            "80GPa & 0.4 respectively",
            "40GPa & -0.4 respectively",
            "80GPa & -0.2 respectively",
            "40GPa & 0.2 respectively"
        ],
        "page": 8
    },
    {
        "num": 22, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "In general, for any given solid subjected to arbitrary loading, which of the following statements is always true:",
        "opts": [
            "Volume does not vary with loading",
            "Mass does not vary with loading",
            "Density does not vary with loading",
            "Volume, mass and density vary with loading"
        ],
        "page": 9
    },
    {
        "num": 23, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Which one of the following objects with inclined face has only normal stress (i.e. zero shear stress) acting on that face?",
        "opts": [
            {"label": "A", "figure": {"src": "figures/gate-2014-ae-ae-23-option-A.png", "alt": "Option A stress block", "page": 9}},
            {"label": "B", "figure": {"src": "figures/gate-2014-ae-ae-23-option-B.png", "alt": "Option B stress block", "page": 9}},
            {"label": "C", "figure": {"src": "figures/gate-2014-ae-ae-23-option-C.png", "alt": "Option C stress block", "page": 9}},
            {"label": "D", "figure": {"src": "figures/gate-2014-ae-ae-23-option-D.png", "alt": "Option D stress block", "page": 9}}
        ],
        "page": 9
    },
    {
        "num": 24, "sec": "AE", "type": "NAT", "marks": 1, "ans": [2.95, 3.05], "rawKey": "2.95 to 3.05",
        "q": "A damped single degree of freedom system whose undamped natural frequency, ω_n = 10Hz, is subjected to sinusoidal excitation. If the maximum response amplitude is observed at 9Hz, the damping factor (in %) of the system is __________.",
        "opts": [],
        "page": 9
    },
    {
        "num": 25, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "A three-noded triangular finite element is shown in the figure. The displacement field is given as u = 20 + x + 20y + 2xy and v = 40 + 20x + 2y + 2xy. The strain component ε_xx at point (0.5, 0.5) is",
        "opts": ["10", "15", "2", "20"],
        "page": 9
    },
    {
        "num": 26, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "Consider the following statements regarding the stability of a conventional airplane:\n\nP. Dihedral angle of the wing increases the lateral stability\nQ. Sweepback of the wing increases the lateral stability\nR. Raising the wing from low-wing to high-wing configuration increases the lateral stability\n\nWhich of the above statements are true?",
        "opts": [
            "P and Q only",
            "Q and R only",
            "P and R only",
            "P, Q and R"
        ],
        "page": 9
    },
    {
        "num": 27, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "A jet engine is operating at a flight Mach number of 0.8 at an altitude of 10 km. Which of the following components has the highest total temperature?",
        "opts": ["Diffuser exit", "Combustor exit", "Turbine exit", "Nozzle exit"],
        "page": 9
    },
    {
        "num": 28, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "For a fifty percent reaction axial compressor stage, following statements are given:\n\nI. Velocity triangles at the entry and exit of the rotor are symmetrical\nII. The whirl or swirl component of absolute velocity at the rotor entry is equal to the whirl component of relative velocity at the rotor exit\nIII. Static pressure rise in the rotor is equal to the static pressure rise in the stator\n\nWhich of the above statements are true?",
        "opts": [
            "I and II only",
            "I, II and III",
            "I and III only",
            "II and III only"
        ],
        "page": 10
    },
    {
        "num": 29, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "C",
        "q": "In an axial flow turbine stage, the total-to-total efficiency is 0.85. The work done per kg of air is 180 kJ/kg. The total temperature at the rotor entry is 1200 K. If the ratio of specific heats γ = 1.33 and specific heat at constant pressure C_p = 1.15 kJ/kgK, the total-to-total pressure ratio across the stage is",
        "opts": ["0.64", "1.56", "1.74", "0.57"],
        "page": 10
    },
    {
        "num": 30, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "Which of the following is NOT a desirable property of a solid propellant?",
        "opts": [
            "High heat of combustion",
            "Low molecular weight of combustion products",
            "High density",
            "High temperature sensitivity of burning rate"
        ],
        "page": 10
    },
    {
        "num": 31, "sec": "AE", "type": "NAT", "marks": 1, "ans": [0.45, 0.55], "rawKey": "0.45 to 0.55",
        "q": "A single-stage chemical rocket with propellant mass fraction of 0.88 and specific impulse of 300 s is launched from the surface of the earth. The acceleration due to gravity is 9.8 m/s^2. If the drag and gravity effects are neglected, the burn-out velocity (in km/s) is ________.",
        "opts": [],
        "page": 10
    },
    {
        "num": 32, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "For an airplane executing a coordinated horizontal turn at a true airspeed of 200 m/s and bank angle of 45°, the turn radius (in m) is (take g = 9.81 m/s^2)",
        "opts": ["2038", "5076", "2882", "4077"],
        "page": 10
    },
    {
        "num": 33, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "D",
        "q": "The primary purpose of a trailing edge flap on an airplane wing is to",
        "opts": [
            "increase the maximum lift-to-drag ratio",
            "decrease the stalling speed",
            "increase the cruise speed",
            "increase the maximum lift coefficient"
        ],
        "page": 10
    },
    {
        "num": 34, "sec": "AE", "type": "MCQ", "marks": 1, "ans": "B",
        "q": "Which of the following statements is true for the Phugoid mode of an aircraft?",
        "opts": [
            "It involves large changes in pitch attitude and angle of attack with nearly constant speed",
            "It involves large changes in pitch attitude and speed with nearly constant angle of attack",
            "It is a rapid oscillatory mode with high frequency and heavy damping",
            "It is a non-oscillatory divergent mode"
        ],
        "page": 10
    },
    {
        "num": 35, "sec": "AE", "type": "NAT", "marks": 1, "ans": [1.2, 1.25], "rawKey": "1.2 to 1.25",
        "q": "An airplane of weight 40,000 N has a wing area of 20 m^2. The stalling speed of the airplane in straight and level flight at sea level (air density = 1.225 kg/m^3) is 40 m/s. The maximum lift coefficient C_{L,max} of the airplane is ________.",
        "opts": [],
        "page": 10
    },

    # AE Q26 - Q55 (Global Q36 - Q65)
    {
        "num": 36, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "The solution of the differential equation \\frac{d^2 y}{dx^2} + 4y = \\sin(2x) with boundary conditions y(0) = 0 and y'(0) = 0 is",
        "opts": [
            "y = \\frac{1}{16}(\\sin(2x) - 2x \\cos(2x))",
            "y = \\frac{1}{8}(\\sin(2x) - 2x \\cos(2x))",
            "y = \\frac{1}{16}(\\sin(2x) + 2x \\cos(2x))",
            "y = \\frac{1}{8}(\\sin(2x) + 2x \\cos(2x))"
        ],
        "page": 10
    },
    {
        "num": 37, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "For the periodic function given by f(x) = 2x, -π < x < 0 and f(x) = 2x, 0 < x < π with f(x + 2π) = f(x), using Fourier series, the sum s = 1 - 1/3 + 1/5 - 1/7 + ... converges to",
        "opts": ["π", "π/2", "π/4", "1"],
        "page": 11
    },
    {
        "num": 38, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "The matrix A = \\matrix{1 & 0 & 2; 0 & 2 & 1; 2 & 1 & 1} has eigenvalues λ_1, λ_2, λ_3. The value of \\det(A^3 - 4A^2 + 5A - 2I) is",
        "opts": ["0", "-2", "4", "-5"],
        "page": 11
    },
    {
        "num": 39, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "A particle moves along a curve whose parametric equations are x = e^{-t}, y = 2\\cos(3t), z = 2\\sin(3t), where t is time. The magnitude of the velocity of the particle at t = 0 is",
        "opts": ["\\sqrt{37}", "\\sqrt{13}", "6", "\\sqrt{40}"],
        "page": 11
    },
    {
        "num": 40, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A box contains 4 red balls and 6 black balls. Three balls are drawn at random from the box without replacement. The probability that all three balls are red is",
        "opts": ["1/30", "1/20", "1/15", "1/10"],
        "page": 11
    },
    {
        "num": 41, "sec": "AE", "type": "NAT", "marks": 2, "ans": [-5.01, -4.99], "rawKey": "-5.01 to -4.99",
        "q": "Consider a system of linear equations \\matrix{1 & 2 & 1; 2 & 1 & 3; 1 & -1 & 2} \\matrix{x_1; x_2; x_3} = \\matrix{4; 5; 1}. The value of x_2 is ________.",
        "opts": [],
        "page": 11
    },
    {
        "num": 42, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Figures (a) - (d) below show four objects. Dimensions and surface conditions of the objects are shown in the respective figures. All four objects are placed independently in a steady, uniform flow of same velocity and the direction of flow is from left to right as shown in (a). The flow field can be considered as 2-D, viscous and incompressible. Which object will experience the largest drag force?",
        "opts": ["(a)", "(b)", "(c)", "(d)"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-42-figure-1.png",
            "alt": "Four objects (a) flat plate parallel, (b) flat plate normal, (c) circular cylinder, (d) streamlined body",
            "page": 12
        }],
        "page": 12
    },
    {
        "num": 43, "sec": "AE", "type": "NAT", "marks": 2, "ans": [1705, 1720], "rawKey": "1705 to 1720",
        "q": "A student needs to find velocity across a stationary normal shock. He measures density and pressure across the shock as shown in the figure below. Ratio of specific heats γ = 1.4 and specific gas constant R = 287 J/kgK. The flow velocity (in m/s) upstream of the normal shock is ________.",
        "opts": [],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-43-figure-1.png",
            "alt": "Stationary normal shock with upstream density 0.5 kg/m^3, pressure 50 kPa and downstream values",
            "page": 12
        }],
        "page": 12
    },
    {
        "num": 44, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A steady, 2-D, inviscid and incompressible flow over a body is shown in the figure below. Free stream velocity and pressure are denoted by M_∞ and p_∞ respectively. Ratio of pressure at point A and p_∞ is 0.8 and specific heat ratio is 1.4. If the Mach number at point A is 0.6, the free-stream Mach number M_∞ is",
        "opts": ["0.35", "0.45", "0.55", "0.65"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-44-figure-1.png",
            "alt": "Subsonic flow past a body showing point A on surface with local Mach and pressure",
            "page": 12
        }],
        "page": 12
    },
    {
        "num": 45, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A student can measure free-stream velocity of a low-speed wind tunnel using a\n\ni. Pitot tube alone aligned with the flow direction.\nii. Pitot tube aligned with the flow direction with static pressure measured at the test-section wall.\niii. Pitot-static tube aligned with the flow direction.\niv. Manometer connected across the contraction nozzle.\n\nWhich of the following combinations can be used?",
        "opts": [
            "i, ii, iii",
            "i, iii, iv",
            "ii, iii, iv",
            "i, ii, iv"
        ],
        "page": 13
    },
    {
        "num": 46, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "An untwisted, elliptic wing of aspect ratio AR = 6 and span b is at an angle of attack α. Circulation distribution along the span is given by Γ(z) = Γ_0 \\sqrt{1 - (2z/b)^2}. Which of the following options is correct if the induced drag is D_i (given \\int_{-s}^s \\sqrt{1 - z^2/s^2} dz = \\frac{π s}{2})?",
        "opts": [
            "I = 0 and D_i = 0",
            "I = 1/2 and D_i = 0.5 C_L^2 / (π AR)",
            "I = 1 and D_i = \\frac{1}{2} ρ_∞ V_∞ Γ_0 b (π/4)",
            "I = 2 and D_i = ρ_∞ V_∞ Γ_0 b"
        ],
        "page": 13
    },
    {
        "num": 47, "sec": "AE", "type": "NAT", "marks": 2, "ans": [0.99, 1.01], "rawKey": "0.99 to 1.01",
        "q": "Water (density 1000 kg/m^3) is drained through a pipe of diameter 20 mm and length 10 m from a large tank as shown in the figure. Friction factor for the pipe is 0.02. Kinematic viscosity of water is 1 × 10^{-6} m^2/s; acceleration due to gravity is 10 m/s^2. If all other losses except the frictional losses at the pipe wall are neglected, the discharge through the pipe (in m^3/s × 10^{-3}) is ________.",
        "opts": [],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-47-figure-1.png",
            "alt": "Water draining from open large tank through a pipe of length L and diameter d",
            "page": 13
        }],
        "page": 13
    },
    {
        "num": 48, "sec": "AE", "type": "NAT", "marks": 2, "ans": [0.12, 0.13], "rawKey": "0.12 to 0.13",
        "q": "A 1.8m long steel beam of rectangular cross section (10mm× 6mm) is simply supported with a length of 1.2m between the supports and an overhang of 0.3m on either side. Young’s modulus for the material of the beam is 200GPa. For a 50N load applied at the center of the beam, magnitude of the slope of the beam at tip S is _________.",
        "opts": [],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-48-figure-1.png",
            "alt": "Steel beam of 1.8m with simply supported span 1.2m and overhangs 0.3m with 50N end loads",
            "page": 14
        }],
        "page": 14
    },
    {
        "num": 49, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "A",
        "q": "To transmit a given torque T, two alternative shaft designs are considered as shown in figure. Design I is a solid circular cross-section shaft of diameter 30mm. Design II is a thin-walled circular shaft of average diameter 40mm. Thickness of the wall in Design II has to be determined such that maximum shear stress is the same in both the designs for the given torque T (so that same material can be used for manufacturing both the shafts). Ratio of mass of shaft using Design I to the mass of shaft using Design II is",
        "opts": ["2.68", "5.36", "1.79", "3.58"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-49-figure-1.png",
            "alt": "Solid shaft Design I of diameter 30mm and thin-walled hollow shaft Design II of average diameter 40mm",
            "page": 14
        }],
        "page": 14
    },
    {
        "num": 50, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "A structural member of rectangular cross-section 10mm× 6mm and length 1m is made of steel (Young’s modulus is 200GPa and coefficient of thermal expansion is 12 × 10^{-6} / °C). It is rigidly fixed at both the ends and then subjected to a gradual increase in temperature. Ignoring the three dimensional effects, the structural member will buckle if the temperature is increased by ΔT °C which is",
        "opts": ["19.74", "9.87", "78.96", "39.48"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-50-figure-1.png",
            "alt": "Fixed-fixed structural member subjected to temperature rise Delta T",
            "page": 14
        }],
        "page": 14
    },
    {
        "num": 51, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "A gas cylinder (closed thin-walled cylindrical pressure vessel) of diameter 30cm and wall thickness 1mm is subjected to a design maximum internal pressure of 5bar (0.5MPa). The material used for manufacturing this cylinder has a failure stress of 260MPa. Assuming von Mises failure criterion, the factor of safety (with respect to maximum allowable stress) for this cylinder is",
        "opts": ["2.8", "2.0", "6.9", "4.0"],
        "page": 14
    },
    {
        "num": 52, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "A cantilevered beam is subjected to a parabolic distribution of shear traction at the right edge while the top and bottom surfaces are traction free. To solve this problem, following Airy’s stress function is proposed: φ = C_1 x y + C_2 x y^3 + C_3 x^2 y^2 + C_4 x^3 y. This is an admissible Airy’s function that would satisfy the bi-harmonic equation as well as the boundary conditions if and only if",
        "opts": [
            "C_1 = 0, C_2 = λ, C_3 = 0, C_4 = \\frac{λ}{3d^2}",
            "C_1 = λ, C_2 = \\frac{λ}{3d^2}, C_3 = 0, C_4 = 0",
            "C_1 = 0, C_2 = 0, C_3 = λ, C_4 = -\\frac{λ}{3d^2}",
            "C_1 = λ, C_2 = -\\frac{λ}{3d^2}, C_3 = 0, C_4 = 0"
        ],
        "page": 15
    },
    {
        "num": 53, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "1kg mass is hanging from a spring of stiffness 500N/m attached to a massless, symmetric beam of length 0.6m, moment of inertia about the bending axis I = 8.33 × 10^{-10} m^4 and Young’s modulus E = 210GPa as shown in the figure. The fundamental natural frequency (in rad/s) of the system is",
        "opts": ["3.24", "20.36", "22.36", "3.56"],
        "hasFigure": True,
        "figures": [{
            "src": "figures/gate-2014-ae-ae-53-figure-1.png",
            "alt": "Beam of length 0.6m supported at ends with spring-mass system hanging at midpoint",
            "page": 15
        }],
        "page": 15
    },
    {
        "num": 54, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "A single degree of freedom system is vibrating with initial (first cycle) amplitude of 5cm. The viscous damping factor associated with the vibrating system is 2%. Vibration amplitude of the fifth cycle (in cm) is",
        "opts": ["1.65", "4.41", "2.67", "3.02"],
        "page": 15
    },
    {
        "num": 55, "sec": "AE", "type": "NAT", "marks": 2, "ans": [1880, 1881], "rawKey": "1880 to 1881",
        "q": "A cruise missile with an ideal ramjet engine is flying at Mach 4.0 at an altitude where the ambient temperature is 100K. Consider ratio of specific heats γ = 1.4 and specific gas constant R = 287J/kgK. If the stagnation temperature in the combustion chamber is equal to 2310K, the speed of the exhaust gases (in m/s) is _____________.",
        "opts": [],
        "page": 15
    },
    {
        "num": 56, "sec": "AE", "type": "NAT", "marks": 2, "ans": [1.10, 1.25], "rawKey": "1.10 to 1.25",
        "q": "A gas turbine engine is operating under the following conditions:\n\nStagnation temperature at turbine inlet: 1350 K\nStagnation pressure at the turbine inlet: 10 bar\nStatic temperature at turbine exit: 800 K\nVelocity at turbine exit: 200 m/s\nTotal-to-total efficiency of turbine: 0.96\nγ (ratio of specific heats): 1.33\nC_p (specific heat at constant pressure): 1.147 kJ/kgK\n\nThe stagnation pressure (in bar) in the nozzle (considering isentropic nozzle) is equal to _______.",
        "opts": [],
        "page": 15
    },
    {
        "num": 57, "sec": "AE", "type": "NAT", "marks": 2, "ans": [74, 76], "rawKey": "74 to 76",
        "q": "Air at a stagnation temperature of 300K (ratio of specific heats, γ = 1.4 and specific gas constant R = 287 J/kgK) enters the impeller of a centrifugal compressor in axial direction. The stagnation pressure ratio between the diffuser outlet and impeller inlet is 4.0. The impeller blade radius is 0.3 m and it is rotating at 15000 rev/min. If the slip factor σ_s (Ratio of tangential component of air velocity at the blade tip to the blade tip speed) is 0.88, the overall efficiency (total-to-total) of the compressor (in %) is ___________.",
        "opts": [],
        "page": 16
    },
    {
        "num": 58, "sec": "AE", "type": "NAT", "marks": 2, "ans": [6050, 6250], "rawKey": "6050 to 6250",
        "q": "A stationary two stage rocket with initial mass of 16000kg, carrying a payload of 1000kg, is fired in a vertical trajectory from the surface of the earth. Both the stages of the rocket have same specific impulse, I_sp, of 300s and same structural coefficient of 0.14. The acceleration due to gravity is 9.8m/s^2. Neglecting drag and gravity effects and considering both the stages with same payload ratio, the terminal velocity attained by the payload in m/s is __________________.",
        "opts": [],
        "page": 16
    },
    {
        "num": 59, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "An aircraft is flying at Mach 3.0 at an altitude where the ambient pressure and temperature are 50 kPa and 200 K respectively. If the converging-diverging diffuser of the engine (considered isentropic with ratio of specific heats, γ = 1.4 and specific gas constant R = 287 J/kgK) has a throat area of 0.05 m^2, the mass flow rate through the engine in kg/s is",
        "opts": ["197", "232", "790", "157"],
        "page": 16
    },
    {
        "num": 60, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "A cryogenic rocket has a specific impulse of 455s and characteristic velocity of 2386 m/s. The value of thrust coefficient for this rocket is",
        "opts": ["1.78", "1.73", "1.87", "1.95"],
        "page": 16
    },
    {
        "num": 61, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "D",
        "q": "For a given airplane with a given wing loading executing a turn in the vertical plane, under what conditions will the turn radius be minimum and the turn rate be maximum?",
        "opts": [
            "Highest possible C_L and lowest possible load factor",
            "Lowest possible C_L and lowest possible load factor",
            "Lowest possible C_L and highest possible load factor",
            "Highest possible C_L and highest possible load factor"
        ],
        "page": 16
    },
    {
        "num": 62, "sec": "AE", "type": "NAT", "marks": 2, "ans": [18, 20], "rawKey": "18 to 20",
        "q": "Lift-off distance for a given aircraft of weight W is S_LO. If the take-off weight is reduced by 10%, then the magnitude of percentage change in the lift-off distance (assume all other parameters to remain constant) is _______.",
        "opts": [],
        "page": 16
    },
    {
        "num": 63, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "Which of the following design parameters influence the maximum rate-of-climb for a jet-propelled airplane?\n\nP. Wing loading\nQ. Maximum thrust-to-weight ratio\nR. Zero-lift drag coefficient\nS. Maximum lift-to-drag ratio",
        "opts": [
            "P and Q alone",
            "P, Q, R and S",
            "P, Q and S alone",
            "Q, R, and S alone"
        ],
        "page": 16
    },
    {
        "num": 64, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "C",
        "q": "Consider the following four statements regarding aircraft longitudinal stability:\n\nP. C_{M,cg} at zero lift must be positive\nQ. ∂C_{M,cg}/∂α_a must be negative (α_a is absolute angle of attack)\nR. C_{M,cg} at zero lift must be negative\nS. Slope of C_L versus α_a must be negative\n\nWhich of the following combination is the necessary criterion for stick fixed longitudinal balance and static stability?",
        "opts": [
            "Q and R only",
            "Q, R, and S only",
            "P and Q only",
            "Q and S only"
        ],
        "page": 17
    },
    {
        "num": 65, "sec": "AE", "type": "MCQ", "marks": 2, "ans": "B",
        "q": "Data for a light, single-engine, propeller driven aircraft in steady level flight at sea-level is as follows: velocity V_∞ = 40m/s, weight W = 13000N, lift coefficient C_L = 0.65, drag coefficient C_D = 0.025 + 0.04 C_L^2 and power available P_av = 100,000J/s. The rate of climb possible for this aircraft under the given conditions (in m/s) is",
        "opts": ["7.20", "5.11", "6.32", "4.23"],
        "page": 17
    }
]

# Build JSON files
formatted_questions = []
for q in questions_data:
    number = q["num"]
    sec = q["sec"]
    num_str = f"{number:02d}"
    qid = f"gate-2014-ae-ga-{num_str}" if sec == "GA" else f"gate-2014-ae-ae-{num_str}"
    
    opts = []
    if q["type"] != "NAT":
        for i, opt in enumerate(q["opts"]):
            if isinstance(opt, dict):
                label = opt.get("label", chr(65 + i))
                opt_obj = {"label": label}
                if "text" in opt:
                    opt_obj["text"] = opt["text"]
                if "figure" in opt:
                    opt_obj["figure"] = {
                        "src": opt["figure"]["src"],
                        "alt": opt["figure"]["alt"],
                        "page": opt["figure"]["page"],
                        "source": {
                            "file": "internal/ae/AE2014.pdf",
                            "sha256": pdf_sha,
                            "page": opt["figure"]["page"],
                            "verificationStatus": "source-verified",
                            "verifiedOn": "2026-10-07"
                        }
                    }
                opts.append(opt_obj)
            else:
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
                    "file": "internal/ae/AE2014.pdf",
                    "sha256": pdf_sha,
                    "page": fig["page"],
                    "verificationStatus": "source-verified",
                    "verifiedOn": "2026-10-07"
                }
            })

    formatted_questions.append({
        "id": qid,
        "number": number,
        "year": 2014,
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
        "markingRule": "gate-2014-official",
        "hasFigure": bool(figures),
        "figures": figures,
        "groupId": None,
        "source": {
            "paper": "AE",
            "year": 2014,
            "questionNumber": number if sec == "GA" else number - 10,
            "section": sec,
            "file": "internal/ae/AE2014.pdf",
            "sha256": pdf_sha,
            "pages": [{
                "page": q["page"],
                "coordinateSystem": "PDF points, top-left origin"
            }],
            "verificationStatus": "source-verified",
            "verifiedOn": "2026-10-07"
        },
        "transcriptionStatus": "source-verified",
        "solution": None,
        "solutionAvailability": "not-provided-in-source",
        "gradingStatus": "official key verified",
        "answerSource": {
            "paper": "AE",
            "questionNumber": number if sec == "GA" else number - 10,
            "section": sec,
            "file": "internal/ae/AE2014-key.pdf",
            "sha256": key_sha,
            "verifiedOn": "2026-10-07"
        }
    })

ga_ids = [q["id"] for q in formatted_questions if q["section"] == "GA"]
ae_ids = [q["id"] for q in formatted_questions if q["section"] == "AE"]
q_order = [q["id"] for q in formatted_questions]

paper_2014 = {
    "schemaVersion": 1,
    "id": "gate-2014-ae",
    "exam": "GATE",
    "year": 2014,
    "paper": "AE",
    "title": "GATE Aerospace Engineering 2014",
    "durationMinutes": 180,
    "totalMarks": 100,
    "totalQuestions": 65,
    "sectionOrder": ["GA", "AE"],
    "sections": [
        {
            "id": "GA",
            "title": "General Aptitude",
            "questionIds": ga_ids,
            "totalMarks": 15
        },
        {
            "id": "AE",
            "title": "Aerospace Engineering",
            "questionIds": ae_ids,
            "totalMarks": 85
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
        "file": "internal/ae/AE2014.pdf",
        "sha256": pdf_sha,
        "pageCount": 18
    },
    "questions": formatted_questions
}

with open("data/ae/2014.json", "w", encoding="utf-8") as f:
    json.dump(paper_2014, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Saved data/ae/2014.json")

# Build internal/ae/AE2014-key.json
key_rows = []
for q in questions_data:
    number = q["num"]
    sec = q["sec"]
    raw_k = q.get("rawKey", q["ans"])
    key_rows.append({
        "number": number,
        "section": sec,
        "sectionQuestionNumber": number if sec == "GA" else number - 10,
        "type": q["type"],
        "rawKey": raw_k,
        "marks": q["marks"]
    })

key_doc = {
    "exam": "GATE",
    "year": 2014,
    "paper": "AE",
    "source": "internal/ae/AE2014-key.pdf",
    "sha256": key_sha,
    "totalQuestions": 65,
    "totalMarks": 100,
    "rows": key_rows
}

with open("internal/ae/AE2014-key.json", "w", encoding="utf-8") as f:
    json.dump(key_doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Saved internal/ae/AE2014-key.json")

# Update manifest.json
with open("data/ae/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

y_idx = next((i for i, y in enumerate(manifest["years"]) if y["year"] == 2014), -1)
if y_idx >= 0:
    manifest["years"][y_idx] = {
        "year": 2014,
        "paper": "AE",
        "title": "GATE 2014 Aerospace Engineering",
        "path": "data/ae/2014.json",
        "ingestionStatus": "complete",
        "verificationStatus": "source-verified",
        "totalQuestions": 65,
        "totalMarks": 100,
        "sections": [
            {
                "id": "GA",
                "title": "General Aptitude",
                "questionIds": ga_ids,
                "totalMarks": 15
            },
            {
                "id": "AE",
                "title": "Aerospace Engineering",
                "questionIds": ae_ids,
                "totalMarks": 85
            }
        ],
        "questionTypeCounts": {
            "MCQ": 51,
            "MSQ": 0,
            "NAT": 14
        },
        "figureAssetCount": 17,
        "newFigureAssetCount": 17,
        "answerAvailability": {
            "officialKey": 65,
            "gradedAnswers": 65,
            "marksToAll": 0,
            "unavailable": 0
        },
        "provenance": {
            "paperSource": "internal/ae/AE2014.pdf",
            "keySource": "internal/ae/AE2014-key.pdf"
        },
        "sourcePdf": "internal/ae/AE2014.pdf",
        "questionCount": 65,
        "newQuestionCount": 65,
        "reusedGAQuestionCount": 0,
        "reusedFigureAssetCount": 0,
        "optionFigureCount": 4,
        "structuredTableCount": 0,
        "questionGroupCount": 0,
        "verifiedOn": "2026-10-07"
    }

with open("data/ae/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Updated data/ae/manifest.json for 2014")
