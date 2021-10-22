from helpers import bts
from corecomponents import Switch
from electriccomponent import ElectricComponent
from integratedcomponent import IntegratedComponent
from corecomponents import LooseWire, AND, INV, Switch
from logicgates import NOR


class RSFlipFlop(IntegratedComponent):

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


class DTFlipFlop(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_data', 'in_clock')
    outputs = ElectricComponent.unpack_io('out_q', 'out_qb')

    def __init__(self,
                 in_data: ElectricComponent = LooseWire(),
                 in_clock: ElectricComponent = LooseWire()):
        self.in_data = in_data
        self.in_clock = in_clock
        self.and1 = AND(INV(self.in_data), self.in_clock)
        self.and2 = AND(self.in_data, self.in_clock)
        self.rsff1 = RSFlipFlop(self.and1, self.and2)
        self.out_q = self.rsff1.out_q
        self.out_qb = self.rsff1.out_qb

    def __str__(self):
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class EightBitLatch(IntegratedComponent):

    inputs = ElectricComponent.unpack_io('in_data:8', 'in_clock')
    outputs = ElectricComponent.unpack_io('out_q', 'out_qb')

    def __init__(self,
                 in_data: ElectricComponent = [LooseWire() for x in range(8)],
                 in_clock: ElectricComponent = LooseWire()):
        self.in_data = in_data
        self.in_clock = in_clock
        self.dtfs = [DTFlipFlop(d, self.in_clock) for d in self.in_data]
        self.out_q = [dtf.out_q for dtf in self.dtfs]

    def __str__(self):
        return ''.join([str(int(q.is_on)) for q in self.out_q])


c = Switch(True)
eba1 = EightBitLatch(bts('01010101'), c)
print(eba1)
c.flip()
print(eba1)


d = Switch(True)
c = Switch(False)
dt1 = DTFlipFlop(d, c)
print(dt1.out_q.is_on)
c.flip()