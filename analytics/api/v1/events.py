from http import HTTPStatus

from fastapi import APIRouter, Depends, Path
from fastapi.security import HTTPBearer

from schemas.error import HttpExceptionModel
from schemas.event import CreateEventResponse, UserEvent
from services.event import EventService, get_event_service

router = APIRouter(redirect_slashes=False, prefix="", tags=["Analytics events"])


@router.post(
    "/{action_name}",
    summary="Отправка события в систему аналитики",
    response_model=CreateEventResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: {"model": HttpExceptionModel},
        HTTPStatus.UNAUTHORIZED: {"model": HttpExceptionModel},
        HTTPStatus.FORBIDDEN: {"model": HttpExceptionModel},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HttpExceptionModel},
    },
    dependencies=[Depends(HTTPBearer())],
)
async def create_click(
    event_create: UserEvent,
    action_name: str = Path(
        ...,
        description="Название пользовательского события. Значения: clicks, views, customs",
        example="views",
    ),
    event_service: EventService = Depends(get_event_service),
) -> CreateEventResponse:
    return await event_service.create_event(action_name, event_create)
