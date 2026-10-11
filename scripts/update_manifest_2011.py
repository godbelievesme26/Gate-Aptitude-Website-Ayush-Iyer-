import json, hashlib

def get_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

with open('data/ae/manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# Find 2011 entry
for i, y_entry in enumerate(manifest['years']):
    if y_entry['year'] == 2011:
        manifest['years'][i] = {
            "year": 2011,
            "paper": "AE",
            "title": "GATE 2011 Aerospace Engineering",
            "path": "data/ae/2011.json",
            "ingestionStatus": "complete",
            "verificationStatus": "source-verified",
            "totalQuestions": 65,
            "totalMarks": 100,
            "sections": [
                {
                    "id": "AE",
                    "title": "Aerospace Engineering",
                    "questionIds": [f"gate-2011-ae-ae-{q:02d}" for q in range(1, 56)],
                    "totalMarks": 85
                },
                {
                    "id": "GA",
                    "title": "General Aptitude",
                    "questionIds": [f"gate-2011-ae-ga-{q:02d}" for q in range(56, 66)],
                    "totalMarks": 15
                }
            ],
            "questionTypeCounts": {
                "MCQ": 60,
                "MSQ": 0,
                "NAT": 5
            },
            "figureAssetCount": 8,
            "newFigureAssetCount": 8,
            "answerAvailability": {
                "officialKey": 65,
                "gradedAnswers": 65,
                "marksToAll": 0,
                "unavailable": 0
            },
            "provenance": {
                "paperPdf": "internal/ae/AE2011.pdf",
                "paperSha256": get_sha256("internal/ae/AE2011.pdf"),
                "keyPdf": "internal/ae/AE2011-key.pdf",
                "keySha256": get_sha256("internal/ae/AE2011-key.pdf")
            }
        }
        break

with open('data/ae/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("Updated data/ae/manifest.json for 2011")
