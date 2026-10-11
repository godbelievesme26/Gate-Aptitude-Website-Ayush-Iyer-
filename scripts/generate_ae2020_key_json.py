import json
import hashlib

pdf_path = "internal/ae/AE2020-key.pdf"
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

ga_rows = [
    (1, 4, "MCQ", "GA", "A", 1),
    (2, 4, "MCQ", "GA", "B", 1),
    (3, 4, "MCQ", "GA", "B", 1),
    (4, 4, "MCQ", "GA", "C", 1),
    (5, 4, "MCQ", "GA", "A", 1),
    (6, 4, "MCQ", "GA", "A", 2),
    (7, 4, "MCQ", "GA", "B", 2),
    (8, 4, "MCQ", "GA", "C", 2),
    (9, 4, "MCQ", "GA", "C", 2),
    (10, 4, "MCQ", "GA", "B", 2),
]

ae_rows = [
    (1, 4, "MCQ", "AE", "C", 1),
    (2, 4, "MCQ", "AE", "D", 1),
    (3, 4, "MCQ", "AE", "A", 1),
    (4, 4, "MCQ", "AE", "C", 1),
    (5, 4, "MCQ", "AE", "D", 1),
    (6, 4, "MCQ", "AE", "C", 1),
    (7, 4, "MCQ", "AE", "B", 1),
    (8, 4, "MCQ", "AE", "C", 1),
    (9, 4, "MCQ", "AE", "B", 1),
    (10, 4, "MCQ", "AE", "D", 1),
    (11, 4, "MCQ", "AE", "A", 1),
    (12, 4, "MCQ", "AE", "A", 1),
    (13, 4, "MCQ", "AE", "C", 1),
    (14, 4, "MCQ", "AE", "B", 1),
    (15, 4, "MCQ", "AE", "C", 1),
    (16, 4, "MCQ", "AE", "D", 1),
    (17, 4, "MCQ", "AE", "C", 1),
    (18, 4, "MCQ", "AE", "A", 1),
    (19, 4, "MCQ", "AE", "B", 1),
    (20, 4, "NAT", "AE", "13.42 to 13.47", 1),
    (21, 4, "NAT", "AE", "-5.62 to -5.57", 1),
    (22, 4, "NAT", "AE", "1.9 to 2.1", 1),
    (23, 4, "NAT", "AE", "29.8 to 30.0", 1),
    (24, 4, "NAT", "AE", "0.009 to 0.011", 1),
    (25, 4, "NAT", "AE", "3.50 to 3.60", 1),
    (26, 4, "MCQ", "AE", "C", 2),
    (27, 4, "MCQ", "AE", "D", 2),
    (28, 4, "MCQ", "AE", "D", 2),
    (29, 4, "MCQ", "AE", "C", 2),
    (30, 4, "MCQ", "AE", "D", 2),
    (31, 4, "MCQ", "AE", "C", 2),
    (32, 4, "MCQ", "AE", "A", 2),
    (33, 4, "MCQ", "AE", "B", 2),
    (34, 4, "MCQ", "AE", "B", 2),
    (35, 4, "NAT", "AE", "0.9 to 1.1", 2),
    (36, 4, "NAT", "AE", "0.010 to 0.012", 2),
    (37, 4, "NAT", "AE", "0.92 to 0.94", 2),
    (38, 4, "NAT", "AE", "0.009 to 0.011", 2),
    (39, 4, "NAT", "AE", "1.9 to 2.1", 2),
    (40, 4, "NAT", "AE", "4.00 to 4.20", 2),
    (41, 4, "NAT", "AE", "1.29 to 1.38", 2),
    (42, 4, "NAT", "AE", "3.55 to 3.58", 2),
    (43, 4, "NAT", "AE", "0.016 to 0.018", 2),
    (44, 4, "NAT", "AE", "55.20 to 55.33", 2),
    (45, 4, "NAT", "AE", "25.60 to 25.70", 2),
    (46, 4, "NAT", "AE", "149.0 to 151.0", 2),
    (47, 4, "NAT", "AE", "1712.0 to 1719.0", 2),
    (48, 4, "NAT", "AE", "91 to 93", 2),
    (49, 4, "NAT", "AE", "87 to 89", 2),
    (50, 4, "NAT", "AE", "27.0 to 27.2", 2),
    (51, 4, "NAT", "AE", "1.43 to 1.45", 2),
    (52, 4, "NAT", "AE", "0.61 to 0.63", 2),
    (53, 4, "NAT", "AE", "3.74 to 3.76", 2),
    (54, 4, "NAT", "AE", "62.95 to 63.08", 2),
    (55, 4, "NAT", "AE", "57.10 to 60.00", 2),
]

all_rows = []
for r in ga_rows:
    all_rows.append({
        "number": r[0],
        "session": r[1],
        "type": r[2],
        "section": r[3],
        "rawKey": r[4],
        "marks": r[5]
    })

for r in ae_rows:
    all_rows.append({
        "number": r[0] + 10,
        "session": r[1],
        "type": r[2],
        "section": r[3],
        "rawKey": r[4],
        "marks": r[5]
    })

data = {
    "exam": "GATE",
    "year": 2020,
    "paper": "AE",
    "source": "internal/ae/AE2020-key.pdf",
    "sha256": pdf_sha256,
    "totalQuestions": len(all_rows),
    "totalMarks": sum(r["marks"] for r in all_rows),
    "rows": all_rows
}

with open("internal/ae/AE2020-key.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Generated internal/ae/AE2020-key.json with {len(all_rows)} rows and {data['totalMarks']} marks.")
