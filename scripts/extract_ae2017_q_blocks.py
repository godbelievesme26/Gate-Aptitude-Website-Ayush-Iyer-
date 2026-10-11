import fitz
import os

os.makedirs('tmp/ae2017_q_imgs', exist_ok=True)
doc = fitz.open('internal/ae/AE2017.pdf')

count = 0
for pno in range(1, len(doc)-2):
    page = doc[pno]
    imgs = page.get_images()
    
    img_boxes = []
    for img in imgs:
        xref = img[0]
        if xref in [219, 321, 323]:
            continue
        rects = page.get_image_rects(xref)
        if rects:
            img_boxes.append((rects[0].y0, xref, rects[0]))
    img_boxes.sort()
    
    for y0, xref, rect in img_boxes:
        count += 1
        base_img = doc.extract_image(xref)
        ext = base_img['ext']
        out_name = f'tmp/ae2017_q_imgs/q_block_{count:02d}_p{pno+1:02d}_xref{xref}.png'
        # Convert to PNG using PIL if needed or write raw
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(base_img['image']))
        im.save(out_name)
        print(f"Saved Q block {count:02d} (Page {pno+1:02d}, y={y0:.1f}): {out_name} ({im.size})")

print(f"Total extracted question blocks: {count}")
