from typing import Callable, List, Optional, Tuple
from switchsimulator.electriccomponent import ElectricComponent
import inspect
from functools import wraps


class CoreComponent(ElectricComponent):
    """
    Parent Class for all core components
    These are the basic buidling blocks that all
    other components are assembled from

    All core components have a singlaur output-line
    called 'out_main'
    """

    out_main: bool

    def compute_state(self) -> None:
        raise NotImplementedError

    def build_circuit(self) -> None:
        raise NotImplementedError

    def setup(self) -> None:
        self.forward_connections: List[Tuple[CoreComponent, str]] = []
        self.build_circuit()
        self.compute_state()

    def get_state(self) -> bool:
        """Returns the current state of the output"""
        return self.out_main

    is_on = property(get_state)

    def add_connection(self, con: 'CoreComponent', port: str) -> None:
        """Called by downstream elements to add them as a forward connection"""
        if (con, port) not in self.forward_connections:
            self.forward_connections.append((con, port))

    def forward_pass(self) -> None:
        for fc in self.forward_connections:
            fc[0].update()

    # TODO: ?keep state
    def update(self) -> None:
        old_state = self.out_main
        self.compute_state()
        if self.out_main != old_state:
            self.forward_pass()

    def __str__(self) -> str:
        return str(int(self.out_main))


class Switch(CoreComponent):
    """
    Simple Switch. It is used to control a gate.
    When the gate is closed it carries a current.
    """

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


class LooseWire(CoreComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    def __init__(self) -> None:
        self.setup()

    def build_circuit(self) -> None:
        pass

    def compute_state(self) -> None:
        self.out_main = False


class _LooseWireSentinel(ElectricComponent):

    def __init__(self) -> None:
        pass


def no_con(n: Optional[int] = None):
    """
    ONLY for use with the @autoparse decorator.
    LooseWires are temporary and will be exchanged by the decorator.
    """
    if n is None:
        return _LooseWireSentinel()
    else:
        return [_LooseWireSentinel() for _ in range(n)]


def exchange_sentinel(x):
    if isinstance(x, list):
        return [exchange_sentinel(e) for e in x]
    elif isinstance(x, tuple):
        return tuple(exchange_sentinel(e) for e in x)
    elif isinstance(x, _LooseWireSentinel):
        return LooseWire()
    else:
        return x


def autoparse(init: Callable) -> Callable:
    inispec = inspect.getfullargspec(init)
    parnames = inispec.args[1:]
    defaults = inispec.defaults

    @wraps(init)
    def wrapped_init(self, *args, **kwargs) -> None:
        # Turn args into kwargs
        kwargs.update(zip(parnames[:len(args)], args))

        # apply default parameter values
        default_start = len(parnames) - len(defaults)
        for i in range(len(defaults)):
            if parnames[default_start + i] not in kwargs:
                kwargs[parnames[default_start + i]] = defaults[i]

        # exchange Sentinels for LooseWires
        for kw in kwargs:
            kwargs[kw] = exchange_sentinel(kwargs[kw])

        init(self, **kwargs)

    return wrapped_init


class INV(CoreComponent):
    """Inverts the input"""

    # inputs = ElectricComponent.unpack_io('in_a', )

    # TODO: type check darf Core, SingleState
    # -> module umstrukturienen: baseclasses mit
    # elctric, core, secondary, singlestate
    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = no_con()) -> None:
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

    @autoparse
    def __init__(self,
                 in_a: ElectricComponent = no_con(),
                 in_b: ElectricComponent = no_con()) -> None:
        self.in_a = in_a
        self.in_b = in_b
        self.setup()

    def build_circuit(self) -> None:
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')


class AND(BaseGate):
    """AND-Gate"""

    def compute_state(self) -> None:
        self.out_main = False
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = True


class OR(BaseGate):
    """OR-Gate"""

    def compute_state(self) -> None:
        self.out_main = False
        if self.in_a.is_on:
            self.out_main = True
        if self.in_b.is_on:
            self.out_main = True


class NOR(BaseGate):
    """NOR-Gate"""

    def compute_state(self) -> None:
        self.out_main = True
        if self.in_a.is_on:
            self.out_main = False
        if self.in_b.is_on:
            self.out_main = False


class NAND(BaseGate):
    """NAND-Gate"""

    def compute_state(self) -> None:
        self.out_main = True
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = False
