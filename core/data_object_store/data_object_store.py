from sqlalchemy import Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from utils.utils import get_uuid


class Base(DeclarativeBase):
    pass


class BaseDataObject(Base):
    __tablename__ = "baseobject"

    id = mapped_column("id", String(50), primary_key=True)

    type = mapped_column("type", String(50))

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
        json = self.__dict__
        return {key: value for key, value in json.items() if not key.startswith("_")}

    def __repr__(self):
        return f"{self.__class__.__name__.upper()}('{self.id}')"


class User(BaseDataObject):
    __tablename__ = "user"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    password = mapped_column("password", String(50))

    __mapper_args__ = {
        "polymorphic_identity": "user",
    }

    def __init__(
            self,
            username: str = None,
            password: str = None
    ):

        super().__init__()

        self.id = username

        self.password = password


class Instrument(BaseDataObject):
    __tablename__ = "instrument"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String(100))

    asset_type = mapped_column("asset_type", String(50))

    status = mapped_column("status", String(50))

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

    instrument_id = mapped_column(String(50), ForeignKey("instrument.id"))

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


class Portfolio(BaseDataObject):
    __tablename__ = "portfolio"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    name = mapped_column("name", String(50))

    user_id = mapped_column(String(50), ForeignKey("user.id"))

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


class Transaction(BaseDataObject):
    __tablename__ = "transaction"

    id = mapped_column(ForeignKey("baseobject.id"), primary_key=True)

    portfolio_id = mapped_column(String(50), ForeignKey("portfolio.id"))

    instrument_id = mapped_column(String(50), ForeignKey("instrument.id"))

    quantity = mapped_column("quantity", Integer)

    price = mapped_column("price", Float)

    date = mapped_column("date", Date)

    __mapper_args__ = {
        "polymorphic_identity": "transaction",
    }

    def __init__(
            self,
            transaction_id: str = None,
            instrument_id: str = None,
            portfolio_id: str = None,
            quantity: int = None,
            price: float = None,
            date: str = None
    ):

        super().__init__()

        self.id = get_uuid() if transaction_id is None else transaction_id

        self.instrument_id = instrument_id

        self.portfolio_id = portfolio_id

        self.date = date

        self.quantity = quantity

        self.price = price


object_list = [_obj for _obj in BaseDataObject.__subclasses__()]
table_list = [BaseDataObject.__table__]
table_list.extend([_obj.__table__ for _obj in object_list])



















