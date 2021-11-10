from typing import List
from switchsimulator.corecomponents import Switch


def bin_to_switch(bin_str: str) -> List[Switch]:
    return [Switch(bool(int(b))) for b in bin_str]


bts = bin_to_switch
