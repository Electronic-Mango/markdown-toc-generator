from itertools import groupby
from os import linesep
from pathlib import Path
from re import MULTILINE, sub
from urllib.parse import quote

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


def handle_summary_toc(
    header_data: dict[Path, list[Header]],
    skip: int,
    take: int,
    in_place: bool,
    target_path: Path | None,
    main_header: str,
) -> None:
    all_paths = {path for full_path in header_data for path in full_path.parents[:-1]}
    all_paths = sorted(all_paths, key=lambda path: (path, len(path.parents)))
    header_data_per_directory = {
        group[0]: list(values)
        for group, values in groupby(header_data.items(), lambda item: item[0].parents[:-1])
    }
    expanded_header_data = {path: header_data_per_directory.get(path, []) for path in all_paths}
    toc = ""
    for dir_path, dir_headers in expanded_header_data.items():
        level = 2
        toc += format_path_header(dir_path, level)
        for file_path, file_headers in dir_headers:
            toc += format_path_header(file_path, level + 1)
            toc += format_headers(file_headers, skip, take, False)
            toc += linesep * 2
    if in_place and target_path and target_path.is_file():
        print(f"Updating {target_path}")
        with open(target_path, "w") as file:
            file.write(f"# {main_header}{linesep * 2}{toc}")
    else:
        print(f"{main_header}:{linesep}{toc}{linesep}")


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


def format_path_header(path: Path, level: int) -> str:
    return f"{'#' * level} [{path.name}]({quote(str(path))}){linesep * 2}"
