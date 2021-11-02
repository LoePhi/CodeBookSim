from electriccomponent import ElectricComponent
from integratedcomponent import SingleStateIC
from corecomponents import LooseWire, OR, AND, NAND, NOR


class XOR(SingleStateIC):
    """XOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.or1 = OR(self.in_a, self.in_b)
        self.nand1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.or1, self.nand1)


class NOR3(SingleStateIC):
    """3-way NOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None,
                 in_c: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.in_c = in_c if in_c is not None else LooseWire()
        self.out_main = NOR(OR(self.in_a, self.in_b), self.in_c)
