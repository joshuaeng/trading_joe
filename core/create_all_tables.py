import loguru

from core.data_object_store.data_object_store import table_list, User
from core.database_service.db_connector import DBConnector


if __name__ == "__main__":

    dbc = DBConnector()

    engine = dbc.engine

    engine.connect()

    init_table_list = table_list

    for table in table_list:
        try:
            loguru.logger.info(f"Creating table {table.__str__()}...")
            table.create(engine)

        except Exception as e:
            loguru.logger.info(f"Cannot create tabe {table.__str__()}. Reason: {e}.")

