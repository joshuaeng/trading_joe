from service.market_data_service.market_data_service import MarketDataService
from core.object_service.object_service import RemoteObjectService

with RemoteObjectService() as roj:

    action_apple = roj.get_object("INSTRUMENT", object_primary_key="AAPL")

mds = MarketDataService()

aapl_listing = mds.get_listings([action_apple])



