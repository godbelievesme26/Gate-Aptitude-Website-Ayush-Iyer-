import json

def build_paper():
    cd_48_49_ctx = "Common Data for Questions 48 and 49:\nA wing and tail are geometrically similar, while tail area is one-third of the wing area and distance between two aerodynamic centres is equal to wing semi-span (b/2). In addition, following data is applicable:\n\\epsilon_{\\alpha} = 0.3, C_{L} = 1.0, C_{L_{\\alpha}} = 0.08/\\text{deg}., \\bar{c} = 2.5\\text{ m}, b = 30\\text{ m}, C_{M_{ac}} = 0, \\eta_{t} = 1.\nThe symbols have their usual aerodynamic interpretation."
    
    cd_50_51_ctx = "Common Data for Questions 50 and 51:\nA thin long circular pipe of 10 mm diameter has porous walls and spins at 60 rpm about its own axis. Fluid is pumped out of the pipe such that it emerges radially relative to the pipe surface at a velocity of 1 m/s.\n[Neglect the effect of gravity.]"

    la_52_53_ctx = "Statement for Linked Answer Questions 52 and 53:\nAir at a stagnation temperature of 15\u00b0C and stagnation pressure 100 kPa enters an axial compressor with an absolute velocity of 120 m/s. Inlet guide vanes direct this absolute velocity to the rotor inlet at an angle of 18\u00b0 to the axial direction. The rotor turning angle is 27\u00b0 and the mean blade speed is 200 m/s. The axial velocity is assumed constant through the stage."

    la_54_55_ctx = "Statement for Linked Answer Questions 54 and 55:\nA thin-walled spherical vessel (1 m inner diameter and 10 mm wall thickness) is made of a material with |\\sigma_{Y}| = 500\\text{ MPa} in both tension and compression."

    q_list = [
        # Q1
        {
            "id": "gate-2012-ae-ae-01",
            "number": 1,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The constraint A^{2} = A on any square matrix A is satisfied for",
            "options": [
                {"label": "A", "text": "the identity matrix only."},
                {"label": "B", "text": "the null matrix only."},
                {"label": "C", "text": "both the identity matrix and the null matrix."},
                {"label": "D", "text": "no square matrix A."}
            ],
            "answer": "C"
        },
        # Q2
        {
            "id": "gate-2012-ae-ae-02",
            "number": 2,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The general solution of the differential equation \\frac{d^{2}y}{dt^{2}} + \\frac{dy}{dt} - 2y = 0 is",
            "options": [
                {"label": "A", "text": "Ae^{-t} + Be^{2t}"},
                {"label": "B", "text": "Ae^{-2t} + Be^{-t}"},
                {"label": "C", "text": "Ae^{-2t} + Be^{t}"},
                {"label": "D", "text": "Ae^{t} + Be^{2t}"}
            ],
            "answer": "C"
        },
        # Q3
        {
            "id": "gate-2012-ae-ae-03",
            "number": 3,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "An aircraft in trimmed condition has zero pitching moment at",
            "options": [
                {"label": "A", "text": "its aerodynamic centre."},
                {"label": "B", "text": "its centre of gravity."},
                {"label": "C", "text": "25% of its mean aerodynamic chord."},
                {"label": "D", "text": "50% of its wing root chord."}
            ],
            "answer": "B"
        },
        # Q4
        {
            "id": "gate-2012-ae-ae-04",
            "number": 4,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "In an aircraft, constant roll rate can be produced using ailerons by applying",
            "options": [
                {"label": "A", "text": "a step input."},
                {"label": "B", "text": "a ramp input."},
                {"label": "C", "text": "a sinusoidal input."},
                {"label": "D", "text": "an impulse input."}
            ],
            "answer": "D"
        },
        # Q5
        {
            "id": "gate-2012-ae-ae-05",
            "number": 5,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "For a symmetric airfoil, the lift coefficient for zero degree angle of attack is",
            "options": [
                {"label": "A", "text": "- 1.0"},
                {"label": "B", "text": "0.0"},
                {"label": "C", "text": "0.5"},
                {"label": "D", "text": "1.0"}
            ],
            "answer": "B"
        },
        # Q6
        {
            "id": "gate-2012-ae-ae-06",
            "number": 6,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The critical Mach number of an airfoil is attained when",
            "options": [
                {"label": "A", "text": "the freestream Mach number is sonic."},
                {"label": "B", "text": "the freestream Mach number is supersonic."},
                {"label": "C", "text": "the Mach number somewhere on the airfoil is unity."},
                {"label": "D", "text": "the Mach number everywhere on the airfoil is supersonic."}
            ],
            "answer": "C"
        },
        # Q7
        {
            "id": "gate-2012-ae-ae-07",
            "number": 7,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The shadowgraph flow visualization technique depends on",
            "options": [
                {"label": "A", "text": "the variation of the value of density in the flow."},
                {"label": "B", "text": "the first derivative of density with respect to spatial coordinate."},
                {"label": "C", "text": "the second derivative of density with respect to spatial coordinate."},
                {"label": "D", "text": "the third derivative of density with respect to spatial coordinate."}
            ],
            "answer": "C"
        },
        # Q8
        {
            "id": "gate-2012-ae-ae-08",
            "number": 8,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The Hohmann ellipse used as earth-Mars transfer orbit has",
            "options": [
                {"label": "A", "text": "apogee at earth and perigee at Mars."},
                {"label": "B", "text": "both apogee and perigee at earth."},
                {"label": "C", "text": "apogee at Mars and perigee at earth."},
                {"label": "D", "text": "both apogee and perigee at Mars."}
            ],
            "answer": "C"
        },
        # Q9
        {
            "id": "gate-2012-ae-ae-09",
            "number": 9,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The governing equation for the static transverse deflection of a beam under an uniformly distributed load, according to Euler-Bernoulli (engineering) beam theory, is a",
            "options": [
                {"label": "A", "text": "2^{nd} order linear homogenous partial differential equation."},
                {"label": "B", "text": "4^{th} order linear non-homogenous ordinary differential equation."},
                {"label": "C", "text": "2^{nd} order linear non-homogenous ordinary differential equation."},
                {"label": "D", "text": "4^{th} order nonlinear homogenous ordinary differential equation."}
            ],
            "answer": "B"
        },
        # Q10
        {
            "id": "gate-2012-ae-ae-10",
            "number": 10,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The Poisson’s ratio, \u03bd of most aircraft grade metallic alloys has values in the range:",
            "options": [
                {"label": "A", "text": "-1 \u2264 \u03bd \u2264 0"},
                {"label": "B", "text": "0 \u2264 \u03bd \u2264 0.2"},
                {"label": "C", "text": "0.2 \u2264 \u03bd \u2264 0.4"},
                {"label": "D", "text": "0.4 \u2264 \u03bd \u2264 0.5"}
            ],
            "answer": "C"
        },
        # Q11
        {
            "id": "gate-2012-ae-ae-11",
            "number": 11,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The value of k for which the system of equations x + 2y + kz = 1; 2x + ky + 8z = 3 has no solution is",
            "options": [
                {"label": "A", "text": "0"},
                {"label": "B", "text": "2"},
                {"label": "C", "text": "4"},
                {"label": "D", "text": "8"}
            ],
            "answer": "C"
        },
        # Q12
        {
            "id": "gate-2012-ae-ae-12",
            "number": 12,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "If u(t) is a unit step function, the solution of the differential equation m\\frac{d^{2}x}{dt^{2}} + kx = u(t) in Laplace domain is",
            "options": [
                {"label": "A", "text": "\\frac{1}{s(ms^{2} + k)}"},
                {"label": "B", "text": "\\frac{1}{ms^{2} + k}"},
                {"label": "C", "text": "\\frac{s}{ms^{2} + k}"},
                {"label": "D", "text": "\\frac{1}{s^{2}(ms^{2} + k)}"}
            ],
            "answer": "A"
        },
        # Q13
        {
            "id": "gate-2012-ae-ae-13",
            "number": 13,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The general solution of the differential equation \\frac{dy}{dx} - 2\\sqrt{y} = 0 is",
            "options": [
                {"label": "A", "text": "y - \\sqrt{x} + C = 0"},
                {"label": "B", "text": "y - x + C = 0"},
                {"label": "C", "text": "\\sqrt{y} - \\sqrt{x} + C = 0"},
                {"label": "D", "text": "\\sqrt{y} - x + C = 0"}
            ],
            "answer": "D"
        },
        # Q14
        {
            "id": "gate-2012-ae-ae-14",
            "number": 14,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "During the ground roll manoeuvre of an aircraft, the force(s) acting on it parallel to the direction of motion",
            "options": [
                {"label": "A", "text": "is thrust alone."},
                {"label": "B", "text": "is drag alone."},
                {"label": "C", "text": "are both thrust and drag."},
                {"label": "D", "text": "are thrust, drag and a part of both weight and lift."}
            ],
            "answer": "D"
        },
        # Q15
        {
            "id": "gate-2012-ae-ae-15",
            "number": 15,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "An aircraft in a steady climb suddenly experiences a 10% drop in thrust. After a new equilibrium is reached at the same speed, the new rate of climb is",
            "options": [
                {"label": "A", "text": "lower by exactly 10%."},
                {"label": "B", "text": "lower by more than 10%."},
                {"label": "C", "text": "lower by less than 10%."},
                {"label": "D", "text": "an unpredictable quantity."}
            ],
            "answer": "B"
        },
        # Q16
        {
            "id": "gate-2012-ae-ae-16",
            "number": 16,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "In an aircraft, the dive manoeuvre can be initiated by",
            "options": [
                {"label": "A", "text": "reducing the engine thrust alone."},
                {"label": "B", "text": "reducing the angle of attack alone."},
                {"label": "C", "text": "generating a nose down pitch rate."},
                {"label": "D", "text": "increasing the engine thrust alone."}
            ],
            "answer": "C"
        },
        # Q17
        {
            "id": "gate-2012-ae-ae-17",
            "number": 17,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "In an aircraft, elevator control effectiveness determines",
            "options": [
                {"label": "A", "text": "turn radius."},
                {"label": "B", "text": "rate of climb."},
                {"label": "C", "text": "forward-most location of the centre of gravity."},
                {"label": "D", "text": "aft-most location of the centre of gravity."}
            ],
            "answer": "C"
        },
        # Q18
        {
            "id": "gate-2012-ae-ae-18",
            "number": 18,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The Mach angle for a flow at Mach 2.0 is",
            "options": [
                {"label": "A", "text": "30\u00b0"},
                {"label": "B", "text": "45\u00b0"},
                {"label": "C", "text": "60\u00b0"},
                {"label": "D", "text": "90\u00b0"}
            ],
            "answer": "A"
        },
        # Q19
        {
            "id": "gate-2012-ae-ae-19",
            "number": 19,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "For a wing of aspect ratio AR, having an elliptical lift distribution, the induced drag coefficient is (where C_{L} is the lift coefficient)",
            "options": [
                {"label": "A", "text": "\\frac{C_{L}}{\\pi AR}"},
                {"label": "B", "text": "\\frac{C_{L}^{2}}{\\pi AR}"},
                {"label": "C", "text": "\\frac{C_{L}}{2\\pi AR}"},
                {"label": "D", "text": "\\frac{C_{L}^{2}}{\\pi AR^{2}}"}
            ],
            "answer": "B"
        },
        # Q20
        {
            "id": "gate-2012-ae-ae-20",
            "number": 20,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "Bernoulli’s equation is valid under steady state",
            "options": [
                {"label": "A", "text": "only along a streamline in inviscid flow, and between any two points in potential flow."},
                {"label": "B", "text": "between any two points in both inviscid flow and potential flow."},
                {"label": "C", "text": "between any two points in inviscid flow, and only along a streamline in potential flow."},
                {"label": "D", "text": "only along a streamline in both inviscid flow and potential flow."}
            ],
            "answer": "A"
        },
        # Q21
        {
            "id": "gate-2012-ae-ae-21",
            "number": 21,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The ratio of flight speed to the exhaust velocity for maximum propulsion efficiency is",
            "options": [
                {"label": "A", "text": "0.0"},
                {"label": "B", "text": "0.5"},
                {"label": "C", "text": "1.0"},
                {"label": "D", "text": "2.0"}
            ],
            "answer": "C"
        },
        # Q22 (MTA)
        {
            "id": "gate-2012-ae-ae-22",
            "number": 22,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The ideal static pressure coefficient of a diffuser with an area ratio of 2.0 is",
            "options": [
                {"label": "A", "text": "0.25"},
                {"label": "B", "text": "0.50"},
                {"label": "C", "text": "0.75"},
                {"label": "D", "text": "1.0"}
            ],
            "answer": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q23
        {
            "id": "gate-2012-ae-ae-23",
            "number": 23,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "A rocket is to be launched from the bottom of a very deep crater on Mars for earth return. The specific impulse of the rocket, measured in seconds, is to be normalized by the acceleration due to gravity at",
            "options": [
                {"label": "A", "text": "the bottom of the crater on Mars."},
                {"label": "B", "text": "Mars standard “sea level”."},
                {"label": "C", "text": "earth’s standard sea level."},
                {"label": "D", "text": "the same depth of the crater on earth."}
            ],
            "answer": "C"
        },
        # Q24
        {
            "id": "gate-2012-ae-ae-24",
            "number": 24,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "In a semi-monocoque construction of an aircraft wing, the skin and spar webs are the primary carriers of",
            "options": [
                {"label": "A", "text": "shear stresses due to an aerodynamic moment component alone."},
                {"label": "B", "text": "normal (bending) stresses due to aerodynamic forces."},
                {"label": "C", "text": "shear stresses due to aerodynamic forces alone."},
                {"label": "D", "text": "shear stresses due to aerodynamic forces and a moment component."}
            ],
            "answer": "D"
        },
        # Q25
        {
            "id": "gate-2012-ae-ae-25",
            "number": 25,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The logarithmic decrement measured for a viscously damped single degree of freedom system is 0.125. The value of the damping factor in % is closest to",
            "options": [
                {"label": "A", "text": "0.5"},
                {"label": "B", "text": "1.0"},
                {"label": "C", "text": "1.5"},
                {"label": "D", "text": "2.0"}
            ],
            "answer": "D"
        },
        # Q26 (NAT)
        {
            "id": "gate-2012-ae-ae-26",
            "number": 26,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "NAT",
            "marks": 2,
            "negativeMarks": 0,
            "question": "The integration \\int_{0}^{1} x^{3} dx computed using trapezoidal rule with n = 4 intervals is _____.",
            "answer": [0.26, 0.27]
        },
        # Q27 (NAT)
        {
            "id": "gate-2012-ae-ae-27",
            "number": 27,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "NAT",
            "marks": 2,
            "negativeMarks": 0,
            "question": "An aircraft has a steady rate of climb of 300 m/s at sea level and 150 m/s at 2500 m altitude. The time taken (in sec) for this aircraft to climb from 500 m altitude to 3000 m altitude is _____.",
            "answer": [13, 14]
        },
        # Q28 (NAT)
        {
            "id": "gate-2012-ae-ae-28",
            "number": 28,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "NAT",
            "marks": 2,
            "negativeMarks": 0,
            "question": "An airfoil generates a lift of 80 N when operating in a freestream flow of 60 m/s. If the ambient pressure and temperature are 100 kPa and 290 K respectively (specific gas constant is 287 J/kg-K), the circulation on the airfoil in m^{2}/s is _____.",
            "answer": [1.1, 1.2]
        },
        # Q29 (NAT)
        {
            "id": "gate-2012-ae-ae-29",
            "number": 29,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "NAT",
            "marks": 2,
            "negativeMarks": 0,
            "question": "A rocket motor has combustion chamber temperature of 2600 K and the products have molecular weight of 25 g/mol and ratio of specific heats 1.2. The universal gas constant is 8314 J/kg-mole-K. The value of theoretical c^{*} (in m/s) is _____.",
            "answer": [1430, 1440]
        },
        # Q30 (NAT)
        {
            "id": "gate-2012-ae-ae-30",
            "number": 30,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "NAT",
            "marks": 2,
            "negativeMarks": 0,
            "question": "The mode shapes of an un-damped two degrees of freedom system are {1 \\quad 0.5}^{T} and {1 \\quad -0.675}^{T}. The corresponding natural frequencies are 0.45 Hz and 1.2471 Hz. The maximum amplitude (in mm) of vibration of the first degree of freedom due to an initial displacement of {2 \\quad 1}^{T} (in mm) and zero initial velocities is _____.",
            "answer": [2, 2]
        },
        # Q31
        {
            "id": "gate-2012-ae-ae-31",
            "number": 31,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The n^{th} derivative of the function y = \\frac{1}{x+3} is",
            "options": [
                {"label": "A", "text": "\\frac{(-1)^{n} n!}{(x+3)^{n+1}}"},
                {"label": "B", "text": "\\frac{(-1)^{n+1} n!}{(x+3)^{n+1}}"},
                {"label": "C", "text": "\\frac{(-1)^{n} (n+1)!}{(x+3)^{n}}"},
                {"label": "D", "text": "\\frac{(-1)^{n} n!}{(x+3)^{n}}"}
            ],
            "answer": "A"
        },
        # Q32
        {
            "id": "gate-2012-ae-ae-32",
            "number": 32,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The volume of a solid generated by rotating the region between semi-circle y = 1 - \\sqrt{1 - x^{2}} and straight line y = 1, about x axis, is",
            "options": [
                {"label": "A", "text": "\\pi^{2} - \\frac{4}{3}\\pi"},
                {"label": "B", "text": "4\\pi^{2} - \\frac{1}{3}\\pi"},
                {"label": "C", "text": "\\pi^{2} - \\frac{3}{4}\\pi"},
                {"label": "D", "text": "\\frac{3}{4}\\pi^{2} - \\pi"}
            ],
            "answer": "A"
        },
        # Q33
        {
            "id": "gate-2012-ae-ae-33",
            "number": 33,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "One eigenvalue of the matrix A = \\begin{bmatrix} 2 & 7 & 10 \\\\ 5 & 2 & 25 \\\\ 1 & 6 & 5 \\end{bmatrix} is – 9.33. One of the other eigenvalues is",
            "options": [
                {"label": "A", "text": "18.33"},
                {"label": "B", "text": "-18.33"},
                {"label": "C", "text": "18.33 - 9.33i"},
                {"label": "D", "text": "18.33 + 9.33i"}
            ],
            "answer": "A"
        },
        # Q34
        {
            "id": "gate-2012-ae-ae-34",
            "number": 34,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "If an aircraft takes off with 10% less fuel in comparison to its standard configuration, its range is",
            "options": [
                {"label": "A", "text": "lower by exactly 10%."},
                {"label": "B", "text": "lower by more than 10%."},
                {"label": "C", "text": "lower by less than 10%."},
                {"label": "D", "text": "an unpredictable quantity."}
            ],
            "answer": "B"
        },
        # Q35 (MTA)
        {
            "id": "gate-2012-ae-ae-35",
            "number": 35,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "An aircraft has an approach speed of 144 kmph with a descent angle of 6.6\u00b0. If the aircraft load factor is 1.2 and constant deceleration at touch down is 0.25g (g = 9.81 m/s^{2}), its total landing distance approximately over a 15 m high obstacle is",
            "options": [
                {"label": "A", "text": "1830 m."},
                {"label": "B", "text": "1380 m."},
                {"label": "C", "text": "830 m."},
                {"label": "D", "text": "380 m."}
            ],
            "answer": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q36
        {
            "id": "gate-2012-ae-ae-36",
            "number": 36,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "An aircraft is trimmed straight and level at true air speed (TAS) of 100 m/s at standard sea level (SSL). Further, pull of 5 N holds the speed at 90 m/s without re-trimming at SSL (air density = 1.22 kg/m^{3}). To fly at 3000 m altitude (air density = 0.91 kg/m^{3}) and 120 m/s TAS without re-trimming, the aircraft needs",
            "options": [
                {"label": "A", "text": "1.95 N upward force."},
                {"label": "B", "text": "1.95 N downward force."},
                {"label": "C", "text": "1.85 N upward force."},
                {"label": "D", "text": "1.75 N downward force."}
            ],
            "answer": "B"
        },
        # Q37
        {
            "id": "gate-2012-ae-ae-37",
            "number": 37,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "An oblique shock wave with a wave angle \u03b2 is generated from a wedge angle of \u03b8. The ratio of the Mach number downstream of the shock to its normal component is",
            "options": [
                {"label": "A", "text": "sin(\u03b2\u2013\u03b8)"},
                {"label": "B", "text": "cos(\u03b2\u2013\u03b8)"},
                {"label": "C", "text": "sin(\u03b8\u2013\u03b2)"},
                {"label": "D", "text": "cos(\u03b8\u2013\u03b2)"}
            ],
            "answer": "A"
        },
        # Q38
        {
            "id": "gate-2012-ae-ae-38",
            "number": 38,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "In a closed-circuit supersonic wind tunnel, the convergent-divergent (C-D) nozzle and test section are followed by a C-D diffuser to swallow the starting shock. Here, we should have the",
            "options": [
                {"label": "A", "text": "diffuser throat larger than the nozzle throat and the shock located just at the diffuser throat."},
                {"label": "B", "text": "diffuser throat larger than the nozzle throat and the shock located downstream of the diffuser throat."},
                {"label": "C", "text": "diffuser throat of the same size as the nozzle throat and the shock located just at the diffuser throat."},
                {"label": "D", "text": "diffuser throat of the same size as the nozzle throat and the shock located downstream of the diffuser throat."}
            ],
            "answer": "B"
        },
        # Q39
        {
            "id": "gate-2012-ae-ae-39",
            "number": 39,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "A vortex flowmeter works on the principle that the Strouhal number of 0.2 is a constant over a wide range of flow rates. If the bluff-body diameter in the flowmeter is 20 mm and the piezo-electric transducer registers the vortex shedding frequency to be 10 Hz, then the velocity of the flow would be measured as",
            "options": [
                {"label": "A", "text": "0.1 m/s"},
                {"label": "B", "text": "1 m/s"},
                {"label": "C", "text": "10 m/s"},
                {"label": "D", "text": "100 m/s"}
            ],
            "answer": "B"
        },
        # Q40
        {
            "id": "gate-2012-ae-ae-40",
            "number": 40,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The stagnation temperatures at the inlet and exit of a combustion chamber are 600 K and 1200 K, respectively. If the heating value of the fuel is 44 MJ/kg and specific heat at constant pressure for air and hot gases are 1.005 kJ/kg.K and 1.147 kJ/kg.K respectively, the fuel-to-air ratio is",
            "options": [
                {"label": "A", "text": "0.0018"},
                {"label": "B", "text": "0.018"},
                {"label": "C", "text": "0.18"},
                {"label": "D", "text": "1.18"}
            ],
            "answer": "B"
        },
        # Q41
        {
            "id": "gate-2012-ae-ae-41",
            "number": 41,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "A solid propellant of density 1800 kg/m^{3} has a burning rate law r = 6.65 \\times 10^{-3}p^{0.45} mm/s, where p is pressure in Pascals. It is used in a rocket motor with a tubular grain with an initial burning area of 0.314 m^{2}. The characteristic velocity is 1450 m/s. What should be the nozzle throat diameter to achieve an equilibrium chamber pressure of 50 bar at the end of the ignition transient?",
            "options": [
                {"label": "A", "text": "35 mm"},
                {"label": "B", "text": "38 mm"},
                {"label": "C", "text": "41 mm"},
                {"label": "D", "text": "45 mm"}
            ],
            "answer": "B"
        },
        # Q42
        {
            "id": "gate-2012-ae-ae-42",
            "number": 42,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "A bipropellant liquid rocket motor operates at a chamber pressure of 40 bar with a nozzle throat diameter of 50 mm. The characteristic velocity is 1540 m/s. If the fuel-oxidizer ratio of the propellant is 1.8, and the fuel density is 900 kg/m^{3}, what should be the minimum fuel tank volume for a burn time of 8 minutes",
            "options": [
                {"label": "A", "text": "1.65 m^{3}"},
                {"label": "B", "text": "1.75 m^{3}"},
                {"label": "C", "text": "1.85 m^{3}"},
                {"label": "D", "text": "1.95 m^{3}"}
            ],
            "answer": "B"
        },
        # Q43
        {
            "id": "gate-2012-ae-ae-43",
            "number": 43,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The propellant in a single stage sounding rocket occupies 60% of its initial mass. If all of it is expended instantaneously at an equivalent exhaust velocity of 3000 m/s, what would be the altitude attained by the payload when launched vertically?\n[Neglect drag and assume acceleration due to gravity to be constant at 9.81 m/s^{2}.]",
            "options": [
                {"label": "A", "text": "315 km"},
                {"label": "B", "text": "335 km"},
                {"label": "C", "text": "365 km"},
                {"label": "D", "text": "385 km"}
            ],
            "answer": "D"
        },
        # Q44
        {
            "id": "gate-2012-ae-ae-44",
            "number": 44,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The Airy stress function, \\phi = \\alpha x^{2} + \\beta xy + \\gamma y^{2} for a thin square panel of size l \\times l automatically satisfies compatibility. If the panel is subjected to uniform tensile stress, \\sigma_{o} on all four edges, the traction boundary conditions are satisfied by",
            "options": [
                {"label": "A", "text": "\\alpha = \\sigma_{o}/2; \\beta = 0; \\gamma = \\sigma_{o}/2."},
                {"label": "B", "text": "\\alpha = \\sigma_{o}; \\beta = 0; \\gamma = \\sigma_{o}."},
                {"label": "C", "text": "\\alpha = 0; \\beta = \\sigma_{o}/4; \\gamma = 0."},
                {"label": "D", "text": "\\alpha = 0; \\beta = \\sigma_{o}/2; \\gamma = 0."}
            ],
            "answer": "A"
        },
        # Q45
        {
            "id": "gate-2012-ae-ae-45",
            "number": 45,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The boundary condition of a rod under longitudinal vibration is changed from fixed-fixed to fixed-free. The fundamental natural frequency of the rod is now k times the original frequency, where k is",
            "options": [
                {"label": "A", "text": "\\frac{1}{2}"},
                {"label": "B", "text": "2"},
                {"label": "C", "text": "\\frac{1}{\\sqrt{2}}"},
                {"label": "D", "text": "\\sqrt{2}"}
            ],
            "answer": "A"
        },
        # Q46
        {
            "id": "gate-2012-ae-ae-46",
            "number": 46,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "A spring-mass system is viscously damped with a viscous damping constant c. The energy dissipated per cycle when the system is undergoing a harmonic vibration X \\cos \\omega_{d} t is given by",
            "options": [
                {"label": "A", "text": "\\pi c \\omega_{d} X^{2}"},
                {"label": "B", "text": "\\pi \\omega_{d} X^{2}"},
                {"label": "C", "text": "\\pi c \\omega_{d} X"},
                {"label": "D", "text": "\\pi c \\omega_{d}^{2} X"}
            ],
            "answer": "A"
        },
        # Q47
        {
            "id": "gate-2012-ae-ae-47",
            "number": 47,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "Buckling of the fuselage skin can be delayed by",
            "options": [
                {"label": "A", "text": "increasing internal pressure."},
                {"label": "B", "text": "placing stiffeners farther apart."},
                {"label": "C", "text": "reducing skin thickness."},
                {"label": "D", "text": "placing stiffeners farther and decreasing internal pressure."}
            ],
            "answer": "A"
        },
        # Q48 (CD)
        {
            "id": "gate-2012-ae-ae-48",
            "number": 48,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "common-data-48-49",
            "groupType": "common-data",
            "groupContext": cd_48_49_ctx,
            "question": "The maximum distance that the centre of gravity can be behind aerodynamic centre without destabilizing the wing-tail combination is",
            "options": [
                {"label": "A", "text": "0.4 m"},
                {"label": "B", "text": "1.4 m"},
                {"label": "C", "text": "2.4 m"},
                {"label": "D", "text": "3.4 m"}
            ],
            "answer": "B"
        },
        # Q49 (CD)
        {
            "id": "gate-2012-ae-ae-49",
            "number": 49,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "common-data-48-49",
            "groupType": "common-data",
            "groupContext": cd_48_49_ctx,
            "question": "The angle of incidence of tail to trim the wing-tail combination for a 5% static margin is",
            "options": [
                {"label": "A", "text": "-1.4\u00b0"},
                {"label": "B", "text": "-0.4\u00b0"},
                {"label": "C", "text": "0.4\u00b0"},
                {"label": "D", "text": "1.4\u00b0"}
            ],
            "answer": "A"
        },
        # Q50 (CD)
        {
            "id": "gate-2012-ae-ae-50",
            "number": 50,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "common-data-50-51",
            "groupType": "common-data",
            "groupContext": cd_50_51_ctx,
            "question": "What is the radial component of the fluid’s velocity at a radial location 0.5 m from the pipe axis?",
            "options": [
                {"label": "A", "text": "0.01 m/s"},
                {"label": "B", "text": "0.1 m/s"},
                {"label": "C", "text": "1 m/s"},
                {"label": "D", "text": "10 m/s"}
            ],
            "answer": "A"
        },
        # Q51 (CD, MTA)
        {
            "id": "gate-2012-ae-ae-51",
            "number": 51,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "common-data-50-51",
            "groupType": "common-data",
            "groupContext": cd_50_51_ctx,
            "question": "What is the tangential component of the fluid’s velocity at the same radial location as above?",
            "options": [
                {"label": "A", "text": "0.01 m/s"},
                {"label": "B", "text": "0.03 m/s"},
                {"label": "C", "text": "0.10 m/s"},
                {"label": "D", "text": "0.31 m/s"}
            ],
            "answer": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q52 (LA, MTA)
        {
            "id": "gate-2012-ae-ae-52",
            "number": 52,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "linked-answer-52-53",
            "groupType": "linked-answer",
            "groupContext": la_52_53_ctx,
            "question": "The blade angle at the inlet of the rotor is",
            "options": [
                {"label": "A", "text": "25.5\u00b0"},
                {"label": "B", "text": "38.5\u00b0"},
                {"label": "C", "text": "48.5\u00b0"},
                {"label": "D", "text": "59.5\u00b0"}
            ],
            "answer": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q53 (LA, MTA)
        {
            "id": "gate-2012-ae-ae-53",
            "number": 53,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "linked-answer-52-53",
            "groupType": "linked-answer",
            "groupContext": la_52_53_ctx,
            "question": "If the mass flow rate is 1 kg/s, the power required to drive the compressor is",
            "options": [
                {"label": "A", "text": "50.5 kW"},
                {"label": "B", "text": "40.5 kW"},
                {"label": "C", "text": "30.5 kW"},
                {"label": "D", "text": "20.5 kW"}
            ],
            "answer": "MTA",
            "gradingRule": "marks-to-all",
            "officialKey": "MTA"
        },
        # Q54 (LA)
        {
            "id": "gate-2012-ae-ae-54",
            "number": 54,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "linked-answer-54-55",
            "groupType": "linked-answer",
            "groupContext": la_54_55_ctx,
            "question": "The internal pressure p_{Y} at yield, based on the von Mises yield criterion, if the vessel is floating in space, is approximately",
            "options": [
                {"label": "A", "text": "500 MPa"},
                {"label": "B", "text": "250 MPa"},
                {"label": "C", "text": "100 MPa"},
                {"label": "D", "text": "20 MPa"}
            ],
            "answer": "D"
        },
        # Q55 (LA)
        {
            "id": "gate-2012-ae-ae-55",
            "number": 55,
            "year": 2012,
            "paper": "AE",
            "section": "AE",
            "subject": "Aerospace Engineering",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "group": "linked-answer-54-55",
            "groupType": "linked-answer",
            "groupContext": la_54_55_ctx,
            "question": "If the vessel is evacuated (internal pressure = 0) and subjected to external pressure, yielding according to the von Mises yield criterion (assuming elastic stability until yield)",
            "options": [
                {"label": "A", "text": "occurs at about half the pressure p_{Y}."},
                {"label": "B", "text": "occurs at about double the pressure p_{Y}."},
                {"label": "C", "text": "occurs at about the same pressure p_{Y}."},
                {"label": "D", "text": "never occurs."}
            ],
            "answer": "C"
        },
        # Q56 (GA)
        {
            "id": "gate-2012-ae-ga-56",
            "number": 56,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nI ___ to have bought a diamond ring.",
            "options": [
                {"label": "A", "text": "have a liking"},
                {"label": "B", "text": "should have liked"},
                {"label": "C", "text": "would like"},
                {"label": "D", "text": "may like"}
            ],
            "answer": "C"
        },
        # Q57 (GA)
        {
            "id": "gate-2012-ae-ga-57",
            "number": 57,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nFood prices ___ again this month.",
            "options": [
                {"label": "A", "text": "have raised"},
                {"label": "B", "text": "have been raising"},
                {"label": "C", "text": "have been rising"},
                {"label": "D", "text": "have arose"}
            ],
            "answer": "C"
        },
        # Q58 (GA)
        {
            "id": "gate-2012-ae-ga-58",
            "number": 58,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nThe administrators went on to implement yet another unreasonable measure, arguing that the measures were already ___ and one more would hardly make a difference.",
            "options": [
                {"label": "A", "text": "reflective"},
                {"label": "B", "text": "utopian"},
                {"label": "C", "text": "luxuriant"},
                {"label": "D", "text": "unpopular"}
            ],
            "answer": "D"
        },
        # Q59 (GA)
        {
            "id": "gate-2012-ae-ga-59",
            "number": 59,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "Choose the most appropriate alternative from the options given below to complete the following sentence:\n\nTo those of us who had always thought him timid, his ___ came as a surprise.",
            "options": [
                {"label": "A", "text": "intrepidity"},
                {"label": "B", "text": "inevitability"},
                {"label": "C", "text": "inability"},
                {"label": "D", "text": "inertness"}
            ],
            "answer": "A"
        },
        # Q60 (GA)
        {
            "id": "gate-2012-ae-ga-60",
            "number": 60,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 1,
            "negativeMarks": 0.3333333333333333,
            "question": "The arithmetic mean of five different natural numbers is 12. The largest possible value among the numbers is",
            "options": [
                {"label": "A", "text": "12"},
                {"label": "B", "text": "40"},
                {"label": "C", "text": "50"},
                {"label": "D", "text": "60"}
            ],
            "answer": "C"
        },
        # Q61 (GA)
        {
            "id": "gate-2012-ae-ga-61",
            "number": 61,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "Two policemen, A and B, fire once each at the same time at an escaping convict. The probability that A hits the convict is three times the probability that B hits the convict. If the probability of the convict not getting injured is 0.5, the probability that B hits the convict is",
            "options": [
                {"label": "A", "text": "0.14"},
                {"label": "B", "text": "0.22"},
                {"label": "C", "text": "0.33"},
                {"label": "D", "text": "0.40"}
            ],
            "answer": "A"
        },
        # Q62 (GA)
        {
            "id": "gate-2012-ae-ga-62",
            "number": 62,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "The total runs scored by four cricketers P, Q, R, and S in years 2009 and 2010 are given in the following table:\n\n| Player | 2009 | 2010 |\n| :--- | :--- | :--- |\n| P | 802 | 1008 |\n| Q | 765 | 912 |\n| R | 429 | 619 |\n| S | 501 | 701 |\n\nThe player with the lowest percentage increase in total runs is",
            "options": [
                {"label": "A", "text": "P"},
                {"label": "B", "text": "Q"},
                {"label": "C", "text": "R"},
                {"label": "D", "text": "S"}
            ],
            "answer": "B"
        },
        # Q63 (GA)
        {
            "id": "gate-2012-ae-ga-63",
            "number": 63,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "If a prime number on division by 4 gives a remainder of 1, then that number can be expressed as",
            "options": [
                {"label": "A", "text": "sum of squares of two natural numbers"},
                {"label": "B", "text": "sum of cubes of two natural numbers"},
                {"label": "C", "text": "sum of square roots of two natural numbers"},
                {"label": "D", "text": "sum of cube roots of two natural numbers"}
            ],
            "answer": "A"
        },
        # Q64 (GA)
        {
            "id": "gate-2012-ae-ga-64",
            "number": 64,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "Two points (4, p) and (0, q) lie on a straight line having a slope of 3/4. The value of (p – q) is",
            "options": [
                {"label": "A", "text": "-3"},
                {"label": "B", "text": "0"},
                {"label": "C", "text": "3"},
                {"label": "D", "text": "4"}
            ],
            "answer": "C"
        },
        # Q65 (GA)
        {
            "id": "gate-2012-ae-ga-65",
            "number": 65,
            "year": 2012,
            "paper": "AE",
            "section": "GA",
            "subject": "General Aptitude",
            "type": "MCQ",
            "marks": 2,
            "negativeMarks": 0.6666666666666666,
            "question": "In the early nineteenth century, theories of social evolution were inspired less by Biology than by the conviction of social scientists that there was a growing improvement in social institutions. Progress was taken for granted and social scientists attempted to discover its laws and phases.\n\nWhich one of the following inferences may be drawn with the greatest accuracy from the above passage?\n\nSocial scientists",
            "options": [
                {"label": "A", "text": "did not question that progress was a fact."},
                {"label": "B", "text": "did not approve of Biology."},
                {"label": "C", "text": "framed the laws of progress."},
                {"label": "D", "text": "emphasized Biology over Social Sciences."}
            ],
            "answer": "A"
        }
    ]

    ae_q_ids = [f"gate-2012-ae-ae-{i:02d}" for i in range(1, 56)]
    ga_q_ids = [f"gate-2012-ae-ga-{i:02d}" for i in range(56, 66)]
    all_q_ids = ae_q_ids + ga_q_ids

    question_refs = []
    for q in q_list:
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
            "context": cd_48_49_ctx,
            "questionIds": ["gate-2012-ae-ae-48", "gate-2012-ae-ae-49"]
        },
        {
            "id": "common-data-50-51",
            "type": "common-data",
            "title": "Common Data for Questions 50 and 51",
            "context": cd_50_51_ctx,
            "questionIds": ["gate-2012-ae-ae-50", "gate-2012-ae-ae-51"]
        },
        {
            "id": "linked-answer-52-53",
            "type": "linked-answer",
            "title": "Statement for Linked Answer Questions 52 and 53",
            "context": la_52_53_ctx,
            "questionIds": ["gate-2012-ae-ae-52", "gate-2012-ae-ae-53"]
        },
        {
            "id": "linked-answer-54-55",
            "type": "linked-answer",
            "title": "Statement for Linked Answer Questions 54 and 55",
            "context": la_54_55_ctx,
            "questionIds": ["gate-2012-ae-ae-54", "gate-2012-ae-ae-55"]
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
            "sha256": "e4dabbfe9f0dddc2fddcb095b33335f54774d610e9071dd5d5222c9063afc07c",
            "pageCount": 10
        },
        "questions": q_list
    }

    with open('data/ae/2012.json', 'w', encoding='utf-8') as f:
        json.dump(paper, f, indent=2, ensure_ascii=False)

    print('Successfully generated data/ae/2012.json conforming to full schema')

build_paper()
