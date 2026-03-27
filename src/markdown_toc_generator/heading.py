from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class Heading(NamedTuple):
    level: int
    name: str
    path: Path
    section_link: str

    def str(self, skip: int, section_only: bool) -> str:
        list_prefix = " " * (self.level - skip - 1) * 2
        file_link = quote(str(self.path)) if not section_only else ""
        return f"{list_prefix}- [{self.name}]({file_link}{self.section_link})"
