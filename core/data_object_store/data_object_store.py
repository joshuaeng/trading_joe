from sqlalchemy import Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from utils.utils import get_uuid


class Base(DeclarativeBase):
    pass


class BaseDataObject(Base):
    __tablename__ = "baseobject"

    id = mapped_column("id", String, primary_key=True)

    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "baseobject",
        "polymorphic_on": "type"
    }

    def set_attribute(self, **kwargs):
        for element in kwargs:

            if element not in self.fields:

                raise Exception(
                    f"'{element.capitalize()}' is not an attribute of {self.__class__.__name__}. "
                    f"Attributes of {self.__class__.__name__} are: {self.fields}"
                )

        self.__dict__.update(**kwargs)

        return self

    def get_attribute(self, attribute: str):
        return self.__getattribute__(attribute)

    @property
    def fields(self):
        return [
            key for key in self.__class__.__dict__.keys() if not key.startswith("_")
        ]

    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return f"{self.__class__.__name__.upper()}('{self.id}')"


class Instrument(BaseDataObject):
    __tablename__ = "instrument"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String)

    asset_type = mapped_column("asset_type", String)

    status = mapped_column("status", String)

    __mapper_args__ = {
        "polymorphic_identity": "instrument",
    }

    def __init__(
            self,
            instrument_id: str = None,
            name: str = None,
            asset_type: str = None,
            status: str = None
    ):

        super().__init__()

        self.id = instrument_id

        self.name = name

        self.asset_type = asset_type

        self.status = status


class Listing(BaseDataObject):
    __tablename__ = "listing"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    instrument_id = mapped_column(String, ForeignKey("instrument.id"))

    date = mapped_column("date", Date)

    price = mapped_column("price", Float)

    __mapper_args__ = {
        "polymorphic_identity": "listing",
    }

    def __init__(
            self,
            listing_id: str = None,
            instrument_id: str = None,
            date: datetime.date = None,
            time: int = None,
            price: float = None
    ):

        super().__init__()

        self.id = get_uuid() if listing_id is None else listing_id

        self.instrument_id = instrument_id

        self.date = date

        self.time = time

        self.price = price


class Transaction(BaseDataObject):
    __tablename__ = "transaction"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    portfolio_id = mapped_column(String, ForeignKey("portfolio.id"))

    instrument_id = mapped_column(String, ForeignKey("instrument.id"))

    quantity = mapped_column("quantity", Integer)

    buy_price = mapped_column("buy_price", Float)

    date = mapped_column("date", Date)

    __mapper_args__ = {
        "polymorphic_identity": "transaction",
    }

    def __init__(
            self,
            transaction_id: str = None,
            instrument_id: str = None,
            portfolio_id: str = None,
            quantity: int = None
    ):

        super().__init__()

        self.id = get_uuid() if transaction_id is None else transaction_id

        self.instrument_id = instrument_id

        self.portfolio_id = portfolio_id

        self.quantity = quantity


class Portfolio(BaseDataObject):
    __tablename__ = "portfolio"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String)

    user_id = mapped_column(String, ForeignKey("user.id"))

    __mapper_args__ = {
        "polymorphic_identity": "portfolio",
    }

    def __init__(
            self,
            portflio_id: str = None,
            name: str = None,
            user_id: str = None
    ):

        super().__init__()

        self.id = get_uuid() if portflio_id is None else portflio_id

        self.name = name

        self.user_id = user_id


class User(BaseDataObject):
    __tablename__ = "user"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String)

    __mapper_args__ = {
        "polymorphic_identity": "user",
    }

    def __init__(
            self,
            user_id: str = None,
            name: str = None
    ):

        super().__init__()

        self.id = get_uuid() if user_id is None else user_id

        self.name = name


class TradingSession(BaseDataObject):
    __tablename__ = "trading_session"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String)

    user_id = mapped_column(String, ForeignKey("user.id"))

    portfolio_id = mapped_column(String, ForeignKey("portfolio.id"))

    __mapper_args__ = {
        "polymorphic_identity": "trading_session",
    }

    def __init__(
            self,
            session_id: str = None,
            user_id: str = None,
            portfolio_id: str = None
    ):
        super().__init__()
        self.id = get_uuid() if session_id is None else session_id
        self.user_id = user_id
        self.portfolio_id = portfolio_id






















