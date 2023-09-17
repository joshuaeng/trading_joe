from datetime import datetime


class InstrumentPrice:
    """InstrumentPrice blueprint"""
    def __init__(
            self,
            price: float = None,
            date: datetime = None
    ):

        self.price = price

        self.date = date
