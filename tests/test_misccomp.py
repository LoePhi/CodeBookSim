from switchsimulator.corecomponents import Switch
from switchsimulator.misccomp import OnesComplement
from switchsimulator.helpers import bts


def test_ones_complement():
    s1 = Switch(True)
    myinp = bts('01010101')
    oc1 = OnesComplement(myinp, s1)
    assert(oc1.__str__() == '10101010')
    s1.flip()
    assert(oc1.__str__() == '01010101')
