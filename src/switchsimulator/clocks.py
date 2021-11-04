import threading
from switchsimulator.secondarycomponents import SecondaryComponent
from switchsimulator.secondarycomponents import SingleStateSC
from switchsimulator.electriccomponent import ElectricComponent
from switchsimulator.corecomponents import INV, CoreComponent, Switch
from switchsimulator.memory import EdgeTrigDTFlipFlop
import time
from switchsimulator.corecomponents import autoparse, no_con
from typing import List


class book_oscillator(SingleStateSC):
    """
    The oscillator from p. 173
    this could be made to work for some time but
    eventually would result in a recursion error
    Use class 'clock' instead
    """

    @autoparse
    def __init__(self):

        self.inv1 = INV()
        self.inv1.connect_input("in_a", self.inv1)

        self.out_main = self.inv1


class clock(SingleStateSC):
    """
    Not actually a clock.
    Just a monkey flipping a Switch very fast
    """

    def __init__(self,
                 in_control: ElectricComponent = no_con(),
                 delay: float = 0,
                 print_hz: bool = False):
        self.in_control = in_control
        self.delay = delay
        self.print_hz = print_hz

        self.out_main = Switch(False)

    def start(self):
        if self.print_hz:
            counter = 0
            timestmp = time.time()
            kcycl = 100
        while(self.in_control.is_on):
            time.sleep(self.delay)
            self.out_main.flip()
            if self.print_hz:
                counter = counter + 1
                if counter == 1000 * kcycl:
                    newtime = time.time()
                    khz = kcycl / (newtime - timestmp)
                    print(str(khz) + "khz")
                    counter = 0
                    timestmp = newtime


class RippleCounter(SecondaryComponent):
    """
    Ripple-Counter, p. 177
    ! This one can be changed to any bitsize
    """

    @autoparse
    def __init__(self,
                 in_clock: ElectricComponent = no_con(),
                 nbit: int = 8):
        self.in_clock = in_clock

        self.inv1 = INV(self.in_clock)

        ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.in_clock)
        ff_tmp.connect_input('in_data', ff_tmp.out_qb)
        self.ffs = [ff_tmp]
        for i in range(1, nbit-1):
            ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.ffs[-1].out_qb)
            ff_tmp.connect_input('in_data', ff_tmp.out_qb)
            self.ffs.append(ff_tmp)

        self.out_main = [ff.out_q for ff in self.ffs[::-1]] + [self.inv1]


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
        print(''.join([str(int(b)) for b in self.bulbs]), end='\r')  # , end='\r'

    def compute_state(self):
        self.bulbs = [d.is_on for d in self.in_data]


sw = Switch(False)
cl = clock(sw, delay=.1, print_hz=False)
rc = RippleCounter(cl, 16)
mon = monitor(rc.out_main, cl)

sw.flip()
x = threading.Thread(target=cl.start)
x.start()


sw.flip()
