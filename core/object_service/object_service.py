from typing import Type

from core.database_service.db_connector import DBConnector
from loguru import logger

from core.data_object_store.data_object_store import \
    Instrument, \
    Transaction, \
    Portfolio, \
    BaseDataObject, \
    User, \
    Listing


__CoreObjectList__ = [Instrument, Transaction, Portfolio, User, Listing]

StrToObjectMap = {_object.__tablename__.upper(): _object for _object in __CoreObjectList__}


class RemoteObjectService:
    def __init__(self):
        """Allows to instanciate an object of type RemoteObjectService.

        The object is used to fetch core object data from the database and parse them into corre objects.

        Example:

            with RemoteObjectService() as object_service:

                user_1 = create_object("USER")

                broker = create_object("BROKER")

                portfolio = create_object("PORTFOLIO")

                trading_session = create_object("TRADING_SESSION")

                user_1.set_attribute(...)
        """
        self.dbc: DBConnector = DBConnector()

    def get_object(self, object_type: str, object_primary_key) -> BaseDataObject:
        """Gets object from database."""
        cls = StrToObjectMap[object_type]

        return self.dbc.orm_session.get(cls, object_primary_key)

    def get_list(self, object_type: str) -> list[BaseDataObject]:
        """Get list of all objects of a certain type from dartabase."""
        cls = StrToObjectMap[object_type]

        return self.dbc.orm_session.query(cls).all()

    def get_list_filter(self, object_type: str, filter_expression) -> list[BaseDataObject]:
        """Gets list of all objects from a certain type, complying with the input filter expression."""
        cls = StrToObjectMap[object_type]

        return self.dbc.orm_session.query(cls).filter(filter_expression)

    def persist_object(self, obj_list: list[BaseDataObject]) -> None:
        """Persists all objects from the input object list into the database."""
        for obj in obj_list:
            self.dbc.orm_session.merge(obj)

    def delete_object(self, obj_list: list[BaseDataObject]) -> None:
        """Deletes all objects from an input object list from the database."""
        for obj in obj_list:

            self.dbc.orm_session.delete(obj)

    def delete_by_object_id(self, id_list: list, object_type: str) -> None:
        """Delete the object from the input type and input id."""
        for object_id in id_list:
            obj = self.dbc.orm_session.get(object_type, object_id)

            self.dbc.orm_session.delete(obj)

    def __enter__(self):
        """Context manager __enter__."""
        self.dbc.connect()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Context manager __exit__"""
        self.dbc.commit()
        self.dbc.close()


def create_object(object_type: str, **kwargs) -> BaseDataObject:
    """Object factory."""
    cls = StrToObjectMap[object_type]

    return cls(**kwargs)
