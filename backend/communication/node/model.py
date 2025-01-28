from dataclasses import dataclass

@dataclass
class RemoteDir:
    ip: str
    local_total: int
    remote_total: int

    # User perspective
    in_sync: list[str]
    changed: list[str]
    outdated: list[str]
