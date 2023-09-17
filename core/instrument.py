from core.instrument_price import InstrumentPrice


class Instrument:
    """Instrument blueprint"""
    def __init__(
            self,
            instrument_id=None,
            name=None,
            price=None
    ):

        self.instrument_id: str = instrument_id

        self.name: str = name

        self.price: InstrumentPrice = price

    def __repr__(self):
        return f"INSTRUMENT('{self.instrument_id}')"

    def __str__(self):
        return self.instrument_id

