from abc import ABC, abstractmethod
from instrument import Instrument
from database_connector.db_connector import DBConnector


class BasePricer(ABC):
    def __init__(
            self,
            instrument: Instrument
    ):

        self.instrument = instrument

        self.connector = DBConnector()

    @abstractmethod
    def pricing_model(self):
        pass

    def price_security(self):
        return self.pricing_model()


class EquityPricer(BasePricer):
    def __init__(
            self,
            instrument: Instrument
    ):

        super().__init__(instrument)

        self.vol \
            = None

    def pricing_model(self):
        pass


