from switchsimulator.electriccomponent import ElectricComponent
from switchsimulator.secondarycomponents import SingleStateSC
from switchsimulator.corecomponents import OR, AND, NAND, NOR
from switchsimulator.corecomponents import autoparse, set_sent


class XOR(SingleStateSC):
    """XOR-Gate"""

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = set_sent(),
                 in_b: ElectricComponent = set_sent()):
        self.in_a = in_a
        self.in_b = in_b

        self.or1 = OR(self.in_a, self.in_b)
        self.nand1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.or1, self.nand1)


class NOR3(SingleStateSC):
    """3-way NOR-Gate"""

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = set_sent(),
                 in_b: ElectricComponent = set_sent(),
                 in_c: ElectricComponent = set_sent()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_c = in_c

        self.out_main = NOR(OR(self.in_a, self.in_b), self.in_c)
