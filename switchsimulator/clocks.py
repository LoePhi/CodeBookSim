from integratedcomponent import IntegratedComponent, SingleStateIC
from electriccomponent import ElectricComponent
from corecomponents import INV, CoreComponent, AND, Switch
from memory import EdgeTrigDTFlipFlop
import time
from helpers import autoparse, _lwd


class oscillator(SingleStateIC):

    @autoparse
    def __init__(self,
                 in_control: ElectricComponent = _lwd()):
        self.inv1 = INV()
        self.and1 = AND(self.inv1, self.in_control)
        self.inv1.connect_input("in_a", self.and1)
        self.out_main = self.inv1


class RippleCounter(IntegratedComponent):

    @autoparse
    def __init__(self,
                 in_clock: ElectricComponent = _lwd(),
                 nbit: int = 8):

        self.inv1 = INV(self.in_clock)

        ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.in_clock)
        ff_tmp.connect_input('in_data', ff_tmp.out_qb)
        self.ffs = [ff_tmp]
        for i in range(1, nbit-1):
            ff_tmp = EdgeTrigDTFlipFlop(in_clock=self.ffs[-1].out_qb)
            ff_tmp.connect_input('in_data', ff_tmp.out_qb)
            self.ffs.append(ff_tmp)

        self.out_main = [ff.out_q for ff in self.ffs[::-1]] + [self.inv1]


class clockmonitor(CoreComponent):

    @autoparse
    def __init__(self,
                 in_data: ElectricComponent = _lwd(4),
                 in_clock: ElectricComponent = _lwd()):
        self.setup()

    def build_circuit(self):
        self.in_clock.add_connection(self, 'in_data')

    def compute_state(self):
        self.out_main = [d.is_on for d in self.in_data]
        print(''.join([str(int(b)) for b in self.out_main]))
        time.sleep(0)


# sw = Switch(False)
# cl = oscillator(sw)
# rc = RippleCounter(cl, 16)
# mon = clockmonitor(rc.out_main, cl)
# cl.out_main.forward_connections = cl.out_main.forward_connections[1:] + [
#     cl.out_main.forward_connections[0]]

# try:
#     import sys
#     sys.setrecursionlimit(1000000000)
#     sw.flip()
# except RecursionError:
#     print("war klar")

class osc2(SingleStateIC):
    def __init__(self, in_control):
        self.out_main = Switch(False)
        self.in_control = in_control

    def start(self):
        while(self.in_control.is_on):
            print(self.in_control)
            self.out_main.flip()
            time.sleep(1)


sw = Switch(False)
cl = osc2(sw)
rc = RippleCounter(cl, 16)
mon = clockmonitor(rc.out_main, cl)
cl.start()

import threading
x = threading.Thread(target=cl.start)
x.start()
sw.flip()
sw.flip()
