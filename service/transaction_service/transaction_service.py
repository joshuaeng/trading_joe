from core.data_object_store.data_object_store import Listing, Portfolio, Transaction
from core.object_service.object_service import RemoteObjectService, create_object


def create_transaction(listing: Listing, quantity: int, portfolio: Portfolio) -> None:
    """
    Creates a transaction.
    Args:
        listing: target listing.
        quantity: quantity to transact. Negative when sold.
        portfolio: targetportfolio.

    Returns:
        JSON representation of the created transaction.
    """

    with RemoteObjectService() as roj:
        transaction = create_object(
            "TRANSACTION",
            instrument_id=listing.instrument_id,
            listing_id=listing.id,
            portfolio_id=portfolio.id,
            quantity=quantity,
        )

        roj.persist_object([transaction])


def load_transactions_from_portfolio(portfolio: Portfolio) -> list[Transaction]:
    with RemoteObjectService() as roj:
        resp = roj.get_object(
            "TRANSACTION", filter_expression=Transaction.portfolio_id == portfolio.id
        )
        transaction_list = resp.extract_object(force_to_list=True)

    return transaction_list


