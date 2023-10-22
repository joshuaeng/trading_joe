from instrument_service.instrument_service import InstrumentService

instrument_service = InstrumentService()

instrument_retreived = instrument_service.get_instrument(instrument_id="test_new")

instrument_retreived.price = 1555

instrument_service.persist_instrument(instrument_retreived)

print("t")







