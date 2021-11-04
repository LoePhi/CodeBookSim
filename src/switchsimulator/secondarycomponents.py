from switchsimulator.electriccomponent import ElectricComponent


class SecondaryComponent(ElectricComponent):

    pass


class SingleStateSC(SecondaryComponent):
    """
    This allows for its children to be used
    like basegates and other core components

    and1 = AND(s1)
    xor1 = XOR(s1, s2)

    xor.out_main.is_on can be written as
    xor.is_on

    and1.connect_input('in_b', xor1.out_main)
    can be written as if XOR were a CoreComponent
    and1.connect_input('in_b', xor1)
    """

    out_main: ElectricComponent

    def get_state(self):
        return self.out_main.get_state()

    is_on = property(get_state)

    def add_connection(self, con, port):
        self.out_main.add_connection(con, port)
