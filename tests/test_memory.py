import pytest
from switchsimulator.corecomponents import Switch
from switchsimulator.memory import RAM_16_1, RAM_8_1, RAM_8_2
from switchsimulator.memory import EdgeTrig8BitLatchPreCl, RSFlipFlop
from switchsimulator.memory import LevelTrigDTFlipFlop, LevelTrigDTFlipFlopCl
from switchsimulator.memory import EdgeTrigDTFlipFlop, EdgeTrigDTFlipFlopPreCl
from switchsimulator.memory import LevelTrig8BitLatch
from switchsimulator.helpers import bts


def test_rs_flipflop():
    r = Switch(False)
    s = Switch(True)
    ff = RSFlipFlop(r, s)
    assert(ff.__str__(True) == '10')  # 10
    assert(ff.__str__() == '1')
    s.open()
    assert(ff.__str__(True) == '10')  # 10
    r.close()
    assert(ff.__str__(True) == '01')  # 01
    assert(ff.__str__() == '0')
    r.open()
    assert(ff.__str__(True) == '01')  # 01
    with pytest.raises(ValueError):
        s.close()
        r.close()
        ff.__str__(True)


def test_lvlt_dt_flipflop():
    d = Switch(False)
    c = Switch(True)
    ff = LevelTrigDTFlipFlop(d, c)
    assert(ff.__str__(True) == '01')
    c.open()
    assert(ff.__str__(True) == '01')
    d.close()
    assert(ff.__str__(True) == '01')
    c.close()
    assert(ff.__str__(True) == '10')
    c.open()
    assert(ff.__str__(True) == '10')
    d.flip()
    assert(ff.__str__(True) == '10')
    c.close()
    assert(ff.__str__(True) == '01')


def test_lvlt_dt_flipflop_cl():
    d = Switch(False)
    c = Switch(True)
    ff = LevelTrigDTFlipFlopCl(d, c)
    assert(ff.__str__(True) == '01')
    c.open()
    assert(ff.__str__(True) == '01')
    d.close()
    assert(ff.__str__(True) == '01')
    c.close()
    assert(ff.__str__(True) == '10')
    c.open()
    assert(ff.__str__(True) == '10')
    d.flip()
    assert(ff.__str__(True) == '10')
    c.close()
    assert(ff.__str__(True) == '01')
    clear = Switch(False)
    ff.connect_input('in_clear', clear)
    d.close()
    assert(ff.__str__() == '1')
    clear.close()
    assert(ff.__str__() == '0')
    clear.open()
    assert(ff.__str__() == '1')
    c.open()
    clear.close()
    assert(ff.__str__() == '0')


def test_edget_dt_flipflop():
    s1 = Switch(True)
    s2 = Switch(False)
    c1 = Switch(True)
    etdtff1 = EdgeTrigDTFlipFlop(s1, c1)
    etdtff2 = EdgeTrigDTFlipFlop(s2, c1)
    c1.flip()  # f
    c1.flip()
    assert(etdtff1.__str__(True) == '10')
    assert(etdtff2.__str__(True) == '01')
    s1.flip()
    assert(etdtff1.__str__(True) == '10')
    c1.flip()
    assert(etdtff1.__str__(True) == '10')
    assert(etdtff2.__str__(True) == '01')
    s2.flip()
    assert(etdtff2.__str__() == '0')
    c1.flip()
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '1')


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
    assert(etdtff1.__str__(True) == '10')
    assert(etdtff2.__str__(True) == '01')
    s1.flip()
    assert(etdtff1.__str__(True) == '10')
    c1.flip()   # off
    assert(etdtff1.__str__(True) == '10')
    assert(etdtff2.__str__(True) == '01')
    s2.flip()
    assert(etdtff2.__str__(True) == '01')
    c1.flip()   # -> on
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '1')

    pre.flip()
    assert(etdtff1.__str__() == '1')
    assert(etdtff2.__str__() == '1')
    pre.flip()
    assert(etdtff1.__str__() == '1')
    assert(etdtff2.__str__() == '1')
    c1.flip()  # off
    assert(etdtff1.__str__() == '1')
    assert(etdtff2.__str__() == '1')
    c1.flip()  # -> on
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '1')
    c1.flip()
    pre.flip()
    assert(etdtff1.__str__() == '1')
    assert(etdtff2.__str__() == '1')
    c1.flip()  # ->on
    assert(etdtff1.__str__() == '1')
    assert(etdtff2.__str__() == '1')
    pre.flip()

    clear.flip()
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '0')
    clear.flip()
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '0')
    c1.flip()  # off
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '0')
    c1.flip()  # -> on
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '1')
    c1.flip()
    clear.flip()
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '0')
    c1.flip()  # ->on
    assert(etdtff1.__str__() == '0')
    assert(etdtff2.__str__() == '0')


