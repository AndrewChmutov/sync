import time
from typing import ClassVar, Self

from pydantic import BaseModel, computed_field


class Settings(BaseModel):
    password: str = ""
    dir: str = ""


class LocalState(BaseModel):
    n_dirs: int
    n_bytes: int
    n_files: int

    @classmethod
    def empty(cls) -> Self:
        return cls(n_dirs=0, n_files=0, n_bytes=0)


class CurrentDevice(BaseModel):
    _TIME: ClassVar[float] = time.time()
    path: str
    local_state: LocalState | None
    agent: str

    @computed_field
    @property
    def uptime(self) -> float:
        return time.time() - self._TIME

    @classmethod
    def empty(cls, agent: str | None = None) -> Self:
        return cls(
            path="Loading",
            local_state=LocalState.empty(),
            agent=agent or "Loading",
        )


class Statistics(BaseModel):
    refreshes: int = 0
    pushes: int = 0
    pulls: int = 0

    sent_bytes: int = 0
    sent_files: int = 0

    received_bytes: int = 0
    received_files: int = 0
