import cProfile
from components import ElectricComponent, Switch, ipp
from logicgates import AND, OR, XOR


# todo: inherit from SingleStateComponent?
class Connector:
    def __init__(self, unit, pout):
        self.unit = unit
        self.pout = pout

    def get_state(self):
        return self.unit.get_state(self.pout)

    is_on = property(get_state)


class HalfAdder:
    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = AND(in_a, in_b)
        self.XOR1 = XOR(in_a, in_b)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")
        self.update()

    def update(self):
        self.out_carry = self.AND1.is_on
        self.out_sum = self.XOR1.is_on

    def get_state(self, pout):
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))


class FullAdder:
    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.HA1 = HalfAdder(in_a, in_b)
        self.HA2 = HalfAdder(in_carry, self.HA1.con_s)
        self.OR1 = OR(self.HA1.con_c, self.HA2.con_c)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")
        self.update()

    def update(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2.con_s.is_on

    def get_state(self, pout):
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))


B0 = Switch(False)
B1 = Switch(True)

asd = HalfAdder(B0, B0)
print(asd)
asd = HalfAdder(B0, B1)
print(asd)
asd = HalfAdder(B1, B0)
print(asd)
asd = HalfAdder(B1, B1)
print(asd)


asd = FullAdder(B0, B0, B0)
print(asd)

asd = FullAdder(B0, B0, B1)
print(asd)

asd = FullAdder(B0, B1, B0)
print(asd)

asd = FullAdder(B1, B0, B0)
print(asd)

asd = FullAdder(B0, B1, B1)
print(asd)

asd = FullAdder(B1, B0, B1)
print(asd)

asd = FullAdder(B1, B1, B0)
print(asd)

asd = FullAdder(B1, B1, B1)
print(asd)


class Eight_Bit_Adder:
    def __init__(self, in_a=None, in_b=None, in_carry=False):
        self.in_a = in_a
        self.in_b = in_b

        self.FAs = [FullAdder(
            Switch(in_a.pop()), Switch(in_b.pop()), Switch(in_carry))]
        for i in range(1, 8):
            self.FAs.append(FullAdder(
                Switch(in_a.pop()), Switch(in_b.pop()), self.FAs[i-1].con_c))

        self.update()

    def update(self):
        # lsb first
        self.out = [y.con_s.is_on for y in self.FAs] + [self.FAs[-1].con_c.is_on]

    def __str__(self):
        bitlist = [str(int(b)) for b in self.out][::-1]
        # bitlist.reverse()
        return ''.join(bitlist)


print(Eight_Bit_Adder(ipp('00000001'), ipp('00000001')))
print(Eight_Bit_Adder(ipp('00001111'), ipp('00001111')))
print(Eight_Bit_Adder(ipp('01111111'), ipp('01111111')))

# import cProfile
# cProfile.run("Eight_Bit_Adder(ipp('00001111'), ipp('00001111'))")
# cProfile.run("Eight_Bit_Adder(ipp('01111111'), ipp('01111111'))")


# todo 16Bitadder
