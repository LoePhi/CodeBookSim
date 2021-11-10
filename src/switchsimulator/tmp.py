# type: ignore

from typing import Callable, TypeVar
from typing_extensions import ParamSpec


T = TypeVar('T')
R = tuple[T, float]
P = ParamSpec('P')


def decorator_block(func: Callable[P, T]) -> Callable[P, R]:
    """
    Decorator.
    """
    def wrapper(*args, **kwargs) -> R:
        result = func(*args, **kwargs)
        return result, 0.1
    return wrapper
