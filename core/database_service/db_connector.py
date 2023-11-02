from core.database_service import config
import sqlalchemy
from sqlalchemy.orm import Session


class DBConnector:
    def __init__(
            self,
            host=None,
            user=None,
            password=None
    ):

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

        self.orm_session = Session(
            bind=self.engine
        )





