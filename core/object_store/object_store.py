from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @property
    def fields(self):
        return [
            key for key in self.__class__.__dict__.keys() if not key.startswith("_")
        ]

    def __repr__(self):
        return f"OBJECT('{self.__class__.__name__}')"


@dataclass
class Instrument(Base):
    __tablename__ = "instrument"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    name = Column("name", String)

    price = Column("price", Float)


@dataclass
class InstrumentPrice(Base):
    __tablename__ = "instrument_price"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    instrument_id = Column(String, ForeignKey("instrument.id"))

    date = Column("date", Date)

    price = Column("price", Float)


@dataclass
class Position(Base):
    __tablename__ = "position"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    portfolio_id = Column(String, ForeignKey("portfolio.id"))

    instrument_id = Column(String, ForeignKey("instrument.id"))

    quantity = Column("quantity", Integer)


@dataclass
class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column("id", Integer, primary_key=True, autoincrement=True)

    name = Column("name", String)
