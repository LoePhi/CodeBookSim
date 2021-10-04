class Bit:
    def __init__(self, is_on=False):
        self._is_on = is_on

    def get_state(self):
        return self._is_on

    is_on = property(get_state)


class INV:
    def __init__(self, pin1=None):
        self.pin1 = pin1

    def update(self):
        self._is_on = not self.pin1.is_on

    def get_state(self):
        self.update()
        return self._is_on

    is_on = property(get_state)

class Gate:
    def __init__(self, pin1=None, pin2=None):
        self.pin1 = pin1
        self.pin2 = pin2

    def update(self):
        raise Exception("Basegate has no logic")

    def get_state(self):
        self.update()
        return self._is_on

    is_on = property(get_state)

class AND(Gate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self._is_on = self.pin1.is_on and self.pin2.is_on


class OR(Gate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self._is_on = self.pin1.is_on or self.pin2.is_on


class NAND(Gate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AND1 = AND(self.pin1, self.pin2)
        self.INV1 = INV(self.AND1)

    def update(self):
        self._is_on = self.INV1.is_on


class NOR(Gate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.OR1 = OR(self.pin1, self.pin2)
        self.INV1 = INV(self.OR1)

    def update(self):
        self._is_on = self.INV1.is_on


class XOR(Gate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.OR1 = OR(self.pin1, self.pin2)
        self.NAND1 = NAND(self.pin1, self.pin2)
        self.AND1 = AND(self.OR1, self.NAND1)

    def update(self):
        self._is_on = self.AND1.is_on




# b1 = Bit(True)
# b2 = Bit(True)
# b3 = Bit(True)
# b4 = Bit(False)

# a1 = AND(b1, b2)
# a2 = AND(b1, b3)
# a3 = AND(b1, b4)

# aa1 = AND(a1, a2)
# aa2 = AND(a1, a3)

# aaa1 = AND(aa1, aa2)

# a1.is_on
# a2.is_on
# a3.is_on

# aa1.is_on
# aa2.is_on

# aaa1.is_on

# asd = NAND(AND(b1, b2), AND(b3, b4))
# asd.is_on

# XOR(AND(b1, b2), AND(b3, b4)).is_on