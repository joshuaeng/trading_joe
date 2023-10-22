from core.database_connector.db_connector import DBConnector
from core.object_store import Instrument
from sqlalchemy import select


class NotAnInstrument(Exception):
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

        with self.dbc.orm_session() as session, session.begin():

            instrument = session.scalars(
                statement=select(Instrument).filter_by(
                    instrument_id=instrument_id
                    )
            ).all()[0]

            session.expunge(instrument)

        return instrument

    def persist_instrument(self, instrument: Instrument):

        if not isinstance(instrument, Instrument):

            raise NotAnInstrument(f"{instrument} is not an object of type Instrument.")

        with self.dbc.orm_session() as session, session.begin():

            session.add(instrument)

            session.commit()
