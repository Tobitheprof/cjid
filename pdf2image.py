import fitz

pdf_path = "./title.pdf"

doc = fitz.open(pdf_path)

for i in range(doc.page_count):
    page = doc[i]
    pix = page.get_pixmap(dpi=400)
    pix.save(f"page_{i + 1}.jpg")