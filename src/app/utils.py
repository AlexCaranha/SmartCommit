def remove_double_spaces(text: str) -> str:
    """Remove espaços duplos em um texto."""
    while "  " in text:
        text = text.replace("  ", " ")
    return text
