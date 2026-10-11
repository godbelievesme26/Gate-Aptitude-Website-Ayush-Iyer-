import fitz
import os
import hashlib

pdf_path = "internal/ae/AE2016.pdf"
with open(pdf_path, "rb") as f:
    sha256 = hashlib.sha256(f.read()).hexdigest()

print(f"AE2016.pdf SHA256: {sha256}")

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

os.makedirs("tmp/ae2016_pages", exist_ok=True)
os.makedirs("tmp/ae2016_extracted_imgs", exist_ok=True)

with open("tmp/ae2016_raw_text.txt", "w", encoding="utf-8") as out:
    for page_idx, page in enumerate(doc):
        # Render high-res image of page
        pix = page.get_pixmap(dpi=200)
        pix.save(f"tmp/ae2016_pages/page_{page_idx+1:02d}.png")
        
        text = page.get_text()
        out.write(f"=== PAGE {page_idx+1} ===\n{text}\n\n")
        
        # Extract embedded images
        image_list = page.get_images(full=True)
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            img_filename = f"tmp/ae2016_extracted_imgs/p{page_idx+1:02d}_img{img_idx+1:02d}_xref{xref}.{image_ext}"
            with open(img_filename, "wb") as f_img:
                f_img.write(image_bytes)

print("Page rendering and text extraction complete.")
