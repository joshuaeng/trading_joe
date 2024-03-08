from core.object_service.object_service import RemoteObjectService, object_list
from typing import Any


def check_type(_object_list: list[Any]):
    for _obj in _object_list:
        if _obj.__class_ not in object_list:
            raise Exception(f"{_obj} type is not supported.")


def persist_objects(_bject_list: list[Any]) -> None:
    with RemoteObjectService() as roj:
        roj.persist_object(object_list)
