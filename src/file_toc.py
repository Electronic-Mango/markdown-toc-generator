from os import linesep
from pathlib import Path
from re import MULTILINE, sub

TOC_REGEX = r"^(#[^#].+)$(\s*-.+\n)*\s*"


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
