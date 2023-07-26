from __future__ import annotations

from litestar import Litestar
from litestar.config.cors import CORSConfig

from ls_crud.users import UsersController, get_users

cors_config = CORSConfig()

routes = [
    UsersController,
    get_users,
]

app = Litestar(
    route_handlers=routes,
    cors_config=cors_config,
    debug=True,
)