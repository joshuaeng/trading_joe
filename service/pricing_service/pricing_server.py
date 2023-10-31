from core.database_service.db_connector import DBConnector
from core.object_store import Instrument, InstrumentPrice
from abc import ABC, abstractmethod


class Pricer(ABC):

    @abstractmethod
    def price(self, instrument: Instrument):
        pass


class EquityInstrumentPricer(Pricer):

    def __init__(self):
        pass

    def price(self, instrument: Instrument):
        pass


class PricingService:

    pricer: Pricer

    def __init__(self):

        self.dbc = DBConnector()

    def set_pricer(self, pricer: Pricer):
        self.pricer = pricer

    def price_instrument(self, instrument: Instrument) -> InstrumentPrice:
        return self.pricer.price(instrument)
