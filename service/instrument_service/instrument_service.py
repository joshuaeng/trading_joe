from core.object_service.object_service import create_object, RemoteObjectService
from core.data_object_store.data_object_store import Instrument


def _load_instrument(instrument_id: str, con: RemoteObjectService) -> Instrument:
    instrument = con.get_object("INSTRUMENT", Instrument.id == instrument_id)

    return instrument.extract_object()


def create_instrument(**kwargs) -> Instrument:
    with RemoteObjectService() as roj:
        instrument = create_object("INSTRUMENT", **kwargs)
        roj.persist_object([instrument])
        instrument = _load_instrument(kwargs.get("instrument_id"), con=roj)

    return instrument


def load_instrument(instrument_id: str) -> Instrument:
    with RemoteObjectService() as roj:
        instrument = _load_instrument(instrument_id, con=roj)

    return instrument


def load_all_instruments(active_only: bool = True) -> list[Instrument]:
    with RemoteObjectService() as roj:

        resp \
            = roj.get_object("INSTRUMENT", filter_expression=Instrument.status == "Active") \
            if active_only else roj.get_object("INSTRUMENT")

        instrument_list = resp.extract_object(force_to_list=True)

    return instrument_list

