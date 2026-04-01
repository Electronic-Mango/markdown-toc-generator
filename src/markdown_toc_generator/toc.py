#!/usr/bin/env python3

from pathlib import Path

from markdown_toc_generator.arguments import parse_arguments
from markdown_toc_generator.heading import Heading
from markdown_toc_generator.output_toc import handle_file_toc, handle_summary_toc
from markdown_toc_generator.parse_headings import parse_headings_from_file


def main() -> None:
    args = parse_arguments()
    root = args.root.resolve()
    summary_path = handle_summary_path(args.summary_path)
    in_place = verify_in_place(args.in_place, args.force)
    if args.include:
        notes_paths = [path.resolve() for path in args.include]
    else:
        normalized_excludes = get_all_excludes(root, args.exclude, summary_path)
        notes_paths = get_all_notes_paths(root, normalized_excludes)
    notes_paths.sort(key=lambda path: (len(path.parents), path))
    heading_data = parse_all_headings(notes_paths)
    if not args.summary_only:
        toc_regex = full_toc_heading_regex(args.toc_heading_regex) or args.toc_regex
        handle_file_toc(heading_data, args.skip, args.take, in_place, toc_regex)
    if args.summary or args.summary_only or summary_path:
        handle_summary_toc(root, heading_data, in_place, summary_path, args.summary_heading)


def normalize(root: Path, path: Path) -> Path:
    return path.resolve().relative_to(root.resolve(), walk_up=True)


def get_all_excludes(root: Path, exclude: list[Path], readme: Path | None) -> set[Path]:
    return {normalize(root, path) for path in [*exclude, readme] if path}


def verify_in_place(in_place: bool, force: bool) -> bool:
    if not in_place or force:
        return in_place
    return input(
        "Changing files in-place can lead to data loss, use at your own risk. "
        "Continue with changes in-place? [y/n] ",
    ).lower() in ("y", "yes")


def get_all_notes_paths(root: Path, exclude: set[Path]) -> list[Path]:
    return [
        path
        for path in root.rglob("*.md")
        if not any(check_excluded_path(normalize(root, path), excluded) for excluded in exclude)
    ]


def check_excluded_path(path: Path, excluded: Path) -> bool:
    return path == excluded if excluded.is_file() else excluded in path.parents


def parse_all_headings(notes_paths: list[Path]) -> dict[Path, list[Heading]]:
    return {path: parse_headings_from_file(path) for path in notes_paths}


def handle_summary_path(path: Path | None) -> Path | None:
    if not path or not (path := path.resolve()).is_dir():
        return path
    print(f"Path '{path}' is a directory, summary will not be written")
    return None


def full_toc_heading_regex(regex: str | None) -> str | None:
    if regex is None:
        return None
    return rf"^({regex})$(\s*-.+\n)*\s*"


if __name__ == "__main__":
    main()
