from abc import ABC, abstractmethod
from core.database_service.db_connector import DBConnector
from core.instrument import Instrument


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

        self.anything = None

    def pricing_model(self):
        return self.vol + self.anything


