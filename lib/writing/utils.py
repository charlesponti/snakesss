personal_pronouns = ["i", "i'm", "i've", "i'll", "i'd", "me", "my", "mine"]


def has_personal_pronouns(words: list[str]) -> bool:
    return any(word in personal_pronouns for word in words)


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", ".,;:!?-_()[]{}\"'"))


def get_words(text: str) -> list[str]:
    normalized_words = remove_punctuation(text).strip().lower().split(" ")
    return [word for word in normalized_words if word != ""]


def is_sub_bullet_point(line: str) -> bool:
    """
    Returns True if the line is an indented bullet point.

    Sub-bullet points have leading whitespace.
    """
    return not is_bullet_point(line) and is_bullet_point(line.strip())


def has_text(line: str) -> bool:
    return line.strip() != ""


def is_bullet_point(line: str) -> bool:
    return line.startswith("-") or line.startswith("•")


def is_extra_empty_line(line: str, lines: list[str]) -> bool:
    """
    Returns True if the line is empty and is preceded by an empty line.
    """
    if len(lines) == 0:
        return False
    return line.strip() == "" and lines[-1].strip() == ""


def get_formatted_line(line: str, lines: list[str]) -> str | None:
    # Ignore headers
    if line.startswith("#"):
        return None
    elif line.startswith("-") or line.startswith("•"):
        return line.strip()
    # Add sub-bullet points to new lines before checking for primary bullet points.
    elif is_sub_bullet_point(line):
        return line
    # Turn all lines into bullet points
    elif (
        has_text(line)
        and not is_bullet_point(line)
        and not is_extra_empty_line(line, lines)
    ):
        return f"- {line.strip()}"

    return None
