from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class Heading(NamedTuple):
    level: int
    name: str
    path: Path
    section_link: str

    def str(self, skip: int, section_only: bool, relative: Path | None = None) -> str:
        list_prefix = " " * (self.level - skip - 1) * 2
        file_link = self.file_link(section_only, relative)
        return f"{list_prefix}- [{self.name}]({file_link}{self.section_link})"

    def file_link(self, section_only: bool, relative: Path | None) -> str:
        if section_only:
            return ""
        link = self.path.relative_to(relative.parent, walk_up=True) if relative else self.path
        return quote(str(link))
