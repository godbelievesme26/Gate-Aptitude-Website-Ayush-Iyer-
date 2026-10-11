import json, hashlib

def get_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

key_pdf = "internal/ae/AE2011-key.pdf"
key_hash = get_sha256(key_pdf)

raw_rows = [
    (1, "AE", 1, "MCQ", "D", 1),
    (2, "AE", 2, "MCQ", "D", 1),
    (3, "AE", 3, "MCQ", "A", 1),
    (4, "AE", 4, "MCQ", "B", 1),
    (5, "AE", 5, "MCQ", "C", 1),
    (6, "AE", 6, "MCQ", "C", 1),
    (7, "AE", 7, "MCQ", "A", 1),
    (8, "AE", 8, "MCQ", "B", 1),
    (9, "AE", 9, "MCQ", "A", 1),
    (10, "AE", 10, "MCQ", "D", 1),
    (11, "AE", 11, "MCQ", "A", 1),
    (12, "AE", 12, "MCQ", "C", 1),
    (13, "AE", 13, "MCQ", "A", 1),
    (14, "AE", 14, "MCQ", "B", 1),
    (15, "AE", 15, "MCQ", "B", 1),
    (16, "AE", 16, "MCQ", "D", 1),
    (17, "AE", 17, "MCQ", "C", 1),
    (18, "AE", 18, "MCQ", "A", 1),
    (19, "AE", 19, "MCQ", "C", 1),
    (20, "AE", 20, "MCQ", "D", 1),
    (21, "AE", 21, "MCQ", "C", 1),
    (22, "AE", 22, "MCQ", "C", 1),
    (23, "AE", 23, "MCQ", "C", 1),
    (24, "AE", 24, "MCQ", "C", 1),
    (25, "AE", 25, "MCQ", "C", 1),
    (26, "AE", 26, "NAT", "2.45 to 2.55", 2),
    (27, "AE", 27, "NAT", "1.30 to 1.35", 2),
    (28, "AE", 28, "NAT", "5.95 to 6.05", 2),
    (29, "AE", 29, "NAT", "29 to 32", 2),
    (30, "AE", 30, "NAT", "80 to 82", 2),
    (31, "AE", 31, "MCQ", "A", 2),
    (32, "AE", 32, "MCQ", "C", 2),
    (33, "AE", 33, "MCQ", "D", 2),
    (34, "AE", 34, "MCQ", "C", 2),
    (35, "AE", 35, "MCQ", "B", 2),
    (36, "AE", 36, "MCQ", "B", 2),
    (37, "AE", 37, "MCQ", "C", 2),
    (38, "AE", 38, "MCQ", "A", 2),
    (39, "AE", 39, "MCQ", "C", 2),
    (40, "AE", 40, "MCQ", "C", 2),
    (41, "AE", 41, "MCQ", "A", 2),
    (42, "AE", 42, "MCQ", "A", 2),
    (43, "AE", 43, "MCQ", "C", 2),
    (44, "AE", 44, "MCQ", "C", 2),
    (45, "AE", 45, "MCQ", "B", 2),
    (46, "AE", 46, "MCQ", "A", 2),
    (47, "AE", 47, "MCQ", "C", 2),
    (48, "AE", 48, "MCQ", "D", 2),
    (49, "AE", 49, "MCQ", "C", 2),
    (50, "AE", 50, "MCQ", "D", 2),
    (51, "AE", 51, "MCQ", "A", 2),
    (52, "AE", 52, "MCQ", "B", 2),
    (53, "AE", 53, "MCQ", "D", 2),
    (54, "AE", 54, "MCQ", "B", 2),
    (55, "AE", 55, "MCQ", "A", 2),
    (56, "GA", 1, "MCQ", "D", 1),
    (57, "GA", 2, "MCQ", "B", 1),
    (58, "GA", 3, "MCQ", "A", 1),
    (59, "GA", 4, "MCQ", "C", 1),
    (60, "GA", 5, "MCQ", "C", 1),
    (61, "GA", 6, "MCQ", "B", 2),
    (62, "GA", 7, "MCQ", "C", 2),
    (63, "GA", 8, "MCQ", "A", 2),
    (64, "GA", 9, "MCQ", "B", 2),
    (65, "GA", 10, "MCQ", "D", 2),
]

rows = []
for num, sec, sec_num, qtype, raw_key, marks in raw_rows:
    rows.append({
        "number": num,
        "section": sec,
        "sectionQuestionNumber": sec_num,
        "type": qtype,
        "rawKey": raw_key,
        "marks": marks
    })

key_json = {
    "exam": "GATE",
    "year": 2011,
    "paper": "AE",
    "source": key_pdf,
    "sha256": key_hash,
    "totalQuestions": 65,
    "totalMarks": 100,
    "rows": rows
}

with open("internal/ae/AE2011-key.json", "w", encoding="utf-8") as f:
    json.dump(key_json, f, indent=2, ensure_ascii=False)

print("Created internal/ae/AE2011-key.json with rows and sha256")
