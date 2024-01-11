from typing import Union

from core.object_service.object_service import RemoteObjectService
from core.data_object_store.data_object_store import *


class PositionService:
    def __init__(self):
        pass

    @staticmethod
    def _get_quantity(transaction_list: Union[list[Transaction], Transaction], instrument: Instrument):

        if not isinstance(transaction_list, list):
            transaction_list = [transaction_list]

        quantities = [
            transaction.quantity for transaction in transaction_list
            if transaction.instrument_id == instrument.id
        ]

        return sum(quantities)

    def _aggregate_transactions(self, transaction_list: Union[list[Transaction], Transaction]):

        if not isinstance(transaction_list, list):
            transaction_list = [transaction_list]

        instrument_ids = list(set([transaction.instrument_id for transaction in transaction_list]))

        with RemoteObjectService() as roj:
            instruments = roj.get_object("INSTRUMENT", filter_expression=Instrument.id.in_(instrument_ids))

            if isinstance(instruments, list):
                position_dictionary = {}
                for instrument in instruments:
                    position_dictionary.update({instrument.id: self._get_quantity(transaction_list, instrument)})

            else:
                position_dictionary = {instruments.id: self._get_quantity(transaction_list, instruments)}

        return position_dictionary

    def evaluate_positions(self, portfolio: Portfolio):

        with RemoteObjectService() as roj:

            transactions = roj.get_object(
                "TRANSACTION",
                filter_expression=Transaction.portfolio_id == portfolio.id
            )

        return self._aggregate_transactions(transactions)




