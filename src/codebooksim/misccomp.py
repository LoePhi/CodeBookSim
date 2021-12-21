from codebooksim.base import MultiBitSOC, SingleBitSOC
from codebooksim.base import no_con, autoparse, InputComponent
from codebooksim.corecomponents import AND, OR, INV
from codebooksim.logicgates import ANDX, OR64K, XOR, AND4, OR8
from typing import List, Sequence, Tuple


class OnesComplement(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_in: Sequence[InputComponent] = no_con(8),
                 in_invert: InputComponent = no_con()) -> None:
        self.in_in = in_in
        self.in_invert = in_invert

        self.out_main = [XOR(inp, self.in_invert) for inp in self.in_in]


class Selector_2_1(SingleBitSOC):
    """
    Compared to the book the selection is reversed.
    This was done to establish parity with the later
    selectors where the 'highest' selection targets
    the first bit
    """

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con(),
                 in_b: InputComponent = no_con(),
                 in_select: InputComponent = no_con()) -> None:
        self.in_a = in_a
        self.in_b = in_b
        self.in_select = in_select

        self.and1 = AND(self.in_a, self.in_select)
        self.and2 = AND(self.in_b, INV(self.in_select))

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

        sel_inv_pairs = tuple(zip(self.in_select, self.invs))
        bcd = [(b, c, d) for b in sel_inv_pairs[0]
               for c in sel_inv_pairs[1] for d in sel_inv_pairs[2]]
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

        sel_inv_pairs = tuple(zip(self.in_select, self.invs))
        bcd = [(b, c, d) for b in sel_inv_pairs[0]
               for c in sel_inv_pairs[1] for d in sel_inv_pairs[2]]
        self.ands = [AND4(self.in_data, *e) for e in bcd]
        self.out_main = self.ands


class Decoder_1_2(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: InputComponent = no_con()) -> None:
        self.in_data = in_data
        self.in_select = in_select

        self.inv = INV(self.in_select)
        self.ands = [AND(self.in_data, self.in_select),
                     AND(self.in_data, self.inv)]
        self.out_main = self.ands


def _gen_combinations(si_pairs: List[Tuple[InputComponent, InputComponent]],
                      combl: List[Sequence[InputComponent]] = []
                      ) -> List[Sequence[InputComponent]]:
    if len(si_pairs) > 0:
        pair = si_pairs.pop()
        if len(combl) == 0:
            combl = [(b,) for b in pair]
            combl = _gen_combinations(si_pairs, combl)
        else:
            combl = [(*t, b) for b in pair for t in combl]
            combl = _gen_combinations(si_pairs, combl)
    return combl


class Decoder_16_64K(MultiBitSOC):

    @autoparse
    def __init__(self,
                 in_data: InputComponent = no_con(),
                 in_select: Sequence[InputComponent] = no_con(16)) -> None:
        self.in_data = in_data
        self.in_select = in_select

        self.invs = [INV(s) for s in self.in_select]
        sel_inv_pairs = list(zip(self.in_select, self.invs))
        all_comb = [t[::-1] for t in _gen_combinations(sel_inv_pairs)]

        self.ands = [ANDX((self.in_data, *c)) for c in all_comb]
        self.out_main = self.ands


class Selector_64K_1(SingleBitSOC):
    """
    select = '0000000000000000' adresses the last lement in in_data
    """

    @autoparse
    def __init__(self,
                 in_data: Sequence[InputComponent] = no_con(2**16),
                 in_select: Sequence[InputComponent] = no_con(16)) -> None:
        self.in_data = in_data
        self.in_select = in_select

        self.invs = [INV(s) for s in self.in_select]
        sel_inv_pairs = list(zip(self.in_select, self.invs))
        all_comb = [t[::-1] for t in _gen_combinations(sel_inv_pairs)]

        self.ands = [ANDX((self.in_data[i], *all_comb[i]))
                     for i in range(len(all_comb))]
        self.out_main = OR64K(self.ands)
