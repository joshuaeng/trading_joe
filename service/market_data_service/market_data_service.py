import csv
import requests
import warnings
from loguru import logger
from service.market_data_service.config import API_KEY
from core.object_service.object_service import RemoteObjectService, create_object
from core.data_object_store.data_object_store import *
from yahoo_fin.stock_info import get_live_price


warnings.filterwarnings("ignore", category=DeprecationWarning)


def _get_instruments_data(self):
    with requests.Session() as s:
        download = s.get(f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}")
        decoded_content = download.content.decode('utf-8')
        my_list = csv.reader(decoded_content.splitlines(), delimiter=',')

    return {
            _list[0]: _list[0:] for _list in my_list if _list[0] != "symbol"
    }


def get_all_instruments(self):

    all_instruments_data = self._get_instruments_data()
    instrument_list = []

    for ric, data in all_instruments_data.items():

        instrument = create_object(
            "INSTRUMENT",
            instrument_id=data[0],
            name=data[1],
            asset_type=data[3],
            status=data[6]
        )

        if len(instrument.get_attribute("name")) <= 40:
            instrument_list.append(instrument)

    return instrument_list


def sync_instruments(self):

    instrument_list = self.get_all_instruments()

    with RemoteObjectService() as roj:
        roj.persist_object(instrument_list)


def get_price(instrument: Instrument):
    return get_live_price(instrument.id)


def create_listing_from_instrument(instrument: Instrument):
    price = get_price(instrument)
    return create_object(
        object_type="LISTING",
        instrument_id=instrument.id,
        date=datetime.now().strftime("%Y-%m-%d"),
        price=price
    )


def sync_listing(listing):
    with RemoteObjectService() as roj:
        roj.persist_object(listing)


def sync_listings():
    with RemoteObjectService() as roj:
        resp = roj.get_object("INSTRUMENT", filter_expression=Instrument.status == "Active")
        instruments = resp.export(force_to_list=True)

    if not instruments:
        raise Exception("There are no instruments in the Database.")

    for instrument in instruments:
        if instrument.get_attribute("asset_type") == "Stock":
            try:
                listing = create_listing_from_instrument(instrument)
                sync_listing([listing])

            except Exception as e:
                logger.exception(f"{e}")
























