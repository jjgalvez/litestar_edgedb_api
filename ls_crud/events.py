from __future__ import annotations

from litestar import (
    status_codes,
    post,

)

from litestar.controller import Controller

from .queries import (
    client,
    create_event_async_edgeql as create_event_qry
)

class EventControler(Controller):

    path = '/events'

    @post(path='/')
    async def post_event(self):
        ...

