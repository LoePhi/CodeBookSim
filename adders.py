from component import ElectricComponent
from singlestatecomp import Switch, Connector, LooseWire
from logicgates import AND, OR, XOR
from helpers import bts8


class HalfAdder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(), in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.setup()
        self.con_sum = Connector(self, "sum")
        self.con_carry = Connector(self, "carry")

    def build_circuit(self):
        self.AND1 = AND(self.in_a, self.in_b)
        self.XOR1 = XOR(self.in_a, self.in_b)
        self.AND1.add_forward_connection(self)
        self.XOR1.add_forward_connection(self)

    def compute_state(self):
        self.out_carry = self.AND1.is_on
        self.out_sum = self.XOR1.is_on

    # TODO: replace with getattr? -> nur carry/sum statt out_carry/out_sum
    def get_state(self, port):
        if port == "carry":
            return self.out_carry
        elif port == "sum":
            return self.out_sum
        else:
            raise ValueError("Invalid Port '" + port + "'")

    def __str__(self):
        return str(int(self.out_carry)) + str(int(self.out_sum))


class FullAdder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_carry', 'out_sum')

    def __init__(self, in_a: ElectricComponent = LooseWire(), in_b: ElectricComponent = LooseWire(), in_carry: ElectricComponent = LooseWire()):
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
        self.OR1.add_forward_connection(self)
        self.HA2.con_sum.add_forward_connection(self)

    def compute_state(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2.con_sum.is_on

    def __str__(self):
        return str(int(self.out_carry)) + str(int(self.out_sum))


# TODO: work with list input
# entweder in complete_check auspacken oder hir direkt auspacken
# hier direkt scheint logischer, aber das macht die inoput spezifikation
# kompliziert -> am besten erstmal neu denken wie das überhaupt gehandhabt werden soll.


class Eight_Bit_Adder(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_a:8', 'in_b:8', 'in_carry')
    outputs = ElectricComponent.unpack_io('out_sum:8', 'out_carry')

    def __init__(self, in_a: ElectricComponent = [LooseWire() for x in range(8)],
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

    def compute_state(self):
        # lsb first
        self.out_sum = [fa.con_sum.is_on for fa in self.full_adders]
        self.out_carry = self.full_adders[0].con_carry.is_on

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


eba1 = Eight_Bit_Adder(bts8('00000001'), bts8('00000001'), Switch(False))
assert(eba1.__str__() == '0_00000010')
eba2 = Eight_Bit_Adder(bts8('00000001'), bts8('00000001'), Switch(True))
assert(eba2.__str__() == '0_00000011')
eba3 = Eight_Bit_Adder(bts8('10000001'), bts8('10000001'), Switch(True))
assert(eba3.__str__() == '1_00000011')


eba4 = Eight_Bit_Adder(bts8('10000001'))
assert(eba4.__str__() == '0_10000001')
eba4.connect_input("in_carry", Switch(True))
assert(eba4.__str__() == '0_10000010')
eba4.connect_input("in_b", bts8('10001100'))
assert(eba4.__str__() == '1_00001110')

# import cProfile
# cProfile.run("Eight_Bit_Adder(ipp('00001111'), ipp('00001111'))")
# cProfile.run("Eight_Bit_Adder(ipp('01111111'), ipp('01111111'))")


# todo 16Bitadder
