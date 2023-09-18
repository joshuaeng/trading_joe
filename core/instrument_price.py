from datetime import datetime


class InstrumentPrice:
    def __init__(
            self,
            price: float = None,
            date: datetime = None
    ):

        self.price = price

        self.date = date
