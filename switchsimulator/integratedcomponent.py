from electriccomponent import ElectricComponent


class IntegratedComponent(ElectricComponent):

    # TODO: I think this should be in integrated_logic_gate
    # (or get_state from there should be in here)
    # or there should be a single_out class
    def add_connection(self, con, port):
        """
        This allows for IntegratedComponents to be used
        like core components if they feature a single out_main-line
        e.g.

        and1 = AND(s1)
        xor1 = XOR(s1, s2)
        and1.connect_input('in_b', xor1.out_main)
        can be written as if XOR were a CoreComponent
        and1.connect_input('in_b', xor1)
        """
        self.out_main.add_connection(con, port)
