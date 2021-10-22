from electriccomponent import ElectricComponent
from corecomponents import LooseWire, OR, AND
from integratedcomponent import IntegratedComponent
from logicgates import XOR
from misccomp import OnesComplement


class HalfAdder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.out_sum = XOR(self.in_a, self.in_b)
        self.out_carry = AND(self.in_a, self.in_b)

    def __str__(self):
        return str(int(self.out_carry.is_on)) + str(int(self.out_sum.is_on))


class FullAdder(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None,
                 in_carry: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.in_carry = in_carry if in_carry is not None else LooseWire()
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
                 in_a: list = None,
                 in_b: list = None,
                 in_carry: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else [
            LooseWire() for x in range(8)]
        self.in_b = in_b if in_b is not None else [
            LooseWire() for x in range(8)]
        self.in_carry = in_carry if in_carry is not None else LooseWire()
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
                 in_a: list = None,
                 in_b: list = None,
                 in_carry: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else [
            LooseWire() for x in range(16)]
        self.in_b = in_b if in_b is not None else [
            LooseWire() for x in range(16)]
        self.in_carry = in_carry if in_carry is not None else LooseWire()
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
                 in_a: list = None,
                 in_b: list = None,
                 in_sub: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else [
            LooseWire() for x in range(8)]
        self.in_b = in_b if in_b is not None else [
            LooseWire() for x in range(8)]
        self.in_sub = in_sub if in_sub is not None else LooseWire()
        self.oc1 = OnesComplement(self.in_b, self.in_sub)
        self.eba1 = Eight_Bit_Adder(
            self.in_a, self.oc1.out_main, self.in_sub)
        self.out_sum = self.eba1.out_sum
        self.out_flow = XOR(self.eba1.out_carry, self.in_sub)

    def __str__(self):
        if not self.out_flow.is_on:
            control = ""
        elif self.in_sub.is_on:
            control = "UnDeRfLoW"
        else:
            control = "OvErFlOw"
        bitlist = [control] + [str(int(b.is_on)) for b in self.out_sum]
        return ''.join(bitlist)
