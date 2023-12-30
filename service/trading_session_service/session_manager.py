from core.object_service.object_service import Instrument, User, Listing, Portfolio, RemoteObjectService, func, create_object


class TradingSession:

    def __init__(self, user: User):

        self.user = user

        self.portfolio = None

        self.portfolio_list = None

    @staticmethod
    def new_portfolio():
        return create_object("PORTFOLIO")

    def load_all_portfolios(self):

        with RemoteObjectService() as objs:

            portfolio_list = objs.get_list_filter("PORTFOLIO", Portfolio.user_id == self.user.id)

        return portfolio_list

    def chose_portfolio(self, portfolio: Portfolio):

        with RemoteObjectService() as objs:

            self.portfolio = objs.get_object("PORTFOLIO", portfolio.id)

    @staticmethod
    def load_all_listings():

        with RemoteObjectService() as roj:

            instruments = roj.get_list("INSTRUMENT")

        return []

    def create_transaction(self, instrument: Instrument, quantity: int):

        transaction = create_object("TRANSACTION")

        transaction.set_attribute(
            instrument_id=instrument.get_attribute("instrument_id"),
            portfolio_id=self.portfolio.get_attribute("portfolio_id"),
            quantity=quantity
        )

        with RemoteObjectService() as objs:

            objs.persist_object([transaction])











