import fitz
import json
import hashlib
import re

pdf_path = "internal/ae/AE2016-key.pdf"
with open(pdf_path, "rb") as f:
    sha256 = hashlib.sha256(f.read()).hexdigest()

doc = fitz.open(pdf_path)
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"

lines = [l.strip() for l in full_text.splitlines() if l.strip()]

# Let's parse rows
# The pattern is:
# Q. No, Type, Section, Key, Marks
# or tokens.

# Let's write the explicit parsed rows to ensure 100% precision
rows = []

# GA: Q1 to Q10 -> paper numbers 1 to 10
ga_keys = [
    (1, "MCQ", "GA", "C", 1),
    (2, "MCQ", "GA", "B", 1),
    (3, "MCQ", "GA", "B", 1),
    (4, "MCQ", "GA", "B", 1),
    (5, "MCQ", "GA", "C", 1),
    (6, "NAT", "GA", "120.0 to 120.0", 2),
    (7, "MCQ", "GA", "C", 2),
    (8, "MCQ", "GA", "C", 2),
    (9, "MCQ", "GA", "A", 2),
    (10, "NAT", "GA", "7.0 to 7.0", 2),
]

for sec_q, qtype, sec, raw_k, marks in ga_keys:
    paper_q = sec_q
    rows.append({
        "number": paper_q,
        "section": sec,
        "sectionQuestionNumber": sec_q,
        "type": qtype,
        "rawKey": raw_k,
        "marks": marks
    })

# AE: Q1 to Q55 -> paper numbers 11 to 65
ae_keys = [
    (1, "MCQ", "AE", "A", 1),
    (2, "NAT", "AE", "-3.0 to -3.0", 1),
    (3, "MCQ", "AE", "D", 1),
    (4, "MCQ", "AE", "C", 1),
    (5, "MCQ", "AE", "D", 1),
    (6, "MCQ", "AE", "C", 1),
    (7, "MCQ", "AE", "C", 1),
    (8, "MCQ", "AE", "A", 1),
    (9, "MCQ", "AE", "B", 1),
    (10, "MCQ", "AE", "B", 1),
    (11, "NAT", "AE", "2.0 to 2.0", 1),
    (12, "MCQ", "AE", "A", 1),
    (13, "MCQ", "AE", "B", 1),
    (14, "NAT", "AE", "5.0 to 5.0", 1),
    (15, "MCQ", "AE", "B", 1),
    (16, "NAT", "AE", "1.0 to 1.0", 1),
    (17, "NAT", "AE", "0.0 to 0.0", 1),
    (18, "MCQ", "AE", "D", 1),
    (19, "MCQ", "AE", "C", 1),
    (20, "MCQ", "AE", "B", 1),
    (21, "MCQ", "AE", "C", 1),
    (22, "MCQ", "AE", "B", 1),
    (23, "MCQ", "AE", "A", 1),
    (24, "MCQ", "AE", "A", 1),
    (25, "MCQ", "AE", "C", 1),
    (26, "NAT", "AE", "162 to 166 OR 1147.0 to 1150.0", 2),
    (27, "MCQ", "AE", "B", 2),
    (28, "NAT", "AE", "2.9 to 3.1", 2),
    (29, "MCQ", "AE", "D", 2),
    (30, "NAT", "AE", "40.0 to 41.0", 2),
    (31, "MCQ", "AE", "B", 2),
    (32, "MCQ", "AE", "B", 2),
    (33, "NAT", "AE", "1305 to 1305", 2),
    (34, "MCQ", "AE", "B", 2),
    (35, "MCQ", "AE", "A", 2),
    (36, "MCQ", "AE", "A", 2),
    (37, "NAT", "AE", "5.0 to 5.0", 2),
    (38, "NAT", "AE", "1.5 to 1.7", 2),
    (39, "MCQ", "AE", "B", 2),
    (40, "NAT", "AE", "2.4 to 2.6", 2),
    (41, "NAT", "AE", "0.99 to 1.01", 2),
    (42, "NAT", "AE", "-11.0 to -11.0", 2),
    (43, "NAT", "AE", "3.13 to 3.15", 2),
    (44, "NAT", "AE", "0.56 to 0.58", 2),
    (45, "NAT", "AE", "548 to 550", 2),
    (46, "NAT", "AE", "310 to 315", 2),
    (47, "MCQ", "AE", "C", 2),
    (48, "NAT", "AE", "7690 to 7710", 2),
    (49, "NAT", "AE", "8.6 to 8.7", 2),
    (50, "NAT", "AE", "25.0 to 25.0", 2),
    (51, "MCQ", "AE", "D", 2),
    (52, "MCQ", "AE", "C", 2),
    (53, "NAT", "AE", "20.0 to 21.0", 2),
    (54, "MCQ", "AE", "C", 2),
    (55, "MCQ", "AE", "B", 2),
]

for sec_q, qtype, sec, raw_k, marks in ae_keys:
    paper_q = 10 + sec_q
    rows.append({
        "number": paper_q,
        "section": sec,
        "sectionQuestionNumber": sec_q,
        "type": qtype,
        "rawKey": raw_k,
        "marks": marks
    })

data = {
    "exam": "GATE",
    "year": 2016,
    "paper": "AE",
    "source": "internal/ae/AE2016-key.pdf",
    "sha256": sha256,
    "totalQuestions": len(rows),
    "totalMarks": sum(r["marks"] for r in rows),
    "rows": rows
}

with open("internal/ae/AE2016-key.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Written internal/ae/AE2016-key.json: {len(rows)} questions, {data['totalMarks']} marks")
