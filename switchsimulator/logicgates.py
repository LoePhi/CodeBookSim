from component import ElectricComponent
from singlestatecomp import SingleStateComponent, LooseWire


class INV(SingleStateComponent):
    """Inverts the input"""

    inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        self._output = not self.in_a.is_on


class LogicGate(SingleStateComponent):
    """
    Logic Gates have two inputs (in_a, in_b) connected to a single output
    """

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.setup()


class AND(LogicGate):
    """AND-Gate"""

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')

    def compute_state(self):
        self._output = self.in_a.is_on and self.in_b.is_on


class OR(LogicGate):
    """OR-Gate"""

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')

    def compute_state(self):
        self._output = self.in_a.is_on or self.in_b.is_on


class NAND(LogicGate):
    """NAND-Gate"""

    def build_circuit(self):
        self.AND1 = AND(self.in_a, self.in_b)
        self.INV1 = INV(self.AND1)
        self.INV1.add_connection(self, '_output')

    def compute_state(self):
        self._output = self.INV1.is_on


class NOR(LogicGate):
    """NOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self.INV1 = INV(self.OR1)
        self.INV1.add_connection(self, '_output')

    def compute_state(self):
        self._output = self.INV1.is_on


class XOR(LogicGate):
    """XOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.AND1 = AND(self.OR1, self.NAND1)
        self.AND1.add_connection(self, '_output')

    def compute_state(self):
        self._output = self.AND1.is_on
