from typing import Sequence
from codebooksim.base import MultiBitSOC, SingleBitSOC
from codebooksim.base import autoparse, no_con, InputComponent
from codebooksim.corecomponents import AND, INV, NOR, OR
from codebooksim.logicgates import NOR3
from codebooksim.misccomp import Decoder_16_64K, Decoder_1_2, Decoder_3_8
from codebooksim.misccomp import Selector_2_1, Selector_8_1, Selector_64K_1


class RSFlipFlop(SingleBitSOC):
    """
    Although all flipflops have two outputs, these outputs
    are always opposites of each other which is why the FFs
    are modeled as SingleBit-Circuits.
    out_q is taken as the main output
    """

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

        self.out_main = self.out_q

    def fullstr(self, full: bool = True) -> str:
        if full:
            if not (self.out_q.is_on + self.out_qb.is_on) == 1:
                raise ValueError("Bad Innput to RS-FlipFlop")
            return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
        else:
            return super().__str__()


class LevelTrigDTFlipFlop(SingleBitSOC):

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

        self.out_main = self.out_q

    def fullstr(self, full: bool = True) -> str:
        if full:
            return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
        else:
            return super().__str__()


class LevelTrigDTFlipFlopCl(SingleBitSOC):

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

        self.out_main = self.out_q

    def fullstr(self, full: bool = True) -> str:
        if full:
            return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
        else:
            return super().__str__()


class EdgeTrigDTFlipFlop(SingleBitSOC):

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

        self.out_main = self.out_q

    def fullstr(self, full: bool = True) -> str:
        if full:
            return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
        else:
            return super().__str__()


class EdgeTrigDTFlipFlopPreCl(SingleBitSOC):

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

        self.out_q = self.nor21
        self.out_qb = self.nor22

        self.out_main = self.out_q

    def fullstr(self, full: bool = True) -> str:
        if full:
            return str(int(self.out_q.is_on)) + str(int(self.out_qb.is_on))
        else:
            return super().__str__()


class LevelTrig8BitLatch(MultiBitSOC):
    """
    documentation
    """

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8),
                 in_clock: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_clock = in_clock

        self.out_q = [LevelTrigDTFlipFlop(
            d, self.in_clock) for d in self.in_data]

        self.out_main = self.out_q


class EdgeTrig8BitLatchPreCl(MultiBitSOC):

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

        self.out_q = [EdgeTrigDTFlipFlopPreCl(
            d, self.in_clock, self.in_preset, self.in_clear)
            for d in self.in_data]

        self.out_main = self.out_q


class RAM_8_1(SingleBitSOC):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: Sequence[InputComponent] = no_con(3),
                 in_write: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_select = in_select
        self.in_write = in_write

        self.dec = Decoder_3_8(self.in_write, self.in_select)
        self.latches = [LevelTrigDTFlipFlop(self.in_data, d) for d in self.dec]
        self.sel = Selector_8_1(self.latches, self.in_select)

        self.out_main = self.sel


class RAM_8_2(MultiBitSOC):
    """
    p. 199
    """

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(2),
                 in_select: Sequence[InputComponent] = no_con(3),
                 in_write: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_select = in_select
        self.in_write = in_write

        self.ram1 = RAM_8_1(self.in_data[0], self.in_select, self.in_write)
        self.ram2 = RAM_8_1(self.in_data[1], self.in_select, self.in_write)

        self.out_main = [self.ram1, self.ram2]


class RAM_16_1(SingleBitSOC):
    """
    The diagram in the book is wrong. This is the correct
    implementation
    """
    # WIP
    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: Sequence[InputComponent] = no_con(4),
                 in_write: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_select = in_select
        self.in_write = in_write

        self.dec12 = Decoder_1_2(self.in_write, self.in_select[0])
        self.ram1 = RAM_8_1(self.in_data, self.in_select[1:], self.dec12[0])
        self.ram2 = RAM_8_1(self.in_data, self.in_select[1:], self.dec12[1])
        self.sel21 = Selector_2_1(self.ram1, self.ram2, self.in_select[0])

        self.out_main = self.sel21


class RAM_64K_1(SingleBitSOC):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: Sequence[InputComponent] = no_con(16),
                 in_write: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_select = in_select
        self.in_write = in_write

        self.dec = Decoder_16_64K(self.in_write, self.in_select)
        self.latches = [LevelTrigDTFlipFlop(self.in_data, d) for d in self.dec]
        self.sel = Selector_64K_1(self.latches, self.in_select)

        self.out_main = self.sel


class RAM_64K_8(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8),
                 in_select: Sequence[InputComponent] = no_con(16),
                 in_write: InputComponent = no_con()) -> None:

        self.in_data = in_data
        self.in_select = in_select
        self.in_write = in_write

        self.rams = [RAM_64K_1(self.in_data[i], self.in_select, self.in_write)
                     for i in range(8)]

        self.out_main = self.rams
