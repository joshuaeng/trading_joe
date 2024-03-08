from core.data_object_store.data_object_store import Listing, Instrument
from core.object_service.object_service import RemoteObjectService, create_object
from datetime import datetime


def create_listing(instrument: Instrument, price: float) -> Listing:
    return create_object(
        object_type="LISTING",
        instrument_id=instrument.id,
        date=datetime.now().strftime("%Y-%m-%d"),
        price=price
    )


def persist_listing(listing: Listing) -> None:
    with RemoteObjectService() as roj:
        roj.persist_object([listing])


def load_listing(instrument: Instrument, date: datetime = None) -> Listing:
    date = datetime.now() if date is None else date
    with RemoteObjectService() as roj:
        resp = roj.get_object(
            "LISTING",
            (Listing.instrument_id == instrument.id).__and__(Listing.date == date.strftime("%Y-%m-%d"))
        )

        return resp.extract_object()


def load_all_listings(date: datetime) -> list[Listing]:
    with RemoteObjectService() as roj:
        resp = roj.get_object("LISTING", Listing.date == date.strftime("%Y-%m-%d"))

    return resp.extract_object(force_to_list=True)


