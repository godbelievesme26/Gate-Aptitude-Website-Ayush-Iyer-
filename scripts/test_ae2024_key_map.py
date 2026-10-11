import sys
import json
import hashlib
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_sha256 = "7bb1331972521a33ceb9da2afcb465ac7b70b9e24c34eba62675ebda3492b570"
key_pdf_sha256 = "b72803362145330364f9fa4fae41f71f65dbeea5b2d7185ad3d0a681c20573be" # We'll compute exact key sha256

with open('AE PYQ Papers/GATE-Aerospace-2024-Key.pdf', 'rb') as f:
    key_pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

print(f"Key SHA256: {key_pdf_sha256}")

# Official Answer Key for AE 2024
# Q1-Q10: GA
# Q11-Q65: AE
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

print(f"Official answers mapped: {len(official_answers)}")
