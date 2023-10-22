from typing import Union
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.database_connector.db_connector import base


class InstrumentPrice:
    def __init__(
            self,
            price: float = None,
            date: datetime = None
    ):

        self.price = price

        self.date = date


class Instrument(base):

    __tablename__ = "instruments"

    instrument_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()

    def __init__(self, instrument_id=None, name=None, price=None):

        super().__init__()

        self.instrument_id: str = instrument_id

        self.name: str = name

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






class PortfolioComponent:
    def __init__(self, instrument: Instrument, quantity: int):

        self.instrument: Instrument = instrument

        self.quantity: int = quantity

    def __repr__(self):
        return {self.instrument.name: self.quantity}


class Portfolio:
    def __init__(
            self,
            portfolio_id: str = None,
            composition=None
    ):
        self.portfolio_id: str = portfolio_id

        self.composition: list[PortfolioComponent] \
            = [] if composition is None else composition

        self.value: Union[None, float] \
            = self._calculate_value()

    def add_instrument(self, instrument_to_add: Instrument, quantity: int):
        self.composition.append(

            PortfolioComponent(

                instrument=instrument_to_add,

                quantity=quantity

            )

        )

    def _calculate_value(self):
        value = 0

        for component in self.composition:

            value += component.instrument.price.price * component.quantity

        return value

    def get_composition(self) -> list[PortfolioComponent]:
        return self.composition



