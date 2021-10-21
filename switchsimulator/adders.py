from component import ElectricComponent
from corecomponents import LooseWire, OR, AND
from logicgates import XOR, IntegratedComponent
from misccomp import OnesComplement


class HalfAdder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.out_sum = XOR(self.in_a, self.in_b)
        self.out_carry = AND(self.in_a, self.in_b)

    def __str__(self):
        return str(int(self.out_carry.is_on)) + str(int(self.out_sum.is_on))


class FullAdder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire(),
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.HA1 = HalfAdder(self.in_a, self.in_b)
        self.HA2 = HalfAdder(self.in_carry, self.HA1.out_sum)
        self.out_sum = self.HA2.out_sum
        self.out_carry = OR(self.HA1.out_carry, self.HA2.out_carry)

    def __str__(self):
        return str(int(self.out_carry.is_on)) + str(int(self.out_sum.is_on))


class Eight_Bit_Adder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_sum:8', 'out_carry')

    def __init__(self,
                 in_a: ElectricComponent = [LooseWire() for x in range(8)],
                 in_b: ElectricComponent = [LooseWire() for x in range(8)],
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.full_adders = [None]*8
        self.full_adders[7] = FullAdder(
            self.in_a[7], self.in_b[7], self.in_carry)
        for i in range(6, -1, -1):
            self.full_adders[i] = FullAdder(
                self.in_a[i], self.in_b[i], self.full_adders[i+1].out_carry)
        self.out_sum = [fa.out_sum for fa in self.full_adders]
        self.out_carry = self.full_adders[0].out_carry

    def __str__(self):
        bitlist = [str(int(self.out_carry.is_on))] + ['_'] + \
            [str(int(b.is_on)) for b in self.out_sum]
        return ''.join(bitlist)


class Sixteen_Bit_Adder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a:16', 'in_b:16', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_sum:16', 'out_carry')

    def __init__(self,
                 in_a: ElectricComponent = [LooseWire() for x in range(16)],
                 in_b: ElectricComponent = [LooseWire() for x in range(16)],
                 in_carry: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.eba_low = Eight_Bit_Adder(
            self.in_a[8:], self.in_b[8:], self.in_carry)
        self.eba_high = Eight_Bit_Adder(
            self.in_a[:8], self.in_b[:8], self.eba_low.out_carry)
        self.out_sum = self.eba_high.out_sum + self.eba_low.out_sum
        self.out_carry = self.eba_high.out_carry

    def __str__(self):
        bitlist = [str(int(self.out_carry.is_on))] + ['_'] + \
            [str(int(b.is_on)) for b in self.out_sum]
        return ''.join(bitlist)


class AddMin(IntegratedComponent):

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
        self.eba1 = Eight_Bit_Adder(
            self.in_a, self.oc1.con_main, self.in_sub)
        self.xor1 = XOR(self.eba1.con_carry, self.in_sub)
        for i in range(8):
            self.eba1.con_sum[i].add_connection(self, "out_sum")
        self.xor1.add_connection(self, "out_flow")

    def compute_state(self):
        self.out_sum = [con.is_on for con in self.eba1.con_sum]
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

# from helpers import bts

# AddMin(bts('00000001'), bts('00000001'), Switch(False))

# oc1 = OnesComplement(bts('00000001'),Switch(True))
# oc1.__dict__
