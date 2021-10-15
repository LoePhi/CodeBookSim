from abc import ABC, abstractmethod
from basemethods import unpack_io

#import utility_functions as uf

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
    inputs = unpack_io()
    outputs = unpack_io()

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

    # TODO: ?keep state
    def update(self):
        old_outputs = [getattr(self, o) for o in self.outputs.keys()]
        self.compute_state()
        new_outputs = [getattr(self, o) for o in self.outputs.keys()]
        if old_outputs != new_outputs:
            self.forward_pass()
