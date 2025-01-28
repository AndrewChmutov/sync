import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    password: str = ""
    dir: str = ""


@dataclass
class LocalDevice:
    _TIME = time.time()
    uptime: float
    n_dirs: int
    n_bytes: int
    n_files: int

    def __init__(self, path: str) -> None:
        self.uptime = time.time() - self._TIME

        entries = list(Path(path).glob("**/*"))
        self.n_files = sum(1 for entry in entries if entry.is_file())
        self.n_dirs = len(entries) - self.n_files
        self.total_size = sum(
            entry.stat().st_size for entry in entries if entry.is_file()
        )


@dataclass
class Statistics:
    refreshes: int = 0
    pushes: int = 0
    pulls: int = 0

    sent_bytes: int = 0
    sent_files: int = 0

    received_bytes: int = 0
    received_files: int = 0
