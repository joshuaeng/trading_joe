from sqlalchemy import Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime
Base = declarative_base()


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

    def __init__(self, instrument_id: str, name: str, asset_type: str, status: str):

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

    def __init__(self, listing_id: str, instrument_id: int, date: datetime, time: int, price: float):

        super().__init__()

        self.id = listing_id

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

    __mapper_args__ = {
        "polymorphic_identity": "transaction",
    }

    def __init__(self, transaction_id: int, instrument_id: int, portfolio_id: int, quantity: int):

        super().__init__()

        self.id = transaction_id

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

    def __init__(self, portflio_id: int, name: str, user_id: int):

        super().__init__()

        self.id = portflio_id

        self.name = name

        self.user_id = user_id


class User(BaseDataObject):
    __tablename__ = "user"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String)

    __mapper_args__ = {
        "polymorphic_identity": "user",
    }

    def __init__(self, user_id: int, name: str):

        super().__init__()

        self.id = user_id

        self.name = name























