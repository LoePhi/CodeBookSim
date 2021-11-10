from switchsimulator.base import MultiBitSOC, SingleBitSOC
from switchsimulator.base import no_con, autoparse, InputComponent
from switchsimulator.corecomponents import AND, OR, INV
from switchsimulator.logicgates import XOR, AND4, OR8
from typing import Sequence


class OnesComplement(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_in: Sequence[InputComponent] = no_con(8),
                 in_invert: InputComponent = no_con()) -> None:
        self.in_in = in_in
        self.in_invert = in_invert

        self.out_main = [XOR(inp, self.in_invert) for inp in self.in_in]


class Selector_2_1(SingleBitSOC):

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con(),
                 in_b: InputComponent = no_con(),
                 in_select: InputComponent = no_con()) -> None:
        self.in_a = in_a
        self.in_b = in_b
        self.in_select = in_select

        self.and1 = AND(self.in_b, self.in_select)
        self.and2 = AND(self.in_a, INV(self.in_select))

        self.out_main = OR(self.and1, self.and2)


class Selector_8_1(SingleBitSOC):
    """
    select = '000' adresses the last lement in in_data
    """

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(8),
                 in_select: Sequence[InputComponent] = no_con(3)) -> None:
        self.in_data = in_data
        self.in_select = in_select

        self.invs = [INV(s) for s in self.in_select]

        selc = tuple(zip(self.in_select, self.invs))
        bcd = [(b, c, d) for b in selc[0] for c in selc[1] for d in selc[2]]
        self.ands = [AND4(self.in_data[i], *bcd[i]) for i in range(8)]
        self.out_main = OR8(self.ands)


class Decoder_3_8(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: Sequence[InputComponent] = no_con(3)) -> None:
        self.in_data = in_data
        self.in_select = in_select

        self.invs = [INV(s) for s in self.in_select]

        selc = tuple(zip(self.in_select, self.invs))
        bcd = [(b, c, d) for b in selc[0] for c in selc[1] for d in selc[2]]
        self.ands = [AND4(self.in_data, *bcd[i]) for i in range(8)]
        self.out_main = self.ands
