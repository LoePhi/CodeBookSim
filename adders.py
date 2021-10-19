import cProfile
from component import ElectricComponent
from singlestatecomp import Switch, Connector, LooseWire
from logicgates import AND, OR, XOR
from helpers import bts


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

# Tests


b1 = Switch(True)
b2 = Switch(True)
b3 = Switch(False)
b4 = Switch(False)

ha1 = HalfAdder(b1, b2)
assert(ha1.__str__() == '10')
ha2 = HalfAdder(b3, b4)
assert(ha2.__str__() == '00')
ha3 = HalfAdder(b1, b3)
assert(ha3.__str__() == '01')
ha4 = HalfAdder(b3, b1)
assert(ha4.__str__() == '01')

b5 = Switch(True)
b6 = Switch(False)

fa1 = FullAdder(b1, b2, b5)
assert(fa1.__str__() == '11')
fa2 = FullAdder(b3, b4, b6)
assert(fa2.__str__() == '00')
fa3 = FullAdder(b1, b2, b6)
assert(fa3.__str__() == '10')
fa4 = FullAdder(b1, b3, b6)
assert(fa4.__str__() == '01')

b1.flip()
assert(ha1.__str__() == '01')
assert(ha4.__str__() == '00')
assert(fa1.__str__() == '10')
assert(fa3.__str__() == '01')
assert(fa4.__str__() == '00')
b1.flip()
assert(ha1.__str__() == '10')
b3.flip()
assert(ha3.__str__() == '10')
assert(fa2.__str__() == '01')
assert(fa4.__str__() == '10')


eba1 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(False))
assert(eba1.__str__() == '0_00000010')
eba2 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(True))
assert(eba2.__str__() == '0_00000011')
eba3 = Eight_Bit_Adder(bts('10000001'), bts('10000001'), Switch(True))
assert(eba3.__str__() == '1_00000011')


eba4 = Eight_Bit_Adder(bts('10000001'))
assert(eba4.__str__() == '0_10000001')
b0 = Switch(True)
eba4.connect_input("in_carry", b0)
assert(eba4.__str__() == '0_10000010')
eba4.connect_input("in_b", bts('10001100'))
assert(eba4.__str__() == '1_00001110')

cProfile.run(
    "Sixteen_Bit_Adder(bts('1000000000000001'),"
    "bts('1000000000000001'), Switch(True))")


# todo 16Bitadder
sba1 = Sixteen_Bit_Adder(bts('1000000000000001'),
                         bts('1000000000000001'), Switch(True))
assert(sba1.__str__() == '0_0000000100000011')
