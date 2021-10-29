from integratedcomponent import IntegratedComponent
from electriccomponent import ElectricComponent
from corecomponents import INV, CoreComponent, LooseWire
from memory import EdgeTrigDTFlipFlop
import time


class Buffer(CoreComponent):
    """Buffer"""

    # inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = None, delay: float = .1):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.delay = delay
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        time.sleep(self.delay)
        self.out_main = self.in_a.is_on
        print(self.out_main)
        # self.out_main = not self.in_a.is_on


class Gate(CoreComponent):
    """Gate"""

    # inputs = ElectricComponent.unpack_io('in_a', )

    def __init__(self, in_a: ElectricComponent = None, delay: float = .1):
        self.in_a = in_a if in_a is not None else LooseWire()
        self.delay = delay
        self.setup()

    def build_circuit(self):
        self.in_a.add_connection(self, 'in_a')

    def compute_state(self):
        time.sleep(self.delay)
        self.out_main = self.in_a.is_on
        print(self.out_main)
        # self.out_main = not self.in_a.is_on


class oscillator(IntegratedComponent):
    def __init__(self, in_a: ElectricComponent = None, clockspeed=1):
        bu1 = Buffer()
        inv1 = INV(bu1)
        bu1.connect_input("in_a", inv1)
        self.out_main = inv1


# try:
#     asd = oscillator()
# except:
#     RecursionError('HI')


# c1 = Switch(False)

# l1 = EdgeTriggeredDTFlipFlop(in_clock=c1)
# l2 = EdgeTriggeredDTFlipFlop(in_clock=l1.out_qb)
# l3 = EdgeTriggeredDTFlipFlop(in_clock=l2.out_qb)
# l4 = EdgeTriggeredDTFlipFlop(in_clock=l3.out_qb)
# l1.connect_input("in_data", l1.out_qb)
# l2.connect_input("in_data", l2.out_qb)
# l3.connect_input("in_data", l3.out_qb)
# l4.connect_input("in_data", l4.out_qb)

# for i in range(10):
#     c1.flip()
#     ou = [l.__str__()[0] for l in [INV(c1), l1, l2, l3, l4]][::-1]
#     print(''.join(ou))
