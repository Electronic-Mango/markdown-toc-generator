#!/usr/bin/env python3

from itertools import groupby
from pathlib import Path

from file_toc import insert_toc
from header import Header
from parse_headers import parse_headers_from_file

README_INTRO = """
# Notes

## Table of Contents
"""

NOTES_ROOT_PATH = Path(__file__).parent.parent
README_PATH = NOTES_ROOT_PATH / "README.md"
SCRIPTS_PATH = NOTES_ROOT_PATH / ".scripts"


def main():
    notes_paths = get_all_notes_paths()
    header_data = parse_headers_from_all_notes(notes_paths)
    update_toc_in_notes(header_data)
    update_toc_in_readme(header_data)


def get_all_notes_paths() -> list[Path]:
    return [
        path
        for path in NOTES_ROOT_PATH.rglob("*.md")
        if path != README_PATH and SCRIPTS_PATH not in path.parents
    ]


def parse_headers_from_all_notes(notes_paths: list[Path]) -> dict[Path, list[Header]]:
    return {path: parse_headers_from_file(NOTES_ROOT_PATH, path) for path in notes_paths}


def update_toc_in_notes(header_data: dict[Path, list[Header]]) -> None:
    for path, headers in header_data.items():
        insert_toc(path, headers)


def update_toc_in_readme(header_data: dict[Path, list[Header]]) -> None:
    readme_headers = prepare_readme_headers(header_data)
    insert_toc(README_PATH, readme_headers, skip=0, section_only=False)


def prepare_readme_headers(header_data: dict[Path, list[Header]]) -> list[Header]:
    headers = [header for _, headers in sorted(header_data.items()) for header in headers]
    headers_grouped_by_parent = group_headers_by_file_parents(headers)
    return [header for header_group in headers_grouped_by_parent for header in header_group]


def group_headers_by_file_parents(headers: list[Header]) -> list[list[Header]]:
    return [
        [
            create_directory_header(parents[0]),
            *[offset_header(header, len(parents)) for header in values],
        ]
        for parents, values in groupby(headers, lambda header: header.relative_path.parents[:-1])
    ]


def create_directory_header(path: Path) -> Header:
    return Header(len(path.parents), path.name, path, "")


def offset_header(header: Header, offset: int) -> Header:
    return Header(header.level + offset, header.name, header.relative_path, header.section_link)


if __name__ == "__main__":
    main()
