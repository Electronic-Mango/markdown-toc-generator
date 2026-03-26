#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from pathlib import Path

from file_toc import handle_file_toc, handle_summary_toc
from header import Header
from parse_headers import parse_headers_from_file


def main():
    args = parse_arguments()
    root = args.root.absolute()
    normalized_excludes = get_all_excludes(root, args.exclude, args.summary_path)
    in_place = verify_in_place(args.in_place, args.force)
    notes_paths = get_all_notes_paths(root, normalized_excludes)
    notes_paths.sort(key=lambda path: (len(path.parents), path))
    header_data = parse_all_headers(notes_paths)
    handle_file_toc(header_data, args.skip, args.take, in_place)
    if args.summary or args.summary_path:
        handle_summary_toc(header_data, 1, 1, in_place, args.summary_path, args.summary_header)


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-r", "--root", type=Path, default=Path())
    parser.add_argument("-e", "--exclude", type=Path, nargs="*", default=[])
    parser.add_argument("-i", "--in-place", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-s", "--skip", type=int, default=0)
    parser.add_argument("-t", "--take", type=int, default=0)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--summary-path", type=Path)
    parser.add_argument("--summary-header", type=str, default="Summary")
    return parser.parse_args()


def normalize(root: Path, path: Path) -> Path:
    return path.absolute().relative_to(root)


def get_all_excludes(root: Path, exclude: list[Path], readme: Path | None) -> set[Path]:
    return {normalize(root, path) for path in exclude + [readme] if path}


def verify_in_place(in_place: bool, force: bool) -> bool:
    if not in_place or force:
        return in_place
    return input(
        "Changing files in-place can lead to data loss, use at your own risk. "
        "Continue with changes in-place? [y/n] "
    ).lower() in ("y", "yes")


def get_all_notes_paths(root: Path, exclude: set[Path]) -> list[Path]:
    return [
        normalize(root, path)
        for path in root.rglob("*.md")
        if not any(check_excluded_path(normalize(root, path), excluded) for excluded in exclude)
    ]


def check_excluded_path(path: Path, excluded: Path) -> bool:
    return path == excluded if excluded.is_file() else excluded in path.parents


def parse_all_headers(notes_paths: list[Path]) -> dict[Path, list[Header]]:
    return {path: parse_headers_from_file(path) for path in notes_paths}


if __name__ == "__main__":
    main()
