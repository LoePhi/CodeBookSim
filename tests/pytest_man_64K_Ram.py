from switchsimulator.memory import RAM_64K_1, RAM_64K_8
from switchsimulator.corecomponents import Switch
from switchsimulator.helpers import bts


def test_ram_64k_1():
    d = Switch(False)
    se = bts('0000000000000000')
    w = Switch(True)
    ra = RAM_64K_1(d, se, w)

    assert ra.__str__() == '0'
    w.flip()  # F
    d.flip()  # T
    assert ra.__str__() == '0'
    w.flip()  # T
    assert ra.__str__() == '1'
    se[10].flip()
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


def test_ram_64k_8():
    d = bts('10001000')
    se = bts('0000000000000000')
    w = Switch(True)
    ra = RAM_64K_8(d, se, w)

    assert ra.__str__() == '10001000'
    w.flip()  # F
    d[7].flip()  # T
    assert ra.__str__() == '10001000'
    w.flip()  # T
    assert ra.__str__() == '10001001'
    se[10].flip()
    assert ra.__str__() == '10001001'
    d[0].flip()  # F
    assert ra.__str__() == '00001001'
    d[0].flip()  # T
    assert ra.__str__() == '10001001'
    se[0].flip()  # 0011
    assert ra.__str__() == '10001001'
    d[7].flip()  # F
    assert ra.__str__() == '10001000'
    w.flip()  # F
    se[0].flip()  # 0010
    assert ra.__str__() == '10001001'
