from typing import Any


def throw_if_none(value: Any, message="Value cannot be None"):
    """Raises a ValueError if the provided value is None.

    Args:
        value: The value to check.
        message (str): The error message to raise if the value is None.
    Raises:
        ValueError: If the value is None.
    """
    if value is None:
        raise ValueError(message)
