from typing import Sequence
from switchsimulator.base import SecondaryComponent
from switchsimulator.base import autoparse, no_con, InputComponent
from switchsimulator.corecomponents import AND, INV, NOR, OR
from switchsimulator.logicgates import NOR3


class RSFlipFlop(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_r: InputComponent = no_con(),
                 in_s: InputComponent = no_con()) -> None:
        self.in_r = in_r
        self.in_s = in_s

        self.nor1 = NOR(self.in_r)
        self.nor2 = NOR(self.nor1, self.in_s)
        self.nor1.connect_input("in_b", self.nor2)

        self.out_q = self.nor1
        self.out_qb = self.nor2

    def __str__(self) -> str:
        if not (self.out_q.is_on or self.out_qb.is_on):
            raise ValueError("Bad Innput to RS-FlipFlop")
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class LevelTrigDTFlipFlop(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_clock: InputComponent = no_con()) -> None:
        self.in_data = in_data
        self.in_clock = in_clock

        self.and1 = AND(INV(self.in_data), self.in_clock)
        self.and2 = AND(self.in_data, self.in_clock)
        self.rsff1 = RSFlipFlop(self.and1, self.and2)

        self.out_q = self.rsff1.out_q
        self.out_qb = self.rsff1.out_qb

    def __str__(self) -> str:
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class LevelTrigDTFlipFlopCl(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_clock: InputComponent = no_con(),
                 in_clear: InputComponent = no_con()) -> None:
        self.in_data = in_data
        self.in_clock = in_clock
        self.in_clear = in_clear

        self.and1 = AND(INV(self.in_data), self.in_clock)
        self.and2 = AND(self.in_data, self.in_clock)
        self.or1 = OR(self.in_clear, self.and1)
        self.rsff1 = RSFlipFlop(self.or1, self.and2)

        self.out_q = self.rsff1.out_q
        self.out_qb = self.rsff1.out_qb

    def __str__(self) -> str:
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class EdgeTrigDTFlipFlop(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_clock: InputComponent = no_con()) -> None:
        self.in_data = in_data
        self.in_clock = in_clock

        self.dtff1 = LevelTrigDTFlipFlop(
            INV(self.in_data), INV(self.in_clock))
        self.dtff2 = LevelTrigDTFlipFlop(self.dtff1.out_qb, self.in_clock)

        self.out_q = self.dtff2.out_q
        self.out_qb = self.dtff2.out_qb

    def __str__(self) -> str:
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class EdgeTrigDTFlipFlopPreCl(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_clock: InputComponent = no_con(),
                 in_preset: InputComponent = no_con(),
                 in_clear: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_clock = in_clock
        self.in_preset = in_preset
        self.in_clear = in_clear

        self.inv_c = INV(self.in_clock)

        self.nor11 = NOR3(self.in_clear)
        self.nor12 = NOR3(self.nor11, self.in_preset, self.inv_c)
        self.nor13 = NOR3(self.nor12, self.inv_c)
        self.nor14 = NOR3(self.nor13, self.in_preset, self.in_data)
        self.nor11.connect_input('in_b', self.nor14)
        self.nor11.connect_input('in_c', self.nor12)
        self.nor13.connect_input('in_c', self.nor14)

        self.nor21 = NOR3(self.in_clear, self.nor12)
        self.nor22 = NOR3(self.nor21, self.in_preset, self.nor13)
        self.nor21.connect_input('in_c', self.nor22)

        self.out_q = self.nor21.out_main
        self.out_qb = self.nor22.out_main

    def __str__(self) -> str:
        return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))


class LevelTrig8BitLatch(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8),
                 in_clock: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_clock = in_clock

        self.dtff = [LevelTrigDTFlipFlop(
            d, self.in_clock) for d in self.in_data]

        self.out_q = [dtf.out_q for dtf in self.dtff]

    def __str__(self) -> str:
        return ''.join([str(int(q.is_on)) for q in self.out_q])


class EdgeTrig8BitLatchPreCl(SecondaryComponent):

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8),
                 in_clock: InputComponent = no_con(),
                 in_preset: InputComponent = no_con(),
                 in_clear: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_clock = in_clock
        self.in_preset = in_preset
        self.in_clear = in_clear

        self.etff = [EdgeTrigDTFlipFlopPreCl(
            d, self.in_clock, self.in_preset, self.in_clear)
            for d in self.in_data]

        self.out_q = [dtf.out_q for dtf in self.etff]

    def __str__(self) -> str:
        return ''.join([str(int(q.is_on)) for q in self.out_q])
