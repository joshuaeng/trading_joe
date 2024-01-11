import datetime

import requests
from service.market_data_service.config import API_KEY
import csv
from enum import Enum
from core.object_service.object_service import RemoteObjectService, create_object
from core.data_object_store.data_object_store import *
from yahoo_fin.stock_info import get_live_price


class Function(str, Enum):

    LISTING_STATUS = "LISTING_STATUS"

    def __str__(self):
        return self.value


class URLBuilder:
    @staticmethod
    def _kwarg_to_str(**kwargs) -> str:
        _str = ""

        for key, value in kwargs.items():
            _str = f"&{key}={value}"

        return _str

    def build_url(self, function: Function, **kwargs):

        return f"https://www.alphavantage.co/query?function=" \
               f"{function + self._kwarg_to_str(**kwargs)}" \
               f"&apikey={API_KEY}"


class MarketDataService:

    def __init__(self):

        self.url_builder = URLBuilder()

    def _get_instruments_data(self):

        url = self.url_builder.build_url(function=Function.LISTING_STATUS)

        with requests.Session() as s:
            download = s.get(url)
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

            instrument_list.append(instrument)

        return instrument_list

    def sync_instruments(self):

        instrument_list = self.get_all_instruments()

        with RemoteObjectService() as roj:
            roj.persist_object(instrument_list)

    @staticmethod
    def get_price(instrument: Instrument):
        return get_live_price(instrument.id)

    def get_listing(self, instrument: Instrument):
        return create_object(
            object_type="LISTING",
            instrument_id=instrument.id,
            date=datetime.date.today().strftime("%Y-%m-%d"),
            time=datetime.datetime.now().strftime("%H"),
            price=self.get_price(instrument)
        )

    def get_listings(self, instrument_list: list[Instrument]):
        return [self.get_listing(instrument) for instrument in instrument_list]

    def sync_listings(self):
        with RemoteObjectService() as roj:
            instruments = roj.get_object("INSTRUMENT", filter_expression=Instrument.status == "Active")
            listings = self.get_listings(instruments)
            roj.persist_object(listings)
























