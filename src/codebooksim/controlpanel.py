from codebooksim.base import MultiOutCircuit
from codebooksim.corecomponents import Switch
from codebooksim.helpers import bts, print_ic_list


class ControlPanel64KB(MultiOutCircuit):
    """
    Control Panel, p. 204
    """

    def __init__(self) -> None:

        self.address = bts('0'*16)
        self.data = bts('0'*8)
        self.write = Switch(False)
        self.takeover = Switch(True)

    def _set_multi_slot(self, slotname: str, bitstr: str) -> None:
        x = getattr(self, slotname)
        for i, a in enumerate(bitstr):
            if a == '0':
                x[i].open()
            elif a == '1':
                x[i].close()
            else:
                raise ValueError(
                    "Address must be specified using a string of 0s and 1s")

    def set_address(self, new_address: str) -> None:
        self._set_multi_slot('address', new_address)

    def set_data(self, new_data: str) -> None:
        self._set_multi_slot('data', new_data)


asd = ControlPanel64KB()
print_ic_list(asd.address)
asd.set_address('0'*10+'1'+'0'*5)
print_ic_list(asd.address)
print_ic_list(asd.data)
asd.set_data('0'*3+'1'+'0'*4)
print_ic_list(asd.data)