def test_lvlt_8_bit_latch():
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


def test_edget_8_bit_latch_precl():
    clock = Switch(False)
    preset = Switch(False)
    clear = Switch(False)

    data = bts('01010101')
    ebl1 = EdgeTrig8BitLatchPreCl(data, clock, preset, clear)
    clock.close()
    assert(ebl1.__str__() == '01010101')
    clock.open()
    assert(ebl1.__str__() == '01010101')
    data[0].flip()
    assert(ebl1.__str__() == '01010101')
    clock.close()
    assert(ebl1.__str__() == '11010101')
    preset.flip()
    assert(ebl1.__str__() == '11111111')
    clock.open()
    assert(ebl1.__str__() == '11111111')
    clock.close()
    preset.flip()
    clear.flip()
    assert(ebl1.__str__() == '00000000')
    clock.open()
    assert(ebl1.__str__() == '00000000')


def test_ram_8_1():
    d = Switch(False)
    se = bts('000')
    w = Switch(True)
    ra = RAM_8_1(d, se, w)
    assert ra.__str__() == '0'
    for s0 in range(2):
        for s1 in range(2):
            for s2 in range(2):
                se[2].flip()
                assert ra.__str__() == '0'
            se[1].flip()
        se[0].flip()
    # Adresse jetzt bei '000'
    w.flip()  # F
    d.flip()  # T
    assert ra.__str__() == '0'
    w.flip()  # T
    assert ra.__str__() == '1'
    se[2].flip()  # 001
    assert ra.__str__() == '1'
    d.flip()
    assert ra.__str__() == '0'
    w.flip()
    se[2].flip()  # 000
    assert ra.__str__() == '1'


def test_ram_16_1():
    d = Switch(False)
    se = bts('0000')
    w = Switch(True)
    ra = RAM_16_1(d, se, w)
    assert ra.__str__() == '0'
    for s0 in range(2):
        for s1 in range(2):
            for s2 in range(2):
                for s3 in range(2):
                    se[3].flip()
                    assert ra.__str__() == '0'
                se[2].flip()
            se[1].flip()
        se[0].flip()
    # Adresse jetzt bei '0000'
    w.flip()  # F
    d.flip()  # T
    assert ra.__str__() == '0'
    w.flip()  # T
    assert ra.__str__() == '1'
    se[2].flip()  # 0010
    assert ra.__str__() == '1'
    d.flip()  # F
    assert ra.__str__() == '0'
    d.flip()  # T
    assert ra.__str__() == '1'
    se[0].flip()  # 0011
    assert ra.__str__() == '1'
    d.flip()  # F
    assert ra.__str__() == '0'
    w.flip()  # F
    se[0].flip()  # 0010
    assert ra.__str__() == '1'


def test_ram_8_2():
    d = bts('00')
    se = bts('000')
    w = Switch(True)
    ra = RAM_8_2(d, se, w)
    assert ra.__str__() == '00'
    for s0 in range(2):
        for s1 in range(2):
            for s2 in range(2):
                se[2].flip()
                assert ra.__str__() == '00'
            se[1].flip()
        se[0].flip()
    # Adresse jetzt bei '000'
    w.flip()  # F
    d[0].flip()  # T
    assert ra.__str__() == '00'
    w.flip()  # T
    assert ra.__str__() == '10'
    se[2].flip()  # 001
    assert ra.__str__() == '10'
    d[0].flip()
    d[1].flip()
    assert ra.__str__() == '01'
    w.flip()
    se[2].flip()  # 000
    assert ra.__str__() == '10'
