from abc import ABC, abstractmethod


class ElectricComponent(ABC):
    """
    Parent class for all components of the electric circuit
    """

    # Each class should have a tuple specifying available inputs and outputs
    # The output tuple is looped over to check if the output changes
    @staticmethod
    def unpack_io(*io_str):
        io_dict = {}
        for i in range(len(io_str)):
            x = io_str[i].split(":")
            io_dict[x[0]] = {'N': int(x[1]) if len(x) > 1 else 1}
        return io_dict
    # inputs = unpack_io()
    # outputs = unpack_io()

    @abstractmethod
    def __init__(self):
        """Attach Inputs"""

    def setup(self):
        self.forward_connections = []
        self.backward_connections = [] # not used
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

        old_input = getattr(self, input_name)
        islist = isinstance(old_input, list)
        
        if not islist:
            old_input = [old_input]
            input_circuit = [input_circuit]
 
        for i in range(len(input_circuit)):
            for fc in old_input[i].forward_connections:
                setattr(fc[0], fc[1], input_circuit[i])
                input_circuit[i].add_connection(fc[0], fc[1])
                fc[0].update()
            
        if not islist:
            input_circuit = input_circuit[0]

        # Not functional, just for tracking
        setattr(self, input_name, input_circuit)


    def add_connection(self, con, port):
        """Called by downstream elements to add the as a forward connection"""
        if con not in self.forward_connections:
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
