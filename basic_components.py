from abc import ABC, abstractmethod

from single_state_components import LooseWire


# todo:
# rename forward to downstream

# todo: alle inputs als False initilisieren und circuit direct bauen
# -> Hilfsklasse DeadEnd die mit get_state/is_property -> False
#   -> muss forward_connections wieitergeben wenn sei ausgetauscht wird!
#       -> eigentlich nicht, da connect_input die fc added
#           -> DeadEnd nach connect input löschen (sollte nicht nötig sein, da nicht mehr referenziert)
#               -> testen indem in loop immer wieder neues DeadEnd als input connected wird
# - das initialisieren der Outputs sollte dann nciht mehr nötig sein

# todo?: alle outputs als connectors ausgeben -> compute_state entfällt außer für die
# grund-bausteine (INV, AND, OR)
# -> dann geht das hier aber nicht mehr ohne weiteres:
#     self.INV1 = INV(self.XOR1)
# -> INV added fc zu XOR1; nicht zu dem connector der aus XOR1 heruas führt
# stattdessen müsste dann
#     self.INV1 = INV(self.XOR1.con_out)
# das erzeugt aber viel getipsel und geht auf Kosten der Lesbarkeit
# es lässt sich sicher so lösen, aber wie hoch sind die KOsten an die Lesbarkeit und der Wartungsaufwand?
# Beifang:
# - jede Menge neue Instanzen
# - zusammengestzte Elemente haben erstmal keinen eigenen state mehr

# merke:
# Solange nicht alle inoputs verbunden sind, werden alle outputs auf falsch gestezt!

class ElectricComponent(ABC):
    """
    Parent class for all components of the electric circuit
    """

    # Each class should have a tuple specifying expected inputs an available outputs
    # inputs = ()
    # outputs = ()

    @abstractmethod
    def __init__(self):
        """Attach Inputs"""

    #todo: refcator
    def setup(self, initial=False):
        """check_complete -> construct -> compute_state"""
        if initial:
            for o in self.outputs:
                setattr(self, o, False)

        self.check_completion()
        if self.is_complete:
            self.build_circuit()
            self.compute_state()

    def check_completion(self):
        self.is_complete = False
        for i in self.inputs:
            if not isinstance(getattr(self, i), ElectricComponent):
                return()
            # try:
            #     if not getattr(self, i).is_complete:
            #         return()
            # except AttributeError:
            #     return()
        self.is_complete = True

    @abstractmethod
    def build_circuit(self):
        """Implement the inner logic of the circuit"""

    @abstractmethod
    def compute_state(self):
        """
        Computes the current state of the output(s)

        This is seperated from get_state to prevent the circuit
        from recursing all the way down
        """

    @abstractmethod
    def get_state(self):
        """Returns the current state of the output(s)"""

    def connect_input(self, input_name, input_circuit):
        """
        Should be used if not all inputs were available at initialization
        """
        if isinstance(getattr(self, input_name), LooseWire):
            setattr(self, input_name, input_circuit)
            input_circuit.add_forward_connection(self)
            self.setup()
        else:
            raise ValueError(input_name + " already connected")

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

    outputs = ('_output', )

    def get_state(self):
        return(self._output)

    is_on = property(get_state)


class Switch(SingleStateComponent):
    """
    Simple Switch
    This component is special in that is has no inputs
    """
    # todo: methods for flip, open, close

    inputs = ()

    def __init__(self, closed: bool = None):
        self.closed = closed
        self.setup(initial=True)

    def build_circuit(self):
        pass

    def compute_state(self):
        self._output = self.closed

    def flip(self):
        self._output = not self._output
        self.forward_pass()

# Alias
# This would be deirable but it breaks "isinstance"
# and inheriting brekas the doc
#Bit = Switch


class Connector(SingleStateComponent):
    """
    The connector is used for addressing indiviudal output lines
    of components that feauture multiple outputs.
    """

    inputs = ('component', )

    def __init__(self, component:ElectricComponent, port):
        self.component = component
        self.port = port
        self.setup(initial=True)

    def build_circuit(self):
        self.component.add_forward_connection(self)

    def compute_state(self):
        self._output = self.component.get_state(self.port)


class LooseWire(SingleStateComponent):
    """
    This component is used solely for initializing unconnected inputs
    It never carries ac current
    """

    inputs = ()

    def __init__(self):
        self.setup(initial=True)

    def build_circuit(self):
        pass

    def compute_state(self):
        pass


# Tests:
assert(Switch(True).is_on is True)
assert(Switch(False).is_on is False)
tmp = Switch(False)
tmp.flip()
assert(tmp.is_on is True)
