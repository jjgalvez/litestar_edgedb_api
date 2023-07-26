# AUTOGENERATED FROM 'ls_crud/queries/get_event_by_name.edgeql' WITH:
#     $ edgedb-py


from __future__ import annotations
import dataclasses
import datetime
import edgedb
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class GetEventByNameResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    address: str | None
    schedule: datetime.datetime | None
    host: GetEventByNameResultHost | None


@dataclasses.dataclass
class GetEventByNameResultHost(NoPydanticValidation):
    id: uuid.UUID
    name: str


async def get_event_by_name(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
) -> GetEventByNameResult | None:
    return await executor.query_single(
        """\
        select Event {
            name, address, schedule,
            host: {name}
        } filter .name = <str>$name;\
        """,
        name=name,
    )