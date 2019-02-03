from .repository import Repository
from .controller import Controller


def make_usecase():
    repo = Repository()
    # We do not have service layer here, since it is pure CRUD.
    return (r"/v1/expenses", Controller, dict(repo=repo))
