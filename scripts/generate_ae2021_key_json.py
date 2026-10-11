import json
import hashlib

pdf_path = "internal/ae/AE2021-key.pdf"
with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

# Parsed from internal/ae/AE2021-key.pdf
# GA Q1-10
ga_rows = [
    (1, 2, "MCQ", "GA", "B", 1),
    (2, 2, "MCQ", "GA", "B", 1),
    (3, 2, "MCQ", "GA", "D", 1),
    (4, 2, "MCQ", "GA", "D", 1),
    (5, 2, "MCQ", "GA", "C", 1),
    (6, 2, "MCQ", "GA", "C", 2),
    (7, 2, "MCQ", "GA", "A", 2),
    (8, 2, "MCQ", "GA", "B", 2),
    (9, 2, "MCQ", "GA", "C", 2),
    (10, 2, "MCQ", "GA", "D", 2),
]

# AE Q1-55
ae_rows = [
    (1, 2, "MCQ", "AE", "D", 1),
    (2, 2, "MCQ", "AE", "B", 1),
    (3, 2, "MCQ", "AE", "B", 1),
    (4, 2, "MCQ", "AE", "A", 1),
    (5, 2, "MCQ", "AE", "B", 1),
    (6, 2, "MCQ", "AE", "A", 1),
    (7, 2, "MCQ", "AE", "D", 1),
    (8, 2, "MCQ", "AE", "C", 1),
    (9, 2, "MCQ", "AE", "D", 1),
    (10, 2, "MCQ", "AE", "B", 1),
    (11, 2, "MCQ", "AE", "D", 1),
    (12, 2, "MCQ", "AE", "C", 1),
    (13, 2, "MCQ", "AE", "B", 1),
    (14, 2, "MSQ", "AE", "A; B; C", 1),
    (15, 2, "MSQ", "AE", "A; B; D", 1),
    (16, 2, "MSQ", "AE", "A; B", 1),
    (17, 2, "NAT", "AE", "0 to 0", 1),
    (18, 2, "NAT", "AE", "0.02 to 0.03", 1),
    (19, 2, "NAT", "AE", "264 to 264 OR 833 to 835", 1),
    (20, 2, "NAT", "AE", "4 to 4", 1),
    (21, 2, "NAT", "AE", "0 to 0", 1),
    (22, 2, "NAT", "AE", "0.2 to 0.2", 1),
    (23, 2, "NAT", "AE", "64.30 to 64.60", 1),
    (24, 2, "NAT", "AE", "6.50 to 6.60", 1),
    (25, 2, "NAT", "AE", "7.75 to 7.77 OR 7750.00 to 7770.00", 1),
    (26, 2, "MCQ", "AE", "A", 2),
    (27, 2, "MCQ", "AE", "C", 2),
    (28, 2, "MCQ", "AE", "B", 2),
    (29, 2, "MCQ", "AE", "C", 2),
    (30, 2, "MCQ", "AE", "D", 2),
    (31, 2, "MSQ", "AE", "B; D", 2),
    (32, 2, "MSQ", "AE", "B; C", 2),
    (33, 2, "MSQ", "AE", "D", 2),
    (34, 2, "MSQ", "AE", "A; C; D", 2),
    (35, 2, "MSQ", "AE", "B; C; D", 2),
    (36, 2, "MSQ", "AE", "A; D", 2),
    (37, 2, "NAT", "AE", "8 to 8", 2),
    (38, 2, "NAT", "AE", "0.66 to 0.68", 2),
    (39, 2, "NAT", "AE", "0.41 to 0.43", 2),
    (40, 2, "NAT", "AE", "98.0 to 98.5", 2),
    (41, 2, "NAT", "AE", "0.005 to 0.009", 2),
    (42, 2, "NAT", "AE", "4.8 to 5.2", 2),
    (43, 2, "NAT", "AE", "605 to 607", 2),
    (44, 2, "NAT", "AE", "216 to 220", 2),
    (45, 2, "NAT", "AE", "20 to 22", 2),
    (46, 2, "NAT", "AE", "274 to 282", 2),
    (47, 2, "NAT", "AE", "18.0 to 19.5", 2),
    (48, 2, "NAT", "AE", "2.35 to 2.50", 2),
    (49, 2, "NAT", "AE", "14.0 to 16.0", 2),
    (50, 2, "NAT", "AE", "2.1 to 2.5", 2),
    (51, 2, "NAT", "AE", "2.2 to 2.6", 2),
    (52, 2, "NAT", "AE", "232 to 238", 2),
    (53, 2, "NAT", "AE", "14.8 to 15.2", 2),
    (54, 2, "NAT", "AE", "9787 to 9795", 2),
    (55, 2, "NAT", "AE", "-0.025 to -0.023", 2),
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
    "year": 2021,
    "paper": "AE",
    "source": "internal/ae/AE2021-key.pdf",
    "sha256": pdf_sha256,
    "totalQuestions": len(all_rows),
    "totalMarks": sum(r["marks"] for r in all_rows),
    "rows": all_rows
}

with open("internal/ae/AE2021-key.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Generated internal/ae/AE2021-key.json with {len(all_rows)} rows and {data['totalMarks']} marks.")
