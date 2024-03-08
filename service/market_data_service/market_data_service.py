import csv
import requests
import warnings
from service.market_data_service.config import API_KEY
from core.data_object_store.data_object_store import *
from yahoo_fin.stock_info import get_live_price


def get_raw_instrument_data() -> dict:
    with requests.Session() as session:
        download = session.get(f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}")
        decoded_content = download.content.decode('utf-8')
        my_list = csv.reader(decoded_content.splitlines(), delimiter=',')

    return {
            _list[0]: _list[0:] for _list in my_list if _list[0] != "symbol"
    }


def get_last_price(instrument: Instrument):
    return get_live_price(instrument.id)
























