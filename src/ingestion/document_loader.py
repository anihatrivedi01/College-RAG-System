import pymupdf
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io


def extract_text_from_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    all_text = []

    for page_number, page in enumerate(doc):

        # Try normal PDF text extraction first
        text = page.get_text().strip()

        if len(text) > 50:
            all_text.append(text)

        else:
            print(f"OCR required for page {page_number + 1}")

            # Render page at high resolution
            pix = page.get_pixmap(dpi=300)

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            # Convert to grayscale
            image = image.convert("L")

            # Increase contrast
            image = ImageEnhance.Contrast(image).enhance(2)

            # Slightly sharpen the image
            image = image.filter(ImageFilter.SHARPEN)

            # OCR
            ocr_text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            all_text.append(ocr_text)

    doc.close()

    return "\n\n".join(all_text)