from electriccomponent import ElectricComponent
from integratedcomponent import IntegratedComponent
from corecomponents import LooseWire, AND, OR, INV
from logicgates import XOR
from helpers import autoparse, _lwd


class OnesComplement(IntegratedComponent):

    # inputs = ElectricComponent.unpack_io('in_in:8', 'in_invert')
    # outputs = ElectricComponent.unpack_io('out_main:8')

    @autoparse
    def __init__(self,
                 in_in: list[ElectricComponent] = _lwd(8),
                 in_invert: ElectricComponent = _lwd()):
        self.out_main = [XOR(inp, self.in_invert) for inp in self.in_in]

    def __str__(self):
        bitlist = [str(int(b.is_on)) for b in self.out_main]
        return ''.join(bitlist)


class Selector_2_1(IntegratedComponent):

    # inputs = ElectricComponent.unpack_io('in_a', 'in_b', 'in_select')
    # outputs = ElectricComponent.unpack_io('out_main')

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None,
                 in_select: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.in_select = in_select if in_select is not None else LooseWire()
        self.and1 = AND(self.in_b, self.in_select)
        self.and2 = AND(self.in_a, INV(self.in_select))
        self.out_main = OR(self.and1, self.and2)

    def __str__(self):
        return str(int(self.out_main.is_on))
