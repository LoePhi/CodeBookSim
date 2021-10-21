import pytest
from switchsimulator.corecomponents import Switch, INV, AND, OR
from switchsimulator.logicgates import NAND, XOR, NOR


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
    assert(and3.is_on is True)
    s1.flip()
    assert(and3.is_on is False)


def test_unstable_recursion():
    s_up = Switch(False)
    s_down = Switch(True)

    and1 = AND(s_up)
    xor1 = XOR(s_down, and1)
    and1.connect_input('in_b', xor1)

    with pytest.raises(RecursionError):
        s_up.flip()
