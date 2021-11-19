from switchsimulator.base import _LWSent, CoreComponent, LooseWire
from switchsimulator.base import autoparse, no_con, InputComponent, use_slots


class Switch(CoreComponent):
    """
    Simple Switch. It is used to control a gate.
    When the gate is closed it carries a current.
    """

    if use_slots:
        __slots__ = ()

    def __init__(self, closed: bool = False) -> None:
        self.out_main = closed
        self.setup()

    def build_circuit(self) -> None:
        pass

    def compute_state(self) -> None:
        pass

    def flip(self) -> None:
        self.out_main = not self.out_main
        self.forward_pass()

    def open(self) -> None:
        self.out_main = False
        self.forward_pass()

    def close(self) -> None:
        self.out_main = True
        self.forward_pass()


class INV(CoreComponent):
    """Inverts the input"""

    if use_slots:
        __slots__ = ('in_a',)

    @autoparse
    def __init__(self,
                 in_a: InputComponent = no_con()) -> None:
        self.in_a = in_a
        self.setup()

    def build_circuit(self) -> None:
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self) -> None:
        self.out_main = True
        if self.in_a.is_on:
            self.out_main = False


class BaseGate(CoreComponent):
    """
    Parent for the baisc logic gates
    """

    if use_slots:
        __slots__ = ('in_a', 'in_b')

    # no @autoparse for speed reasons
    def __init__(self,
                 in_a: InputComponent = _LWSent(),
                 in_b: InputComponent = _LWSent()) -> None:

        self.in_a = in_a if not isinstance(in_a, _LWSent) else LooseWire()
        self.in_b = in_b if not isinstance(in_b, _LWSent) else LooseWire()
        self.setup()

    def build_circuit(self) -> None:
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')


class AND(BaseGate):
    """AND-Gate"""

    if use_slots:
        __slots__ = ()

    def compute_state(self) -> None:
        self.out_main = False
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = True


class OR(BaseGate):
    """OR-Gate"""
    if use_slots:
        __slots__ = ()

    def compute_state(self) -> None:
        self.out_main = False
        if self.in_a.is_on:
            self.out_main = True
        if self.in_b.is_on:
            self.out_main = True


class NOR(BaseGate):
    """NOR-Gate"""
    if use_slots:
        __slots__ = ()

    def compute_state(self) -> None:
        self.out_main = True
        if self.in_a.is_on:
            self.out_main = False
        if self.in_b.is_on:
            self.out_main = False


class NAND(BaseGate):
    """NAND-Gate"""
    if use_slots:
        __slots__ = ()

    def compute_state(self) -> None:
        self.out_main = True
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = False
