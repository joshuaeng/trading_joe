from core.object_service.object_service import ObjectService

with ObjectService() as object_service:

    instrument = object_service.create_object("INSTRUMENT")

    x = object_service.get_list("INSTRUMENT")

    instrument.set_attribute(id=1)

    portfolio = object_service.create_object("PORTFOLIO")

    position = object_service.create_object("POSITION")

    object_service.persist([position])
