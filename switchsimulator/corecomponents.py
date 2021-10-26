from electriccomponent import ElectricComponent


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
        """Returns the current state of the output"""
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
        old_state = self.out_main
        self.compute_state()
        if self.out_main != old_state:
            self.forward_pass()

    def __str__(self):
        return str(int(self.out_main))


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


class LooseWire(CoreComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries a current
    """

    def __init__(self):
        self.setup()

    def build_circuit(self):
        pass

    def compute_state(self):
        self.out_main = False


class INV(CoreComponent):
    """Inverts the input"""

    inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        self.out_main = False if self.in_a.is_on else True
        # self.out_main = not self.in_a.is_on


class BaseGate(CoreComponent):

    inputs = ElectricComponent.unpack_io('in_a', 'in_b')

    def __init__(self, in_a: ElectricComponent = None,
                 in_b: ElectricComponent = None):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.in_b = in_b if in_b is not None else LooseWire()
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')
        self.in_b.add_connection(self, 'in_b')


class AND(BaseGate):
    """AND-Gate"""

    def compute_state(self):
        self.out_main = False
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = True
        # self.out_main = self.in_a.is_on and self.in_b.is_on


class OR(BaseGate):
    """OR-Gate"""

    def compute_state(self):
        self.out_main = False
        if self.in_a.is_on:
            self.out_main = True
        if self.in_b.is_on:
            self.out_main = True
#        self.out_main = self.in_a.is_on or self.in_b.is_on


class NOR(BaseGate):
    """NOR-Gate"""

    def compute_state(self):
        self.out_main = True
        if self.in_a.is_on:
            self.out_main = False
        if self.in_b.is_on:
            self.out_main = False


class NAND(BaseGate):
    """NAND-Gate"""

    def compute_state(self):
        self.out_main = True
        if self.in_a.is_on:
            if self.in_b.is_on:
                self.out_main = False
