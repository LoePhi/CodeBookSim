import pytest
from codebooksim.corecomponents import Switch, INV, AND, OR, NOR, NAND
from codebooksim.logicgates import XOR, NOR3, OR8, AND4
from codebooksim.logicgates import AND17, ANDX, OR64K, ORX
from codebooksim.helpers import bts


s1 = Switch(True)
s2 = Switch(True)
s3 = Switch(False)
s4 = Switch(False)


def test_inverter():
    i1 = INV(s1)
    i3 = INV(s3)
    assert(not i1.is_on)
    assert(i3.is_on)


def test_and():
    and_12 = AND(s1, s2)
    and_13 = AND(s1, s3)
    and_34 = AND(s3, s4)
    assert(and_12.is_on)
    assert(not and_13.is_on)
    assert(not and_13.is_on)
    assert(not and_34.is_on)


def test_or():
    or_12 = OR(s1, s2)
    or_13 = OR(s1, s3)
    or_34 = OR(s3, s4)
    assert(or_12.is_on)
    assert(or_13.is_on)
    assert(not or_34.is_on)


def test_nand():
    nand_12 = NAND(s1, s2)
    nand_13 = NAND(s1, s3)
    nand_34 = NAND(s3, s4)
    assert(not nand_12.is_on)
    assert(nand_13.is_on)
    assert(nand_34.is_on)


def test_xor():
    xor_12 = XOR(s1, s2)
    xor_13 = XOR(s1, s3)
    xor_34 = XOR(s3, s4)
    assert(not xor_12.is_on)
    assert(xor_13.is_on)
    assert(not xor_34.is_on)


def test_nor():
    nor_12 = NOR(s1, s2)
    nor_13 = NOR(s1, s3)
    nor_34 = NOR(s3, s4)
    assert(not nor_12.is_on)
    assert(not nor_13.is_on)
    assert(nor_34.is_on)


def test_combine():
    and_12 = AND(s1, s2)
    and_13 = AND(s1, s3)
    comb1 = AND(and_12, INV(and_13))
    comb2 = AND(and_12, and_13)
    assert(comb1.is_on)
    assert(not comb2.is_on)


def test_forward_prop():
    s5 = Switch(True)
    inv1 = INV(s5)
    and1 = AND(s1, s5)
    or1 = OR(s3, s5)
    nand1 = NAND(s1, s5)
    xor1 = XOR(s5, s1)
    nor1 = NOR(s5, s3)
    s5.flip()
    assert(inv1.is_on)
    assert(not and1.is_on)
    assert(not or1.is_on)
    assert(nand1.is_on)
    assert(xor1.is_on)
    assert(nor1.is_on)


def test_unconnected_input():
    or1 = OR(s1)
    nor1 = NOR(in_b=s1)
    assert(or1.is_on)
    assert(not nor1.is_on)
    s1.flip()
    assert(not or1.is_on)
    assert(nor1.is_on)
    or1.connect_input("in_b", s2)
    nor1.connect_input("in_a", s2)
    assert(or1.is_on)
    assert(not nor1.is_on)


def test_connect_multiprop():
    """Test forward prob trough multiple layers after new connect"""
    s1 = Switch(True)
    s2 = Switch(True)
    s3 = Switch(True)
    and1 = AND(in_b=s1)
    and2 = AND(and1, s2)
    and3 = AND(and2, s3)
    and1.connect_input('in_a', Switch(True))
    assert(and3.is_on)
    s1.flip()
    assert(not and3.is_on)


def test_connect_multiprop_noncore():
    """Test forward prob trough multiple layers after new connect"""
    s1 = Switch(True)
    s2 = Switch(True)
    s3 = Switch(True)
    nand1 = NAND(in_b=s1)  # T
    xor1 = XOR(in_a=s2)  # T
    nor1 = NOR(nand1, xor1)  # F
    nand1.connect_input('in_a', s3)
    xor1.connect_input('in_b', s3)
    assert(nor1.is_on)
    s3.flip()
    assert(not nor1.is_on)


def test_unstable_recursion():
    s_up = Switch(False)
    s_down = Switch(True)

    and1 = AND(s_up)
    xor1 = XOR(s_down, and1)
    and1.connect_input('in_b', xor1)

    with pytest.raises(RecursionError):
        s_up.flip()


def test_nor3():
    s1 = Switch(False)
    s2 = Switch(False)
    s3 = Switch(False)
    s4 = Switch(True)
    s5 = Switch(True)
    s6 = Switch(True)
    nor1 = NOR3(s1, s2, s3)
    nor2 = NOR3(s6, s4, s5)
    nor3 = NOR3(s3, s1, s2)
    nor4 = NOR3(s3, s4, s2)
    nor5 = NOR3(s6, s4, s2)
    assert(nor1.is_on)
    assert(not nor2.is_on)
    assert(nor3.is_on)
    assert(not nor4.is_on)
    assert(not nor5.is_on)
    nor6 = NOR3(s1, in_c=s3)
    nor6.connect_input('in_b', s2)
    assert(nor6.is_on)


def test_and4():
    x = bts('0000')
    y = AND4(*x)
    assert not y.is_on
    x[0].flip()
    assert not y.is_on
    x[1].flip()
    assert not y.is_on
    x[2].flip()
    assert not y.is_on
    x[3].flip()
    assert y.is_on
    x[0].flip()
    assert not y.is_on


def test_or8():
    x = bts('00000000')
    y = OR8(x)
    assert not y.is_on
    x[0].flip()
    assert y.is_on
    x[0].flip()
    assert not y.is_on
    x[7].flip()
    assert y.is_on


def test_and17():
    x = bts('01111111111111101')
    y = AND17(x)
    assert not y.is_on
    x[0].flip()
    assert not y.is_on
    x[15].flip()
    assert y.is_on


def test_andx():
    x = bts('01111111111111101')
    y = ANDX(x)
    assert not y.is_on
    x[0].flip()
    assert not y.is_on
    x[15].flip()
    assert y.is_on


def test_orx():
    x = bts('000000000000000000000')
    y = ORX(x)
    assert not y.is_on
    x[0].flip()
    assert y.is_on
    x[0].flip()
    x[10].flip()
    assert y.is_on
    x[10].flip()
    assert not y.is_on
    x[-1].flip()
    assert y.is_on
    x[-1].flip()
    assert not y.is_on


def test_or64k():
    x = bts('0'*(2**16))
    y = OR64K(x)
    assert not y.is_on
    x[0].flip()
    assert y.is_on
    x[0].flip()
    x[10].flip()
    assert y.is_on
    x[10].flip()
    assert not y.is_on
    x[-1].flip()
    assert y.is_on
    x[-1].flip()
    assert not y.is_on
