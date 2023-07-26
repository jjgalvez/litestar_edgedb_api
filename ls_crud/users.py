from __future__ import annotations

from typing import List
from litestar import (
    status_codes,
    get, post, put, delete,
)
from litestar.controller import Controller
from litestar.exceptions import HTTPException

import edgedb

from .queries import get_user_by_name_async_edgeql as get_user_by_name_qrr
from .queries import get_users_async_edgeql as get_users_qry
from .queries import create_user_async_edgeql as create_user_qry
from .queries import update_user_async_edgeql as update_user_qry
from .queries import delete_user_async_edgeql as delete_user_qry

from .queries import client

from .models import User

@get(path='/users')
async def get_users() -> List[User]:
    users = await get_users_qry.get_users(client)
    return User.returnUsers(users)

# @get(path='/users')
# async def get_users() -> List[get_users_qry.GetUsersResult]:
#     users = await get_users_qry.get_users(client)
#     print(type(users[0]))
#     return users

class UsersController(Controller):
    path = '/user'

    @delete(path='/{user:str}', status_code=200)
    async def del_user(self, user:str) -> User:
        try:
            deleted_user = await delete_user_qry.delete_user(
                client,
                name=user
            )
        except edgedb.errors.ConstraintViolationError:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=f'{user} can not be deleted at this time'
            )
        if not deleted_user:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=f'User {user} was not found'
            )
        return User.returnUser(deleted_user)

    @put('/{user:str}')
    async def put_user(self, data:User, user:str) -> User:

        try:
            updated_user = await update_user_qry.update_user(client,
                                new_name=data.name,
                                currrent_name=user)
        except edgedb.errors.ConstraintViolationError:
            raise HTTPException(
                detail=f'Username {data.name} already exsits in the database',
                status_code=status_codes.HTTP_400_BAD_REQUEST
            )
        if not updated_user:
            raise HTTPException(
                detail=f'User {user} was not found in database',
                status_code=status_codes.HTTP_404_NOT_FOUND
            )
        return User.returnUser(updated_user)


    @get('/{user:str}')
    async def get_user(self, user:str) -> User:
        print(user)
        _user = await get_user_by_name_qrr.get_user_by_name(client, name=user)
        if not _user:
            raise HTTPException(
                detail=f'No user named: {user} found in the database', 
                status_code=status_codes.HTTP_404_NOT_FOUND
                )
        return User.returnUser(_user)

    @post('/')
    async def post_user(self, data: User) -> User:
        created_user = await create_user_qry.create_user(client, name=data.name)
        return User.returnUser(created_user)