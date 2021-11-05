from switchsimulator.memory import EdgeTrig8BitLatchPreCl
from switchsimulator.electriccomponent import ElectricComponent
from switchsimulator.corecomponents import OR, AND, autoparse, no_con
from switchsimulator.secondarycomponents import SecondaryComponent
from switchsimulator.logicgates import XOR
from switchsimulator.misccomp import OnesComplement
from typing import List


class HalfAdder(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    # outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = no_con(),
                 in_b: ElectricComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b

        self.out_sum = XOR(self.in_a, self.in_b)
        self.out_carry = AND(self.in_a, self.in_b)

    def __str__(self):
        return str(int(self.out_carry.is_on)) + str(int(self.out_sum.is_on))


class FullAdder(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_carry')
    # outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = no_con(),
                 in_b: ElectricComponent = no_con(),
                 in_carry: ElectricComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry

        self.HA1 = HalfAdder(self.in_a, self.in_b)
        self.HA2 = HalfAdder(self.in_carry, self.HA1.out_sum)

        self.out_sum = self.HA2.out_sum
        self.out_carry = OR(self.HA1.out_carry, self.HA2.out_carry)

    def __str__(self):
        return str(int(self.out_carry.is_on)) + str(int(self.out_sum.is_on))


class Eight_Bit_Adder(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_carry')
    # outputs = ElectricComponent.unpack_io('out_sum:8', 'out_carry')

    @autoparse
    def __init__(self,
                 in_a: List[ElectricComponent] = no_con(8),
                 in_b: List[ElectricComponent] = no_con(8),
                 in_carry: ElectricComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry

        self.adders = [FullAdder(self.in_a[7], self.in_b[7], self.in_carry)]
        for i in range(7):
            self.adders.append(FullAdder(
                self.in_a[6-i], self.in_b[6-i], self.adders[i].out_carry)
            )
        self.adders.reverse()

        self.out_sum = [fa.out_sum for fa in self.adders]
        self.out_carry = self.adders[0].out_carry

    def __str__(self):
        bitlist = [str(int(self.out_carry.is_on))] + ['_'] + \
            [str(int(b.is_on)) for b in self.out_sum]
        return ''.join(bitlist)


class Sixteen_Bit_Adder(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a:16', 'in_b:16', 'in_carry')
    # outputs = ElectricComponent.unpack_io('out_sum:16', 'out_carry')

    @autoparse
    def __init__(self,
                 in_a: List[ElectricComponent] = no_con(16),
                 in_b: List[ElectricComponent] = no_con(16),
                 in_carry: ElectricComponent = no_con()):
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


class Adder(SecondaryComponent):
    """
    """

    @autoparse
    def __init__(self,
                 in_a: List[ElectricComponent],
                 in_b: List[ElectricComponent],
                 in_carry: ElectricComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry

        self.nbit = len(self.in_a)
        if len(self.in_b) != self.nbit:
            raise ValueError("Inputs must be of identical length")

        self.adders = [FullAdder(
            self.in_a[self.nbit-1],
            self.in_b[self.nbit-1],
            self.in_carry)]
        for i in range(self.nbit-1):
            self.adders.append(FullAdder(
                self.in_a[self.nbit-2-i],
                self.in_b[self.nbit-2-i],
                self.adders[i].out_carry)
            )
        self.adders.reverse()

        self.out_sum = [fa.out_sum for fa in self.adders]
        self.out_carry = self.adders[0].out_carry

    def __str__(self):
        bitlist = [str(int(self.out_carry.is_on))] + ['_'] + \
            [str(int(b.is_on)) for b in self.out_sum]
        return ''.join(bitlist)


class AddMin(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_sub')
    # outputs = ElectricComponent.unpack_io('out_sum:8', 'out_flow')

    @autoparse
    def __init__(self,
                 in_a: List[ElectricComponent] = no_con(8),
                 in_b: List[ElectricComponent] = no_con(8),
                 in_sub: ElectricComponent = no_con()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_sub = in_sub

        self.oc1 = OnesComplement(self.in_b, self.in_sub)
        self.eba1 = Eight_Bit_Adder(self.in_a, self.oc1.out_main, self.in_sub)

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


class AddingMachine2(SecondaryComponent):
    """
    The second of two adding machines (p. 170)
    !!! Because the monkeys are not very good at pressing
    a button and immediately releasing it an
    Edge-Triggered Latch is used instead of the
    Level-Triggered Latch in the book
    """

    @autoparse
    def __init__(self,
                 in_a: List[ElectricComponent] = no_con(8),
                 in_add: ElectricComponent = no_con(),
                 in_clear: ElectricComponent = no_con()) -> None:
        self.in_a = in_a
        self.in_add = in_add
        self.in_clear = in_clear

        self.eba = Eight_Bit_Adder(self.in_a)
        self.ebl = EdgeTrig8BitLatchPreCl(
            self.eba.out_sum, self.in_add, in_clear=self.in_clear)
        self.eba.connect_input('in_b', self.ebl.out_q)

        self.out_bulbs = self.ebl.out_q

    def __str__(self):
        bitlist = [str(int(b.is_on)) for b in self.out_bulbs]
        return ''.join(bitlist)
