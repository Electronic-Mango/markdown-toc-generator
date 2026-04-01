from pathlib import Path
from re import search, sub

from markdown_toc_generator.heading import Heading

HEADING_REGEX = r"^(#+) (.+)"
CODE_BLOCK_REGEX = r"^```"


def parse_headings_from_file(path: Path, ignore: list[str]) -> list[Heading]:
    headings = get_all_headings(path.read_text().splitlines(), ignore)
    return [Heading(level, name, path, create_section_link(name)) for level, name in headings]


def get_all_headings(lines: list[str], ignore: list[str]) -> list[tuple[int, str]]:
    headings = []
    is_code_block = False
    for line in lines:
        if search(CODE_BLOCK_REGEX, line):
            is_code_block = not is_code_block
        if is_code_block:
            continue
        if match := search(HEADING_REGEX, line):
            level = len(match.group(1))
            name = match.group(2)
            if any(search(regex, name) for regex in ignore):
                continue
            headings.append((level, strip_link_from_name(name)))
    return headings


def strip_link_from_name(name: str) -> str:
    return sub(r"(?:\[([^]]+)\]\([^)]+\))", r"\1", name)


def create_section_link(name: str) -> str:
    section_link = sub(r"[^0-9a-z-_ ]", "", name.lower()).replace(" ", "-")
    return f"#{section_link}"
