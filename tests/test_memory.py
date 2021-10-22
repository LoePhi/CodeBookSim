import pytest
from switchsimulator.corecomponents import Switch
from switchsimulator.memory import RSFlipFlop, DTFlipFlop, EightBitLatch
from switchsimulator.helpers import bts


def test_rs_flipflop():
    r = Switch(False)
    s = Switch(True)
    ff = RSFlipFlop(r, s)
    assert(ff.__str__() == '10')  # 10
    s.open()
    assert(ff.__str__() == '10')  # 10
    r.close()
    assert(ff.__str__() == '01')  # 01
    r.open()
    assert(ff.__str__() == '01')  # 01
    with pytest.raises(ValueError):
        s.close()
        r.close()
        ff.__str__()


def test_dt_flipflop():
    d = Switch(False)
    c = Switch(True)
    ff = DTFlipFlop(d, c)
    assert(ff.__str__() == '01')
    c.open()
    assert(ff.__str__() == '01')
    d.close()
    assert(ff.__str__() == '01')
    c.close()
    assert(ff.__str__() == '10')
    c.open()
    assert(ff.__str__() == '10')
    d.flip()
    assert(ff.__str__() == '10')
    c.close()
    assert(ff.__str__() == '01')


def test_eight_bit_latch():
    clock = Switch(True)
    data = bts('01010101')
    ebl1 = EightBitLatch(data, clock)
    assert(ebl1.__str__() == '01010101')
    clock.flip()
    assert(ebl1.__str__() == '01010101')
    data[0].flip()
    assert(ebl1.__str__() == '01010101')
    ebl2 = EightBitLatch(data, clock)
    clock.flip()
    assert(ebl1.__str__() == '11010101')
    assert(ebl2.__str__() == '11010101')
