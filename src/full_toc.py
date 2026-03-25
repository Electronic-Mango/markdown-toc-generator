#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from os import linesep
from pathlib import Path

from file_toc import insert_toc
from header import Header
from parse_headers import parse_headers_from_file


def main():
    args = parse_arguments()
    root = args.root.absolute()
    normalized_excludes = {normalize(root, path) for path in args.exclude}
    notes_paths = get_all_notes_paths(root, normalized_excludes)
    notes_paths.sort(key=lambda path: (len(path.parents), path))
    header_data = parse_headers_from_all_notes(notes_paths)
    update_toc_in_files(header_data, args.skip, args.in_place)


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-r", "--root", type=Path, default=Path())
    parser.add_argument("-e", "--exclude", type=Path, nargs="*", default=[])
    parser.add_argument("-i", "--in-place", action="store_true")
    parser.add_argument("-s", "--skip", type=int, default=0)
    return parser.parse_args()


def normalize(root: Path, path: Path) -> Path:
    return path.absolute().relative_to(root)


def get_all_notes_paths(root: Path, exclude: set[Path]) -> list[Path]:
    return [
        normalize(root, path)
        for path in root.rglob("*.md")
        if not any(check_excluded_path(normalize(root, path), excluded) for excluded in exclude)
    ]


def check_excluded_path(path: Path, excluded: Path) -> bool:
    return path == excluded if excluded.is_file() else excluded in path.parents


def parse_headers_from_all_notes(notes_paths: list[Path]) -> dict[Path, list[Header]]:
    return {path: parse_headers_from_file(path) for path in notes_paths}


def update_toc_in_files(header_data: dict[Path, list[Header]], skip: int, in_place: bool) -> None:
    for path, headers in header_data.items():
        if not (toc := format_headers(headers, skip=skip, section_only=True)):
            continue
        if in_place:
            insert_toc(path, toc)
        else:
            print(f"{path}:{linesep}{toc}{linesep}")


def format_headers(headers: list[Header], skip: int, section_only: bool) -> str:
    return linesep.join(header.str(skip, section_only) for header in headers if header.level > skip)


if __name__ == "__main__":
    main()
