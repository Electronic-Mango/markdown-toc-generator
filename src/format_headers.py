from os import linesep

from header import Header


def format_headers(headers: list[Header], skip_level: int, section_only: bool) -> str:
    return linesep.join(
        format_single_header(header, skip_level, section_only)
        for header in headers
        if header.level > skip_level
    )


def format_single_header(header: Header, skip_level: int, section_only: bool) -> str:
    list_prefix = " " * (header.level - skip_level - 1) * 2
    file_link = header.file_link if not section_only else ""
    return f"{list_prefix}- [{header.name}]({file_link}{header.section_link})"
