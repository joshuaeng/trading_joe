from core.object_service.object_service import ObjectService, Instrument

object_service = ObjectService()

instrument = object_service.create_object(Instrument, name="test_final", price=99.99)

instr = object_service.update_object(instrument, price=70)

