from core.object_service.object_service import RemoteObjectService, create_object

with RemoteObjectService() as object_service:

    user_1 = create_object("USER")

    broker = create_object("BROKER")

    portfolio = create_object("PORTFOLIO")

    trading_session = create_object("TRADING_SESSION")

