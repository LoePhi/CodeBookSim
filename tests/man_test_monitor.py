from switchsimulator.corecomponents import Switch
from switchsimulator.monitor import monitor
from switchsimulator.clocks import clock, RippleCounter
from switchsimulator.adders import AddingMachine2
from switchsimulator.helpers import bts
import threading
from time import sleep


def test_clock_mode_counter():
    sw = Switch(False)
    cl = clock(sw)
    rc = RippleCounter(cl, 16)
    mon = monitor(rc.out_main, cl)
    sw.flip()
    x = threading.Thread(target=cl.start)
    x.start()
    sleep(.1)
    sw.flip()


def test_update_mode_adder():
    s_add = Switch(False)
    s_clear = Switch(False)
    bits = bts('00000010')

    am = AddingMachine2(bits, s_add, s_clear)
    mon = monitor(am.out_bulbs, mode='update')

    s_clear.close()
    s_clear.open()
    for i in range(100):
        sleep(.02)
        s_add.flip()
    print(am)


print("Counting:")
test_clock_mode_counter()
sleep(1)
print("\nAdding:")
test_update_mode_adder()
