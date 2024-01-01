from core.object_service.object_service import \
    RemoteObjectService, \
    Portfolio, \
    Transaction, \
    Instrument


class PositionService:
    def __init__(self):
        pass

    @staticmethod
    def _get_quantity(transaction_list: list[Transaction], instrument: Instrument):

        quantities = [
            transaction.quantity for transaction in transaction_list
            if transaction.instrument_id == instrument.id
        ]

        return sum(quantities)

    def _aggregate_transactions(self, transaction_list: list[Transaction]):

        instrument_ids = list(set([transaction.instrument_id for transaction in transaction_list]))
        with RemoteObjectService() as roj:
            instuments = roj.get_object("INSTRUMENT", filter_expression=Instrument.id in instrument_ids)

        position_dictionary = {
            instrument: self._get_quantity(transaction_list, instrument) for instrument in instuments
        }

        return position_dictionary

    def evaluate_positions(self, portfolio: Portfolio):

        with RemoteObjectService() as roj:

            transactions = roj.get_object(
                "TRANSACTION",
                filter_expression=Transaction.portfolio_id == portfolio.id
            )

        return self._aggregate_transactions(transactions)




