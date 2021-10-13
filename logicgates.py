from basic_components import ElectricComponent, SingleStateComponent, Switch, LooseWire


class INV(SingleStateComponent):
    """Inverts the input"""

    inputs = ('in_a', )

    def __init__(self, in_a:ElectricComponent=LooseWire):
        self.in_a = in_a
        self.setup(initial=True)

    def build_circuit(self):
        self.in_a.add_forward_connection(self)

    def compute_state(self):
        self._output = not self.in_a.is_on


class LogicGate(SingleStateComponent):
    """
    Logic Gates have two inputs (in_a, in_b) connected to a single output
    """

    inputs = ('in_a', 'in_b')

    def __init__(self, in_a:ElectricComponent=LooseWire, in_b:ElectricComponent=LooseWire):
        self.in_a = in_a
        self.in_b = in_b
        self.setup(initial=True)



class AND(LogicGate):
    """AND-Gate"""

    def build_circuit(self):        
        self.in_a.add_forward_connection(self)
        self.in_b.add_forward_connection(self)

    def compute_state(self):
        self._output = self.in_a.is_on and self.in_b.is_on


class OR(LogicGate):
    """OR-Gate"""

    def build_circuit(self):
        self.in_a.add_forward_connection(self)
        self.in_b.add_forward_connection(self)
    
    def compute_state(self):
        self._output = self.in_a.is_on or self.in_b.is_on


class NAND(LogicGate):
    """NAND-Gate"""

    def build_circuit(self):
        self.AND1 = AND(self.in_a, self.in_b)
        self.INV1 = INV(self.AND1)
        self.INV1.add_forward_connection(self)


    def compute_state(self):
        self._output = self.INV1.is_on


class NOR(LogicGate):
    """NOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self.INV1 = INV(self.OR1)
        self.INV1.add_forward_connection(self)

    def compute_state(self):
        self._output = self.INV1.is_on


class XOR(LogicGate):
    """XOR-Gate"""

    def build_circuit(self):
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.AND1 = AND(self.OR1, self.NAND1)
        self.AND1.add_forward_connection(self)

    def compute_state(self):
        self._output = self.AND1.is_on


# Tests

b1 = Switch(True)
b2 = Switch(True)
b3 = Switch(False)
b4 = Switch(False)

i1 = INV(b1)
i3 = INV(b3)
assert(i1.is_on is False)
assert(i3.is_on is True)

and_12 = AND(b1, b2)
and_13 = AND(b1, b3)
and_34 = AND(b3, b4)
assert(and_12.is_on is True)
assert(and_13.is_on is False)
assert(and_13.is_on is False)

or_12 = OR(b1, b2)
or_13 = OR(b1, b3)
or_34 = OR(b3, b4)
assert(or_12.is_on is True)
assert(or_13.is_on is True)
assert(or_34.is_on is False)

nand_12 = NAND(b1, b2)
nand_13 = NAND(b1, b3)
nand_34 = NAND(b3, b4)
assert(nand_12.is_on is False)
assert(nand_13.is_on is True)
assert(nand_34.is_on is True)

xor_12 = XOR(b1, b2)
xor_13 = XOR(b1, b3)
xor_34 = XOR(b3, b4)
assert(xor_12.is_on is False)
assert(xor_13.is_on is True)
assert(xor_34.is_on is False)

nor_12 = NOR(b1, b2)
nor_13 = NOR(b1, b3)
nor_34 = NOR(b3, b4)
assert(nor_12.is_on is False)
assert(nor_13.is_on is False)
assert(nor_34.is_on is True)

comb1 = AND(and_12, INV(and_13))
comb2 = AND(and_12, and_13)
assert(comb1.is_on is True)
assert(comb2.is_on is False)

b3.flip()
assert(comb1.is_on is False)
assert(comb2.is_on is True)
assert(i3.is_on is False)
assert(and_13.is_on is True)
assert(or_34.is_on is True)
assert(nand_13.is_on is False)
assert(xor_34.is_on is True)
assert(nor_34.is_on is False)