from codebooksim.corecomponents import Switch
from codebooksim.adders import Adder, AddingMachine2, HalfAdder, FullAdder
from codebooksim.adders import Eight_Bit_Adder, Sixteen_Bit_Adder, AddMin
from codebooksim.helpers import bts

s1 = Switch(True)
s2 = Switch(True)
s3 = Switch(False)
s4 = Switch(False)

s5 = Switch(True)
s6 = Switch(False)


def test_half_adder():
    ha1 = HalfAdder(s1, s2)
    assert(str(ha1).__str__() == '10')
    ha2 = HalfAdder(s3, s4)
    assert(str(ha2) == '00')
    ha3 = HalfAdder(s1, s3)
    assert(str(ha3) == '01')
    ha4 = HalfAdder(s3, s1)
    assert(str(ha4) == '01')


def test_full_adder():
    fa1 = FullAdder(s1, s2, s5)
    assert(str(fa1) == '11')
    fa2 = FullAdder(s3, s4, s6)
    assert(str(fa2) == '00')
    fa3 = FullAdder(s1, s2, s6)
    assert(str(fa3) == '10')
    fa4 = FullAdder(s1, s3, s6)
    assert(str(fa4) == '01')


def test_propagation():
    ha1 = HalfAdder(s1, s2)
    ha3 = HalfAdder(s1, s3)
    ha4 = HalfAdder(s3, s1)
    fa1 = FullAdder(s1, s2, s5)
    fa2 = FullAdder(s3, s4, s6)
    fa3 = FullAdder(s1, s2, s6)
    fa4 = FullAdder(s1, s3, s6)
    s1.flip()
    assert(str(ha1) == '01')
    assert(str(ha4) == '00')
    assert(str(fa1) == '10')
    assert(str(fa3) == '01')
    assert(str(fa4) == '00')
    s1.flip()
    assert(str(ha1) == '10')
    s3.flip()
    assert(str(ha3) == '10')
    assert(str(fa2) == '01')
    assert(str(fa4) == '10')


def test_Eight_Bit_Adder():
    eba1 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(False))
    assert(str(eba1) == '0_00000010')
    eba2 = Eight_Bit_Adder(bts('00000001'), bts('00000001'), Switch(True))
    assert(str(eba2) == '0_00000011')
    eba3 = Eight_Bit_Adder(bts('10000001'), bts('10000001'), Switch(True))
    assert(str(eba3) == '1_00000011')


def test_Eight_Bit_Adder_connect_input():
    eba4 = Eight_Bit_Adder(bts('10000001'))
    assert(str(eba4) == '0_10000001')
    b0 = Switch(True)
    eba4.connect_input("in_carry", b0)
    assert(str(eba4) == '0_10000010')
    eba4.connect_input("in_b", bts('10001100'))
    assert(str(eba4) == '1_00001110')
    b0.flip()
    assert(str(eba4) == '1_00001101')


def test_Sixteen_Bit_Adder():
    s1 = Switch(True)
    sba1 = Sixteen_Bit_Adder(bts('1000000000000001'),
                             bts('1000000000000001'), s1)
    assert(str(sba1) == '1_0000000000000011')
    s1.flip()
    assert(str(sba1) == '1_0000000000000010')


def test_Adder():
    # 8bit
    eba4 = Adder(bts('10000001'), bts('00001100'))
    assert(str(eba4) == '0_10001101')
    b0 = Switch(True)
    eba4.connect_input("in_carry", b0)
    assert(str(eba4) == '0_10001110')
    b0.flip()
    assert(str(eba4) == '0_10001101')

    # 16 bit
    s1 = Switch(True)
    sba1 = Adder(bts('1000000000000001'),
                 bts('1000000000000001'), s1)
    assert(str(sba1) == '1_0000000000000011')
    s1.flip()
    assert(str(sba1) == '1_0000000000000010')

    try:
        s1 = Switch(True)
        sba1 = Adder(bts('101'), bts('1'))
        assert False
    except ValueError:
        assert True


def test_AddMin():
    sub = Switch(False)
    am1 = AddMin(bts('00000001'), bts('00000001'), sub)
    assert(str(am1) == '00000010')
    am2 = AddMin(bts('00000101'), bts('00000011'), sub)
    assert(str(am2) == '00001000')
    am3 = AddMin(bts('10000000'), bts('10000001'), sub)
    assert(str(am3) == 'OvErFlOw00000001')
    sub.flip()
    assert(str(am1) == '00000000')
    assert(str(am2) == '00000010')
    assert('UnDeRfLoW' in str(am3))


def test_AddMachine():
    inp_sw = bts('00000001')
    s_add = Switch(False)
    s_cl = Switch(False)
    am2 = AddingMachine2(inp_sw, s_add, s_cl)
    s_cl.close()
    assert(str(am2) == '00000000')
    s_cl.open()
    assert(str(am2) == '00000000')
    s_add.flip()
    assert(str(am2) == '00000001')
    s_add.flip()
    s_add.flip()
    assert(str(am2) == '00000010')
    inp_sw[1].flip()
    inp_sw[7].flip()
    assert(str(am2) == '00000010')
    s_add.flip()
    s_add.flip()
    assert(str(am2) == '01000010')
