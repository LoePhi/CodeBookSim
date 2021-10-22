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

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.AND1 = AND(self.in_a, self.in_b)
        self.out_main = INV(self.AND1)


class NOR(IntegratedLogicGate):
    """NOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.OR1 = OR(self.in_a, self.in_b)
        self.out_main = INV(self.OR1)


class XOR(IntegratedLogicGate):
    """XOR-Gate"""

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.OR1, self.NAND1)
