from typing import Optional

from clickhouse_driver import connect
from clickhouse_driver.dbapi.connection import Connection
from clickhouse_driver.dbapi.cursor import Cursor
from clickhouse_driver.dbapi.extras import DictCursor
from store.base import BaseAccessor

from core.config import settings


class ClickhouseAccessor(BaseAccessor):
    """Clickhouse ацессор - контекстный менеджер подключения к БД."""

    def __init__(self):
        self.connection: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self):
        try:
            self.connection = connect(
                host=settings.database.host,
                port=settings.database.port,
                user=settings.database.user,
                password=settings.database.password,
                alt_hosts=settings.database.alt_hosts,
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            return self
        except Exception as exc:
            if self.connection:
                self.connection.rollback()
                self.__close()
            raise exc

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    @property
    def conn(self):
        return self.connection

    @property
    def curs(self):
        return self.cursor
