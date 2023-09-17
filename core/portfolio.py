from instrument import Instrument


class Portfolio:
    def __init__(self):
        self.composition = dict()
        self.value = None
        self.transaction_history = None

    def add_instrument(self, instrument: Instrument, quantity: int):
        self.composition.update(
            {
                instrument: quantity
            }
        )

    def calculate_value(self):
        value = 0
        for instrument, quantity in self.composition.items():
            value += instrument.last_price * quantity

        self.value = value

