from component import ElectricComponent
from singlestatecomp import Connector, LooseWire, Switch
from logicgates import AND, OR, XOR
from misccomp import OnesComplement


class HalfAdder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.setup()
        self.con_sum = Connector(self, "out_sum")
        self.con_carry = Connector(self, "out_carry")

    def build_circuit(self):
        self.AND1 = AND(self.in_a, self.in_b)
        self.XOR1 = XOR(self.in_a, self.in_b)
        self.XOR1.add_connection(self, "out_sum")
        self.AND1.add_connection(self, "out_carry")

    def compute_state(self):
        self.out_sum = self.XOR1.is_on
        self.out_carry = self.AND1.is_on

    def __str__(self):
        return str(int(self.out_carry)) + str(int(self.out_sum))


class FullAdder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire(),
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.setup()
        self.con_sum = Connector(self, "out_sum")
        self.con_carry = Connector(self, "out_carry")

    def build_circuit(self):
        self.HA1 = HalfAdder(self.in_a, self.in_b)
        self.HA2 = HalfAdder(self.in_carry, self.HA1.con_sum)
        self.OR1 = OR(self.HA1.con_carry, self.HA2.con_carry)
        self.HA2.con_sum.add_connection(self, "out_sum")
        self.OR1.add_connection(self, "out_carry")

    def compute_state(self):
        self.out_sum = self.HA2.con_sum.is_on
        self.out_carry = self.OR1.is_on

    def __str__(self):
        return str(int(self.out_carry)) + str(int(self.out_sum))


class Eight_Bit_Adder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_sum:8', 'out_carry')

    def __init__(self,
                 in_a: ElectricComponent = [LooseWire() for x in range(8)],
                 in_b: ElectricComponent = [LooseWire() for x in range(8)],
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.setup()
        self.con_sum = Connector(self, "out_sum")
        self.con_carry = Connector(self, "out_carry")

    def build_circuit(self):
        self.full_adders = [None]*8
        self.full_adders[7] = FullAdder(
            self.in_a[7], self.in_b[7], self.in_carry)
        for i in range(6, -1, -1):
            self.full_adders[i] = FullAdder(
                self.in_a[i], self.in_b[i], self.full_adders[i+1].con_carry)
        for i in range(7, -1, -1):
            self.full_adders[i].con_sum.add_connection(
                self, 'out_sum@' + str(i))
        self.full_adders[0].con_carry.add_connection(self, 'out_carry')

    def compute_state(self):
        self.out_sum = [fa.con_sum.is_on for fa in self.full_adders]
        self.out_carry = self.full_adders[0].con_carry.is_on

    def __str__(self):
        bitlist = [str(int(self.out_carry))] + ['_'] + \
            [str(int(b)) for b in self.out_sum]
        return ''.join(bitlist)


class Sixteen_Bit_Adder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a:16', 'in_b:16', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_sum:16', 'out_carry')

    def __init__(self,
                 in_a: ElectricComponent = [LooseWire() for x in range(16)],
                 in_b: ElectricComponent = [LooseWire() for x in range(16)],
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.setup()
        self.con_sum = Connector(self, "out_sum")
        self.con_carry = Connector(self, "out_carry")

    def build_circuit(self):
        self.eba_low = Eight_Bit_Adder(
            self.in_a[:8], self.in_b[:8], self.in_carry)
        self.eba_high = Eight_Bit_Adder(
            self.in_a[8:], self.in_b[8:], self.eba_low.con_carry)
        self.eba_low.con_sum.add_connection(self, "out_sum")
        self.eba_high.con_sum.add_connection(self, "out_carry")

    def compute_state(self):
        self.out_sum = self.eba_low.con_sum.is_on + self.eba_high.con_sum.is_on
        self.out_carry = self.eba_high.con_carry.is_on

    def __str__(self):
        bitlist = [str(int(self.out_carry))] + ['_'] + \
            [str(int(b)) for b in self.out_sum]
        return ''.join(bitlist)


class AddMin(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_sub')
    outputs = ElectricComponent.unpack_io('out_sum:8', 'out_flow')

    def __init__(self,
                 in_a: ElectricComponent = [LooseWire() for x in range(8)],
                 in_b: ElectricComponent = [LooseWire() for x in range(8)],
                 in_sub: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_sub = in_sub
        self.setup()
        self.con_sum = Connector(self, "out_sum")
        self.con_flow = Connector(self, "out_flow")

    def build_circuit(self):
        self.oc1 = OnesComplement(self.in_b, self.in_sub)
        self.eba1 = Eight_Bit_Adder(self.in_a, self.oc1, self.in_sub)
        self.xor1 = XOR(self.eba1.con_carry, self.in_sub)
        self.eba1.con_sum.add_connection(self, "out_sum")
        self.xor1.add_connection(self, "out_flow")

    def compute_state(self):
        self.out_sum = self.eba1.con_sum.is_on
        self.out_flow = self.xor1.is_on

    def __str__(self):
        if not self.out_flow:
            control = ""
        elif self.in_sub.is_on:
            control = "UnDeRfLoW"
        else:
            control = "OvErFlOw"
        bitlist = [control] + [str(int(b)) for b in self.out_sum]
        return ''.join(bitlist)

from helpers import bts

AddMin(bts('00000001'), bts('00000001'), Switch(False))

oc1 = OnesComplement(bts('00000001'),Switch(True))
oc1.__dict__