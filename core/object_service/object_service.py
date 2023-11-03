from core.database_service.db_connector import DBConnector
from sqlalchemy import or_, and_
from core.object_store.object_store import Instrument, Position, Portfolio, BaseObject
from dataclasses import dataclass


@dataclass
class Options:

    __ObjectList__ = [Instrument, Position, Portfolio]

    ObjectMap = {_object.__tablename__.upper(): _object for _object in __ObjectList__}

    QueryOperators = [or_, and_]


class ObjectService:
    def __init__(self):
        self.dbc = DBConnector()
        self.options = Options()

    def create_object(self, object_type: str) -> BaseObject:
        cls = self.options.ObjectMap[object_type]

        return cls()

    def get_object(self, object_type: str, object_primary_key: str) -> BaseObject:
        cls = self.options.ObjectMap[object_type]

        return self.dbc.orm_session.get(cls, object_primary_key)

    def get_list(self, object_type: str) -> list[BaseObject]:
        cls = self.options.ObjectMap[object_type]

        return self.dbc.orm_session.query(cls).all()

    def get_list_filter(self, object_type: str, filter_expression) -> list[BaseObject]:
        cls = self.options.ObjectMap[object_type]

        return self.dbc.orm_session.query(cls).filter(filter_expression)

    def persist(self, obj_list: list[BaseObject]) -> None:
        for obj in obj_list:

            self.dbc.orm_session.add(obj)

    def delete(self, obj_list: list[BaseObject]) -> None:
        for obj in obj_list:

            self.dbc.orm_session.delete(obj)

    def delete_by_object_id(self, id_list: list, object_type: str) -> None:
        for object_id in id_list:
            obj = self.dbc.orm_session.get(object_type, object_id)

            self.dbc.orm_session.delete(obj)

    def __enter__(self):
        self.dbc.connect()

        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.dbc.commit()

        self.dbc.close()

