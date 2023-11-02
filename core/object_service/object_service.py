from sqlalchemy.orm import DeclarativeBase
from core.database_service.db_connector import DBConnector
from typing import Type, Any
from datetime import datetime
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Date


class _Base(DeclarativeBase):
    @property
    def fields(self):
        return [
            key for key in self.__dict__.keys()
        ]


class ObjectService:
    def __init__(self):

        self.dbc = DBConnector()

    def get_object(self,
                   object_type: Type[_Base],
                   object_primary_key: str
                   ) -> Any:

        with self.dbc.orm_session as session, session.begin():
            obj = session.get(object_type, object_primary_key)

            session.expunge(obj)

        return obj

    def get_list(self, object_type: Type[_Base]):

        with self.dbc.orm_session as session, session.begin():
            obj_list = session.query(object_type).all()

            for obj in obj_list:
                session.expunge(obj)

        return obj_list

    def persist(self, obj_list: list[_Base]) -> None:

        with self.dbc.orm_session as session, session.begin():
            for obj in obj_list:
                session.add(obj)

            session.commit()

    def delete(self, obj_list: list[_Base]) -> None:

        with self.dbc.orm_session as session, session.begin():
            for obj in obj_list:
                session.delete(obj)

            session.commit()

    def delete_by_object_id(self, id_list: list, object_type: Type[_Base]) -> None:

        with self.dbc.orm_session as session, session.begin():
            for object_id in id_list:
                obj = session.get(object_type, object_id)
                session.delete(obj)

            session.commit()


class Instrument(_Base):

    __tablename__ = "instruments"
    instrument_id = Column("instrument_id", String, primary_key=True, )
    name = Column("name", String)
    price = Column("price", Float)

    def __init__(self, instrument_id: str, name: str):

        super().__init__()
        self.instrument_id: str = instrument_id
        self.name = name
        self.price = None


class InstrumentPrice(_Base):

    __tablename__ = "instrument_price"
    id = Column(primary_key=True, autoincrement=True)
    instrument_id = Column(String, ForeignKey("instruments.instrument_id"))
    date = Column("date", Date)
    price = Column("price", Float)

    def __init__(self, instrument_id: str, price: float = None, date: datetime = None):

        super().__init__()
        self.instrument_id = instrument_id
        self.price = price
        self.date = date


class Position(_Base):

    __tablename__ = "position"
    id = Column(primary_key=True, autoincrement=True)
    portfolio_id = Column(String, ForeignKey("portfolio.portfolio_id"))
    instrument_id = Column(String, ForeignKey("instruments.instrument_id"))
    quantity = Column("quantity", Integer)

    def __init__(
            self,
            portfolio_id: str = None,
            instrument_id: str = None,
            quantity: int = None
    ):

        super().__init__()
        self._portfolio_id: str = portfolio_id
        self._instrument_id = instrument_id
        self._quantity = quantity


class Portfolio(_Base):

    __tablename__ = "portfolio"
    portfolio_id = Column("portfolio_id", String, primary_key=True)
    name = Column("name", String)

    def __init__(self, portfolio_id: str, name: str):

        super().__init__()
        self.portfolio_id = portfolio_id
        self.name = name




