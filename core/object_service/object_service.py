from core.database_service.db_connector import DBConnector
from typing import Type, Any
from sqlalchemy import or_, and_
from core.object_store.object_store import Instrument, Position, Portfolio, Base


ObjectMap = {"INSTRUMENT": Instrument, "POSITION": Position, "PORTFOLIO": Portfolio}

QueryOperators = [or_, and_]


class ObjectService:
    def __init__(self):
        self.dbc = DBConnector()

    @staticmethod
    def update_object(obj: Base, **kwargs) -> Base:
        for element in kwargs:
            if element not in obj.fields:
                raise Exception(
                    f"'{element.capitalize()}' is not an attribute of {obj.__class__.__name__}. "
                    f"Attributes of {obj.__class__.__name__} are: {obj.fields}"
                )

        obj.__dict__.update(**kwargs)

        return obj

    def create_object(self, object_type: str, **kwargs) -> Base:
        object_type = ObjectMap[object_type]

        return self.update_object(object_type(), **kwargs)

    def get_object(self, object_type: Type[Base], object_primary_key: str) -> Any:
        return self.dbc.orm_session.get(object_type, object_primary_key)

    def get_list(self, object_type: Type[Base]) -> list[Any]:
        return self.dbc.orm_session.query(object_type).all()

    def get_list_filter(self, object_type: Type[Base], filter_expression):
        return self.dbc.orm_session.query(object_type).filter(filter_expression)

    def persist(self, obj_list: list[Base]) -> None:
        for obj in obj_list:
            self.dbc.orm_session.add(obj)

        self.dbc.orm_session.commit()

    def delete(self, obj_list: list[Base]) -> None:
        for obj in obj_list:
            self.dbc.orm_session.delete(obj)

        self.dbc.orm_session.commit()

    def delete_by_object_id(self, id_list: list, object_type: Type[Base]) -> None:
        for object_id in id_list:
            obj = self.dbc.orm_session.get(object_type, object_id)
            self.dbc.orm_session.delete(obj)

        self.dbc.orm_session.commit()

