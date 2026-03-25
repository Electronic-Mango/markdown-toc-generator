from pathlib import Path
from re import search, sub

from header import Header

HEADER_REGEX = r"^(#+) (.+)"
CODE_BLOCK_REGEX = r"^```"


def parse_headers_from_file(root: Path, path: Path) -> list[Header]:
    with open(path, "r") as file:
        text = file.readlines()
    headers = get_all_headers(text)
    return [Header(level, name, *create_header_link(root, path, name)) for level, name in headers]


def get_all_headers(lines: list[str]) -> list[tuple[int, str]]:
    headers = []
    is_code_block = False
    for line in lines:
        if search(CODE_BLOCK_REGEX, line):
            is_code_block = not is_code_block
        if is_code_block:
            continue
        if match := search(HEADER_REGEX, line):
            headers.append((len(match.group(1)), match.group(2)))
    return headers


def create_header_link(root: Path, path: Path, name: str) -> str:
    file_link = path.relative_to(root)
    section_link = sub(r"[^0-9a-z-_ ]", "", name.lower()).replace(" ", "-")
    return file_link, f"#{section_link}"
