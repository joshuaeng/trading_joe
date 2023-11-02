from core.object_service.object_service import ObjectService

with ObjectService() as object_service:

    instrument = object_service.create_object("INSTRUMENT", name="TESLA_UQ", price=100, id=1)

    portfolio = object_service.create_object("PORTFOLIO", name="test", id=1)

    position = object_service.create_object("POSITION", id=6, portfolio_id=2, instrument_id=1)

    object_service.persist([position])
