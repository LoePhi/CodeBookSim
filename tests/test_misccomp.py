from switchsimulator.corecomponents import Switch
from switchsimulator.misccomp import Decoder_1_2, Decoder_3_8, OnesComplement
from switchsimulator.misccomp import Selector_2_1, Selector_8_1
from switchsimulator.helpers import bts


def test_ones_complement():
    s1 = Switch(True)
    myinp = bts('01010101')
    oc1 = OnesComplement(myinp, s1)
    assert(str(oc1) == '10101010')
    s1.flip()
    assert(str(oc1) == '01010101')
    s1.flip()
    assert(str(oc1) == '10101010')


def test_selector_2_1():
    s1 = Switch(True)
    s2 = Switch(False)
    ss = Switch(False)
    sel1 = Selector_2_1(s2, s1, ss)
    sel2 = Selector_2_1(s1, s2, ss)
    assert(str(sel1) == str(s1))
    assert(str(sel2) == str(s2))
    ss.flip()
    assert(str(sel1) == str(s2))
    assert(str(sel2) == str(s1))
    ss = Switch(True)
    sel1 = Selector_2_1(s2, s1, ss)
    sel2 = Selector_2_1(s1, s2, ss)
    assert(str(sel1) == str(s2))
    assert(str(sel2) == str(s1))


def test_selector_8_1():
    d = bts('11010000')
    se = bts('000')
    y = Selector_8_1(d, se)
    assert not y.is_on
    d[7].flip()
    assert y.is_on
    d[7].flip()
    assert not y.is_on
    se[0].flip()
    assert y.is_on
    se[1].flip()
    assert y.is_on
    se[2].flip()
    assert y.is_on
    se[0].flip()
    assert not y.is_on


def test_decoder_3_8():
    d = Switch(True)
    se = bts('000')
    y = Decoder_3_8(d, se)
    assert str(y) == '00000001'
    d.flip()
    assert str(y) == '00000000'
    se[0].flip()
    assert str(y) == '00000000'
    d.flip()
    assert str(y) == '00010000'


def test_decoder_1_2():
    d = Switch(True)
    se = Switch(False)
    y = Decoder_1_2(d, se)
    assert str(y) == '01'
    d.flip()
    assert str(y) == '00'
    se.flip()
    assert str(y) == '00'
    d.flip()
    assert str(y) == '10'
