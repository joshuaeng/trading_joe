from core.database_service import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from enum import Enum


class ConnectionStatus(Enum):

    CONNECTED = 1

    DISCONNECTED = 2


class DBConnector:
    def __init__(self, host=None, user=None, password=None):
        self._host = config.host if host is None else host

        self._user = config.user if user is None else user

        self._password = config.password if password is None else password

        self.engine = sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{self._user}:{self._password}@{self._host}/trading_joe"
        )

        self.orm_session = None

        self.connection_status = ConnectionStatus.DISCONNECTED

    def connect(self):

        session = sessionmaker(bind=self.engine)

        self.orm_session = session()

        self.connection_status = ConnectionStatus.CONNECTED




