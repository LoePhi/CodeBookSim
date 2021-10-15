from abc import ABC, abstractmethod


# FIXME: Rebuilding the circuit is currently neccesary, because the
# inner circuit elemts that depend on the LooseWire do not
# update their inputs automatically
# Howver, rebuilding the circuit will not release the prvious circuit objects
# because the dead inputs that were connected maintain a reference in their
# forward connections

class ElectricComponent(ABC):
    """
    Parent class for all components of the electric circuit
    """

    # Each class should have a tuple specifying available inputs and outputs
    # The output tuple is looped over to check if the output changes
    # inputs = ()
    # outputs = ()

    @abstractmethod
    def __init__(self):
        """Attach Inputs"""

    def setup(self):
        self.build_circuit()
        self.compute_state()

    @abstractmethod
    def build_circuit(self):
        """
        Implement the inner logic of the circuit
        All Components that are used by get_state need to 
        have their forward connections added here
        """

    @abstractmethod
    def compute_state(self):
        """
        Computes the current state of the output(s)

        This is seperated from get_state to prevent the circuit
        from recursing all the way down
        """

    def get_state(self, port):
        """Returns the current state of the output(s)"""
        return getattr(self, port)

    def connect_input(self, input_name: str, input_circuit: 'ElectricComponent'):
        """
        Should be used if not all inputs were available at initialization
        """
        # TODO: checken, dass loose-wire bzw. list von looseWire
        setattr(self, input_name, input_circuit)
        self.setup()

    def add_forward_connection(self, con):
        """Called by downstream elements to add the as a forward connection"""
        if not hasattr(self, 'forward_connections'):
            self.forward_connections = []
        if con not in self.forward_connections:
            self.forward_connections.append(con)

    def forward_pass(self):
        if hasattr(self, 'forward_connections'):
            for fc in self.forward_connections:
                fc.update()

    # only do forward pass if state_change
    def update(self):
        old_outputs = [getattr(self, o) for o in self.outputs]
        self.compute_state()
        new_outputs = [getattr(self, o) for o in self.outputs]
        if old_outputs != new_outputs:
            self.forward_pass()


class SingleStateComponent(ElectricComponent):
    """
    Parent Class for all components with a singular output
    """

    inputs = ()
    outputs = ('_output', )

    def get_state(self):
        return(self._output)

    is_on = property(get_state)


class Switch(SingleStateComponent):
    """
    Simple Switch
    This component is special in that is has no inputs
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

# TODO: Alias
# This would be deirable but it breaks "isinstance"
# and inheriting brekas the doc
# Bit = Switch


class Connector(SingleStateComponent):
    """
    The connector is used for addressing indiviudal output lines
    of components that feauture multiple outputs.
    """

    inputs = ('component_')

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
