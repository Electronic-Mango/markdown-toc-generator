from argparse import ArgumentParser, Namespace
from pathlib import Path

TOC_REGEX = r"^(#[^#].+)$(\s*-.+\n)*\s*"


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description=(
            "Markdown Table-of-Contents generator, print them to console, "
            "or insert them into Markdown files themselves"
        ),
    )
    parser.add_argument(
        "-r",
        "--root",
        type=Path,
        default=Path(),
        help="set root path for all operations, by default current path is used",
    )
    sources_group = parser.add_mutually_exclusive_group()
    sources_group.add_argument(
        "-e",
        "--exclude",
        type=Path,
        nargs="*",
        default=[],
        help=(
            "paths (relative to root) which should be excluded from analysis, "
            "can be single files, can be entire directories;"
            "use either '--exclude', or '--include'"
        ),
    )
    sources_group.add_argument(
        "-i",
        "--include",
        type=Path,
        nargs="*",
        default=[],
        help=(
            "specify paths to files which should be analyzed;use either '--include', or '--exclude'"
        ),
    )
    parser.add_argument(
        "-p",
        "--in-place",
        action="store_true",
        help=(
            "insert generated ToC into the files, POTENTIALLY DESCTRUCTIVE operation "
            "as entire contents of the file is read, ToC is inserted, "
            "then entire file is overwritten"
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="skip confirmation for potentially destructive operations (e.g. for --in-place flag)",
    )
    parser.add_argument(
        "-s",
        "--skip",
        type=int,
        default=0,
        help="how many levels should be skipped from ToC (starting at the highest)",
    )
    parser.add_argument(
        "-t",
        "--take",
        type=int,
        default=0,
        help=(
            "how many levels should be added to ToC (starting from the highest) "
            "relative to --take ('--skip 1 --take 3' results in levels 2-4 to be included in ToC)"
        ),
    )
    in_place_regex_group = parser.add_mutually_exclusive_group()
    in_place_regex_group.add_argument(
        "--toc-regex",
        default=TOC_REGEX,
        help=(
            "regex used to insert ToC into file with --in-place, "
            "first capture group looks for a 'prefix' string for the ToC (which is preserved), "
            "the second one looks for the ToC itself (which will be replaced), "
            f"'{TOC_REGEX}' used by default"
        ),
    )
    in_place_regex_group.add_argument(
        "--toc-heading-regex",
        default=None,
        help=(
            "regex used to insert ToC into file with --in-place, "
            "this regex should match only the heading after which ToC should be inserted,"
            "not the entire ToC text block; input regex will be wrapped as '^<regex>$'"
        ),
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="generate summary of all analyzed files",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="analyze all files, but print/write only summary",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        help=(
            "insert the generated summary into a file (--in-place flag is still required), "
            "POTENTIALLY VERY DESCTRUCTIVE as entire file will be replaced by the summary, "
            "no smart analysis is done, entire file is rewritten"
        ),
    )
    parser.add_argument(
        "--summary-heading",
        type=str,
        default="# Summary:",
        help="main heading used for generated summary",
    )
    return parser.parse_args()
