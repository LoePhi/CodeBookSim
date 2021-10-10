from abc import ABC, abstractmethod


class ElectricComponent(ABC):
    """Parent class for all components of the electric circuit"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        """Computes the output - has to be defined on the component level"""
        pass

    @abstractmethod
    def get_state(self):
        """Can be called to return the output"""
        pass




class SingleStateComponent(ElectricComponent):
    """
    Parent Class for all components with a singular output
    """

    def get_state(self):
        return(self._out)

    is_on = property(get_state)


class Switch(SingleStateComponent):
    """Simple Switch"""

    def __init__(self, closed=False):
        self._out = closed

    def update(self):
        pass


# Alias
Bit = Switch


def ipp(inp):
    """
    Input parser
    Converts input to bool or list of bool
    Input -> Output:
    List -> List (unchecked)
    bool -> bool
    single int (0,1) -> bool
    ...
    """

    # int: 101 -> ['1', '0', '1'] -> 
    # str: '101' -> ['1', '0', '1']
    # bool: True -> 

    if isinstance(inp, (bool, list)):
        return inp
    if isinstance(inp, (int)):
        inp = str(inp)
    if isinstance(inp, str):
        inp = list(inp)
    out = []
    for i in inp:
        if i not in ('0', '1'):
            raise ValueError("bad input")
        out = [bool(int(i)) for i in inp]
    if len(out) == 1:
        return out[0]
    else:
        return out



# Tests:
# print(Switch(True).is_on == True)
# print(Switch(False).is_on == False)
# print(Bit(True).is_on == True)
# print(Bit(False).is_on == False)

# 12 -> error
# 10 -> [True, False]
# '10' -> [True, False]
# '12' -> Error
# True -> True
# True, False -> True, False

# ipp(12)
# ipp(10)
# ipp(1)
# ipp(0)
# ipp('12')
# ipp('10')
# ipp(True)
# ipp([True, False])

