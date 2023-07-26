# AUTOGENERATED FROM:
#     'ls_crud/queries/create_user.edgeql'
#     'ls_crud/queries/delete_user.edgeql'
#     'ls_crud/queries/get_user_by_name.edgeql'
#     'ls_crud/queries/get_users.edgeql'
#     'ls_crud/queries/update_user.edgeql'
# WITH:
#     $ edgedb-py --file ls_crud/queries/generaged_async.py


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
class CreateUserResult(NoPydanticValidation):
    id: uuid.UUID
    name: str
    created_at: datetime.datetime


async def create_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
) -> CreateUserResult:
    return await executor.query_single(
        """\
        select (
            insert User {
                name := <str>$name
            }
        ) {
            name,
            created_at
        };\
        """,
        name=name,
    )


async def delete_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
) -> CreateUserResult | None:
    return await executor.query_single(
        """\
        select (
            delete User filter .name = <str>$name
        ) {name, created_at};\
        """,
        name=name,
    )


async def get_user_by_name(
    executor: edgedb.AsyncIOExecutor,
    *,
    name: str,
) -> CreateUserResult | None:
    return await executor.query_single(
        """\
        select User {name, created_at}
        filter User.name = <str>$name\
        """,
        name=name,
    )


async def get_users(
    executor: edgedb.AsyncIOExecutor,
) -> list[CreateUserResult]:
    return await executor.query(
        """\
        select User {name, created_at};\
        """,
    )


async def update_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    currrent_name: str,
    new_name: str,
) -> CreateUserResult | None:
    return await executor.query_single(
        """\
        select (
            update User filter .name = <str>$currrent_name
                set {name := <str>$new_name}
                )
                {name, created_at};\
        """,
        currrent_name=currrent_name,
        new_name=new_name,
    )
