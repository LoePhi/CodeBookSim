from typing import Sequence
from switchsimulator.base import SingleStateSC
from switchsimulator.corecomponents import OR, AND, NAND, NOR
from switchsimulator.base import autoparse, no_con, InputComponent


class XOR(SingleStateSC):
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


class NOR3(SingleStateSC):
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


class AND4(SingleStateSC):
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


class OR8(SingleStateSC):
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
