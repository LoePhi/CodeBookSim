from components import SingleStateComponent, Switch


class Inverter(SingleStateComponent):
    """Inverts the input"""

    def __init__(self, in_a=None):
        self.in_a = in_a
        self.update()

    def update(self):
        self._out = not self.in_a.is_on

    def get_state(self):
        return self._out

    is_on = property(get_state)


# Alias
INV = Inverter
NOT = Inverter


class AND(SingleStateComponent):
    """AND-Gate"""

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.update()

    def update(self):
        self._out = self.in_a.is_on and self.in_b.is_on


class OR(SingleStateComponent):
    """OR-Gate"""

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.update()

    def update(self):
        self._out = self.in_a.is_on or self.in_b.is_on


class NAND(SingleStateComponent):
    """NAND-Gate"""

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = AND(self.in_a, self.in_b)
        self.INV1 = INV(self.AND1)
        self.update()

    def update(self):
        self._out = self.INV1.is_on


class NOR(SingleStateComponent):
    """NOR-Gate"""

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.INV1 = INV(self.OR1)
        self.update()

    def update(self):
        self._out = self.INV1.is_on


class XOR(SingleStateComponent):
    """XOR-Gate"""

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.OR1 = OR(self.in_a, self.in_b)
        self.NAND1 = NAND(self.in_a, self.in_b)
        self.AND1 = AND(self.OR1, self.NAND1)
        self.update()

    def update(self):
        self._out = self.AND1.is_on


b1 = Switch(True)
b2 = Switch(True)
b3 = Switch(True)
b4 = Switch(False)

a1 = AND(b1, b2)
a2 = AND(b1, b3)
a3 = AND(b1, b4)

aa1 = AND(a1, a2)
aa2 = AND(a1, a3)

aaa1 = AND(aa1, aa2)

a1.is_on
a2.is_on
a3.is_on

aa1.is_on
aa2.is_on

aaa1.is_on

asd = NAND(AND(b1, b2), AND(b3, b4))
asd.is_on

XOR(AND(b1, b2), AND(b3, b4)).is_on
