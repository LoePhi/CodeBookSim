from electriccomponent import ElectricComponent
from integratedcomponent import IntegratedComponent
from corecomponents import LooseWire, OR, AND, NAND, NOR


class IntegratedLogicGate(IntegratedComponent):

    # inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    # outputs = ElectricComponent.unpack_io('out_main')

    def get_state(self):
        return self.out_main.get_state()

    is_on = property(get_state)


class XOR(IntegratedLogicGate):
    """XOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.OR1, self.NAND1)


class NOR3(IntegratedLogicGate):
    """3-way NOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None,
                 in_c: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.in_c = in_c if in_c is not None else LooseWire()
        self.out_main = NOR(OR(self.in_a, self.in_b), self.in_c)
