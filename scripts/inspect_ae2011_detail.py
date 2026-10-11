import fitz, os, re

doc = fitz.open('internal/ae/AE2011.pdf')

for pno, page in enumerate(doc):
    print(f"\n============================== PAGE {pno+1} ==============================")
    text = page.get_text('text')
    print(text)
