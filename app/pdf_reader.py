from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract readable text from a PDF file.

    Args:
        file_path: Path to the saved PDF file.

    Returns:
        Extracted text as a string.
    """

    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as error:
        raise Exception(f"Failed to read PDF file: {str(error)}")