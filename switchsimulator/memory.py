from electriccomponent import ElectricComponent
from corecomponents import LooseWire, AND, INV
from logicgates import NOR


class RSFlipFlop(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_r', 'in_s')
    outputs = ElectricComponent.unpack_io('out_q', 'out_qb')

    def __init__(self,
                 in_r: ElectricComponent = LooseWire(),
                 in_s: ElectricComponent = LooseWire()):
        self.in_r = in_r
        self.in_s = in_s
        self.nor1 = NOR(self.in_r)
        self.nor2 = NOR(self.nor1, self.in_s)
        self.nor1.connect_input("in_b", self.nor2)
        self.out_q = self.nor1
        self.out_qb = self.nor2

    def __str__(self):
        if not (self.out_q.is_on or self.out_qb.is_on):
            raise ValueError("Bad Innput to RS-FlipFlop")
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class DTFlipFlop(ElectricComponent):

    inputs = ElectricComponent.unpack_io('in_clock', 'in_data')
    outputs = ElectricComponent.unpack_io('out_q', 'out_qb')

    def __init__(self,
                 in_clock: ElectricComponent = LooseWire(),
                 in_data: ElectricComponent = LooseWire()):
        self.in_clock = in_clock
        self.in_data = in_data
        self.and1 = AND(self.in_clock, INV(self.in_data))
        self.and2 = AND(self.in_clock, self.in_data)
        self.rsff1 = RSFlipFlop(self.and1, self.and2)
        self.out_q = self.rsff1.out_q
        self.out_qb = self.rsff1.out_qb

    def __str__(self):
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
