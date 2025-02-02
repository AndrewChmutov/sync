from enum import StrEnum

from pydantic import BaseModel


class Status(StrEnum):
    SYNC = "sync"
    CHANGED = "changed"
    OUTDATED = "outdated"


class PathWithStatus:
    path: str
    status: Status


class RemoteDir(BaseModel):
    ip: str
    paths: list[PathWithStatus]
