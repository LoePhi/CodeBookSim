# type: ignore

import sys
print(1)


class B:
    pass


class A(B):
    __slots__ = ('a')

    def __init__(self, a) -> None:
        self.a = a
        self.b = 3


A(2)

sys.getsizeof(A(2))
