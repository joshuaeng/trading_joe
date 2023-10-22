from enum import Enum
from core.database_service import config
import sqlalchemy
from sqlalchemy.orm import Session, declarative_base

base = declarative_base()


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

        self.state: ConnectorState \
            = ConnectorState.OFFLINE

        self._host \
            = config.host if host is None else host

        self._user \
            = config.user if user is None else user

        self._password \
            = config.password if password is None else password

        self.engine \
            = sqlalchemy.create_engine(
                f"mysql+mysqlconnector://{self._user}:{self._password}@{self._host}/trading_joe"
            )

        self._orm_session = None

        self._connection = None

    def _init_orm_session(self):
        self._orm_session = Session(bind=self.engine)

    def orm_session(self) -> Session:

        self._init_orm_session()

        return self._orm_session


