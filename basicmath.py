import basicgates as bg


class HalfAdder:
    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.AND1 = bg.AND(in_a, in_b)
        self.XOR1 = bg.XOR(in_a, in_b)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")

    def update(self):
        self.out_carry = self.AND1.is_on
        self.out_sum = self.XOR1.is_on

    def get_state(self, pout):
        self.update()
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))


class Connector:
    def __init__(self, unit, pout):
        self.unit = unit
        self.pout = pout

    def get_state(self):
        return self.unit.get_state(self.pout)

    is_on = property(get_state)


class FullAdder:
    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.HA1 = HalfAdder(in_a, in_b)
        self.HA2 = HalfAdder(in_carry, self.HA1.con_s)
        self.OR1 = bg.OR(self.HA1.con_c, self.HA2.con_c)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")

    def update(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2.con_s.is_on

    def get_state(self, pout):
        self.update()
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))


B0 = bg.Bit(False)
B1 = bg.Bit(True)

asd = HalfAdder(B0, B0)
print(asd)
# asd = HalfAdder(B0, B1)
# print(asd)
# asd = HalfAdder(B1, B0)
# print(asd)
# asd = HalfAdder(B1, B1)
# print(asd)


asd = FullAdder(B0, B0, B0)
print(asd)

# asd = FullAdder(B0, B0, B1)
# print(asd)

# asd = FullAdder(B0, B1, B0)
# print(asd)

# asd = FullAdder(B1, B0, B0)
# print(asd)

# asd = FullAdder(B0, B1, B1)
# print(asd)

# asd = FullAdder(B1, B0, B1)
# print(asd)

# asd = FullAdder(B1, B1, B0)
# print(asd)

# asd = FullAdder(B1, B1, B1)
# print(asd)


class Eight_Bit_Adder:
    def __init__(self, in_a=None, in_b=None, in_carry=False):
        self.in_a = in_a
        self.in_b = in_b
        self.a = [FullAdder(bg.Bit(bool(int(in_a.pop()))), bg.Bit(
            bool(int(in_b.pop()))), bg.Bit(in_carry))]
        for i in range(1, 6):
            self.a.append(FullAdder(bg.Bit(bool(int(in_a.pop()))),
                          bg.Bit(bool(int(in_b.pop()))), self.a[i-1].con_c))

    def update(self):
        # lsb first
        self.out = [y.con_s.is_on for y in self.a] + [self.a[-1].con_c.is_on]

    def __str__(self):
        self.update()
        bitlist = [str(int(b)) for b in self.out][::-1]
        #bitlist.reverse()
        return ''.join(bitlist)

qwe = Eight_Bit_Adder(list('00001111'), list('00001111'))
cProfile.run('print(qwe.a[0])')
cProfile.run('print(qwe.a[1])')
cProfile.run('print(qwe.a[2])')
cProfile.run('print(qwe.a[3])')

qwe = Eight_Bit_Adder(list('00000001'), list('00000001'))
print(qwe)


qwe = Eight_Bit_Adder(list('111111'), list('111111'))
print(qwe)

qwe = Eight_Bit_Adder(list('00000001'), list('00000001'))
print(qwe)


qwe = Eight_Bit_Adder(list('11111111'), list('11111111'))

print(qwe)
qwe = Eight_Bit_Adder(list('00000001'), list('00000001'))
print(qwe)


qwe = Eight_Bit_Adder(list('11111111'), list('11111111'))
print(qwe)
qwe = Eight_Bit_Adder(list('00000001'), list('00000001'))
print(qwe)


qwe = Eight_Bit_Adder(list('11111111'), list('11111111'))
print(qwe)

def phelp():
    fg = Eight_Bit_Adder(list('11111111'), list('11111111'))
    print(fg)

phelp()

# todo 16Bitadder

import cProfile
cProfile.run('print(qwe)')

# performance scheiße weil für jedes bit wieder alles geupdatet wird