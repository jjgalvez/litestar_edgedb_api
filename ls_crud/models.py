from __future__ import annotations

from pydantic import BaseModel
from typing import Optional
import uuid
import datetime

class User(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    created_at: Optional[datetime.datetime] = None


class EventRequestData(BaseModel):
    name: str
    address: str
    schedule: str
    host_name: str

