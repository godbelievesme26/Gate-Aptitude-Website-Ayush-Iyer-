import sys
import os
import json
import hashlib
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'AE PYQ Papers/AE2024.pdf'
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

doc = fitz.open(pdf_path)

# Official Answer Key & Types & Marks
official_answers = {
    1: {"type": "MCQ", "section": "GA", "marks": 1, "answer": "A"},
    2: {"type": "MCQ", "section": "GA", "marks": 1, "answer": "D"},
    3: {"type": "MCQ", "section": "GA", "marks": 1, "answer": "A"},
    4: {"type": "MCQ", "section": "GA", "marks": 1, "answer": "C"},
    5: {"type": "MCQ", "section": "GA", "marks": 1, "answer": "A"},
    6: {"type": "MCQ", "section": "GA", "marks": 2, "answer": "C"},
    7: {"type": "MCQ", "section": "GA", "marks": 2, "answer": "A"},
    8: {"type": "MCQ", "section": "GA", "marks": 2, "answer": "C"},
    9: {"type": "MCQ", "section": "GA", "marks": 2, "answer": "A"},
    10: {"type": "MCQ", "section": "GA", "marks": 2, "answer": "A"},
    11: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    12: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    13: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    14: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "C"},
    15: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    16: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    17: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    18: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "C"},
    19: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "A"},
    20: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "D"},
    21: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "B"},
    22: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "B"},
    23: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "C"},
    24: {"type": "MCQ", "section": "AE", "marks": 1, "answer": "C"},
    25: {"type": "MSQ", "section": "AE", "marks": 1, "answer": ["B", "C", "D"]},
    26: {"type": "MSQ", "section": "AE", "marks": 1, "answer": ["A", "B"]},
    27: {"type": "MSQ", "section": "AE", "marks": 1, "answer": ["A", "B", "C"]},
    28: {"type": "MSQ", "section": "AE", "marks": 1, "answer": ["A", "B", "D"]},
    29: {"type": "NAT", "section": "AE", "marks": 1, "answer": [0.24, 0.26]},
    30: {"type": "NAT", "section": "AE", "marks": 1, "answer": 24},
    31: {"type": "NAT", "section": "AE", "marks": 1, "answer": 0.35},
    32: {"type": "NAT", "section": "AE", "marks": 1, "answer": 0},
    33: {"type": "NAT", "section": "AE", "marks": 1, "answer": 1.5},
    34: {"type": "NAT", "section": "AE", "marks": 1, "answer": 75000},
    35: {"type": "NAT", "section": "AE", "marks": 1, "answer": [0.54, 0.56]},
    36: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "A"},
    37: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "B"},
    38: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "D"},
    39: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "B"},
    40: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "A"},
    41: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "A"},
    42: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "D"},
    43: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "D"},
    44: {"type": "MCQ", "section": "AE", "marks": 2, "answer": "D"},
    45: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "B", "C"]},
    46: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "B"]},
    47: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "B"]},
    48: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "B", "C"]},
    49: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "C"]},
    50: {"type": "MSQ", "section": "AE", "marks": 2, "answer": ["A", "C"]},
    51: {"type": "NAT", "section": "AE", "marks": 2, "answer": [1.4, 1.6]},
    52: {"type": "NAT", "section": "AE", "marks": 2, "answer": 0},
    53: {"type": "NAT", "section": "AE", "marks": 2, "answer": [141.0, 141.5]},
    54: {"type": "NAT", "section": "AE", "marks": 2, "answer": [14900, 15100]},
    55: {"type": "NAT", "section": "AE", "marks": 2, "answer": [1.72, 1.74]},
    56: {"type": "NAT", "section": "AE", "marks": 2, "answer": [4.9, 5.1]},
    57: {"type": "NAT", "section": "AE", "marks": 2, "answer": [2500, 2600]},
    58: {"type": "NAT", "section": "AE", "marks": 2, "answer": [230, 240]},
    59: {"type": "NAT", "section": "AE", "marks": 2, "answer": [227.0, 231.0]},
    60: {"type": "NAT", "section": "AE", "marks": 2, "answer": [1.05, 1.07]},
    61: {"type": "NAT", "section": "AE", "marks": 2, "answer": [0.80, 0.84]},
    62: {"type": "NAT", "section": "AE", "marks": 2, "answer": [17.7, 17.9]},
    63: {"type": "NAT", "section": "AE", "marks": 2, "answer": [0.018, 0.022]},
    64: {"type": "NAT", "section": "AE", "marks": 2, "answer": [63.0, 64.5]},
    65: {"type": "NAT", "section": "AE", "marks": 2, "answer": 1.0}
}

