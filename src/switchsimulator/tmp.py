# import attr


# class foo:
#     am = 3


# @attr.s
# class Co:
#     myvar = attr.ib(default=attr.Factory(foo))

#     def __init__(self, myvar) -> None:
#         print(id(self.myvar))

#     def asd(self):
#         return id(self.myvar)

# z = foo()
# print(id(z))

# a = Co(z)
# print(a.asd())
# b = Co()
# print(b.asd())


from typing import Iterable, Union, List
from functools import wraps


class dusent:
    pass


def check_sentinel(x):
    if isinstance(x, list):
        return[check_sentinel(e) for e in x]
    elif isinstance(x, tuple):
        return[check_sentinel(e) for e in x]
    elif isinstance(x, dusent):
        return "hi"
    else:
        return x


def autoparse2(init):

    @wraps(init)
    def wrapped_init(self, *args, **kwargs):
        args = tuple(check_sentinel(a) for a in args)
        for kw in kwargs:
            kwargs[kw] = check_sentinel(kwargs[kw])
        init(self, *args, **kwargs)
    return wrapped_init

class dummy:
    @autoparse2
    def __init__(self,
     a=[dusent() for _ in range(5)], b=[2, [dusent()]], c=dusent, d=(dusent, dusent)) -> None:
        print(a)
        print(b)
        print(c)
        print(d)

dummy(2, d=3)