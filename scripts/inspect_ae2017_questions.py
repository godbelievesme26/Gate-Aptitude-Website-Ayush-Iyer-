import fitz

doc = fitz.open('internal/ae/AE2017.pdf')
with open('tmp/ae2017_text_dump.txt', 'w', encoding='utf-8') as f:
    for pno in range(len(doc)):
        f.write(f"\n==================== PAGE {pno+1} ====================\n")
        f.write(doc[pno].get_text())

print("Written tmp/ae2017_text_dump.txt")
