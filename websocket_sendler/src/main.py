import asyncio
import json

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
import backoff
from pydantic import ValidationError
import websockets

from src.core.logger import logger
from src.core.config import settings
from src.models.notifications import WebSocketNotification
from src.utils.decode_jwt import decode_jwt_and_get_userid
from websockets.server import WebSocketServerProtocol

ws_connT: dict[str, websockets.server.WebSocketServerProtocol] = {}


async def handler(ws: WebSocketServerProtocol):
    user_id_token = json.loads(await ws.recv())
    logger.info(f"{user_id_token} {type(user_id_token)}")
    if (user_id := await decode_jwt_and_get_userid(user_id_token.get("user_id"))) is None:
        logger.warning(f"{user_id}")
        await ws.close(1011, "Некорректный JWT токен")
        return

    ws_connT[user_id] = ws
    logger.warning("Пользователь подключен %s", user_id)
    try:
        await ws.wait_closed()
    finally:
        del ws_connT[user_id]
        logger.warning("Пользователь отключен %s", user_id)


async def send_by_websocket(message: AbstractIncomingMessage) -> None:
    try:
        notification = WebSocketNotification.parse_raw(message.body)
    except ValidationError:
        logger.exception("Ошибка при обработке данных по ws: %s", message.body)
        return

    if ws := ws_connT.get(str(notification.user_id)) is not None:
        await ws.send(notification.msg_body)


@backoff.on_exception(backoff.expo, Exception, max_tries=settings.app.backoff_max_tries)
async def init_rabbit():
    connection = await connect(
        host=settings.rabbit.host,
        port=settings.rabbit.port,
        login=settings.rabbit.user,
        password=settings.rabbit.password,
    )
    return connection


async def process_notifications():
    connection = await init_rabbit()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.websocket.exchange)
        logger.info("Прослушивание очереди %s", settings.websocket.exchange)
        await queue.consume(send_by_websocket, no_ack=True)
        await asyncio.Future()


async def main():
    async with websockets.serve(handler, settings.websocket.host, settings.websocket.port):
        logger.info("Старт вебсокета на %s:%s", settings.websocket.host, settings.websocket.port)
        await process_notifications()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as k_exc:
        logger.info("Ручное завершение работы приложения")
