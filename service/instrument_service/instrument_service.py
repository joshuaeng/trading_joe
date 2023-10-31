from core.database_service.db_connector import DBConnector
from core.object_store import Instrument


class _NotAnInstrument(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class InstrumentService:
    """
    Allows to fetch/insert instruments from/into the trading_joe database.
    """
    def __init__(self):
        self.dbc = DBConnector()

    @staticmethod
    def new_instrument(instrument_id: str, name: str) \
            -> Instrument:

        return Instrument(
            instrument_id=instrument_id,
            name=name
        )

    def get_instrument(self, instrument_id: str) -> Instrument:

        return self.dbc.get_object(
            object_type=Instrument,
            object_primary_key=instrument_id
        )

    def persist_instrument(self, instrument: Instrument) -> None:

        self.dbc.persist_object(obj=instrument)




