import json

def get_page_for_q(num):
    if 1 <= num <= 10:
        return 2
    elif 11 <= num <= 20:
        return 3
    elif 21 <= num <= 30:
        return 4
    elif 31 <= num <= 38:
        return 5
    elif 39 <= num <= 47:
        return 6
    elif 48 <= num <= 55:
        return 7
    elif 56 <= num <= 61:
        return 8
    elif 62 <= num <= 65:
        return 9
    return 2

def build_paper():
    cd_48_49_ctx = "Common Data for Questions 48 and 49:\nA wing and tail are geometrically similar, while tail area is one-third of the wing area and distance between two aerodynamic centres is equal to wing semi-span (b/2). In addition, following data is applicable:\n\\epsilon_{\\alpha} = 0.3, C_{L} = 1.0, C_{L_{\\alpha}} = 0.08/\\text{deg}., \\bar{c} = 2.5\\text{ m}, b = 30\\text{ m}, C_{M_{ac}} = 0, \\eta_{t} = 1.\nThe symbols have their usual aerodynamic interpretation."
    
    cd_50_51_ctx = "Common Data for Questions 50 and 51:\nA thin long circular pipe of 10 mm diameter has porous walls and spins at 60 rpm about its own axis. Fluid is pumped out of the pipe such that it emerges radially relative to the pipe surface at a velocity of 1 m/s.\n[Neglect the effect of gravity.]"

    la_52_53_ctx = "Statement for Linked Answer Questions 52 and 53:\nAir at a stagnation temperature of 15\u00b0C and stagnation pressure 100 kPa enters an axial compressor with an absolute velocity of 120 m/s. Inlet guide vanes direct this absolute velocity to the rotor inlet at an angle of 18\u00b0 to the axial direction. The rotor turning angle is 27\u00b0 and the mean blade speed is 200 m/s. The axial velocity is assumed constant through the stage."

    la_54_55_ctx = "Statement for Linked Answer Questions 54 and 55:\nA thin-walled spherical vessel (1 m inner diameter and 10 mm wall thickness) is made of a material with |\\sigma_{Y}| = 500\\text{ MPa} in both tension and compression."

    pdf_sha = "e4dabbfe9f0dddc2fddcb095b33335f54774d610e9071dd5d5222c9063afc07c"

    raw_questions = [
        # Q1
        {
            "num": 1,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The constraint A^{2} = A on any square matrix A is satisfied for",
            "opts": [
                ("A", "the identity matrix only."),
                ("B", "the null matrix only."),
                ("C", "both the identity matrix and the null matrix."),
                ("D", "no square matrix A.")
            ],
            "ans": "C"
        },
        # Q2
        {
            "num": 2,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The general solution of the differential equation \\frac{d^{2}y}{dt^{2}} + \\frac{dy}{dt} - 2y = 0 is",
            "opts": [
                ("A", "Ae^{-t} + Be^{2t}"),
                ("B", "Ae^{-2t} + Be^{-t}"),
                ("C", "Ae^{-2t} + Be^{t}"),
                ("D", "Ae^{t} + Be^{2t}")
            ],
            "ans": "C"
        },
        # Q3
        {
            "num": 3,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "An aircraft in trimmed condition has zero pitching moment at",
            "opts": [
                ("A", "its aerodynamic centre."),
                ("B", "its centre of gravity."),
                ("C", "25% of its mean aerodynamic chord."),
                ("D", "50% of its wing root chord.")
            ],
            "ans": "B"
        },
        # Q4
        {
            "num": 4,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "In an aircraft, constant roll rate can be produced using ailerons by applying",
            "opts": [
                ("A", "a step input."),
                ("B", "a ramp input."),
                ("C", "a sinusoidal input."),
                ("D", "an impulse input.")
            ],
            "ans": "D"
        },
        # Q5
        {
            "num": 5,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "For a symmetric airfoil, the lift coefficient for zero degree angle of attack is",
            "opts": [
                ("A", "- 1.0"),
                ("B", "0.0"),
                ("C", "0.5"),
                ("D", "1.0")
            ],
            "ans": "B"
        },
        # Q6
        {
            "num": 6,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The critical Mach number of an airfoil is attained when",
            "opts": [
                ("A", "the freestream Mach number is sonic."),
                ("B", "the freestream Mach number is supersonic."),
                ("C", "the Mach number somewhere on the airfoil is unity."),
                ("D", "the Mach number everywhere on the airfoil is supersonic.")
            ],
            "ans": "C"
        },
        # Q7
        {
            "num": 7,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The shadowgraph flow visualization technique depends on",
            "opts": [
                ("A", "the variation of the value of density in the flow."),
                ("B", "the first derivative of density with respect to spatial coordinate."),
                ("C", "the second derivative of density with respect to spatial coordinate."),
                ("D", "the third derivative of density with respect to spatial coordinate.")
            ],
            "ans": "C"
        },
        # Q8
        {
            "num": 8,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The Hohmann ellipse used as earth-Mars transfer orbit has",
            "opts": [
                ("A", "apogee at earth and perigee at Mars."),
                ("B", "both apogee and perigee at earth."),
                ("C", "apogee at Mars and perigee at earth."),
                ("D", "both apogee and perigee at Mars.")
            ],
            "ans": "C"
        },
        # Q9
        {
            "num": 9,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The governing equation for the static transverse deflection of a beam under an uniformly distributed load, according to Euler-Bernoulli (engineering) beam theory, is a",
            "opts": [
                ("A", "2^{nd} order linear homogenous partial differential equation."),
                ("B", "4^{th} order linear non-homogenous ordinary differential equation."),
                ("C", "2^{nd} order linear non-homogenous ordinary differential equation."),
                ("D", "4^{th} order nonlinear homogenous ordinary differential equation.")
            ],
            "ans": "B"
        },
        # Q10
        {
            "num": 10,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The Poisson’s ratio, \u03bd of most aircraft grade metallic alloys has values in the range:",
            "opts": [
                ("A", "-1 \u2264 \u03bd \u2264 0"),
                ("B", "0 \u2264 \u03bd \u2264 0.2"),
                ("C", "0.2 \u2264 \u03bd \u2264 0.4"),
                ("D", "0.4 \u2264 \u03bd \u2264 0.5")
            ],
            "ans": "C"
        },
        # Q11
        {
            "num": 11,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The value of k for which the system of equations x + 2y + kz = 1; 2x + ky + 8z = 3 has no solution is",
            "opts": [
                ("A", "0"),
                ("B", "2"),
                ("C", "4"),
                ("D", "8")
            ],
            "ans": "C"
        },
        # Q12
        {
            "num": 12,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "If u(t) is a unit step function, the solution of the differential equation m\\frac{d^{2}x}{dt^{2}} + kx = u(t) in Laplace domain is",
            "opts": [
                ("A", "\\frac{1}{s(ms^{2} + k)}"),
                ("B", "\\frac{1}{ms^{2} + k}"),
                ("C", "\\frac{s}{ms^{2} + k}"),
                ("D", "\\frac{1}{s^{2}(ms^{2} + k)}")
            ],
            "ans": "A"
        },
        # Q13
        {
            "num": 13,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The general solution of the differential equation \\frac{dy}{dx} - 2\\sqrt{y} = 0 is",
            "opts": [
                ("A", "y - \\sqrt{x} + C = 0"),
                ("B", "y - x + C = 0"),
                ("C", "\\sqrt{y} - \\sqrt{x} + C = 0"),
                ("D", "\\sqrt{y} - x + C = 0")
            ],
            "ans": "D"
        },
        # Q14
        {
            "num": 14,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "During the ground roll manoeuvre of an aircraft, the force(s) acting on it parallel to the direction of motion",
            "opts": [
                ("A", "is thrust alone."),
                ("B", "is drag alone."),
                ("C", "are both thrust and drag."),
                ("D", "are thrust, drag and a part of both weight and lift.")
            ],
            "ans": "D"
        },
        # Q15
        {
            "num": 15,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "An aircraft in a steady climb suddenly experiences a 10% drop in thrust. After a new equilibrium is reached at the same speed, the new rate of climb is",
            "opts": [
                ("A", "lower by exactly 10%."),
                ("B", "lower by more than 10%."),
                ("C", "lower by less than 10%."),
                ("D", "an unpredictable quantity.")
            ],
            "ans": "B"
        },
        # Q16
        {
            "num": 16,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "In an aircraft, the dive manoeuvre can be initiated by",
            "opts": [
                ("A", "reducing the engine thrust alone."),
                ("B", "reducing the angle of attack alone."),
                ("C", "generating a nose down pitch rate."),
                ("D", "increasing the engine thrust alone.")
            ],
            "ans": "C"
        },
        # Q17
        {
            "num": 17,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "In an aircraft, elevator control effectiveness determines",
            "opts": [
                ("A", "turn radius."),
                ("B", "rate of climb."),
                ("C", "forward-most location of the centre of gravity."),
                ("D", "aft-most location of the centre of gravity.")
            ],
            "ans": "C"
        },
        # Q18
        {
            "num": 18,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The Mach angle for a flow at Mach 2.0 is",
            "opts": [
                ("A", "30\u00b0"),
                ("B", "45\u00b0"),
                ("C", "60\u00b0"),
                ("D", "90\u00b0")
            ],
            "ans": "A"
        },
        # Q19
        {
            "num": 19,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "For a wing of aspect ratio AR, having an elliptical lift distribution, the induced drag coefficient is (where C_{L} is the lift coefficient)",
            "opts": [
                ("A", "\\frac{C_{L}}{\\pi AR}"),
                ("B", "\\frac{C_{L}^{2}}{\\pi AR}"),
                ("C", "\\frac{C_{L}}{2\\pi AR}"),
                ("D", "\\frac{C_{L}^{2}}{\\pi AR^{2}}")
            ],
            "ans": "B"
        },
        # Q20
        {
            "num": 20,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "Bernoulli’s equation is valid under steady state",
            "opts": [
                ("A", "only along a streamline in inviscid flow, and between any two points in potential flow."),
                ("B", "between any two points in both inviscid flow and potential flow."),
                ("C", "between any two points in inviscid flow, and only along a streamline in potential flow."),
                ("D", "only along a streamline in both inviscid flow and potential flow.")
            ],
            "ans": "A"
        },
        # Q21
        {
            "num": 21,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The ratio of flight speed to the exhaust velocity for maximum propulsion efficiency is",
            "opts": [
                ("A", "0.0"),
                ("B", "0.5"),
                ("C", "1.0"),
                ("D", "2.0")
            ],
            "ans": "C"
        },
        # Q22 (MTA)
        {
            "num": 22,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The ideal static pressure coefficient of a diffuser with an area ratio of 2.0 is",
            "opts": [
                ("A", "0.25"),
                ("B", "0.50"),
                ("C", "0.75"),
                ("D", "1.0")
            ],
            "ans": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q23
        {
            "num": 23,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "A rocket is to be launched from the bottom of a very deep crater on Mars for earth return. The specific impulse of the rocket, measured in seconds, is to be normalized by the acceleration due to gravity at",
            "opts": [
                ("A", "the bottom of the crater on Mars."),
                ("B", "Mars standard “sea level”."),
                ("C", "earth’s standard sea level."),
                ("D", "the same depth of the crater on earth.")
            ],
            "ans": "C"
        },
        # Q24
        {
            "num": 24,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "In a semi-monocoque construction of an aircraft wing, the skin and spar webs are the primary carriers of",
            "opts": [
                ("A", "shear stresses due to an aerodynamic moment component alone."),
                ("B", "normal (bending) stresses due to aerodynamic forces."),
                ("C", "shear stresses due to aerodynamic forces alone."),
                ("D", "shear stresses due to aerodynamic forces and a moment component.")
            ],
            "ans": "D"
        },
        # Q25
        {
            "num": 25,
            "sec": "AE",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The logarithmic decrement measured for a viscously damped single degree of freedom system is 0.125. The value of the damping factor in % is closest to",
            "opts": [
                ("A", "0.5"),
                ("B", "1.0"),
                ("C", "1.5"),
                ("D", "2.0")
            ],
            "ans": "D"
        },
        # Q26 (NAT)
        {
            "num": 26,
            "sec": "AE",
            "type": "NAT",
            "marks": 2,
            "neg": 0,
            "q": "The integration \\int_{0}^{1} x^{3} dx computed using trapezoidal rule with n = 4 intervals is _____.",
            "opts": [],
            "ans": [0.26, 0.27]
        },
        # Q27 (NAT)
        {
            "num": 27,
            "sec": "AE",
            "type": "NAT",
            "marks": 2,
            "neg": 0,
            "q": "An aircraft has a steady rate of climb of 300 m/s at sea level and 150 m/s at 2500 m altitude. The time taken (in sec) for this aircraft to climb from 500 m altitude to 3000 m altitude is _____.",
            "opts": [],
            "ans": [13, 14]
        },
        # Q28 (NAT)
        {
            "num": 28,
            "sec": "AE",
            "type": "NAT",
            "marks": 2,
            "neg": 0,
            "q": "An airfoil generates a lift of 80 N when operating in a freestream flow of 60 m/s. If the ambient pressure and temperature are 100 kPa and 290 K respectively (specific gas constant is 287 J/kg-K), the circulation on the airfoil in m^{2}/s is _____.",
            "opts": [],
            "ans": [1.1, 1.2]
        },
        # Q29 (NAT)
        {
            "num": 29,
            "sec": "AE",
            "type": "NAT",
            "marks": 2,
            "neg": 0,
            "q": "A rocket motor has combustion chamber temperature of 2600 K and the products have molecular weight of 25 g/mol and ratio of specific heats 1.2. The universal gas constant is 8314 J/kg-mole-K. The value of theoretical c^{*} (in m/s) is _____.",
            "opts": [],
            "ans": [1430, 1440]
        },
        # Q30 (NAT)
        {
            "num": 30,
            "sec": "AE",
            "type": "NAT",
            "marks": 2,
            "neg": 0,
            "q": "The mode shapes of an un-damped two degrees of freedom system are {1 \\quad 0.5}^{T} and {1 \\quad -0.675}^{T}. The corresponding natural frequencies are 0.45 Hz and 1.2471 Hz. The maximum amplitude (in mm) of vibration of the first degree of freedom due to an initial displacement of {2 \\quad 1}^{T} (in mm) and zero initial velocities is _____.",
            "opts": [],
            "ans": [2, 2]
        },
        # Q31
        {
            "num": 31,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The n^{th} derivative of the function y = \\frac{1}{x+3} is",
            "opts": [
                ("A", "\\frac{(-1)^{n} n!}{(x+3)^{n+1}}"),
                ("B", "\\frac{(-1)^{n+1} n!}{(x+3)^{n+1}}"),
                ("C", "\\frac{(-1)^{n} (n+1)!}{(x+3)^{n}}"),
                ("D", "\\frac{(-1)^{n} n!}{(x+3)^{n}}")
            ],
            "ans": "A"
        },
        # Q32
        {
            "num": 32,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The volume of a solid generated by rotating the region between semi-circle y = 1 - \\sqrt{1 - x^{2}} and straight line y = 1, about x axis, is",
            "opts": [
                ("A", "\\pi^{2} - \\frac{4}{3}\\pi"),
                ("B", "4\\pi^{2} - \\frac{1}{3}\\pi"),
                ("C", "\\pi^{2} - \\frac{3}{4}\\pi"),
                ("D", "\\frac{3}{4}\\pi^{2} - \\pi")
            ],
            "ans": "A"
        },
        # Q33
        {
            "num": 33,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "One eigenvalue of the matrix A = \\begin{bmatrix} 2 & 7 & 10 \\\\ 5 & 2 & 25 \\\\ 1 & 6 & 5 \\end{bmatrix} is – 9.33. One of the other eigenvalues is",
            "opts": [
                ("A", "18.33"),
                ("B", "-18.33"),
                ("C", "18.33 - 9.33i"),
                ("D", "18.33 + 9.33i")
            ],
            "ans": "A"
        },
        # Q34
        {
            "num": 34,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "If an aircraft takes off with 10% less fuel in comparison to its standard configuration, its range is",
            "opts": [
                ("A", "lower by exactly 10%."),
                ("B", "lower by more than 10%."),
                ("C", "lower by less than 10%."),
                ("D", "an unpredictable quantity.")
            ],
            "ans": "B"
        },
        # Q35 (MTA)
        {
            "num": 35,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "An aircraft has an approach speed of 144 kmph with a descent angle of 6.6\u00b0. If the aircraft load factor is 1.2 and constant deceleration at touch down is 0.25g (g = 9.81 m/s^{2}), its total landing distance approximately over a 15 m high obstacle is",
            "opts": [
                ("A", "1830 m."),
                ("B", "1380 m."),
                ("C", "830 m."),
                ("D", "380 m.")
            ],
            "ans": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q36
        {
            "num": 36,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "An aircraft is trimmed straight and level at true air speed (TAS) of 100 m/s at standard sea level (SSL). Further, pull of 5 N holds the speed at 90 m/s without re-trimming at SSL (air density = 1.22 kg/m^{3}). To fly at 3000 m altitude (air density = 0.91 kg/m^{3}) and 120 m/s TAS without re-trimming, the aircraft needs",
            "opts": [
                ("A", "1.95 N upward force."),
                ("B", "1.95 N downward force."),
                ("C", "1.85 N upward force."),
                ("D", "1.75 N downward force.")
            ],
            "ans": "B"
        },
        # Q37
        {
            "num": 37,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "An oblique shock wave with a wave angle \u03b2 is generated from a wedge angle of \u03b8. The ratio of the Mach number downstream of the shock to its normal component is",
            "opts": [
                ("A", "sin(\u03b2\u2013\u03b8)"),
                ("B", "cos(\u03b2\u2013\u03b8)"),
                ("C", "sin(\u03b8\u2013\u03b2)"),
                ("D", "cos(\u03b8\u2013\u03b2)")
            ],
            "ans": "A"
        },
        # Q38
        {
            "num": 38,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "In a closed-circuit supersonic wind tunnel, the convergent-divergent (C-D) nozzle and test section are followed by a C-D diffuser to swallow the starting shock. Here, we should have the",
            "opts": [
                ("A", "diffuser throat larger than the nozzle throat and the shock located just at the diffuser throat."),
                ("B", "diffuser throat larger than the nozzle throat and the shock located downstream of the diffuser throat."),
                ("C", "diffuser throat of the same size as the nozzle throat and the shock located just at the diffuser throat."),
                ("D", "diffuser throat of the same size as the nozzle throat and the shock located downstream of the diffuser throat.")
            ],
            "ans": "B"
        },
        # Q39
        {
            "num": 39,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "A vortex flowmeter works on the principle that the Strouhal number of 0.2 is a constant over a wide range of flow rates. If the bluff-body diameter in the flowmeter is 20 mm and the piezo-electric transducer registers the vortex shedding frequency to be 10 Hz, then the velocity of the flow would be measured as",
            "opts": [
                ("A", "0.1 m/s"),
                ("B", "1 m/s"),
                ("C", "10 m/s"),
                ("D", "100 m/s")
            ],
            "ans": "B"
        },
        # Q40
        {
            "num": 40,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The stagnation temperatures at the inlet and exit of a combustion chamber are 600 K and 1200 K, respectively. If the heating value of the fuel is 44 MJ/kg and specific heat at constant pressure for air and hot gases are 1.005 kJ/kg.K and 1.147 kJ/kg.K respectively, the fuel-to-air ratio is",
            "opts": [
                ("A", "0.0018"),
                ("B", "0.018"),
                ("C", "0.18"),
                ("D", "1.18")
            ],
            "ans": "B"
        },
        # Q41
        {
            "num": 41,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "A solid propellant of density 1800 kg/m^{3} has a burning rate law r = 6.65 \\times 10^{-3}p^{0.45} mm/s, where p is pressure in Pascals. It is used in a rocket motor with a tubular grain with an initial burning area of 0.314 m^{2}. The characteristic velocity is 1450 m/s. What should be the nozzle throat diameter to achieve an equilibrium chamber pressure of 50 bar at the end of the ignition transient?",
            "opts": [
                ("A", "35 mm"),
                ("B", "38 mm"),
                ("C", "41 mm"),
                ("D", "45 mm")
            ],
            "ans": "B"
        },
        # Q42
        {
            "num": 42,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "A bipropellant liquid rocket motor operates at a chamber pressure of 40 bar with a nozzle throat diameter of 50 mm. The characteristic velocity is 1540 m/s. If the fuel-oxidizer ratio of the propellant is 1.8, and the fuel density is 900 kg/m^{3}, what should be the minimum fuel tank volume for a burn time of 8 minutes",
            "opts": [
                ("A", "1.65 m^{3}"),
                ("B", "1.75 m^{3}"),
                ("C", "1.85 m^{3}"),
                ("D", "1.95 m^{3}")
            ],
            "ans": "B"
        },
        # Q43
        {
            "num": 43,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The propellant in a single stage sounding rocket occupies 60% of its initial mass. If all of it is expended instantaneously at an equivalent exhaust velocity of 3000 m/s, what would be the altitude attained by the payload when launched vertically?\n[Neglect drag and assume acceleration due to gravity to be constant at 9.81 m/s^{2}.]",
            "opts": [
                ("A", "315 km"),
                ("B", "335 km"),
                ("C", "365 km"),
                ("D", "385 km")
            ],
            "ans": "D"
        },
        # Q44
        {
            "num": 44,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The Airy stress function, \\phi = \\alpha x^{2} + \\beta xy + \\gamma y^{2} for a thin square panel of size l \\times l automatically satisfies compatibility. If the panel is subjected to uniform tensile stress, \\sigma_{o} on all four edges, the traction boundary conditions are satisfied by",
            "opts": [
                ("A", "\\alpha = \\sigma_{o}/2; \\beta = 0; \\gamma = \\sigma_{o}/2."),
                ("B", "\\alpha = \\sigma_{o}; \\beta = 0; \\gamma = \\sigma_{o}."),
                ("C", "\\alpha = 0; \\beta = \\sigma_{o}/4; \\gamma = 0."),
                ("D", "\\alpha = 0; \\beta = \\sigma_{o}/2; \\gamma = 0.")
            ],
            "ans": "A"
        },
        # Q45
        {
            "num": 45,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The boundary condition of a rod under longitudinal vibration is changed from fixed-fixed to fixed-free. The fundamental natural frequency of the rod is now k times the original frequency, where k is",
            "opts": [
                ("A", "\\frac{1}{2}"),
                ("B", "2"),
                ("C", "\\frac{1}{\\sqrt{2}}"),
                ("D", "\\sqrt{2}")
            ],
            "ans": "A"
        },
        # Q46
        {
            "num": 46,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "A spring-mass system is viscously damped with a viscous damping constant c. The energy dissipated per cycle when the system is undergoing a harmonic vibration X \\cos \\omega_{d} t is given by",
            "opts": [
                ("A", "\\pi c \\omega_{d} X^{2}"),
                ("B", "\\pi \\omega_{d} X^{2}"),
                ("C", "\\pi c \\omega_{d} X"),
                ("D", "\\pi c \\omega_{d}^{2} X")
            ],
            "ans": "A"
        },
        # Q47
        {
            "num": 47,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "Buckling of the fuselage skin can be delayed by",
            "opts": [
                ("A", "increasing internal pressure."),
                ("B", "placing stiffeners farther apart."),
                ("C", "reducing skin thickness."),
                ("D", "placing stiffeners farther and decreasing internal pressure.")
            ],
            "ans": "A"
        },
        # Q48 (CD)
        {
            "num": 48,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "common-data-48-49",
            "groupType": "common-data",
            "groupContext": cd_48_49_ctx,
            "q": "The maximum distance that the centre of gravity can be behind aerodynamic centre without destabilizing the wing-tail combination is",
            "opts": [
                ("A", "0.4 m"),
                ("B", "1.4 m"),
                ("C", "2.4 m"),
                ("D", "3.4 m")
            ],
            "ans": "B"
        },
        # Q49 (CD)
        {
            "num": 49,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "common-data-48-49",
            "groupType": "common-data",
            "groupContext": cd_48_49_ctx,
            "q": "The angle of incidence of tail to trim the wing-tail combination for a 5% static margin is",
            "opts": [
                ("A", "-1.4\u00b0"),
                ("B", "-0.4\u00b0"),
                ("C", "0.4\u00b0"),
                ("D", "1.4\u00b0")
            ],
            "ans": "A"
        },
        # Q50 (CD)
        {
            "num": 50,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "common-data-50-51",
            "groupType": "common-data",
            "groupContext": cd_50_51_ctx,
            "q": "What is the radial component of the fluid’s velocity at a radial location 0.5 m from the pipe axis?",
            "opts": [
                ("A", "0.01 m/s"),
                ("B", "0.1 m/s"),
                ("C", "1 m/s"),
                ("D", "10 m/s")
            ],
            "ans": "A"
        },
        # Q51 (CD, MTA)
        {
            "num": 51,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "common-data-50-51",
            "groupType": "common-data",
            "groupContext": cd_50_51_ctx,
            "q": "What is the tangential component of the fluid’s velocity at the same radial location as above?",
            "opts": [
                ("A", "0.01 m/s"),
                ("B", "0.03 m/s"),
                ("C", "0.10 m/s"),
                ("D", "0.31 m/s")
            ],
            "ans": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q52 (LA, MTA)
        {
            "num": 52,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "linked-answer-52-53",
            "groupType": "linked-answer",
            "groupContext": la_52_53_ctx,
            "q": "The blade angle at the inlet of the rotor is",
            "opts": [
                ("A", "25.5\u00b0"),
                ("B", "38.5\u00b0"),
                ("C", "48.5\u00b0"),
                ("D", "59.5\u00b0")
            ],
            "ans": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q53 (LA, MTA)
        {
            "num": 53,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "linked-answer-52-53",
            "groupType": "linked-answer",
            "groupContext": la_52_53_ctx,
            "q": "If the mass flow rate is 1 kg/s, the power required to drive the compressor is",
            "opts": [
                ("A", "50.5 kW"),
                ("B", "40.5 kW"),
                ("C", "30.5 kW"),
                ("D", "20.5 kW")
            ],
            "ans": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q54 (LA)
        {
            "num": 54,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "linked-answer-54-55",
            "groupType": "linked-answer",
            "groupContext": la_54_55_ctx,
            "q": "The internal pressure p_{Y} at yield, based on the von Mises yield criterion, if the vessel is floating in space, is approximately",
            "opts": [
                ("A", "500 MPa"),
                ("B", "250 MPa"),
                ("C", "100 MPa"),
                ("D", "20 MPa")
            ],
            "ans": "D"
        },
        # Q55 (LA)
        {
            "num": 55,
            "sec": "AE",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "groupId": "linked-answer-54-55",
            "groupType": "linked-answer",
            "groupContext": la_54_55_ctx,
            "q": "If the vessel is evacuated (internal pressure = 0) and subjected to external pressure, yielding according to the von Mises yield criterion (assuming elastic stability until yield)",
            "opts": [
                ("A", "occurs at about half the pressure p_{Y}."),
                ("B", "occurs at about double the pressure p_{Y}."),
                ("C", "occurs at about the same pressure p_{Y}."),
                ("D", "never occurs.")
            ],
            "ans": "C"
        },
        # Q56 (GA)
        {
            "num": 56,
            "sec": "GA",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nI ___ to have bought a diamond ring.",
            "opts": [
                ("A", "have a liking"),
                ("B", "should have liked"),
                ("C", "would like"),
                ("D", "may like")
            ],
            "ans": "C"
        },
        # Q57 (GA)
        {
            "num": 57,
            "sec": "GA",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nFood prices ___ again this month.",
            "opts": [
                ("A", "have raised"),
                ("B", "have been raising"),
                ("C", "have been rising"),
                ("D", "have arose")
            ],
            "ans": "C"
        },
        # Q58 (GA)
        {
            "num": 58,
            "sec": "GA",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nThe administrators went on to implement yet another unreasonable measure, arguing that the measures were already ___ and one more would hardly make a difference.",
            "opts": [
                ("A", "reflective"),
                ("B", "utopian"),
                ("C", "luxuriant"),
                ("D", "unpopular")
            ],
            "ans": "D"
        },
        # Q59 (GA)
        {
            "num": 59,
            "sec": "GA",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nTo those of us who had always thought him timid, his ___ came as a surprise.",
            "opts": [
                ("A", "intrepidity"),
                ("B", "inevitability"),
                ("C", "inability"),
                ("D", "inertness")
            ],
            "ans": "A"
        },
        # Q60 (GA)
        {
            "num": 60,
            "sec": "GA",
            "type": "MCQ",
            "marks": 1,
            "neg": 0.3333333333333333,
            "q": "The arithmetic mean of five different natural numbers is 12. The largest possible value among the numbers is",
            "opts": [
                ("A", "12"),
                ("B", "40"),
                ("C", "50"),
                ("D", "60")
            ],
            "ans": "C"
        },
        # Q61 (GA)
        {
            "num": 61,
            "sec": "GA",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "Two policemen, A and B, fire once each at the same time at an escaping convict. The probability that A hits the convict is three times the probability that B hits the convict. If the probability of the convict not getting injured is 0.5, the probability that B hits the convict is",
            "opts": [
                ("A", "0.14"),
                ("B", "0.22"),
                ("C", "0.33"),
                ("D", "0.40")
            ],
            "ans": "A"
        },
        # Q62 (GA)
        {
            "num": 62,
            "sec": "GA",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "The total runs scored by four cricketers P, Q, R, and S in years 2009 and 2010 are given in the following table:\n\n| Player | 2009 | 2010 |\n| :--- | :--- | :--- |\n| P | 802 | 1008 |\n| Q | 765 | 912 |\n| R | 429 | 619 |\n| S | 501 | 701 |\n\nThe player with the lowest percentage increase in total runs is",
            "opts": [
                ("A", "P"),
                ("B", "Q"),
                ("C", "R"),
                ("D", "S")
            ],
            "ans": "B"
        },
        # Q63 (GA)
        {
            "num": 63,
            "sec": "GA",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "If a prime number on division by 4 gives a remainder of 1, then that number can be expressed as",
            "opts": [
                ("A", "sum of squares of two natural numbers"),
                ("B", "sum of cubes of two natural numbers"),
                ("C", "sum of square roots of two natural numbers"),
                ("D", "sum of cube roots of two natural numbers")
            ],
            "ans": "A"
        },
        # Q64 (GA)
        {
            "num": 64,
            "sec": "GA",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "Two points (4, p) and (0, q) lie on a straight line having a slope of 3/4. The value of (p – q) is",
            "opts": [
                ("A", "-3"),
                ("B", "0"),
                ("C", "3"),
                ("D", "4")
            ],
            "ans": "C"
        },
        # Q65 (GA)
        {
            "num": 65,
            "sec": "GA",
            "type": "MCQ",
            "marks": 2,
            "neg": 0.6666666666666666,
            "q": "In the early nineteenth century, theories of social evolution were inspired less by Biology than by the conviction of social scientists that there was a growing improvement in social institutions. Progress was taken for granted and social scientists attempted to discover its laws and phases.\n\nWhich one of the following inferences may be drawn with the greatest accuracy from the above passage?\n\nSocial scientists",
            "opts": [
                ("A", "did not question that progress was a fact."),
                ("B", "did not approve of Biology."),
                ("C", "framed the laws of progress."),
                ("D", "emphasized Biology over Social Sciences.")
            ],
            "ans": "A"
        }
    ]

    q_objects = []
    for rq in raw_questions:
        num = rq["num"]
        sec = rq["sec"]
        qid = f"gate-2012-ae-{sec.lower()}-{num:02d}"
        page_num = get_page_for_q(num)
        
        q_obj = {
            "id": qid,
            "number": num,
            "year": 2012,
            "paper": "AE",
            "section": sec,
            "subject": "Aerospace Engineering" if sec == "AE" else "General Aptitude",
            "type": rq["type"],
            "marks": rq["marks"],
            "negativeMarks": rq["neg"],
            "question": rq["q"],
            "options": [{"label": l, "text": t} for l, t in rq["opts"]],
            "answer": rq["ans"],
            "acceptedAnswers": rq["ans"] if isinstance(rq["ans"], list) else [rq["ans"]],
            "markingRule": "gate-2012-official",
            "hasFigure": False,
            "figures": [],
            "groupId": rq.get("groupId"),
            "source": {
                "paper": "AE",
                "year": 2012,
                "questionNumber": num,
                "section": sec,
                "file": "internal/ae/AE2012.pdf",
                "sha256": pdf_sha,
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
        if rq.get("gradingRule"):
            q_obj["gradingRule"] = rq["gradingRule"]
        if rq.get("officialKey"):
            q_obj["officialKey"] = rq["officialKey"]
            
        q_objects.append(q_obj)

    ae_q_ids = [f"gate-2012-ae-ae-{i:02d}" for i in range(1, 56)]
    ga_q_ids = [f"gate-2012-ae-ga-{i:02d}" for i in range(56, 66)]
    all_q_ids = ae_q_ids + ga_q_ids

    question_refs = []
    for q in q_objects:
        question_refs.append({
            "id": q["id"],
            "number": q["number"],
            "section": q["section"]
        })

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
            "questionIds": ["gate-2012-ae-ae-48", "gate-2012-ae-ae-49"]
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
            "questionIds": ["gate-2012-ae-ae-50", "gate-2012-ae-ae-51"]
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
            "questionIds": ["gate-2012-ae-ae-52", "gate-2012-ae-ae-53"],
            "dependencies": [
                {
                    "questionId": "gate-2012-ae-ae-53",
                    "dependsOn": "gate-2012-ae-ae-52"
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
            "questionIds": ["gate-2012-ae-ae-54", "gate-2012-ae-ae-55"],
            "dependencies": [
                {
                    "questionId": "gate-2012-ae-ae-55",
                    "dependsOn": "gate-2012-ae-ae-54"
                }
            ]
        }
    ]

    paper = {
        "schemaVersion": 1,
        "id": "gate-2012-ae",
        "exam": "GATE",
        "year": 2012,
        "paper": "AE",
        "title": "GATE Aerospace Engineering 2012",
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
            "file": "internal/ae/AE2012.pdf",
            "sha256": pdf_sha,
            "pageCount": 10
        },
        "questions": q_objects
    }

    with open('data/ae/2012.json', 'w', encoding='utf-8') as f:
        json.dump(paper, f, indent=2, ensure_ascii=False)

    print('Successfully generated data/ae/2012.json with full schema')

build_paper()
