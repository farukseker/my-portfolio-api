from dataclasses import dataclass


@dataclass
class RequestSnapshot:
    ip: str | None
    user_agent: str | None
    referer: str | None
    path: str
    user_id: int | None
    is_superuser: bool
