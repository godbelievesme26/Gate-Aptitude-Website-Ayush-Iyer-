import json
import hashlib

key_rows = [
    {"number": 1, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "B", "marks": 1},
    {"number": 2, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "C", "marks": 1},
    {"number": 3, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "C", "marks": 1},
    {"number": 4, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "A", "marks": 1},
    {"number": 5, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "B;C", "marks": 1},
    {"number": 6, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "C", "marks": 2},
    {"number": 7, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "C", "marks": 2},
    {"number": 8, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "A", "marks": 2},
    {"number": 9, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "A", "marks": 2},
    {"number": 10, "session": 8, "type": "MCQ", "section": "GA", "rawKey": "B", "marks": 2},
    {"number": 11, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 1},
    {"number": 12, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "D", "marks": 1},
    {"number": 13, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 14, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 1},
    {"number": 15, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 1},
    {"number": 16, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 17, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 18, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "D", "marks": 1},
    {"number": 19, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "A", "marks": 1},
    {"number": 20, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 21, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 22, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "A", "marks": 1},
    {"number": 23, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 1},
    {"number": 24, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;C", "marks": 1},
    {"number": 25, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;D", "marks": 1},
    {"number": 26, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;C", "marks": 1},
    {"number": 27, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "A;D", "marks": 1},
    {"number": 28, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;C", "marks": 1},
    {"number": 29, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "A;C;D", "marks": 1},
    {"number": 30, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;C;D", "marks": 1},
    {"number": 31, "session": 8, "type": "NAT", "section": "AE", "rawKey": "8.6 to 9.1", "marks": 1},
    {"number": 32, "session": 8, "type": "NAT", "section": "AE", "rawKey": "5.55 to 5.80", "marks": 1},
    {"number": 33, "session": 8, "type": "NAT", "section": "AE", "rawKey": "109 to 111", "marks": 1},
    {"number": 34, "session": 8, "type": "NAT", "section": "AE", "rawKey": "5.7 to 6.0", "marks": 1},
    {"number": 35, "session": 8, "type": "NAT", "section": "AE", "rawKey": "51.5 to 52.6", "marks": 1},
    {"number": 36, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 2},
    {"number": 37, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 2},
    {"number": 38, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 2},
    {"number": 39, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 2},
    {"number": 40, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 2},
    {"number": 41, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "C", "marks": 2},
    {"number": 42, "session": 8, "type": "MCQ", "section": "AE", "rawKey": "B", "marks": 2},
    {"number": 43, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "A;B", "marks": 2},
    {"number": 44, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "A;C", "marks": 2},
    {"number": 45, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "A", "marks": 2},
    {"number": 46, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;C;D", "marks": 2},
    {"number": 47, "session": 8, "type": "MSQ", "section": "AE", "rawKey": "B;D", "marks": 2},
    {"number": 48, "session": 8, "type": "NAT", "section": "AE", "rawKey": "7.4 to 7.7", "marks": 2},
    {"number": 49, "session": 8, "type": "NAT", "section": "AE", "rawKey": "2", "marks": 2},
    {"number": 50, "session": 8, "type": "NAT", "section": "AE", "rawKey": "88 to 91", "marks": 2},
    {"number": 51, "session": 8, "type": "NAT", "section": "AE", "rawKey": "9500 to 9800", "marks": 2},
    {"number": 52, "session": 8, "type": "NAT", "section": "AE", "rawKey": "1.24 to 1.28", "marks": 2},
    {"number": 53, "session": 8, "type": "NAT", "section": "AE", "rawKey": "0.14 to 0.15", "marks": 2},
    {"number": 54, "session": 8, "type": "NAT", "section": "AE", "rawKey": "-0.057 to -0.053", "marks": 2},
    {"number": 55, "session": 8, "type": "NAT", "section": "AE", "rawKey": "49 to 51 OR -51 to -49", "marks": 2},
    {"number": 56, "session": 8, "type": "NAT", "section": "AE", "rawKey": "44 to 46", "marks": 2},
    {"number": 57, "session": 8, "type": "NAT", "section": "AE", "rawKey": "2.6 to 2.7", "marks": 2},
    {"number": 58, "session": 8, "type": "NAT", "section": "AE", "rawKey": "43 to 48", "marks": 2},
    {"number": 59, "session": 8, "type": "NAT", "section": "AE", "rawKey": "1", "marks": 2},
    {"number": 60, "session": 8, "type": "NAT", "section": "AE", "rawKey": "0.95 to 1.05", "marks": 2},
    {"number": 61, "session": 8, "type": "NAT", "section": "AE", "rawKey": "2700 to 2960", "marks": 2},
    {"number": 62, "session": 8, "type": "NAT", "section": "AE", "rawKey": "19 to 21", "marks": 2},
    {"number": 63, "session": 8, "type": "NAT", "section": "AE", "rawKey": "1.7 to 1.8", "marks": 2},
    {"number": 64, "session": 8, "type": "NAT", "section": "AE", "rawKey": "545 to 555", "marks": 2},
    {"number": 65, "session": 8, "type": "NAT", "section": "AE", "rawKey": "6 to 6", "marks": 2}
]

with open('internal/ae/AE2022-key.pdf', 'rb') as f:
    key_sha256 = hashlib.sha256(f.read()).hexdigest()

key_doc = {
    "exam": "GATE",
    "year": 2022,
    "paper": "AE",
    "source": "internal/ae/AE2022-key.pdf",
    "sha256": key_sha256,
    "totalQuestions": 65,
    "totalMarks": 100,
    "rows": key_rows
}

with open('internal/ae/AE2022-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_doc, f, indent=2)

print("Created internal/ae/AE2022-key.json")
