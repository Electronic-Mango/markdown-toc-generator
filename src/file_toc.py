from os import linesep
from pathlib import Path
from re import MULTILINE, sub

from header import Header

TOC_REGEX = r"^(#[^#].+)$(\s*-.+\n)*\s*"


def insert_toc(path: Path, headers: list[Header], skip: int = 1, section_only: bool = True) -> None:
    if not headers or not (new_toc := format_headers(headers, skip, section_only)):
        print(f"No changes made to: {path}")
        return
    with open(path, "r") as file:
        text = file.read()
    new_toc = f"{linesep * 2}{new_toc}{linesep * 3}"
    if new_toc in text:
        print(f"No changes made to: {path}")
        return
    print(f"Updating ToC in: {path}")
    sub_regex = rf"\1{new_toc}"
    new_text = sub(TOC_REGEX, sub_regex, text, count=1, flags=MULTILINE)
    with open(path, "w") as file:
        file.write(new_text)


def format_headers(headers: list[Header], skip_level: int, section_only: bool) -> str:
    return linesep.join(
        header.str(skip_level, section_only)
        for header in headers
        if header.level > skip_level
    )
