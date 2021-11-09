# type: ignore
from typing import Any, Union, overload


class parent:

    def __init__(self) -> None:
        ...

    @overload
    def funa(self, a: int) -> int:
        ...

    @overload
    def funa(self, a: Any) -> Any:
        ...

    def funa(self, a: Union[int, Any]) -> Union[int, Any]:
        return a


for a in ('a1', '1a'):
    for b in ('b1', '1b'):
        for c in ('c1', '1c'):
            print(a+b+c)


[a+b+c for a in ('a', 'A') for b in ('b', 'B') for c in ('c', 'C')]
print(a+b+c)

q = tuple(zip(['A', 'B', 'C'], ['a', 'b', 'c']))
y = [(a, b, c) for a in q[0] for b in q[1] for c in q[2]]
list(y)


def print_some(a, b, c, d):
    print(a+b+c+d)


print_some('1', *y[0])

q = tuple(zip(['0', '0', '0'], ['1', '1', '1']))
y = [(a, b, c) for a in q[2] for b in q[1] for c in q[0]]
list(y)
