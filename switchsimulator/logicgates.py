from component import ElectricComponent
from corecomponents import LooseWire, INV, OR, AND, Switch


class IntegratedComponent(ElectricComponent):

    def compute_state(self):
        raise NotImplementedError("nocomp")

    def get_state(self, port):
        return getattr(self, port).get_state()

    def build_circuit(self):
        pass


class NAND(IntegratedComponent):
    """NAND-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_a')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = AND(self.in_a, self.in_b)
        self.out_a = INV(self.AND1)



a = Switch(True)
b = Switch(False)
nand1 = NAND(a, b)
nand2 = NAND(nand1, b)
nand3 = NAND(nand1, nand2)
nand2.get_state()
nand3.get_state()
b.flip()

class NOR(LogicGate):
    """NOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self._output = INV(self.OR1)


class XOR(LogicGate):
    """XOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self._output = AND(self.OR1, self.NAND1)
