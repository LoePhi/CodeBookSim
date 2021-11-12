# flake8: noqa
import cProfile
from switchsimulator.corecomponents import Switch
from switchsimulator.adders import Sixteen_Bit_Adder
from switchsimulator.helpers import bts
from switchsimulator.misccomp import Decoder_16_64K, Selector_64K_1
from switchsimulator.memory import RAM_64K_1


# cProfile.run(
#     "Sixteen_Bit_Adder(bts('1111111111111111'),"
#     "bts('1000000000000001'), Switch(False))")

# cProfile.run("Decoder_16_64K(Switch(True),bts('0000000000000000'))")

# cProfile.run("Selector_64K_1()")

cProfile.run("RAM_64K_1(Switch(False), bts('0000000000000000'), Switch(True))")

x = RAM_64K_1(Switch(False), bts('0000000000000000'), Switch(True))