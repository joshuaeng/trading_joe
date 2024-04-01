from core.data_object_store.data_object_store import Transaction


def calculate_net_position(transaction_list: list[Transaction]):
    net_position: dict = {}
    for transaction in transaction_list:
        if transaction.instrument_id in net_position.keys():
            net_position[transaction.instrument_id] \
                += transaction.quantity

        else:
            net_position[transaction.instrument_id] \
                = transaction.quantity

    return net_position
