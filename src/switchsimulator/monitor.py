from switchsimulator.electriccomponent import ElectricComponent
from switchsimulator.corecomponents import autoparse, no_con
from typing import List


class monitor(ElectricComponent):
    """
    not really core because out_main has more than 1 bit
    """

    @autoparse
    def __init__(self,
                 in_data: List[ElectricComponent],
                 in_clock: ElectricComponent = no_con(),
                 mode: str = 'clock'):
        self.in_data = in_data
        self.in_clock = in_clock
        self.mode = mode

        self.backward_connections = []  # not used
        self.build_circuit()

    def build_circuit(self):
        if self.mode == 'update':
            for d in self.in_data:
                d.add_connection(self, 'in_data')
        if self.mode == 'clock':
            self.in_clock.add_connection(self, 'in_clock')
        self.bulbs = [False for _ in self.in_data]

    def update(self):
        self.compute_state()
        print('                   ', end='\r')
        print(''.join([str(int(b)) for b in self.bulbs]), end='\r')

    def compute_state(self):
        self.bulbs = [d.is_on for d in self.in_data]
