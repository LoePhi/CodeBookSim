from typing import List, Sequence
from switchsimulator.base import ElectricElement, InputComponent
from switchsimulator.corecomponents import Switch


def bin_to_switch(bin_str: str) -> Sequence[Switch]:
    return [Switch(bool(int(b))) for b in bin_str]


bts = bin_to_switch


def print_ic_list(compl: Sequence[InputComponent]) -> None:
    print(''.join([ee.__str__() for ee in compl]))
