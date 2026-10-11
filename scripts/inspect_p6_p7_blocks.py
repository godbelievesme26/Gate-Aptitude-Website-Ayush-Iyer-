import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')

# Check page 6 drawings and text positions
p6 = doc[5]
print("--- Page 6 Text Blocks ---")
for b in p6.get_text("blocks"):
    print(f"Block: bbox={b[:4]}, text={b[4][:50]!r}")

print("\n--- Page 7 Text Blocks ---")
p7 = doc[6]
for b in p7.get_text("blocks"):
    print(f"Block: bbox={b[:4]}, text={b[4][:50]!r}")
