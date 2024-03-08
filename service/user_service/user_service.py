from core.object_service.object_service import RemoteObjectService, create_object
from core.data_object_store.data_object_store import User


def load_user_from_id(user_id: str):
    with RemoteObjectService() as roj:
        resp = roj.get_object("USER", user_id)
        user = resp.extract_object()

    return user


def create_user(username: str, password: str) -> User:
    """
    Creates new user.
    Args:
        username: name of the new user.
        password: password of the new user.

    Returns:
        User

    """
    crypted_password = hash(password)

    new_user = create_object("USER", username=username, password=crypted_password)

    with RemoteObjectService() as roj:
        roj.persist_object(obj_list=[new_user])

    return new_user


def load_user(username: str, password: str) -> User:
    """
    Loads user.
    Args:
        username: name of the user.
        password: password of the userr

    Returns:
        User
    """
    crypted_password = hash(password)

    with RemoteObjectService() as roj:
        resp = roj.get_object(
            object_type="USER",
            filter_expression=(User.id == username).__and__(User.password == crypted_password)
        )

    return resp.extract_object()

