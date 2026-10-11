import fitz
import os

doc = fitz.open("internal/ae/AE2020.pdf")
os.makedirs("tmp/ae2020_questions", exist_ok=True)

# Map pages to questions
page_qs = {
    1: ["GA_01", "GA_02", "GA_03", "GA_04", "GA_05"],
    2: ["GA_06", "GA_07", "GA_08", "GA_09", "GA_10"],
    3: ["AE_01", "AE_02", "AE_03", "AE_04"],
    4: ["AE_05", "AE_06", "AE_07"],
    5: ["AE_08", "AE_09", "AE_10", "AE_11", "AE_12", "AE_13"],
    6: ["AE_14", "AE_15", "AE_16", "AE_17", "AE_18"],
    7: ["AE_19", "AE_20", "AE_21", "AE_22", "AE_23", "AE_24", "AE_25", "AE_26"],
    8: ["AE_27", "AE_28", "AE_29"],
    9: ["AE_30", "AE_31"],
    10: ["AE_32", "AE_33", "AE_34"],
    11: ["AE_35", "AE_36", "AE_37"],
    12: ["AE_38", "AE_39", "AE_40", "AE_41", "AE_42"],
    13: ["AE_43", "AE_44", "AE_45", "AE_46", "AE_47", "AE_48", "AE_49"],
    14: ["AE_50", "AE_51", "AE_52", "AE_53"],
    15: ["AE_54", "AE_55"]
}

# Note: Some questions span across page boundaries if any. Let's check markers per page.
for page_idx in range(15):
    page = doc[page_idx]
    blocks = page.get_text("blocks")
    page_markers = []
    for b in blocks:
        text = b[4].strip()
        if text.startswith("Q.No."):
            page_markers.append((text, b[1], b[3])) # text, top, bottom
    
    page_markers.sort(key=lambda x: x[1])
    q_names = page_qs[page_idx + 1]
    
    print(f"Page {page_idx+1}: {len(page_markers)} markers vs {len(q_names)} expected")
    
    for i, (qname, marker) in enumerate(zip(q_names, page_markers)):
        y_top = marker[1] - 5
        if i + 1 < len(page_markers):
            y_bottom = page_markers[i+1][1] - 5
        else:
            y_bottom = page.rect.height - 30 # bottom of content
            
        rect = fitz.Rect(40, y_top, page.rect.width - 40, y_bottom)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)
        pix.save(f"tmp/ae2020_questions/{qname}.png")

print("All question crops saved.")
