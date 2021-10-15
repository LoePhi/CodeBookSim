from component import ElectricComponent


class SingleStateComponent(ElectricComponent):
    """
    Parent Class for all components with a singular output
    """

    outputs = ElectricComponent.unpack_io('_output', )

    def get_state(self):
        return(self._output)

    is_on = property(get_state)


class Switch(SingleStateComponent):
    """
    Simple Switch
    It carries a current when it is closed
    """
    # TODO: methods for flip, open, close

    def __init__(self, closed: bool = False):
        self.closed = closed
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self._output = self.closed

    def flip(self):
        self._output = not self._output
        self.forward_pass()

    def open(self):
        self._output = False
        self.forward_pass()

    def close(self):
        self._output = True
        self.forward_pass()

# TODO: Alias
# This would be deirable but it breaks "isinstance"
# and inheriting brekas the doc
# Bit = Switch


class Connector(SingleStateComponent):
    """
    The connector is used for addressing indiviudal output lines
    of components that feauture multiple outputs.
    """

    inputs = ElectricComponent.unpack_io('component_')

    def __init__(self, component: ElectricComponent, port: str):
        self.component = component
        self.port = port
        self.setup()

    def build_circuit(self):
        self.component.add_forward_connection(self)

    def compute_state(self):
        self._output = self.component.get_state(self.port)


class LooseWire(SingleStateComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    # HACK: This makes LooseWire() cretae new instances
    # when used as default function paramter. Might not be needed
    # when/if all arguments are parsed
    __slots__ = ['_output']

    def __init__(self):
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self._output = False


# Tests:
assert(Switch(True).is_on is True)
assert(Switch(False).is_on is False)
tmp = Switch(False)
tmp.flip()
assert(tmp.is_on is True)
