from sqlalchemy.orm import DeclarativeBase
from core.database_service.db_connector import DBConnector
from typing import Type, Any, Callable
from sqlalchemy import ForeignKey, Column, String, Integer, Float, Date
from dataclasses import dataclass


class _Base(DeclarativeBase):

    @property
    def fields(self):
        return [key for key in self.__class__.__dict__.keys() if not key.startswith("_")]

    def __repr__(self):
        return f"OBJECT('{self.__class__.__name__}')"


class ObjectService:
    def __init__(self):

        self.dbc = DBConnector()

    @staticmethod
    def update_object(obj: _Base, **kwargs) -> _Base:

        for element in kwargs:

            if element not in obj.fields:
                raise Exception(
                    f"'{element.capitalize()}' is not an attribute of {obj.__class__.__name__}. "
                    f"Attributes of {obj.__class__.__name__} are: {obj.fields}"
                )

        obj.__dict__.update(**kwargs)

        return obj

    def create_object(self, constructor: Callable, **kwargs) -> _Base:
        return self.update_object(constructor(), **kwargs)

    def get_object(self, object_type: Type[_Base], object_primary_key: str) -> Any:
        return self.dbc.orm_session.get(object_type, object_primary_key)

    def get_list(self, object_type: Type[_Base]) -> list[Any]:
        return self.dbc.orm_session.query(object_type).all()

    def persist(self, obj_list: list[_Base]) -> None:
        for obj in obj_list:
            self.dbc.orm_session.add(obj)

    def delete(self, obj_list: list[_Base]) -> None:
        for obj in obj_list:
            self.dbc.orm_session.delete(obj)

    def delete_by_object_id(self, id_list: list, object_type: Type[_Base]) -> None:
        for object_id in id_list:
            obj = self.dbc.orm_session.get(object_type, object_id)
            self.dbc.orm_session.delete(obj)


@dataclass
class Instrument(_Base):

    __tablename__ = "instruments"

    instrument_id = Column("instrument_id", String, primary_key=True)

    name = Column("name", String)

    price = Column("price", Float)


@dataclass
class InstrumentPrice(_Base):

    __tablename__ = "instrument_price"

    id = Column(primary_key=True, autoincrement=True)

    instrument_id = Column(String, ForeignKey("instruments.instrument_id"))

    date = Column("date", Date)

    price = Column("price", Float)


@dataclass
class Position(_Base):

    __tablename__ = "position"

    id = Column(primary_key=True, autoincrement=True)

    portfolio_id = Column(String, ForeignKey("portfolio.portfolio_id"))

    instrument_id = Column(String, ForeignKey("instruments.instrument_id"))

    quantity = Column("quantity", Integer)


@dataclass
class Portfolio(_Base):

    __tablename__ = "portfolio"

    portfolio_id = Column("portfolio_id", String, primary_key=True)

    name = Column("name", String)

