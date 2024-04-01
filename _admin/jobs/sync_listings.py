from loguru import logger
from core.data_object_store.data_object_store import Instrument, Listing
from service.instrument_service.instrument_service import load_all_instruments
from service.listing_service.listing_service import create_listing, persist_listing
from service.market_data_service.market_data_service import get_last_price


def create_listing_from_instrument(instrument: Instrument):
    price: float = get_last_price(instrument)
    listing: Listing = create_listing(instrument, price)

    return listing


def main():
    instruments: list[Instrument] = load_all_instruments()

    if not instruments:
        raise Exception("There are no instruments in the Database.")

    for instrument in instruments:
        if instrument.get_attribute("asset_type") == "Stock":
            try:
                listing: Listing = create_listing_from_instrument(instrument)
                persist_listing(listing)

            except Exception as e:
                logger.exception(f"{e}")


if __name__ == "__main__":
    main()
