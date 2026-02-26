import fitz  # pymupdf


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ValueError("Empty PDF file.")

    text = ""

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text("text")
                if isinstance(page_text, str):
                    text += page_text

    except Exception:
        raise ValueError("Invalid or corrupted PDF file.")

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("No readable text found in PDF.")

    return cleaned_text