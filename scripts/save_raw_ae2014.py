import fitz
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("internal/ae/AE2014.pdf")

# Let's read text from pages 5 to 17
full_text = ""
for pno in range(4, 17):
    page = doc[pno]
    full_text += f"\n<<<PAGE_{pno+1}>>>\n" + page.get_text()

# Save raw text to file for careful inspection
with open("tmp/ae2014_raw_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("Saved tmp/ae2014_raw_text.txt")
