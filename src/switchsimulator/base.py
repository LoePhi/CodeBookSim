from typing import Any, Iterable, Iterator, Sequence, Union, overload
from typing import List, Tuple, Optional, Callable, TypeVar
from typing_extensions import ParamSpec
import inspect
from functools import wraps


use_slots = True


class ElectricElement():
    """
    Parent class for all components of the electric circuit
    """

    if use_slots:
        __slots__ = ()

    def __init__(self) -> None:
        raise NotImplementedError

    # type cheat
    # add_connection ist hier nur, weil
    # connect_input sich sonst beschwert
    # -> connect_input in kinder packen, aber die
    # gleich bleibenden elemente wieder hier hoch verlagern
    def add_connection(self, con: 'CoreComponent', port: str) -> None:
        raise NotImplementedError

    def get_state(self) -> bool:
        raise NotImplementedError

    def connect_input(self,
                      port: str,
                      component: Union['ElectricElement',
                                       Sequence['ElectricElement']]) -> None:
        """
        Should be used if not all inputs were available at initialization
        """

        old_input = getattr(self, port)
        old_input = old_input if isinstance(
            old_input, Iterable) else [old_input]

        if not isinstance(component, Iterable):
            component = [component]

        if len(old_input) != len(component):
            raise ValueError("New input has wrong size")

        for i in range(len(component)):
            for fc in old_input[i].forward_connections:
                setattr(fc[0], fc[1], component[i])
                component[i].add_connection(fc[0], fc[1])
                fc[0].update()

        # Not functional, just for tracking
        component = component[0] if len(component) == 1 else component
        setattr(self, port, component)

    @staticmethod
    def _prt_dict_atom(a: Any) -> str:
        if isinstance(a, ElectricElement):
            retstr = a.__class__.__name__ + ' at ' + hex(id(a))
        else:
            retstr = str(a)
        return retstr

    @staticmethod
    def _prt_collection(c: Iterable[Any]) -> str:
        str_list = []
        for a in c:
            str_list.append(ElectricElement._prt_dict_elem(a))
        return ', '.join(str_list)

    @staticmethod
    def _prt_dict_elem(e: Any) -> str:
        if isinstance(e, list):
            retstr = "[" + ElectricElement._prt_collection(e) + "]"
        elif isinstance(e, tuple):
            retstr = "(" + ElectricElement._prt_collection(e) + ")"
        else:
            retstr = ElectricElement._prt_dict_atom(e)
        return retstr

    def __repr__(self) -> str:
        """
        Mea culpa
        """
        retstr = ElectricElement._prt_dict_atom(self) + ' '
        retstr = retstr + str(self.__class__.__base__) + '\n'
        sd = self.__dict__
        for k in sd:
            retstr = retstr + str(k) + ': ' + self._prt_dict_elem(sd[k]) + '\n'
        return retstr


_fc_type = List[Tuple[Union['CoreComponent', 'Monitor'], str]]


class CoreComponent(ElectricElement):
    """
    Parent Class for all core components
    These are the basic buidling blocks that all
    other components are assembled from

    All core components have a singlaur output-line
    called 'out_main'
    """

    if use_slots:
        __slots__ = ('out_main', 'forward_connections')

    out_main: bool

    def compute_state(self) -> None:
        raise NotImplementedError

    def build_circuit(self) -> None:
        raise NotImplementedError

    def setup(self) -> None:

        self.forward_connections: _fc_type = []
        self.build_circuit()
        self.compute_state()

    def get_state(self) -> bool:
        """Returns the current state of the output"""
        return self.out_main

    is_on = property(get_state)

    def add_connection(self,
                       con: Union['CoreComponent', 'Monitor'],
                       port: str) -> None:
        """Called by downstream elements to add them as a forward connection"""
        # TODO: think about whether to place this check
        # somwhere else or if it is even needed. Here, it
        # makes construction awfully slow for large amounts
        # of forward_connections
        # if (con, port) not in self.forward_connections:
        self.forward_connections.append((con, port))

    def forward_pass(self) -> None:
        for fc in self.forward_connections:
            fc[0].update()

    def update(self) -> None:
        old_state = self.out_main
        self.compute_state()
        if self.out_main != old_state:
            self.forward_pass()

    def __str__(self) -> str:
        return str(int(self.out_main))


