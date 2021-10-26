from switchsimulator.corecomponents import Switch
from switchsimulator.misccomp import OnesComplement, Selector_2_1
from switchsimulator.helpers import bts


def test_ones_complement():
    s1 = Switch(True)
    myinp = bts('01010101')
    oc1 = OnesComplement(myinp, s1)
    assert(oc1.__str__() == '10101010')
    s1.flip()
    assert(oc1.__str__() == '01010101')


def test_selector_2_1():
    s1 = Switch(True)
    s2 = Switch(False)
    ss = Switch(False)
    sel1 = Selector_2_1(s1, s2, ss)
    sel2 = Selector_2_1(s2, s1, ss)
    assert(sel1.__str__() == s1.__str__())
    assert(sel2.__str__() == s2.__str__())
    ss.flip()
    assert(sel1.__str__() == s2.__str__())
    assert(sel2.__str__() == s1.__str__())
    ss = Switch(True)
    sel1 = Selector_2_1(s1, s2, ss)
    sel2 = Selector_2_1(s2, s1, ss)
    assert(sel1.__str__() == s2.__str__())
    assert(sel2.__str__() == s1.__str__())
