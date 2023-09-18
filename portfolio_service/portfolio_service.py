from core.portfolio import Portfolio, PortfolioComponent
from database_connector.db_connector import DBConnector


class PortfolioService:
    def __init__(self):
        self.dbc = DBConnector()

    @staticmethod
    def new_portfolio(composition: list[PortfolioComponent]):

        return Portfolio(

            composition=composition

        )

    def charge_portfolio(self):
        pass

    def persist_portfolio(self):
        pass

    def delete_portfolio(self):
        pass

