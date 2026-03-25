#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from itertools import groupby
from pathlib import Path

from file_toc import insert_toc
from header import Header
from parse_headers import parse_headers_from_file


def main():
    args = parse_arguments()
    notes_paths = get_all_notes_paths(args.root, args.exclude, args.readme)
    header_data = parse_headers_from_all_notes(args.root, notes_paths)
    print("Updating notes...")
    update_toc_in_notes(header_data)
    print("Updating README.md")
    update_toc_in_readme(header_data, args.readme or args.root / "README.md")


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-r", "--root", type=Path, required=True, default=Path())
    parser.add_argument("-e", "--exclude", type=Path, nargs="*")
    parser.add_argument("--readme", type=Path)
    return parser.parse_args()


def get_all_notes_paths(root: Path, excluded_paths: list[Path], readme: Path | None) -> list[Path]:
    return [
        path
        for path in root.rglob("*.md")
        if not any(
            check_excluded_path(path, excluded.absolute())
            for excluded in set(excluded_paths + [readme])
            if excluded
        )
    ]


def check_excluded_path(path: Path, excluded: Path) -> bool:
    return path == excluded if excluded.is_file() else excluded in path.parents


def parse_headers_from_all_notes(root: Path, notes_paths: list[Path]) -> dict[Path, list[Header]]:
    return {path: parse_headers_from_file(root, path) for path in notes_paths}


def update_toc_in_notes(header_data: dict[Path, list[Header]]) -> None:
    for path, headers in header_data.items():
        insert_toc(path, headers)


def update_toc_in_readme(header_data: dict[Path, list[Header]], readme_path: Path) -> None:
    readme_headers = prepare_readme_headers(header_data)
    insert_toc(readme_path, readme_headers, skip=0, section_only=False)


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
