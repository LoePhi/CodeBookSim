from component import ElectricComponent
from corecomponents import LooseWire
from logicgates import XOR, IntegratedComponent


# TODO: bessere namen für in-, outputs; v.a. _output ersetzen
class OnesComplement(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_in:8', 'in_invert')
    outputs = ElectricComponent.unpack_io('_outline:8')

    def __init__(self,
                 in_in: ElectricComponent = [LooseWire() for x in range(8)],
                 in_invert: ElectricComponent = LooseWire()):
        self.in_in = in_in
        self.in_invert = in_invert
        self.out_main = [XOR(inp, self.in_invert) for inp in self.in_in]

    def __str__(self):
        bitlist = [str(int(b.is_on)) for b in self.out_main]
        return ''.join(bitlist)
