from service.market_data_service.market_data_service import MarketDataService

if __name__ == "__main__":
    mds = MarketDataService()
    mds.sync_listings()
