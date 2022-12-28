"""Item parameters."""

from pydantic import BaseModel


class Item(BaseModel):
    """Item parameters.

    Args:
        name (str): name of the item
        value (str): value of the item
    """
    name: str
    value: str
