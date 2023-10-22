from typing import Union
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.database_service.db_connector import base
from abc import ABC


class Named(ABC):
    def __init__(self, name: str):
        self._name = name

    def get_name(self):
        return self._name

    def __repr__(self):
        return self._name


class InstrumentPrice(Named):
    def __init__(self, name: str, price: float = None, date: datetime = None):

        super().__init__(name)

        self._price = price

        self._date = date

    def get_price(self):
        return self._price

    def get_date(self):
        return self._date

    def __repr__(self):
        return


class Instrument(base, Named):

    __tablename__ = "instruments"

    instrument_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()

    def __init__(self, instrument_id=None, name=None, price=None):

        super().__init__(name)

        self.instrument_id: str = instrument_id

        self.price: InstrumentPrice = price

    def get_instrument_id(self) -> str:
        return self.instrument_id

    def get_instrument_name(self) -> str:
        return self.name

    def get_price(self) -> Union[None, InstrumentPrice]:
        return self.price

    def __repr__(self):
        return f"INSTRUMENT('{self.instrument_id}')"

    def __str__(self):
        return self.instrument_id


class PortfolioComponent(Named):
    def __init__(self, instrument: Instrument, quantity: int, name: str):

        super().__init__(name)

        self.instrument: Instrument = instrument

        self.quantity: int = quantity

    def __repr__(self):
        return {self.instrument.name: self.quantity}


class Portfolio(Named):
    def __init__(self, name: str, portfolio_id: str = None, composition=None):

        super().__init__(name)

        self._portfolio_id: str = portfolio_id

        self._composition: list[PortfolioComponent] \
            = [] if composition is None else composition

    def get_portfolio_id(self) -> str:
        return self._portfolio_id

    def get_composition(self) -> list[PortfolioComponent]:
        return self._composition



