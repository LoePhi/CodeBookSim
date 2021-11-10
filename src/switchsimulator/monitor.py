from switchsimulator.base import Monitor
from switchsimulator.base import autoparse, no_con, InputComponent
from typing import List


class Lightbulbs(Monitor):
    """
    just some lightbulbs
    """

    @autoparse
    def __init__(self,
                 in_data: List[InputComponent],
                 in_clock: InputComponent = no_con(),
                 mode: str = 'clock') -> None:
        self.in_data = in_data
        self.in_clock = in_clock
        self.mode = mode

        self.build_circuit()

    def build_circuit(self) -> None:
        if self.mode == 'update':
            for d in self.in_data:
                d.add_connection(self, 'in_data')
        if self.mode == 'clock':
            self.in_clock.add_connection(self, 'in_clock')
        self.bulbs = [False for _ in self.in_data]

    def update(self) -> None:
        self.compute_state()
        print('                   ', end='\r')
        print(''.join([str(int(b)) for b in self.bulbs]), end='\r')

    def compute_state(self) -> None:
        self.bulbs = [d.is_on for d in self.in_data]
