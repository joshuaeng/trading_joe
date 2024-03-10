from core.data_object_store.data_object_store import Portfolio, User
from core.object_service.object_service import RemoteObjectService, create_object


def load_portfolio_from_id(portfolio_id: str) -> Portfolio:
    """
    Loads the portfolio object associated to input portfolio id.
    Args:
        portfolio_id: id of the target portfolio

    Returns:
        target portfolio

    """
    with RemoteObjectService() as roj:
        resp = roj.get_object(portfolio_id)
        portfolio = resp.extract_object()

    return portfolio


def load_user_portfolios(user: User) -> list[Portfolio]:
    """
    Loads all portfolios linked to the user.
    Args:
        user:target user.

    Returns:
        JSON representation of the linked portfolios.
    """
    with RemoteObjectService() as roj:
        resp = roj.get_object("PORTFOLIO", Portfolio.user_id == user.id)
        portfolio_list = resp.extract_object(force_to_list=True)

    return portfolio_list


def create_portfolio(name: str, user: User) -> Portfolio:
    """
    Creates new portfolio
    Args:
        name: name of the portfolio.
        user: target user.

    Returns:
        JSON representation of the new portfolio.
    """
    with RemoteObjectService() as roj:
        new_portfolio = create_object("PORTFOLIO")

        new_portfolio.set_attribute(user_id=user.id, name=name)
        roj.persist_object([new_portfolio])

    return new_portfolio
