from core.object_service.object_service import ObjectService, Instrument

object_service = ObjectService()

instrument_list = object_service.get_list(Instrument)

inst = instrument_list[0]



