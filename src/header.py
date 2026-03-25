from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class Header(NamedTuple):
    level: int
    name: str
    relative_path: Path
    section_link: str

    @property
    def file_link(self) -> str:
        return quote(f"./{self.relative_path}")

    def str(self, skip: int, section_only: bool) -> str:
        list_prefix = " " * (self.level - skip - 1) * 2
        file_link = self.file_link if not section_only else ""
        return f"{list_prefix}- [{self.name}]({file_link}{self.section_link})"
