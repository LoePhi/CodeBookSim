from switchsimulator.singlestatecomp import Switch
from switchsimulator.logicgates import INV, AND, OR, NAND, XOR, NOR


b1 = Switch(True)
b2 = Switch(True)
b3 = Switch(False)
b4 = Switch(False)

i1 = INV(b1)
i3 = INV(b3)


def test_inverter():
    assert(not i1.is_on)
    assert(i3.is_on)


and_12 = AND(b1, b2)
and_13 = AND(b1, b3)
and_34 = AND(b3, b4)


def test_and():
    assert(and_12.is_on)
    assert(not and_13.is_on)
    assert(not and_13.is_on)


or_12 = OR(b1, b2)
or_13 = OR(b1, b3)
or_34 = OR(b3, b4)


def test_or():
    assert(or_12.is_on is True)
    assert(or_13.is_on is True)
    assert(or_34.is_on is False)


nand_12 = NAND(b1, b2)
nand_13 = NAND(b1, b3)
nand_34 = NAND(b3, b4)


def test_nand():
    assert(nand_12.is_on is False)
    assert(nand_13.is_on is True)
    assert(nand_34.is_on is True)


xor_12 = XOR(b1, b2)
xor_13 = XOR(b1, b3)
xor_34 = XOR(b3, b4)


def test_xor():
    assert(xor_12.is_on is False)
    assert(xor_13.is_on is True)
    assert(xor_34.is_on is False)


nor_12 = NOR(b1, b2)
nor_13 = NOR(b1, b3)
nor_34 = NOR(b3, b4)


def test_nor():
    assert(nor_12.is_on is False)
    assert(nor_13.is_on is False)
    assert(nor_34.is_on is True)


comb1 = AND(and_12, INV(and_13))
comb2 = AND(and_12, and_13)


def test_combine():
    assert(comb1.is_on is True)
    assert(comb2.is_on is False)
