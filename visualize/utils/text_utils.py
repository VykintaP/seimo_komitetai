def shorten(text: str, max_length: int = 15) -> str:
    """
    Shortens text to a specified maximum length and adds ellipsis if needed.

    Args:
        text: The text to shorten
        max_length: Maximum length of the shortened text

    Returns:
        Shortened text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 2] + "..."
