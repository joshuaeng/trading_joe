from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase


class BaseObject(DeclarativeBase):

    def set_attribute(self, **kwargs):
        for element in kwargs:

            if element not in self.fields:

                raise Exception(
                    f"'{element.capitalize()}' is not an attribute of {self.__class__.__name__}. "
                    f"Attributes of {self.__class__.__name__} are: {self.fields}"
                )

        self.__dict__.update(**kwargs)

        return self

    def get_attribute(self, attribute):
        return self.__getattribute__(attribute)

    @property
    def fields(self):
        return [
            key for key in self.__class__.__dict__.keys() if not key.startswith("_")
        ]

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.get_attribute('id')}')"


@dataclass
class Instrument(BaseObject):
    __tablename__ = "instrument"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    name = Column("name", String)

    price = Column("price", Float)


@dataclass
class InstrumentPrice(BaseObject):
    __tablename__ = "instrument_price"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    instrument_id = Column(String, ForeignKey("instrument.id"))

    date = Column("date", Date)

    price = Column("price", Float)


@dataclass
class Position(BaseObject):
    __tablename__ = "position"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    portfolio_id = Column(String, ForeignKey("portfolio.id"))

    instrument_id = Column(String, ForeignKey("instrument.id"))

    quantity = Column("quantity", Integer)


@dataclass
class Portfolio(BaseObject):
    __tablename__ = "portfolio"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    name = Column("name", String)
