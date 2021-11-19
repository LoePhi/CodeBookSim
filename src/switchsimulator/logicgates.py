import functools
from typing import Sequence
from switchsimulator.base import SingleBitSOC
from switchsimulator.corecomponents import OR, AND, NAND, NOR
from switchsimulator.base import autoparse, no_con, InputComponent


class XOR(SingleBitSOC):
    """XOR-Gate"""

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con(),
                 in_b: InputComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b

        self.or1 = OR(self.in_a, self.in_b)
        self.nand1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.or1, self.nand1)


class NOR3(SingleBitSOC):
    """3-way NOR-Gate"""

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con(),
                 in_b: InputComponent = no_con(),
                 in_c: InputComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_c = in_c

        self.out_main = NOR(OR(self.in_a, self.in_b), self.in_c)


class AND4(SingleBitSOC):
    """4-way AND-Gate"""

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con(),
                 in_b: InputComponent = no_con(),
                 in_c: InputComponent = no_con(),
                 in_d: InputComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_c = in_c
        self.in_d = in_d

        self.and1 = AND(self.in_a, self.in_b)
        self.and2 = AND(self.in_c, self.in_d)
        self.out_main = AND(self.and1, self.and2)


class OR8(SingleBitSOC):
    """
    8-way OR-gate
    """
    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8)) -> None:

        self.in_data = in_data
        self.ors = [OR(self.in_data[0], self.in_data[1])]
        for i in range(6):
            self.ors.append(OR(self.ors[i], self.in_data[i+2]))
        self.out_main = self.ors[-1]


class ANDX(SingleBitSOC):
    """General AND-Gate. Does not support delayed connections
    Can become problematioc for large inputs because of the
    reduce chain"""

    def __init__(self, in_data: Sequence[InputComponent]) -> None:
        self.in_data = in_data

        self.out_main = functools.reduce(AND, self.in_data)


class AND17(SingleBitSOC):
    """General AND-Gate. Does not support delayed connections"""

    def __init__(self, in_data: Sequence[InputComponent] = no_con(17)) -> None:
        self.in_data = in_data

        and1 = AND4(*in_data[:4])
        and2 = AND4(*in_data[4:8])
        and3 = AND4(*in_data[8:12])
        and4 = AND4(*in_data[12:16])
        and5 = AND4(and1, and2, and3, and4)
        self.out_main = AND(and5, in_data[16])


class ORX(SingleBitSOC):
    """
    General OR-Gate. Does not support delayed connections
    This should be faster if high memory adressses are never
    accessed.
    However, if they are accessed it can become unstable
    because of the reduce chain.
    """

    def __init__(self, in_data: Sequence[InputComponent]) -> None:
        self.in_data = in_data

        self.out_main = functools.reduce(OR, self.in_data)


def _recor(x: Sequence[InputComponent]) -> OR:
    halflen = len(x) // 2
    if halflen == 1:
        return OR(x[0], x[1])
    else:
        return OR(_recor(x[:halflen]), _recor(x[halflen:]))


class OR64K(SingleBitSOC):
    """2^16 OR-Gate"""

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(2**16)) -> None:
        self.in_data = in_data

        self.out_main = _recor(self.in_data)
