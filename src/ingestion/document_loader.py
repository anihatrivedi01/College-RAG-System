import pymupdf
import pytesseract
from PIL import Image, ImageOps
import io


def preprocess_for_ocr(image):
    image = ImageOps.grayscale(image)
    image = image.point(lambda x: 0 if x < 180 else 255)
    return image


def extract_text_from_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc):

        text = page.get_text().strip()

        if len(text) > 50:
            page_text = text

        else:
            print(f"OCR required for page {page_number + 1}")

            pix = page.get_pixmap(dpi=300)

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            image = preprocess_for_ocr(image)

            page_text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            ).strip()

        if page_text:
            pages.append({
                "text": page_text,
                "page": page_number + 1
            })

    doc.close()

    return pages