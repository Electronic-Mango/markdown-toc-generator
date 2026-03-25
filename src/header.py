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
