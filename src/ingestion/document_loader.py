import pymupdf
import pytesseract
from PIL import Image
import io


def extract_text_from_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text().strip()

        if len(text) > 50:
            pages.append({
                "text": text,
                "page": page_number + 1
            })

        else:
            print(f"OCR required for page {page_number + 1}")

            pix = page.get_pixmap(dpi=300)

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            ocr_text = pytesseract.image_to_string(image).strip()

            pages.append({
                "text": ocr_text,
                "page": page_number + 1
            })

    doc.close()

    return pages