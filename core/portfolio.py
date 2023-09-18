from instrument import Instrument


class PortfolioComponent:
    def __init__(self, instrument: Instrument, quantity: int):

        self.instrument: Instrument = instrument

        self.quantity: int = quantity

    def __repr__(self):
        return {self.instrument.name: self.quantity}


class Portfolio:
    def __init__(
            self,
            composition=None
    ):

        self.composition: list[PortfolioComponent] \
            = [] if composition is None else composition

        self.value = None

    def add_instrument(self, instrument_to_add: Instrument, quantity: int):
        self.composition.append(

            PortfolioComponent(

                instrument=instrument_to_add,

                quantity=quantity

            )

        )

    def calculate_value(self):
        value = 0

        for component in self.composition:

            value += component.instrument.price.price * component.quantity

        self.value = value



