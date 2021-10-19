from component import ElectricComponent
from singlestatecomp import Connector, Switch, LooseWire
from logicgates import NOR


class FlipFlop(ElectricComponent):

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
        # TOSO ist das hier correkt? bei den anderen auch?
        self.NOR1.add_connection(self, "out_q")
        self.NOR2.add_connection(self, "out_qb")

    def compute_state(self):
        self.out_q = self.NOR1.is_on
        self.out_qb = self.NOR2.is_on
        if not (self.out_q or self.out_qb):
            raise ValueError("Bad Innput to RS-FlipFlop" + str(self))
        # TODO? raiseError if both outputs are off (==bothinputs on)?

    def __str__(self):
        return str(int(self.out_q)) + str(int(self.out_qb))


r = Switch(False)
s = Switch(False)
ff = FlipFlop(r, s)

s.close()
print(ff)  # 10
s.open()
print(ff)  # 10
r.close()
print(ff)  # 01
r.open()
print(ff)  # 01
r.close()
s.close()
print(ff)
r.open()
s.open()
print(ff)
s.close()
r.close()
print(ff)
