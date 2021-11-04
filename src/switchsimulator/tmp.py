from switchsimulator.corecomponents import Switch, OR
from switchsimulator.clocks import monitor
from switchsimulator.adders import AddingMachine2
from switchsimulator.helpers import bts

s_add = Switch(False)
s_clear = Switch(False)
bits = bts('00000010')

am = AddingMachine2(bits, s_add, s_clear)
mon = monitor(am.out_bulbs, mode='update')

s_clear.close()
s_clear.open()
for i in range(100):
    s_add.flip()
print(am)
