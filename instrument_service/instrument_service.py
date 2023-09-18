from database_connector.db_connector import DBConnector
from core.instrument import Instrument


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

    def _get_instrument(self, instrument_id: str) \
            -> Instrument:

        instrument_data = self.dbc.query(

            f"SELECT * "

            f"FROM trading_joe.instruments "

            f"WHERE instrument_id = '{instrument_id}'"

        )

        return Instrument(

            instrument_id=instrument_id,

            name=instrument_data[0]["name"]

        )

    def _persist_instrument(self, instrument: Instrument) \
            -> None:

        self.dbc.query(
            f"INSERT INTO trading_joe.instruments ("

            f"instrument_id, "
            f"name"

            f") "

            f"VALUES("

            f"'{None if instrument.instrument_id is None else instrument.instrument_id}', "
            f"'{None if instrument.name is None else instrument.name}'"

            f")"
        )

    def get_instrument(self, instrument_ids: list) \
            -> dict[str, Instrument]:

        instruments = dict()

        for instrument_id in instrument_ids:

            instruments.update(

                {
                    instrument_id: self._get_instrument(instrument_id)
                }

            )

            return instruments

    def persist_instruments(self, instruments: list) \
            -> None:

        for instrument in instruments:

            self._persist_instrument(instrument)

    def delete_instrument(self):
        pass









