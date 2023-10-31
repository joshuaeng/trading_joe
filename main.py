from service.instrument_service.instrument_service import InstrumentService

instrument_service = InstrumentService()

instrument_test = instrument_service.new_instrument(instrument_id="quentin", name="quentin_")

instrument_test.price = 100

instrument_service.persist_instrument(instrument_test)

instrument_retreived = instrument_service.get_instrument(instrument_id="quentin")

instrument_retreived.price = 1555

instrument_service.persist_instrument(instrument_retreived)

print("t")







