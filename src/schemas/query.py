from typing import List
import strawberry

from src.schemas.types import Notebook


def get_notebooks():
    return []


@strawberry.type
class Query:
    notebooks: List[Notebook] = strawberry.field(resolver=get_notebooks)
