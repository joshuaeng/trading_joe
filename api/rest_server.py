from service.listing_service.listing_service import load_listing, load_all_listings
from service.instrument_service.instrument_service import load_instrument
from service.portfolio_service.portfolio_service import (
    load_user_portfolios,
    create_portfolio,
    load_portfolio_from_id,
)
from service.user_service.user_service import load_user, create_user, load_user_from_id
from service.transaction_service.transaction_service import create_transaction, load_transactions_from_portfolio
from service.position_service.position_service import calculate_net_position

from fastapi import FastAPI, HTTPException
from datetime import datetime


app = FastAPI(
    title="TradingJoe",
    docs_url="/",
)


@app.get("/user")
def get_user(username: str, password: str) -> dict:
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
def post_user(username: str, password: str) -> dict:
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
def get_portfolios(user_id: str) -> dict:
    """
    Loads all portfolios linked to the user.
    Args:
        user_id: if of the user.

    Returns:
        JSON representation of the linked portfolios.
    """
    try:
        user = load_user_from_id(user_id)
        portfolio_list = load_user_portfolios(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return {
        portfolio.get_attribute("name"): portfolio.to_json()
        for portfolio in portfolio_list
    }


@app.post("/portfolio/create")
def post_portfolio(name: str, user_id: str) -> dict:
    """
    Creates new portfolio
    Args:
        name: name of the portfolio.
        user_id: id of the user.

    Returns:
        JSON representation of the new portfolio.
    """
    try:
        user = load_user_from_id(user_id)
        new_portfolio = create_portfolio(name, user)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return new_portfolio.to_json()


@app.get("/listing")
def get_listings(date: str) -> dict:
    """
    Gets all listings.
    Args:
        date: date in "YYYY-MM-DD" format.
    Returns:
        JSON representation of all listings.
    """
    try:
        date = datetime.strptime(date, "YYYY-MM-DD")
        listings = load_all_listings(date)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return {listing.instrument_id: listing.to_json() for listing in listings}


@app.post("/transaction/create")
def post_transaction(ric: str, quantity: int, portfolio_id: str) -> dict:
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
        portfolio = load_portfolio_from_id(portfolio_id)
        old_transactions = load_transactions_from_portfolio(portfolio)
        position_map = calculate_net_position(old_transactions)
        expected_net_position_after_transaction = position_map[ric] + quantity

        if expected_net_position_after_transaction < 0:
            raise Exception(f"Cannot short sell.")

        else:
            instrument = load_instrument(ric)
            listing = load_listing(instrument)
            create_transaction(listing, quantity, portfolio)

    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

    return {
        "transaction": {
            "instrument": ric,
            "quantity:": quantity,
            "execution_price": listing.price,
            "portfolio": portfolio.name,
        },
        "status": "booked"
    }
