from __future__ import annotations

import dataclasses
from pydantic import BaseModel
from typing import Optional, List
import uuid
import edgedb
import datetime

class User(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    created_at: Optional[datetime.datetime] = None

    @classmethod
    def returnUsers(self, users:List[edgedb.Object]) -> List(User):
        _users = [
            self(**dataclasses.asdict(x))
            for x in users
        ]
        return _users
    @classmethod
    def returnUser(self, user: edgedb.Object) -> User:
        return self(**dataclasses.asdict(user))


class Event(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    address: Optional[str] = None
    schedule: Optional[datetime.datetime] = None
    host: Optional[User] = None

    @classmethod
    def returnEvent(self, event: edgedb.Object) -> Event:
        return self(**dataclasses.asdict(self))
