from core.portfolio import Portfolio, PortfolioComponent
from core.database_service.db_connector import DBConnector


class PortfolioService:
    def __init__(self):
        self.dbc = DBConnector()

    @staticmethod
    def new_portfolio(portfolio_id: str, composition: list[PortfolioComponent]):

        return Portfolio(

            portfolio_id=portfolio_id,

            composition=composition

        )

    def charge_portfolio(self, portfolio_id: str):
        portfolio_data \
            = self.dbc.query(
                query=f"SELECT * "
                      f"FROM trading_joe.portfolio "
                      f"WHERE portfolio_id = {portfolio_id}"
            )

        return Portfolio(
            portfolio_id=portfolio_id,

        )

    def persist_portfolio(self):
        pass

    def delete_portfolio(self):
        pass

