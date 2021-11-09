from typing import Any, Iterable, Sequence, Union, overload
from typing import List, Tuple, Optional, Callable
import inspect
from functools import wraps


class ElectricComponent():
    """
    Parent class for all components of the electric circuit
    """

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
                      component: Union['ElectricComponent',
                                       Sequence['ElectricComponent']]) -> None:
        """
        Should be used if not all inputs were available at initialization
        """

        old_input = getattr(self, port)
        old_input = old_input if isinstance(old_input, list) else [old_input]

        if isinstance(component, ElectricComponent):
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
        if isinstance(a, ElectricComponent):
            retstr = a.__class__.__name__ + ' at ' + hex(id(a))
        else:
            retstr = str(a)
        return retstr

    @staticmethod
    def _prt_collection(c: Iterable[Any]) -> str:
        str_list = []
        for a in c:
            str_list.append(ElectricComponent._prt_dict_elem(a))
        return ', '.join(str_list)

    @staticmethod
    def _prt_dict_elem(e: Any) -> str:
        if isinstance(e, list):
            retstr = "[" + ElectricComponent._prt_collection(e) + "]"
        elif isinstance(e, tuple):
            retstr = "(" + ElectricComponent._prt_collection(e) + ")"
        else:
            retstr = ElectricComponent._prt_dict_atom(e)
        return retstr

    def __repr__(self) -> str:
        """
        Mea culpa
        """
        retstr = ElectricComponent._prt_dict_atom(self) + ' '
        retstr = retstr + str(self.__class__.__base__) + '\n'
        sd = self.__dict__
        for k in sd:
            retstr = retstr + str(k) + ': ' + self._prt_dict_elem(sd[k]) + '\n'
        return retstr


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
        T = List[Tuple[Union[CoreComponent, Monitor], str]]
        self.forward_connections: T = []
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


class _LooseWireSentinel(LooseWire):

    def __init__(self) -> None:
        pass


@overload
def no_con(n: int) -> List[_LooseWireSentinel]:
    ...


@overload
def no_con() -> _LooseWireSentinel:
    ...


def no_con(n: Optional[int] = None) -> Union[
        _LooseWireSentinel, List[_LooseWireSentinel]]:
    """
    ONLY for use with the @autoparse decorator.
    LooseWires are temporary and will be exchanged by the decorator.
    """
    if n is None:
        return _LooseWireSentinel()
    else:
        return [_LooseWireSentinel() for _ in range(n)]


@overload
def exchange_sentinel(x: Sequence[_LooseWireSentinel]) -> Sequence[LooseWire]:
    ...


@overload
def exchange_sentinel(x: _LooseWireSentinel) -> LooseWire:
    ...


@overload
def exchange_sentinel(x: Any) -> Any:
    ...


def exchange_sentinel(x: Union[
        Sequence[_LooseWireSentinel], _LooseWireSentinel, Any]) -> Union[
        Sequence[LooseWire], LooseWire, Any]:
    if isinstance(x, list):
        return [exchange_sentinel(e) for e in x]
    elif isinstance(x, _LooseWireSentinel):
        return LooseWire()
    else:
        return x


def autoparse(init: Callable[..., None]) -> Callable[..., None]:
    inispec = inspect.getfullargspec(init)
    parnames: List[str] = inispec.args[1:]
    defaults = inispec.defaults

    @wraps(init)
    def wrapped_init(self: ElectricComponent,
                     *args: Any, **kwargs: Any) -> None:

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


class SecondaryComponent(ElectricComponent):
    """
    Parent class for componenets that are assembled from
    other components
    """

    pass


class SingleStateSC(SecondaryComponent):
    """
    This allows for its children to be used
    like basegates and other core components

    and1 = AND(s1)
    xor1 = XOR(s1, s2)

    xor.out_main.is_on can be written as
    xor.is_on

    and1.connect_input('in_b', xor1.out_main)
    can be written as if XOR were a CoreComponent
    and1.connect_input('in_b', xor1)
    """

    out_main: Union[CoreComponent, 'SingleStateSC']

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
InputComponent = Union[CoreComponent, SingleStateSC, LooseWire]


class Monitor(ElectricComponent):
    """
    Parent class for all output devices
    """
    pass

    def update(self) -> None:
        raise NotImplementedError
