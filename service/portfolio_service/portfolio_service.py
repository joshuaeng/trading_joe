from core.object_store import Position, Portfolio
from core.database_service.db_connector import DBConnector


class PortfolioService:
    def __init__(self):

        self.dbc = DBConnector()

    @staticmethod
    def create_portfolio(
            portfolio_id: str,
            name: str,
            positions: list[Position] = None
            ) -> Portfolio:

        ptf = Portfolio(
            portfolio_id=portfolio_id,
            name=name
        )

        ptf.add_positions(positions)

        return ptf

    def persist_portfolio(self, position_list: list[Position]) -> None:
        pass

    def get_portfolio(self, portfolio_id):
        return self.dbc.get_object(
            object_type=Portfolio,
            object_primary_key=portfolio_id
        )




