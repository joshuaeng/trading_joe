from core.database_service.db_connector import DBConnector
from core.data_object_store.data_object_store import BaseDataObject, object_list
from typing import Union, Any
from loguru import logger

StrToObjectMap = {_object.__tablename__.upper(): _object for _object in object_list}


class _Response:
    """Response class. allow to instantiate a Response object."""

    def __init__(self, query_result: Union[Any, list[Any]]) -> None:
        self._query_result = query_result

        self.len = len(self._query_result)

    def extract_object(self, force_to_list: bool = False) -> Union[Any, list[Any]]:
        """Returns tarrget object or object list."""
        if force_to_list:
            return self._query_result

        elif not force_to_list:
            return self._query_result[0] if self.len == 1 else self._query_result

        else:
            raise Exception("No object to extract.")


class RemoteObjectService:
    def __init__(self):
        """Allows to instanciate an object of type RemoteObjectService.

        The object is used to fetch core object data from the database and parse them into corre objects.
        """
        self.dbc: DBConnector = DBConnector()

    def get_object(self, object_type: str, filter_expression=None) -> _Response:
        """Gets list of all objects of a specified type, complying with the input filter expression.
           If filter expression is not specified, all the objects of the specified type are retreived.

        Args:
            object_type: type of the object to get from db.
            filter_expression: filter expression.
                element output into a list.

        Returns:
            List of all objects of the specified type matching with the input filter expreession.
            If the list contains only one object then the object is returned.

        Example:
            with RemoteObjectStore as roj:
                instrument = roj.get_object_list("INSTRUMENT", Instrument.id == "AAPL")
                all_instruments = roj.get_object_list("INSTRUMENT")
        """
        cls = StrToObjectMap[object_type]

        result = (
            self.dbc.orm_session.query(cls).all()
            if filter_expression is None
            else self.dbc.orm_session.query(cls).filter(filter_expression).all()
        )

        return _Response(query_result=result)

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
            logger.info(f"Persisting {obj.__repr__()}")
            try:
                self.dbc.orm_session.merge(obj)
            except Exception as e:
                logger.exception("Could not persist object.")
                raise e

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


def create_object(object_type: str, **kwargs) -> Any:
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
