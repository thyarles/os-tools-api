def decode_text(content) -> str:
    """Decode bytes to string with multiple fallback encodings."""

    encodings = ['utf-8', 'latin-1', 'ISO-8859-1']
    
    for encoding in encodings:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    try:
        return content.decode('cp1252')
    except UnicodeDecodeError:
        return content.decode('latin-1', errors='ignore')