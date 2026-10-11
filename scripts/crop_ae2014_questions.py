import fitz
import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

os.makedirs("tmp/ae2014_clean_crops", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# Question boundaries on pages 5 to 17
# Page 5 (index 4): GA Q1 - Q7
# Page 6 (index 5): GA Q8 - Q10
# Page 7 (index 6): AE Q1 - Q7
# Page 8 (index 7): AE Q8 - Q11
# Page 9 (index 8): AE Q12 - Q17
# Page 10 (index 9): AE Q18 - Q26
# Page 11 (index 10): AE Q27 - Q31
# Page 12 (index 11): AE Q32 - Q34
# Page 13 (index 12): AE Q35 - Q37
# Page 14 (index 13): AE Q38 - Q41
# Page 15 (index 14): AE Q42 - Q46
# Page 16 (index 15): AE Q47 - Q53
# Page 17 (index 16): AE Q54 - Q55

# Let's crop each question precisely with DPI=200 for clean reading
# We can define crops per page and per question

def render_rect(page_idx, rect, dpi=200):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    return pix

# Let's check text and bboxes on each page to find question vertical cuts
# Let's write a helper that splits page vertically between questions
print("Processing AE2014 questions...")
