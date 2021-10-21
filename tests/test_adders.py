from switchsimulator.corecomponents import Switch
from switchsimulator.adders import HalfAdder, FullAdder
from switchsimulator.adders import Eight_Bit_Adder, Sixteen_Bit_Adder, AddMin
from switchsimulator.helpers import bts

s1 = Switch(True)
s2 = Switch(True)
s3 = Switch(False)
s4 = Switch(False)

s5 = Switch(True)
s6 = Switch(False)


def test_half_adder():
    ha1 = HalfAdder(s1, s2)
    assert(ha1.__str__() == '10')
    ha2 = HalfAdder(s3, s4)
    assert(ha2.__str__() == '00')
    ha3 = HalfAdder(s1, s3)
    assert(ha3.__str__() == '01')
    ha4 = HalfAdder(s3, s1)
    assert(ha4.__str__() == '01')


def test_full_adder():
    fa1 = FullAdder(s1, s2, s5)
    assert(fa1.__str__() == '11')
    fa2 = FullAdder(s3, s4, s6)
    assert(fa2.__str__() == '00')
    fa3 = FullAdder(s1, s2, s6)
    assert(fa3.__str__() == '10')
    fa4 = FullAdder(s1, s3, s6)
    assert(fa4.__str__() == '01')


def test_propagation():
    ha1 = HalfAdder(s1, s2)
    ha3 = HalfAdder(s1, s3)
    ha4 = HalfAdder(s3, s1)
    fa1 = FullAdder(s1, s2, s5)
    fa2 = FullAdder(s3, s4, s6)
    fa3 = FullAdder(s1, s2, s6)
    fa4 = FullAdder(s1, s3, s6)
    s1.flip()
    assert(ha1.__str__() == '01')
    assert(ha4.__str__() == '00')
    assert(fa1.__str__() == '10')
    assert(fa3.__str__() == '01')
    assert(fa4.__str__() == '00')
    s1.flip()
    assert(ha1.__str__() == '10')
    s3.flip()
    assert(ha3.__str__() == '10')
    assert(fa2.__str__() == '01')
    assert(fa4.__str__() == '10')


def test_Eight_Bit_Adder():
    eba1 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(False))
    assert(eba1.__str__() == '0_00000010')
    eba2 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(True))
    assert(eba2.__str__() == '0_00000011')
    eba3 = Eight_Bit_Adder(bts('10000001'), bts('10000001'), Switch(True))
    assert(eba3.__str__() == '1_00000011')


def test_Eight_Bit_Adder_connect_input():
    eba4 = Eight_Bit_Adder(bts('10000001'))
    assert(eba4.__str__() == '0_10000001')
    b0 = Switch(True)
    eba4.connect_input("in_carry", b0)
    assert(eba4.__str__() == '0_10000010')
    eba4.connect_input("in_b", bts('10001100'))
    assert(eba4.__str__() == '1_00001110')
    b0.flip()
    assert(eba4.__str__() == '1_00001101')


def test_Sixteen_Bit_Adder():
    s1 = Switch(True)
    sba1 = Sixteen_Bit_Adder(bts('1000000000000001'),
                                bts('1000000000000001'), s1)
    assert(sba1.__str__() == '1_0000000000000011')
    s1.flip()
    assert(sba1.__str__() == '1_0000000000000010')


# def test_AddMin():
#     am = AddMin(bts('00000001'), bts('00000001'), Switch(False))
#     assert(eba1.__str__() == '0_00000010')
#     eba2 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(True))
#     assert(eba2.__str__() == '0_00000011')
#     eba3 = Eight_Bit_Adder(bts('10000001'), bts('10000001'), Switch(True))
#     assert(eba3.__str__() == '1_00000011')
