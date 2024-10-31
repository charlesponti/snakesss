from typing import List, TypedDict

self_referential_pronouns = [
    "i",
    "i'm",
    "i've",
    "i'll",
    "i'd",
    "me",
    "my",
    "mine",
    "myself",
]

personal_pronouns = self_referential_pronouns + [
    "you",
    "you're",
    "you've",
    "you'll",
    "you'd",
    "your",
    "yours",
    "yourself",
]


def has_self_referential_pronouns(words: list[str]) -> bool:
    return any(word in self_referential_pronouns for word in words)


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
    elif has_text(line) and not is_bullet_point(line) and not is_extra_empty_line(line, lines):
        return f"- {line.strip()}"


class Section(TypedDict):
    __text__: list[str]
    sections: dict[str, "Section"]


def get_header_line_contents(line: str) -> tuple[int, str]:
    splits = line.split(" ")
    depth = len(splits[0])
    section_name = " ".join(splits[1:])
    return depth, section_name


def get_document_sections(
    file_lines: List[str],
    get_empty_sections: bool = False,
) -> tuple[Section, List[str]]:
    current_section: Section = {"__text__": [], "sections": {}}
    section_stack: List[tuple[int, str, Section]] = [(0, "", current_section)]
    empty_sections: List[str] = []

    for line in file_lines:
        line = line.strip()
        if line.startswith("#"):
            depth, section_name = get_header_line_contents(line)
            prev_depth, prev_section_name, prev_section = section_stack[-1]
            if get_empty_sections and prev_section["__text__"] == [] and len(prev_section_name) > 0:
                empty_sections.append(prev_section_name)

            # Pop stack until we find parent section
            while section_stack and section_stack[-1][0] >= depth:
                section_stack.pop()

            # Create new section
            new_section: Section = {"__text__": [], "sections": {}}
            parent_section = section_stack[-1][2]
            parent_section["sections"][section_name] = new_section
            section_stack.append((depth, section_name, new_section))
        else:
            if line:
                section_stack[-1][2]["__text__"].append(line)

    if get_empty_sections:
        return current_section, empty_sections

    return current_section, []


def get_empty_sections(parent_section: Section) -> list[str]:
    """
    Recursively walk through a document dictionary and return a list of empty section names.
    """
    empty_sections = []

    # Ensure that input is a dictionary
    if isinstance(parent_section, dict):
        # Ensure that the dictionary has a `sections` key
        if "sections" in parent_section:
            # Get section name and section from the sections dictionary
            for name, section in parent_section["sections"].items():
                # Check if the section is empty
                if section["__text__"] == [] and section["sections"] == {}:
                    empty_sections.append(name)
                # Recursively get empty sections from nested sections
                empty_sections.extend(get_empty_sections(section))

    return empty_sections


def get_section_names(parent_section: Section) -> list[str]:
    """
    Recursively walk through a document dictionary and return a list of all section names.
    """
    section_names = []

    # Ensure that input is a dictionary
    if isinstance(parent_section, dict):
        # Ensure that the dictionary has a `sections` key
        if "sections" in parent_section:
            # Get section name and section from the sections dictionary
            for name, section in parent_section["sections"].items():
                section_names.append(name)
                # Recursively get names from nested sections
                section_names.extend(get_section_names(section))

    return section_names
