from component import ElectricComponent
from singlestatecomp import Connector, LooseWire
from logicgates import NOR


class RSFlipFlop(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_r', 'in_s')
    outputs = ElectricComponent.unpack_io('out_q', 'out_qb')

    def __init__(self,
                 in_r: ElectricComponent = LooseWire(),
                 in_s: ElectricComponent = LooseWire()):
        self.in_r = in_r
        self.in_s = in_s
        self.setup()
        self.con_q = Connector(self, "out_q")
        self.con_qb = Connector(self, "out_qb")

    def build_circuit(self):
        self.NOR1 = NOR(self.in_r)
        self.NOR2 = NOR(self.NOR1, self.in_s)
        self.NOR1.connect_input("in_b", self.NOR2)
        self.NOR1.add_connection(self, "out_q")
        self.NOR2.add_connection(self, "out_qb")

    def compute_state(self):
        self.out_q = self.NOR1.is_on
        self.out_qb = self.NOR2.is_on
        if not (self.out_q or self.out_qb):
            raise ValueError("Bad Innput to RS-FlipFlop" + str(self))

    def __str__(self):
        return str(int(self.out_q)) + str(int(self.out_qb))
