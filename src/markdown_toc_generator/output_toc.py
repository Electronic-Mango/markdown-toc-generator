from itertools import groupby
from os import linesep
from pathlib import Path
from re import MULTILINE, sub
from urllib.parse import quote

from markdown_toc_generator.heading import Heading


def handle_file_toc(
    heading_data: dict[Path, list[Heading]],
    skip: int,
    take: int,
    in_place: bool,
    toc_regex: str,
) -> None:
    for path, headings in heading_data.items():
        if not (toc := format_headings(headings, skip, take, True)):
            continue
        if in_place:
            insert_toc(path, toc, toc_regex)
        else:
            print(f"{path}:{linesep}{toc}{linesep}")


def handle_summary_toc(
    root: Path,
    heading_data: dict[Path, list[Heading]],
    in_place: bool,
    target_path: Path | None,
    main_heading: str,
) -> None:
    all_paths = {path for full_path in heading_data for path in full_path.parents[:-1]}
    all_paths = sorted(all_paths, key=lambda path: (path, len(path.parents)))
    heading_data_per_directory = {
        group[0]: dict(values).values()
        for group, values in groupby(heading_data.items(), lambda item: item[0].parents[:-1])
    }
    expanded_heading_data = {path: heading_data_per_directory.get(path, []) for path in all_paths}
    toc = ""
    for dir_path, dir_headings in expanded_heading_data.items():
        if root not in dir_path.parents:
            continue
        level = 2
        toc += format_path_heading(root, dir_path, level, target_path is None)
        for file_headings in dir_headings:
            # toc += format_path_heading(file_path, level + 1)
            first_heading = file_headings[0]
            toc += format_note_heading(first_heading, level, target_path)
            toc += format_headings(file_headings, 1, 1, target_path is None, target_path)
            toc += linesep * 2
    summary = f"{main_heading}{linesep * 2}{toc}"
    if in_place and target_path:
        existing_target_text = target_path.read_text()
        if summary.strip() == existing_target_text.strip():
            print(f"No changes made to: '{target_path}'")
        else:
            print(f"Updating summary in: '{target_path}'")
            target_path.write_text(summary)
    else:
        print(f"{linesep * 2}{summary}")


def format_headings(
    headings: list[Heading],
    skip: int,
    take: int,
    section_only: bool,
    relative_to: Path | None = None,
) -> str:
    return linesep.join(
        heading.str(skip, section_only, relative_to)
        for heading in headings
        if level_in_range(heading.level, skip, take)
    )


def level_in_range(level: int, skip: int, take: int) -> bool:
    return (level > skip and level <= (take + skip)) if take else (level > skip)


def insert_toc(path: Path, toc: str, toc_regex: str) -> None:
    toc = (linesep * 2) + toc + (linesep * 3)
    text = path.read_text()
    if toc in text:
        print(f"No changes made to: '{path}'")
        return
    print(f"Updating ToC in: '{path}'")
    sub_regex = rf"\1{toc}"
    new_text = sub(toc_regex, sub_regex, text, count=1, flags=MULTILINE)
    path.write_text(new_text)


def format_path_heading(root: Path, path: Path, level: int, section_only: bool) -> str:
    if section_only:
        return f"{'#' * level} {path.name}{linesep * 2}"
    relative_path = path.resolve().relative_to(root.resolve(), walk_up=True)
    return f"{'#' * level} [{path.name}]({quote(str(relative_path))}){linesep * 2}"


def format_note_heading(heading: Heading, level: int, target_path: Path | None = None) -> str:
    return f"{'#' * (level + 1)}{heading.str(0, target_path is None, target_path)[1:]}{linesep * 2}"
