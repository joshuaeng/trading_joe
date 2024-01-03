import datetime
from core.object_service.object_service import Instrument, User, TradingSession, Listing, Portfolio, RemoteObjectService, create_object
from service.market_data_service.market_data_service import MarketDataService
from service.position_service.position_service import PositionService
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/user")
def get_user(user_name: str) -> dict:
    with RemoteObjectService() as roj:
        user = roj.get_object("USER", filter_expression=User.name == user_name)

    return user.to_json()


@app.post(path="/user/create")
def create_new_user(user_name: str) -> dict:
    new_user = create_object("USER", name=user_name)

    with RemoteObjectService() as roj:
        roj.persist_object(obj_list=[new_user])

    return new_user.to_json()


@app.post("/portfolio/create")
def create_new_portfolio(name: str, user_id: str) -> dict:

    new_portfolio = create_object("PORTFOLIO")

    new_portfolio.set_attribute(
        user_id=user_id,
        name=name
    )

    with RemoteObjectService() as roj:
        roj.persist_object([new_portfolio])

    return new_portfolio.to_json()


@app.get("/tradingsession")
def load_trading_session(user_id: str) -> dict:
    with RemoteObjectService() as roj:
        trading_session = roj.get_object("TRADINGSESSION", filter_expression=TradingSession.user_id == user_id)

    return trading_session.to_json()


@app.post("/tradingsession/ceate")
def create_new_trading_session(user_id: str, portfolio_id: str) -> dict:
    trading_session = create_object("TRADING_SESSION")
    trading_session.set_attribute(
        user_id=user_id,
        portfolio_id=portfolio_id
    )

    return trading_session.to_json()


@app.get("/portfolio")
def load_user_portfolios(user_id: str) -> dict:
    """Shows all portfolios assigned to user.

    Returns:
        List of portfolios.
    """

    with RemoteObjectService() as roj:

        portfolio_list = roj.get_object("PORTFOLIO", Portfolio.user_id == user_id)

    return {portfolio.name: portfolio.to_json() for portfolio in portfolio_list}


@app.get("/listing")
def load_all_listings() -> dict:

    with RemoteObjectService() as roj:

        instruments: list[Instrument] = roj.get_object("INSTRUMENT")

    listings = MarketDataService().get_listings(instruments)

    return {listing.instrument_id: listing.to_json() for listing in listings}


@app.post("/transaction/create")
def create_transaction(listing_id: str, quantity: int, portfolio_id: str) -> None:

    with RemoteObjectService() as roj:
        listing: Listing = roj.get_object("LISTING", filter_expression=Listing.id == listing_id)

    transaction = create_object("TRANSACTION")

    transaction.set_attribute(
        instrument_id=listing.instrument_id,
        portfolio_id=portfolio_id,
        quantity=quantity,
        date=datetime.datetime.now().strftime("%Y-%m-%d"),
        buy_price=listing.price
    )

    with RemoteObjectService() as objs:

        objs.persist_object([transaction])


@app.post("/portfolio/evaluate")
def evaluate_portfolio(portfolio_id: str) -> dict:
    with RemoteObjectService() as roj:
        portfolio: Portfolio = roj.get_object("PORTFOLIO", filter_expression=Portfolio.id == portfolio_id)
    return PositionService().evaluate_positions(portfolio)


if __name__ == "__main__":
    uvicorn.run(app)







