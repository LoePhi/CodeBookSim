from electriccomponent import ElectricComponent


class IntegratedComponent(ElectricComponent):

    def add_connection(self, con, port):
        """
        The connection is passed on until a corecomponent is found
        """
        # TODO: work with lists
        for out in self.outputs:
            getattr(self, out).add_connection(con, port)
