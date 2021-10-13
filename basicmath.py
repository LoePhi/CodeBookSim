from components import ElectricComponent, SingleStateComponent, Switch, ipp
from logicgates import AND, OR, XOR





class HalfAdder(ElectricComponent):

    inputs = ('in_a', 'in_b')
    outputs = ('out_carry', 'out_sum')

    def __init__(self, in_a=None, in_b=None):
        self.in_a = in_a
        self.in_b = in_b
        self.setup(initial=True)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")

    def build_circuit(self):
        self.AND1 = AND(self.in_a, self.in_b)
        self.XOR1 = XOR(self.in_a, self.in_b)
        self.AND1.add_forward_connection(self)
        self.XOR1.add_forward_connection(self)

    def compute_state(self):
        self.out_carry = self.AND1.is_on
        self.out_sum = self.XOR1.is_on

    # todo: replace with getattr?
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

    inputs = ('in_a', 'in_b', 'in_carry')
    outputs = ('out_carry', 'out_sum')

    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.setup(initial=True)
        self.con_c = Connector(self, "carry")
        self.con_s = Connector(self, "sum")

    def build_circuit(self):
        self.HA1 = HalfAdder(self.in_a, self.in_b)
        self.HA2 = HalfAdder(self.in_carry, self.HA1.con_s)
        self.OR1 = OR(self.HA1.con_c, self.HA2.con_c)
        self.OR1.add_forward_connection(self)
        self.HA2.con_s.add_forward_connection(self)

    def compute_state(self):
        self.out_carry = self.OR1.is_on
        self.out_sum = self.HA2.con_s.is_on

    # todo: replace with getattr?
    def get_state(self, port):
        if port == "carry":
            return self.out_carry
        elif port == "sum":
            return self.out_sum
        else:
            raise ValueError("Invalid Port '" + port + "'")

    def __str__(self):
        return str(int(self.out_carry)) + str(int(self.out_sum))



B0 = Switch(False)
B1 = Switch(True)

asd = HalfAdder(B0, B1)
print(asd)
B0.flip()
print(asd)
B0.flip()

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


# todo: work with list input
# entweder in complete_check auspacken oder hir direkt auspacken
# hier direkt scheint logischer, aber das macht die inoput spezifikation
# kompliziert -> am besten erstmal neu denken wie das überhaupt gehandhabt werden soll.
 
class Eight_Bit_Adder(ElectricComponent):

    inputs = ('in_a', 'in_b', 'in_carry') 

    def __init__(self, in_a=None, in_b=None, in_carry=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_carry = in_carry
        self.setup(initial=True)

    def build_circuit(self):
        self.FAs = [FullAdder(
            Switch(self.in_a.pop()), Switch(self.in_b.pop()), Switch(self.in_carry))]
        for i in range(1, 8):
            self.FAs.append(FullAdder(
                Switch(self.in_a.pop()), Switch(self.in_b.pop()), self.FAs[i-1].con_c))

    def compute_state(self):
        # lsb first
        self.out = [y.con_s.is_on for y in self.FAs] + [self.FAs[-1].con_c.is_on]

    def get_state(self):
        pass

    def __str__(self):
        bitlist = [str(int(b)) for b in self.out][::-1]
        # bitlist.reverse()
        return ''.join(bitlist)

asd = Eight_Bit_Adder(ipp('00000001'), ipp('00000001'))

print(Eight_Bit_Adder(ipp('00000001'), ipp('00000001')))
print(Eight_Bit_Adder(ipp('00001111'), ipp('00001111')))
print(Eight_Bit_Adder(ipp('01111111'), ipp('01111111')))

# import cProfile
# cProfile.run("Eight_Bit_Adder(ipp('00001111'), ipp('00001111'))")
# cProfile.run("Eight_Bit_Adder(ipp('01111111'), ipp('01111111'))")


# todo 16Bitadder
