from component import ElectricComponent


class CoreComponent(ElectricComponent):
    """
    Parent Class for all core components
    This are the basic buidling blocks that all
    other components are assembled from

    All core components have a singlaur output-line
    called 'out_main'
    """

    outputs = ElectricComponent.unpack_io('out_main', )

    def setup(self):
        self.forward_connections = []
        self.backward_connections = []  # not used
        self.build_circuit()
        self.compute_state()

    def get_state(self):
        """Returns the current state of the output(s)"""
        return self.out_main

    is_on = property(get_state)

    def add_connection(self, con, port):
        """Called by downstream elements to add the as a forward connection"""
        if (con, port) not in self.forward_connections:
            self.forward_connections.append((con, port))
        # backward connections can be used for debugging the circuit
        if self not in con.backward_connections:
            con.backward_connections.append(self)

    def forward_pass(self):
        for fc in self.forward_connections:
            fc[0].update()

    # TODO: ?keep state
    def update(self):
        old_outputs = [getattr(self, o) for o in self.outputs.keys()]
        self.compute_state()
        new_outputs = [getattr(self, o) for o in self.outputs.keys()]
        if old_outputs != new_outputs:
            self.forward_pass()


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
        self.out_main = self.closed

    def flip(self):
        self.out_main = not self.out_main
        self.forward_pass()

    def open(self):
        self.out_main = False
        self.forward_pass()

    def close(self):
        self.out_main = True
        self.forward_pass()


# class Connector(CoreComponent):
#     """
#     The connector is used for addressing indiviudal output lines
#     of components that feauture multiple outputs.
#     """
#     # TODO: hier comupte und so überarbeiten
#     # alle anderen core-elemnte haben nur bool out

#     inputs = ElectricComponent.unpack_io('in_a')

#     def __init__(self, in_a: ElectricComponent, port: str):
#         self.in_a = in_a
#         self.port = port
#         self.setup()

#     def build_circuit(self):
#         self.in_a.add_connection(self, '_in_a')

#     def compute_state(self):
#         self.out_main = self.in_a.get_state(self.port)


class LooseWire(CoreComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    # HACK: This makes LooseWire() cretae new instances
    # when used as default function paramter. Might not be needed
    # when/if all arguments are parsed
    __slots__ = ['out_main']

    def __init__(self):
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self.out_main = False


class INV(CoreComponent):
    """Inverts the input"""

    inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = LooseWire()):
        self.in_a = in_a
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        self.out_main = False if self.in_a.is_on else True


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
        self.out_main = False
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = True


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
        self.out_main = False
        if self.in_a.is_on:
            self.out_main = True
        if self.in_b.is_on:
            self.out_main = True
