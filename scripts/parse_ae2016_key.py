import fitz  # PyMuPDF
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

print("--- FULL TEXT OF KEY PDF ---")
print(full_text)
