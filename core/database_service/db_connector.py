from core.database_service import config
import sqlalchemy
from sqlalchemy.orm import Session, DeclarativeBase
from typing import Type


class Base(DeclarativeBase):
    pass


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

        self._orm_session = Session(
            bind=self.engine
        )

    def get_object(self, object_type: Type[Base], object_primary_key: str):

        with self._orm_session as session, session.begin():

            obj = session.get(object_type, object_primary_key)

            session.expunge(obj)

        return obj

    def persist_object(self, obj: Base):

        with self._orm_session as session, session.begin():

            session.add(obj)

            session.commit()

        return obj




