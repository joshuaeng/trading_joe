from service.market_data_service.market_data_service import get_raw_instrument_data
from service.instrument_service.instrument_service import create_instrument


def main():
    all_instruments_data = get_raw_instrument_data()
    instrument_list = []

    for ric, data in all_instruments_data.items():
        instrument = create_instrument(
            instrument_id=ric, name=data[1], asset_type=data[3], status=data[6]
        )

        if len(instrument.get_attribute("name")) <= 40:
            instrument_list.append(instrument)

    return instrument_list


if __name__ == "__main__":
    main()
