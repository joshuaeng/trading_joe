from enum import Enum
import pymysql as sql
from database_connector import config
import logging


class ConnectorState(Enum):

    CONNECTED = 1

    DISCONNECTED = 2

    OFFLINE = 3


class DBConnector:
    def __init__(
            self,
            host=None,
            user=None,
            password=None
    ):

        self.state: ConnectorState = ConnectorState.OFFLINE

        self._host = config.host if host is None else host

        self._user = config.user if user is None else user

        self._password = config.password if password is None else password

        self.connection = None

    def _connect(self):

        logging.info(f"Connecting to {self._host}...")

        self.connection = sql.connect(
            host=self._host,
            user=self._user,
            password=self._password
        )

        logging.info(f"Connected to {self._host}.")

        self.state = ConnectorState.CONNECTED

    def _disconnect(self):
        self.connection.close()

        self.state = ConnectorState.DISCONNECTED

    def query(self, query: str):

        self._connect()

        with self.connection.cursor(sql.cursors.DictCursor) as cursor:

            cursor.execute(query=query)

            self.connection.commit()

        self._disconnect()

        return cursor.fetchall()


