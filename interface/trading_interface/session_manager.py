import datetime
from core.object_service.object_service import Instrument, User, Listing, Portfolio, RemoteObjectService, create_object
from service.market_data_service.market_data_service import MarketDataService
from service.position_service.position_service import PositionService


class TradingSession:
    """Allows to instanciate a TradingSession object.

    Args:
        user: user
        portfolio: portfolio

    Example:

    """

    def __init__(self, user: User, portfolio: Portfolio = None) -> None:

        self.user: User = user

        self.active_portfolio: Portfolio = portfolio

    def new_portfolio(self, name: str) -> None:
        new_portfolio = create_object("PORTFOLIO")

        new_portfolio.set_attribute(
            user_id=self.user.id,
            name=name
        )

        self.active_portfolio = new_portfolio

        with RemoteObjectService() as roj:
            roj.persist_object([new_portfolio])

    def load_existing_portfolios(self):

        with RemoteObjectService() as roj:

            portfolio_list = roj.get_object_list("PORTFOLIO", Portfolio.user_id == self.user.id)

        return portfolio_list

    def set_active_portfolio(self, portfolio: Portfolio) -> None:

        self.active_portfolio = portfolio

    @staticmethod
    def load_all_listings():

        with RemoteObjectService() as roj:

            instruments: list[Instrument] = roj.get_object_list("INSTRUMENT")

        return MarketDataService().get_listings(instruments)

    def create_transaction(self, listing: Listing, quantity: int):

        transaction = create_object("TRANSACTION")

        transaction.set_attribute(
            instrument_id=listing.instrument_id,
            portfolio_id=self.active_portfolio.id,
            quantity=quantity,
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
            buy_price=listing.price
        )

        with RemoteObjectService() as objs:

            objs.persist_object([transaction])

    def show_active_portfolio(self):
        if self.active_portfolio is None:

            return "No active portfolio is set."

        else:
            return PositionService().evaluate_positions(self.active_portfolio)











