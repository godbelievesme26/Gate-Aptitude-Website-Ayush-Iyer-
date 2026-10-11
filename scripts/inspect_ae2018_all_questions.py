import fitz
import json

doc = fitz.open('internal/ae/AE2018.pdf')

questions = []
for pno in range(12):
    page = doc[pno]
    text = page.get_text()
    print(f"\n==================== PAGE {pno+1} ====================")
    print(text)

