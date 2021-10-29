import pytest
from switchsimulator.corecomponents import Switch
from switchsimulator.memory import RSFlipFlop, LevelTrigDTFlipFlop
from switchsimulator.memory import LevelTrig8BitLatch, EdgeTrigDTFlipFlop
from switchsimulator.memory import EdgeTrigDTFlipFlopPreCl
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


def test_lvlt_dt_flipflop():
    d = Switch(False)
    c = Switch(True)
    ff = LevelTrigDTFlipFlop(d, c)
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


def test_edget_dt_flipflop():
    s1 = Switch(True)
    s2 = Switch(False)
    c1 = Switch(True)
    etdtff1 = EdgeTrigDTFlipFlop(s1, c1)
    etdtff2 = EdgeTrigDTFlipFlop(s2, c1)
    c1.flip()  # f
    c1.flip()
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '01')
    s1.flip()
    assert(etdtff1.__str__() == '10')
    c1.flip()
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '01')
    s2.flip()
    assert(etdtff2.__str__() == '01')
    c1.flip()
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '10')


def test_eight_bit_latch():
    clock = Switch(True)
    data = bts('01010101')
    ebl1 = LevelTrig8BitLatch(data, clock)
    assert(ebl1.__str__() == '01010101')
    clock.flip()
    assert(ebl1.__str__() == '01010101')
    data[0].flip()
    assert(ebl1.__str__() == '01010101')
    ebl2 = LevelTrig8BitLatch(data, clock)
    clock.flip()
    assert(ebl1.__str__() == '11010101')
    assert(ebl2.__str__() == '11010101')


def test_edget_dt_flipflop_precl():
    s1 = Switch(True)
    s2 = Switch(False)
    c1 = Switch(True)
    pre = Switch(False)
    clear = Switch(False)
    etdtff1 = EdgeTrigDTFlipFlopPreCl(s1, c1, pre, clear)
    etdtff2 = EdgeTrigDTFlipFlopPreCl(s2, c1, pre, clear)
    c1.flip()
    c1.flip()   # -> on
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '01')
    s1.flip()
    assert(etdtff1.__str__() == '10')
    c1.flip()   # off
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '01')
    s2.flip()
    assert(etdtff2.__str__() == '01')
    c1.flip()   # -> on
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '10')

    pre.flip()
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '10')
    pre.flip()
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '10')
    c1.flip()  # off
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '10')
    c1.flip()  # -> on
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '10')
    c1.flip()
    pre.flip()
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '10')
    c1.flip()  # ->on
    assert(etdtff1.__str__() == '10')
    assert(etdtff2.__str__() == '10')
    pre.flip()

    clear.flip()
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '01')
    clear.flip()
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '01')
    c1.flip()  # off
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '01')
    c1.flip()  # -> on
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '10')
    c1.flip()
    clear.flip()
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '01')
    c1.flip()  # ->on
    assert(etdtff1.__str__() == '01')
    assert(etdtff2.__str__() == '01')
