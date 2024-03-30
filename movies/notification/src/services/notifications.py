import datetime
from functools import lru_cache
from http import HTTPStatus

import bson
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from motor.core import AgnosticClient
from pymongo.errors import DuplicateKeyError

from core.config import settings
from db.mongo import get_mongo
from schemas.notifications import EmailNotification, PushNotificationState, PushNotification
from services.base import BaseService


class NotificationsService(BaseService):
    """
    Класс для реализации логики работы с закладками.
    """

    async def send_email_notification(self, request: EmailNotification):
        try:
            await self.db().insert_one({
                "id": bson.Binary.from_uuid(request.id),
                "type": "email",
                "subject": request.subject,
                "to": request.to,
                "body": request.body,
                "updated_at": None,
                "delivered_at": None,
                "ts": datetime.datetime.utcnow()
            })
        except DuplicateKeyError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Уведомление с таким идентификатором уже существует"
            )

    async def send_push_notification(self, request: PushNotification):
        try:
            await self.db().insert_one({
                "id": bson.Binary.from_uuid(request.id),
                "type": "push",
                "subject": request.subject,
                "to": request.to,
                "body": request.body,
                "read": False,
                "updated_at": None,
                "delivered_at": None,
                "ts": datetime.datetime.utcnow()
            })
        except DuplicateKeyError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Уведомление с таким идентификатором уже существует"
            )

    async def mark_notification_as_read(self, notification_id):
        await self.db().update_one({
            'id': bson.Binary.from_uuid(notification_id)
        }, {'$set': {'read': True}}, upsert=True)

    async def get_notifications_history(self, user_id) -> list[PushNotificationState]:
        return [PushNotificationState(**x, to=user_id) for x in
                await self.db().find(
                    {
                        "to": user_id,
                        "type": "push",
                        "delivered_at": {
                            '$gt': datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.show_timeout)}},
                    projection={"to": False}
                ).to_list(settings.push_limit)]


@lru_cache
def get_notifications_service(
    jwt: AuthJWT = Depends(),
    mongo: AgnosticClient = Depends(get_mongo),
) -> NotificationsService:
    return NotificationsService(jwt, mongo)
