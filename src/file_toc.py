from os import linesep
from pathlib import Path
from re import MULTILINE, sub

from header import Header

TOC_REGEX = r"^(#[^#].+)$(\s*-.+\n)*\s*"


def handle_file_toc(
    header_data: dict[Path, list[Header]], skip: int, take: int, in_place: bool
) -> None:
    for path, headers in header_data.items():
        if not (toc := format_headers(headers, skip, take, True)):
            continue
        if in_place:
            insert_toc(path, toc)
        else:
            print(f"{path}:{linesep}{toc}{linesep}")


def format_headers(headers: list[Header], skip: int, take: int, section_only: bool) -> str:
    return linesep.join(
        header.str(skip, section_only)
        for header in headers
        if level_in_range(header.level, skip, take)
    )


def level_in_range(level: int, skip: int, take: int) -> bool:
    return (level > skip and level <= (take + skip)) if take else (level > skip)


def insert_toc(path: Path, toc: str) -> None:
    toc = (linesep * 2) + toc + (linesep * 3)
    with open(path, "r") as file:
        text = file.read()
    if toc in text:
        print(f"No changes made to: {path}")
        return
    print(f"Updating ToC in: {path}")
    sub_regex = rf"\1{toc}"
    new_text = sub(TOC_REGEX, sub_regex, text, count=1, flags=MULTILINE)
    with open(path, "w") as file:
        file.write(new_text)
