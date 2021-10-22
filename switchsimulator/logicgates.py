from electriccomponent import ElectricComponent
from integratedcomponent import IntegratedComponent
from corecomponents import LooseWire, INV, OR, AND


class IntegratedLogicGate(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_main')

    def get_state(self):
        return self.out_main.get_state()

    is_on = property(get_state)


class NAND(IntegratedLogicGate):
    """NAND-Gate"""

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = AND(self.in_a, self.in_b)
        self.out_main = INV(self.AND1)


class NOR(IntegratedLogicGate):
    """NOR-Gate"""

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.out_main = INV(self.OR1)


class XOR(IntegratedLogicGate):
    """XOR-Gate"""

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.OR1, self.NAND1)
