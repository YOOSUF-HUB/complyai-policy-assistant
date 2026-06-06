def split_text_into_chunks(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    """
    Split long text into smaller overlapping chunks.

    Args:
        text: Full extracted document text.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters repeated between chunks.

    Returns:
        A list of text chunks.
    """

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks