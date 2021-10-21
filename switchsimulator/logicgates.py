from component import ElectricComponent
from corecomponents import LooseWire, INV, OR, AND


class IntegratedComponent(ElectricComponent):

    # TODOTHIS
    def add_connection(self, con, port):
        """
        The connection is passed on until a corecomponent is found
        """
        for out in self.outputs:
            getattr(self, out).add_connection(con, port)


class ICSingleLine(IntegratedComponent):

    def get_state(self, port="out_main"):
        return getattr(self, port).get_state(port)

    is_on = property(get_state)


class NAND(ICSingleLine):
    """NAND-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_main')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = AND(self.in_a, self.in_b)
        self.out_main = INV(self.AND1)


class NOR(ICSingleLine):
    """NOR-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_main')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.out_main = INV(self.OR1)


class XOR(ICSingleLine):
    """XOR-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_main')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.out_main = AND(self.OR1, self.NAND1)

from corecomponents import Switch
a = Switch(True)
b=Switch(True)
and1 = AND(a,b)
or1 = OR(and1, b)