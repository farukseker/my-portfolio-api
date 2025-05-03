from pydantic import BaseModel
from typing import Optional


class MeetingModel(BaseModel):
    title: Optional[str]
    notes: Optional[str]
