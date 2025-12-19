from pdf2image import convert_from_path
import pytesseract
import os

def pdf_to_text(pdf_path: str, txt_path: str = "input.txt", dpi: int = 300):
    # 1) Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=dpi)
    print(f"Converted {len(pages)} pages to images")

    all_lines = []

    for i, page in enumerate(pages):
        print(f"OCR on page {i}")
        text = pytesseract.image_to_string(page) or ""
        for line in text.splitlines():
            if line.strip():
                all_lines.append(line.rstrip())

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

if __name__ == "__main__":
    pdf_to_text("ZCPP_2 1.pdf", "input.txt")
    print("Extracted input.txt from ZCPP_2 1.pdf via Tesseract OCR")