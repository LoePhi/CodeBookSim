from switchsimulator.electriccomponent import ElectricComponent
from switchsimulator.secondarycomponents import SecondaryComponent
from switchsimulator.corecomponents import AND, OR, INV, set_sent, autoparse
from switchsimulator.logicgates import XOR
from typing import List


class OnesComplement(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_in:8', 'in_invert')
    # outputs = ElectricComponent.unpack_io('out_main:8')

    @autoparse
    def __init__(self,
                 in_in: List[ElectricComponent] = set_sent(8),
                 in_invert: ElectricComponent = set_sent()):
        self.in_in = in_in
        self.in_invert = in_invert

        self.out_main = [XOR(inp, self.in_invert) for inp in self.in_in]

    def __str__(self):
        bitlist = [str(int(b.is_on)) for b in self.out_main]
        return ''.join(bitlist)


class Selector_2_1(SecondaryComponent):

    # inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_select')
    # outputs = ElectricComponent.unpack_io('out_main')

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = set_sent(),
                 in_b: ElectricComponent = set_sent(),
                 in_select: ElectricComponent = set_sent()):
        self.in_a = in_a
        self.in_b = in_b
        self.in_select = in_select

        self.and1 = AND(self.in_b, self.in_select)
        self.and2 = AND(self.in_a, INV(self.in_select))

        self.out_main = OR(self.and1, self.and2)

    def __str__(self):
        return str(int(self.out_main.is_on))
