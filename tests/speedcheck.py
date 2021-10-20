# flake8: noqa
import cProfile
from switchsimulator.singlestatecomp import Switch
from switchsimulator.adders import Sixteen_Bit_Adder
from switchsimulator.helpers import bts


cProfile.run(
    "Sixteen_Bit_Adder(bts('1111111111111111'),"
    "bts('1000000000000001'), Switch(False))")