class LooseWire(CoreComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    if use_slots:
        __slots__ = ()

    def __init__(self) -> None:
        self.setup()

    def build_circuit(self) -> None:
        pass

    def compute_state(self) -> None:
        self.out_main = False


class _LWSent(LooseWire):

    if use_slots:
        __slots__ = ()

    def __init__(self) -> None:
        pass


@overload
def no_con(n: int) -> List[_LWSent]:
    ...


@overload
def no_con() -> _LWSent:
    ...


def no_con(n: Optional[int] = None) -> Union[
        _LWSent, List[_LWSent]]:
    """
    ONLY for use with the @autoparse decorator.
    LooseWires are temporary and will be exchanged by the decorator.
    """
    if n is None:
        return _LWSent()
    else:
        return [_LWSent() for _ in range(n)]


@overload
def exchange_sentinel(x: Sequence[_LWSent]) -> Sequence[LooseWire]:
    ...


@overload
def exchange_sentinel(x: _LWSent) -> LooseWire:
    ...


@overload
def exchange_sentinel(x: Any) -> Any:
    ...


def exchange_sentinel(x: Union[
        Sequence[_LWSent], _LWSent, Any]) -> Union[
        Sequence[LooseWire], LooseWire, Any]:
    if isinstance(x, list):
        return [exchange_sentinel(e) for e in x]
    elif isinstance(x, _LWSent):
        return LooseWire()
    else:
        return x


_P = ParamSpec("_P")
_R = TypeVar("_R")


# remove type ignore when mypy has support for paramspec
# https://github.com/python/mypy/issues/8645
def autoparse(init: Callable[_P, _R]) -> Callable[_P, _R]:  # type: ignore
    inispec = inspect.getfullargspec(init)
    parnames: List[str] = inispec.args[1:]
    defaults = inispec.defaults

    @wraps(init)
    def wrapped_init(self: ElectricElement,
                     *args: _P.args,  # type: ignore
                     **kwargs: _P.kwargs) -> None:  # type: ignore

        # Turn args into kwargs
        kwargs.update(zip(parnames[:len(args)], args))

        if defaults is None:
            raise ValueError("Wrapped function has no default arguments")

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


class CombinedCircuit(ElectricElement):
    """
    Parent class for componenets that are assembled from
    other components
    """
    if use_slots:
        __slots__ = ()
    ...


class SingleOutCircuit(CombinedCircuit):
    """
    Parent for all combined circuits with a a single
    output of any size
    """
    if use_slots:
        __slots__ = ()
    ...


class SingleBitSOC(SingleOutCircuit):
    """
    For all Circuits that have a single 1-bit output

    Circuits of this type can be used
    like basegates and other core components

    and1 = AND(s1)
    xor1 = XOR(s1, s2)

    xor.out_main.is_on can be written as
    xor.is_on

    and1.connect_input('in_b', xor1.out_main)
    can be written as if XOR were a CoreComponent
    and1.connect_input('in_b', xor1)
    """

    if use_slots:
        __slots__ = ('out_main')

    out_main: Union[CoreComponent, 'SingleBitSOC']

    def get_state(self) -> bool:
        return self.out_main.get_state()

    is_on = property(get_state)

    def add_connection(self,
                       con: Union['CoreComponent', 'Monitor'],
                       port: str) -> None:
        self.out_main.add_connection(con, port)

    def __str__(self) -> str:
        return str(int(self.out_main.is_on))


# Only CoreComponents and SinglestateSC can be used as
# directly inputs. Secondary components have to be adressed
# by there their ports, which are are also either CoreComponents
# or SinglestateSC
InputComponent = Union[CoreComponent, SingleBitSOC]


class MultiBitSOC(SingleOutCircuit):
    """
    Parent class for all circuits that have
    a single multibit output
    """
    if use_slots:
        __slots__ = ('out_main')

    out_main: Sequence[InputComponent]

    def __str__(self) -> str:
        bitlist = [str(int(b.is_on)) for b in self.out_main]
        return ''.join(bitlist)

    def __iter__(self) -> Iterator[InputComponent]:
        for elem in self.out_main:
            yield elem

    def __len__(self) -> int:
        return len(self.out_main)

    def __getitem__(self, i: int) -> InputComponent:
        return self.out_main[i]


class MultiOutCircuit(CombinedCircuit):
    """
    Parent class for all circuits that have
    multiple output (== adders)

    When using these circuits as inputs, they
    have to be adressed by naming their outputs
    (e.g. x = HalfAdder(a,b); y = Halfadder(c,x.carry))
    """
    if use_slots:
        __slots__ = ()


class Monitor(ElectricElement):
    """
    Parent class for all output devices
    """
    if use_slots:
        __slots__ = ()

    def update(self) -> None:
        raise NotImplementedError
