import pymupdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = pymupdf.open('internal/ae/AE2025.pdf')
page32 = doc[31]
print("Page 32 text blocks:")
for b in page32.get_text("blocks"):
    print(f"  bbox: {b[:4]} -> {b[4]!r}")