# Figure Asset Details mapping
figure_metadata = {
    8: [{"src": "figures/gate-2024-ae-ga-08-figure-1.png", "alt": "Pie chart of macronutrient energy contribution: Carbohydrates 35%, Proteins 20%, Unsaturated fat 20%, Saturated fat 20%, Trans fat 5%.", "page": 6}],
    10: [{"src": "figures/gate-2024-ae-ga-10-figure-1.png", "alt": "Grid of squares with horizontal line AB and symmetric arrangement.", "page": 7}],
    14: [{"src": "figures/gate-2024-ae-ae-14-figure-1.png", "alt": "Free vibration response time histories P, Q, R, S.", "page": 11}],
    18: [{"src": "figures/gate-2024-ae-ae-18-figure-1.png", "alt": "Pressure vs specific volume (p-v) diagram with processes 1, 2, 3, 4.", "page": 14}],
    23: [{"src": "figures/gate-2024-ae-ae-23-figure-1.png", "alt": "Supersonic flow over wedge and expansion corner with waves 1, 2, 3.", "page": 18}],
    24: [{"src": "figures/gate-2024-ae-ae-24-figure-1.png", "alt": "Steady flow past two airfoils with flow parameters and distances.", "page": 19}],
    25: [
        {"src": "figures/gate-2024-ae-ae-25-figure-1.png", "alt": "Stress-strain graph for nonlinear elastic material (Option A).", "page": 20},
        {"src": "figures/gate-2024-ae-ae-25-figure-2.png", "alt": "Stress-strain graph for linear elastic material (Option D).", "page": 20}
    ],
    28: [{"src": "figures/gate-2024-ae-ae-28-figure-1.png", "alt": "Pitching moment coefficient vs angle of attack curves P, Q, R.", "page": 22}],
    37: [{"src": "figures/gate-2024-ae-ae-37-figure-1.png", "alt": "Region in first quadrant bounded by y=x and y=x^2 rotated about x-axis.", "page": 25}],
    43: [{"src": "figures/gate-2024-ae-ae-43-figure-1.png", "alt": "Shock structures at Mach numbers M1, M2, M3 over a wedge.", "page": 29}],
    44: [{"src": "figures/gate-2024-ae-ae-44-figure-1.png", "alt": "Prandtl-Meyer expansion fan in supersonic flow through a divergent duct.", "page": 30}],
    46: [{"src": "figures/gate-2024-ae-ae-46-figure-1.png", "alt": "Yield loci for Tresca (hexagon) and von Mises (ellipse) in plane stress.", "page": 32}],
    48: [{"src": "figures/gate-2024-ae-ae-48-figure-1.png", "alt": "Variation of yawing moment coefficient (Cn) with sideslip angle (beta).", "page": 34}],
    52: [{"src": "figures/gate-2024-ae-ae-52-figure-1.png", "alt": "State of stress on infinitesimal element and Mohr circle.", "page": 36}],
    53: [{"src": "figures/gate-2024-ae-ae-53-figure-1.png", "alt": "Pin-jointed plane truss structure under applied load.", "page": 36}],
    54: [{"src": "figures/gate-2024-ae-ae-54-figure-1.png", "alt": "Thin-walled open beam cross section with dimensions.", "page": 37}],
    63: [{"src": "figures/gate-2024-ae-ae-63-figure-1.png", "alt": "Control volume wake deficit profile behind an object in a wind tunnel.", "page": 39}]
}

# Option Figure Mapping
option_figures = {
    20: {
        "A": {"src": "figures/gate-2024-ae-ae-20-option-A.png", "alt": "Drag polar curve option A.", "page": 16},
        "B": {"src": "figures/gate-2024-ae-ae-20-option-B.png", "alt": "Drag polar curve option B.", "page": 16},
        "C": {"src": "figures/gate-2024-ae-ae-20-option-C.png", "alt": "Drag polar curve option C.", "page": 16},
        "D": {"src": "figures/gate-2024-ae-ae-20-option-D.png", "alt": "Drag polar curve option D.", "page": 16}
    }
}

print("Metadata maps defined.")
