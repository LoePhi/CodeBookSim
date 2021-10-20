from component import ElectricComponent
from corecomponents import LooseWire, INV, OR, AND, Switch


class IntegratedComponent(ElectricComponent):

    def compute_state(self):
        raise NotImplementedError("nocomp")

    def build_circuit(self):
        pass


class ICSingleLine(IntegratedComponent):
    def get_state(self, port="out_a"):
        return getattr(self, port).get_state(port)

    is_on = property(get_state)

    # TODOTHIS
    def add_connection(self, con, port):
        """Called by downstream elements to add the as a forward connection"""
        self.out_a.add_connection((con, port))


class NAND(ICSingleLine):
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
nand2 = NAND(nand1, a)
nand1.is_on  # T
nand2.is_on  # F

or1 = OR(a, b)  # T
nand3 = NAND(nand1, or1)
nand3.is_on  # F
b.flip()
nand3.is_on  # T

# waruzm hat 
nand1.out_a.forward_connections[0][0].__dict__
# keine backward connection zu 
nand1.out_a.__dict__

# 

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
