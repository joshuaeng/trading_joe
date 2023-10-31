from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.database_service.db_connector import Base


class Instrument(Base):

    __tablename__ = "instruments"

    instrument_id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()

    price: Mapped[float] = mapped_column()

    def __init__(self, instrument_id: str, name: str):

        super().__init__()

        self._instrument_id: str = instrument_id

        self._name = name

    def get_instrument_id(self) -> str:
        return self._instrument_id

    def get_instrument_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"INSTRUMENT('{self.instrument_id}')"

    def __str__(self):
        return self.instrument_id


class InstrumentPrice(Base):

    __tablename__ = "instrument_price"

    nb_line: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    instrument_id: Mapped[str] = mapped_column()

    date: Mapped[datetime] = mapped_column()

    price: Mapped[float] = mapped_column()

    def __init__(self, instrument_id: str, price: float = None, date: datetime = None):

        super().__init__()

        self._instrument_id = instrument_id

        self._price = price

        self._date = date

    def get_instrument_id(self):
        return self._instrument_id

    def get_price(self):
        return self._price

    def get_date(self):
        return self._date


class Position(Base):

    __tablename__ = "position"

    line_nb: Mapped[float] = mapped_column(primary_key=True, autoincrement=True)

    portfolio_id: Mapped[str] = mapped_column()

    instrument: Mapped[str] = mapped_column()

    quantity: Mapped[int] = mapped_column()

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


class Portfolio(Base):

    __tablename__ = "portfolio"

    portfolio_id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()

    def __init__(self, portfolio_id: str, name: str):

        super().__init__()

        self._portfolio_id = portfolio_id

        self._name = name

        self.composition: list[Position] = []

    def get_portfolio_id(self):
        return self._portfolio_id

    def get_name(self):
        return self._name

    def get_composition(self):
        return self.composition

    def add_positions(self, positions: list[Position]):
        self.composition.extend(positions)






