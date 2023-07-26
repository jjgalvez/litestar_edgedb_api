from __future__ import annotations

from litestar import (
    status_codes,
    get, post, put, delete,

)

from litestar.controller import Controller
from litestar.exceptions import HTTPException

import edgedb

from .queries import (
    client,
    create_event_async_edgeql as create_event_qry,
    delete_event_async_edgeql as delete_event_qry,
    get_event_by_name_async_edgeql as get_event_by_name_qry,
    get_events_async_edgeql as get_events_qry,
    update_event_async_edgeql as update_event_qry,
)

from .models import Event, EventRequestData

@get('/events')
async def get_events() -> List[Event]:
    events = await get_events_qry.get_events(client)
    return Event.returnEvents(events)

class EventControler(Controller):

    path = '/event'

    @get('/{name:str}')
    async def get_event_by_name(self, name:str) -> Event:
        event = await get_event_by_name_qry.get_event_by_name(
            client,
            name = name
        )
        if not event:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=f'{name} does not exsist'
            )
        return Event.returnEvent(event)

    @post(path='/')
    async def post_event(self, data : EventRequestData) -> Event:
        print(data)
        try:
            created_event = await create_event_qry.create_event(
                client,
                name=data.name,
                address=data.address,
                schedule=data.schedule,
                host_name=data.host_name,
            )
        except edgedb.errors.InvalidValueError:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail='Invalid date time format'
            )
        except edgedb.errors.ConstraintViolationError:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=f'Event name {data.name} already exsists'
            )
        return Event.returnEvent(created_event)
    
    @put('/{current_name:str}')
    async def update_event(self, current_name:str, data:EventRequestData) -> Event:
        try:
            updated_event = await update_event_qry.update_event(
                client,
                current_name=current_name,
                name=data.name,
                address=data.address,
                schedule=data.schedule,
                host_name=data.host_name,
            )
        except edgedb.errors.InvalidValueError:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail = 'Invalid date formate'
            )
        except edgedb.errors.ConstraintViolationError:
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST,
                detail=f'Event named {data.name} already exists'
            )
        
        if not updated_event:
            raise HTTPException(
                status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Update event for {data.name} failed'
            )
        return Event.returnEvent(updated_event)

    @delete('/{name:str}', status_code=200)
    async def delete_event(self, name:str) -> Event:
        deleted_event = await delete_event_qry.delete_event(
            client,
            name=name
        )
        if not deleted_event:
            raise HTTPException(
                status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Delete event for {name} failed'
            )
        return Event.returnEvent(deleted_event)