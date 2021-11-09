from typing import List
from switchsimulator.base import CoreComponent, SecondaryComponent
from switchsimulator.base import SingleStateSC
from switchsimulator.corecomponents import INV, Switch, OR
from switchsimulator.memory import EdgeTrigDTFlipFlop
import time
from switchsimulator.base import autoparse, no_con, InputComponent


class book_oscillator(SingleStateSC):
    """
    USE CLASS 'clock' INSTEAD
    The oscillator from p. 173
    ! Added an OR to serve as a buffer
    Creating an instance will results in an immediate
    RecursionError.
    This could be made to work for some time by usign a Switch
    to delay the start but eventually would still fail
    with a stack overflow
    """

    def __init__(self) -> None:

        self.inv1 = INV()
        self.or1 = OR(self.inv1)
        self.inv1.connect_input("in_a", self.or1)

        self.out_main = self.inv1


class clock(SingleStateSC):
    """
    Not actually a clock.
    Just a monkey flipping a Switch very fast
    """

    def __init__(self,
                 in_control: InputComponent = no_con(),
                 delay: float = 0,
                 print_hz: bool = False) -> None:
        self.in_control = in_control
        self.delay = delay
        self.print_hz = print_hz

        self.out_main = Switch(False)

    def start(self) -> None:
        if self.print_hz:
            counter = 0
            timestmp = time.time()
            kcycl = 100
        while(self.in_control.is_on):
            time.sleep(self.delay)
            assert isinstance(self.out_main, Switch)
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
                 in_clock: InputComponent = no_con(),
                 nbit: int = 8) -> None:
        self.in_clock = in_clock

        self.inv1 = INV(self.in_clock)

        ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.in_clock)
        ff_tmp.connect_input('in_data', ff_tmp.out_qb)
        self.ffs = [ff_tmp]
        for i in range(1, nbit-1):
            ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.ffs[-1].out_qb)
            ff_tmp.connect_input('in_data', ff_tmp.out_qb)
            self.ffs.append(ff_tmp)

        self.ffs.reverse()
        self.out_main: List[CoreComponent] = [ff.out_q for ff in self.ffs]
        self.out_main.append(self.inv1)

    def __str__(self) -> str:
        bitlist = [str(int(b.is_on)) for b in self.out_main]
        return ''.join(bitlist)
