# flake8: noqa
import cProfile
from codebooksim.corecomponents import Switch
from codebooksim.adders import Sixteen_Bit_Adder
from codebooksim.helpers import bts
from codebooksim.misccomp import Decoder_16_64K, Selector_64K_1
from codebooksim.memory import RAM_64K_1, RAM_64K_8
import tracemalloc


# cProfile.run(
#     "Sixteen_Bit_Adder(bts('1111111111111111'),"
#     "bts('1000000000000001'), Switch(False))")

# cProfile.run("Decoder_16_64K(Switch(True),bts('0000000000000000'))")

# cProfile.run("Selector_64K_1()")

#cProfile.run("RAM_64K_1(Switch(True), bts('0000000000000000'), Switch(True))")

#cProfile.run("RAM_64K_8(bts('01010101'), bts('0000000000000000'), Switch(True))")

tracemalloc.start()

_ = RAM_64K_1(Switch(True), bts('0000000000000000'), Switch(True))

snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('lineno')
for stat in stats[:20]:
    print(stat)
