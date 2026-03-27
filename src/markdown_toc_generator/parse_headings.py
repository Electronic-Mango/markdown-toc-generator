from pathlib import Path
from re import search, sub

from markdown_toc_generator.heading import Heading

HEADER_REGEX = r"^(#+) (.+)"
CODE_BLOCK_REGEX = r"^```"


def parse_headings_from_file(path: Path) -> list[Heading]:
    with open(path, "r") as file:
        text = file.readlines()
    headings = get_all_headings(text)
    return [Heading(level, name, path, create_section_link(name)) for level, name in headings]


def get_all_headings(lines: list[str]) -> list[tuple[int, str]]:
    headings = []
    is_code_block = False
    for line in lines:
        if search(CODE_BLOCK_REGEX, line):
            is_code_block = not is_code_block
        if is_code_block:
            continue
        if match := search(HEADER_REGEX, line):
            headings.append((len(match.group(1)), match.group(2)))
    return headings


def create_section_link(name: str) -> str:
    section_link = sub(r"[^0-9a-z-_ ]", "", name.lower()).replace(" ", "-")
    return f"#{section_link}"
