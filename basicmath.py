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
        self.HA1_c = Connector(self.HA1, "carry")
        self.HA1_s = Connector(self.HA1, "sum")
        self.HA2 = HalfAdder(in_carry, self.HA1_s)
        self.HA2_c = Connector(self.HA2, "carry")
        self.HA2_s = Connector(self.HA2, "sum")
        self.OR1 = bg.OR(self.HA1_c, self.HA2_c)

    def update(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2_s.get_state()

    def get_state(self, pout):
        self.update()
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))

class YFullAdder:
    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.HA1 = HalfAdder(in_a, in_b)
        self.HA2 = HalfAdder(in_carry, self.HA1.con_s)
        self.OR1 = bg.OR(self.HA1.con_c, self.HA2.con_c)

    def update(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2.con_s.get_state()

    def get_state(self, pout):
        self.update()
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))

class XFullAdder:
    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.HA1_c, self.HA1_s = make_half_adder(in_a, in_b)
        self.HA2_c, self.HA2_s = make_half_adder(in_carry, self.HA1_s)
        self.OR1 = bg.OR(self.HA1_c, self.HA2_c)

    def update(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2_s.get_state()

    def get_state(self, pout):
        self.update()
        if pout == "carry":
            return self.out_carry
        if pout == "sum":
            return self.out_sum

    def __str__(self):
        self.update()
        return str(int(self.out_carry)) + str(int(self.out_sum))


def make_half_adder(in_a, in_b):
    tmp = HalfAdder(in_a, in_b)
    cc = Connector(tmp, "carry")
    cs = Connector(tmp, "sum")
    return cc, cs

B0 = bg.Bit(False)
B1 = bg.Bit(True)

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


asd = XFullAdder(B0, B0, B0)
print(asd)

asd = XFullAdder(B0, B0, B1)
print(asd)

asd = XFullAdder(B0, B1, B0)
print(asd)

asd = XFullAdder(B1, B0, B0)
print(asd)

asd = XFullAdder(B0, B1, B1)
print(asd)

asd = XFullAdder(B1, B0, B1)
print(asd)

asd = XFullAdder(B1, B1, B0)
print(asd)

asd = XFullAdder(B1, B1, B1)
print(asd)


asd = YFullAdder(B0, B0, B0)
print(asd)

asd = YFullAdder(B0, B0, B1)
print(asd)

asd = YFullAdder(B0, B1, B0)
print(asd)

asd = YFullAdder(B1, B0, B0)
print(asd)

asd = YFullAdder(B0, B1, B1)
print(asd)

asd = YFullAdder(B1, B0, B1)
print(asd)

asd = YFullAdder(B1, B1, B0)
print(asd)

asd = YFullAdder(B1, B1, B1)
print(asd)
