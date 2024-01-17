from core.object_service.object_service import RemoteObjectService, create_object
from core.data_object_store.data_object_store import *
from service.position_service.position_service import evaluate_positions
from service.user_service.user_service import load_user, create_user
from fastapi import FastAPI, HTTPException
import uvicorn


app = FastAPI(title="TradingJoe", docs_url="/")


@app.get("/user")
def load_user(username: str, password: str) -> dict:
    """
    Gets user.
    Args:
        username: name of the user.
        password: password of the userr

    Returns:
        JSON representation of user.
    """
    try:
        user = load_user(username, password)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return user.to_json()


@app.post(path="/user/create")
def create_user(username: str, password: str) -> dict:
    """
    Creates new user.
    Args:
        username: name of the new user.
        password: password of the new user.

    Returns:
        JSON representation of new user.

    """
    try:
        user = create_user(username, password)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return user.to_json()


@app.get("/portfolio")
def load_portfolios(user_id: str) -> dict:
    """
    Loads all portfolios linked to the user.
    Args:
        user_id: if of the user.

    Returns:
        JSON representation of the linked portfolios.
    """
    try:
        with RemoteObjectService() as roj:
            resp = roj.get_object("PORTFOLIO", Portfolio.user_id == user_id)
            portfolio_list = resp.export(force_to_list=True)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return {portfolio.get_attribute("name"): portfolio.to_json() for portfolio in portfolio_list}


@app.post("/portfolio/create")
def create_portfolio(name: str, user_id: str) -> dict:
    """
    Creates new portfolio
    Args:
        name: name of the portfolio.
        user_id: id of the user.

    Returns:
        JSON representation of the new portfolio.
    """
    try:
        new_portfolio = create_object("PORTFOLIO")

        new_portfolio.set_attribute(
            user_id=user_id,
            name=name
        )

        with RemoteObjectService() as roj:
            roj.persist_object([new_portfolio])

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return new_portfolio.to_json()


@app.get("/listing")
def load_listings() -> dict:
    """
    Gets all listings.
    Returns:
        JSON representation of all listings.
    """
    try:
        with RemoteObjectService() as roj:
            resp = roj.get_object("LISTING", filter_expression=Listing.date == datetime.now().strftime("%Y-%m-%d"))
            listings = resp.export(force_to_list=True)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return {listing.instrument_id: listing.to_json() for listing in listings}


@app.post("/portfolio/evaluate")
def evaluate_portfolio(portfolio_id: str) -> dict:
    """
    Evaluates the positions in a portfolio
    Args:
        portfolio_id: id of the portfolio.

    Returns:
        JSON with keys -> instrument_id and value -> quantity (int)

    """
    try:
        with RemoteObjectService() as roj:
            resp = roj.get_object("PORTFOLIO", filter_expression=Portfolio.id == portfolio_id)
            portfolio = resp.export()

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return evaluate_positions(portfolio)


@app.post("/transaction/create")
def create_transaction(ric: str, quantity: int, portfolio_id: str) -> str:
    """
    Creates a transaction.
    Args:
        ric: id of the listing.
        quantity: quantity to transact. Negative when sold.
        portfolio_id: id of the portfolio.

    Returns:
        JSON representation of the created transaction.
    """

    try:
        with RemoteObjectService() as roj:
            resp = roj.get_object("LISTING", filter_expression=(
                    Listing.instrument_id == ric).__and__(Listing.date == datetime.now().strftime("%Y-%m-%d")))
            listing = resp.export()

            transaction = create_object(
                "TRANSACTION",
                instrument_id=ric,
                portfolio_id=portfolio_id,
                quantity=quantity,
                date=datetime.now().strftime("%Y-%m-%d"),
                price=listing.get_attribute("price")
            )

            roj.persist_object([transaction])

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return "Transaction created"


if __name__ == "__main__":
    uvicorn.run(app)







