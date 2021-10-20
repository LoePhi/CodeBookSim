from component import ElectricComponent


class CoreComponent(ElectricComponent):
    """
    Parent Class for all core components
    This are the basic buidling blocks that all
    other components are assembled from

    All core components have a singlaur output-line
    called 'out_a'
    """

    outputs = ElectricComponent.unpack_io('out_a', )

    def setup(self):
        self.forward_connections = []
        self.backward_connections = []  # not used
        self.build_circuit()
        self.compute_state()

    def get_state(self, port="out_a"):
        """Returns the current state of the output(s)"""
        return getattr(self, port)
        
    is_on = property(get_state)

class Switch(CoreComponent):
    """
    Simple Switch
    It carries a current when it is closed
    """

    def __init__(self, closed: bool = False):
        self.closed = closed
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self.out_a = self.closed

    def flip(self):
        self.out_a = not self.out_a
        self.forward_pass()

    def open(self):
        self.out_a = False
        self.forward_pass()

    def close(self):
        self.out_a = True
        self.forward_pass()


class Connector(CoreComponent):
    """
    The connector is used for addressing indiviudal output lines
    of components that feauture multiple outputs.
    """
    # TODO: hier comupte und so überarbeiten
    # alle anderen core-elemnte haben nur bool out

    inputs = ElectricComponent.unpack_io('in_a')

    def __init__(self, in_a: ElectricComponent, port: str):
        self.in_a = in_a
        self.port = port
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, '_in_a')

    def compute_state(self):
        self.out_a = self.in_a.get_state(self.port)


class LooseWire(CoreComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    # HACK: This makes LooseWire() cretae new instances
    # when used as default function paramter. Might not be needed
    # when/if all arguments are parsed
    __slots__ = ['out_a']

    def __init__(self):
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self.out_a = False


class INV(CoreComponent):
    """Inverts the input"""

    inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        self.out_a = not self.in_a.get_state()


class AND(CoreComponent):
    """AND-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')

    def compute_state(self):
        self.out_a = self.in_a.get_state() and self.in_b.get_state()


class OR(CoreComponent):
    """OR-Gate"""

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')

    def __init__(self, in_a: ElectricComponent = LooseWire(),
                 in_b: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.in_b = in_b
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')

    def compute_state(self):
        self.out_a = self.in_a.get_state() or self.in_b.get_state()
