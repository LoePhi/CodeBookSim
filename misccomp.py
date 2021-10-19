from component import ElectricComponent
from singlestatecomp import LooseWire, Switch
from logicgates import XOR
from helpers import bts


class OnesComplement(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_in:8', 'in_invert')
    outputs = ElectricComponent.unpack_io('_outline')

    def __init__(self,
                 in_in: ElectricComponent = [LooseWire() for x in range(8)],
                 in_invert: ElectricComponent = LooseWire()):
        self.in_in = in_in
        self.in_invert = in_invert
        self.setup()

    def build_circuit(self):
        self.xors = [XOR(inp, self.in_invert) for inp in self.in_in]
        for xor in self.xors:
            xor.add_connection(self, 'outline')

    def compute_state(self):
        self._outline = [xor.is_on for xor in self.xors]

    def __str__(self):
        bitlist = [str(int(b)) for b in self._outline]
        return ''.join(bitlist)


i1 = Switch(True)
myinp = bts('01010101')
asd = OnesComplement(myinp, i1)
print(asd)
i1.flip()
print(asd)
