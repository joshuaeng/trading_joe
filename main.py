from core.instrument import Instrument
from instrument_service.instrument_service import InstrumentService

instrument = Instrument(
    instrument_id="instrument_3",
    name="test_instrument"
)

_is = InstrumentService()

instrument_inst = _is.get_instrument([instrument.instrument_id])




