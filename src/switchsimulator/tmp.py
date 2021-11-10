# type: ignore


from typing import Iterable
from switchsimulator.helpers import bts
from switchsimulator.misccomp import OnesComplement

asd = OnesComplement(bts('00110011'))
isinstance(asd, Iterable)
