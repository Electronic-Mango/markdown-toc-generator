#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from itertools import groupby
from os import linesep
from pathlib import Path

from file_toc import insert_toc
from header import Header
from parse_headers import parse_headers_from_file


def main():
    args = parse_arguments()
    root = args.root.absolute()
    readme = args.readme.absolute()
    excluded_paths = {path.absolute() for path in args.exclude + [readme] if path}
    notes_paths = get_all_notes_paths(root, excluded_paths)
    header_data = parse_headers_from_all_notes(root, notes_paths)
    update_toc_in_files(root, header_data, args.in_place)
    update_toc_in_readme(root, header_data, readme, args.in_place)


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-r", "--root", type=Path, default=Path())
    parser.add_argument("-e", "--exclude", type=Path, nargs="*")
    parser.add_argument("--readme", type=Path)
    parser.add_argument("-i", "--in-place", action="store_true")
    return parser.parse_args()


def get_all_notes_paths(root: Path, excluded_paths: set[Path]) -> list[Path]:
    return [
        path
        for path in root.rglob("*.md")
        if not any(check_excluded_path(path, excluded) for excluded in excluded_paths)
    ]


def check_excluded_path(path: Path, excluded: Path) -> bool:
    return path == excluded if excluded.is_file() else excluded in path.parents


def parse_headers_from_all_notes(root: Path, notes_paths: list[Path]) -> dict[Path, list[Header]]:
    return {path: parse_headers_from_file(root, path) for path in notes_paths}


def update_toc_in_files(root: Path, header_data: dict[Path, list[Header]], in_place: bool) -> None:
    for path, headers in header_data.items():
        if not (toc := format_headers(headers, skip_level=1, section_only=True)):
            continue
        if in_place:
            insert_toc(path, toc)
        else:
            print(f"{path.relative_to(root)}:{linesep}{toc}{linesep}")


def update_toc_in_readme(root: Path, header_data: dict[Path, list[Header]], readme_path: Path | None, in_place: bool) -> None:
    if not readme_path:
        return
    readme_headers = prepare_readme_headers(root, header_data)
    toc = format_headers(readme_headers, skip_level=0, section_only=False)
    if in_place:
        insert_toc(readme_path, toc)
    else:
        print(f"{readme_path.relative_to(root)}:{linesep}{toc}")


def format_headers(headers: list[Header], skip_level: int, section_only: bool) -> str:
    return linesep.join(
        header.str(skip_level, section_only) for header in headers if header.level > skip_level
    )


def prepare_readme_headers(root: Path, header_data: dict[Path, list[Header]]) -> list[Header]:
    headers = [header for _, headers in sorted(header_data.items()) for header in headers]
    headers_grouped_by_parent = group_headers_by_file_parents(root, headers)
    return [header for header_group in headers_grouped_by_parent for header in header_group]


def group_headers_by_file_parents(root: Path, headers: list[Header]) -> list[list[Header]]:
    return [
        [
            create_directory_header(parents[0]),
            *[offset_header(header, len(parents)) for header in values],
        ]
        for parents, values in groupby(
            headers, lambda header: header.path.relative_to(root).parents[:-1]
        )
    ]


def create_directory_header(path: Path) -> Header:
    return Header(len(path.parents), path.name, path, "")


def offset_header(header: Header, offset: int) -> Header:
    return Header(header.level + offset, header.name, header.path, header.section_link)


if __name__ == "__main__":
    main()
