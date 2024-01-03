from core.database_service.db_connector import DBConnector
from typing import Union

from core.data_object_store.data_object_store import \
    Instrument, \
    Transaction, \
    Portfolio, \
    BaseDataObject, \
    User, \
    TradingSession, \
    Listing


__CoreObjectList__ = [Instrument, Transaction, Portfolio, User, Listing, TradingSession]

StrToObjectMap = {_object.__tablename__.upper(): _object for _object in __CoreObjectList__}


class RemoteObjectService:
    def __init__(self):
        """Allows to instanciate an object of type RemoteObjectService.

        The object is used to fetch core object data from the database and parse them into corre objects.
        """
        self.dbc: DBConnector = DBConnector()

    def get_object(self, object_type: str, filter_expression=None) -> Union[list[BaseDataObject], BaseDataObject]:
        """Gets list of all objects of a specified type, complying with the input filter expression.
           If filter expression is not specified, all the objects of the specified type are retreived.

        Args:
            object_type: type of the object to get from db.
            filter_expression: filter expression.

        Returns:
            List of all objects of the specified type matching with the input filter expreession.
            If the list contains only one object then the object is returned.

        Example:
            with RemoteObjectStore as roj:
                instrument = roj.get_object_list("INSTRUMENT", Instrument.id == "AAPL")
                all_instruments = roj.get_object_list("INSTRUMENT")
        """
        cls = StrToObjectMap[object_type]

        result = self.dbc.orm_session.query(cls).all() \
            if filter_expression is None \
            else self.dbc.orm_session.query(cls).filter(filter_expression).all()

        return result[0] if len(result) == 1 else result

    def persist_object(self, obj_list: list[BaseDataObject]) -> None:
        """Persists all objects from the input object list into the database.

        Args:
            obj_list: list of objects to persist.

        Returns:
            None

        Example:
            with RemoteObjectStore as roj:
                roj.persist_object([..., ...])
        """
        for obj in obj_list:
            self.dbc.orm_session.merge(obj)

    def delete_object(self, obj_list: list[BaseDataObject]) -> None:
        """Deletes all objects from an input object list from the database.

        Args:
            obj_list: list of objects to delete.

        Returns:
            None

        Example:
            with RemoteObjectStore as roj:
                roj.delete_object([..., ...])
        """
        for obj in obj_list:

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
    """Object factory.

    Args:
        object_type: type of the object to create.
        **kwargs to describe other attributes of the object that will be instanciated.

    Returns:
        Object of the specified type with the input carachteristics.

    Example:
        aapl = create_object("INSTRUMENT", **kwargs)
    """
    cls = StrToObjectMap[object_type]

    return cls(**kwargs)
