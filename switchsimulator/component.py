from abc import ABC, abstractmethod


class ElectricComponent(ABC):
    """
    Parent class for all components of the electric circuit
    """

    # Each class should have a tuple specifying available inputs and outputs
    # The output tuple is looped over to check if the output changes
    @staticmethod
    def unpack_io(*io_str):
        io_dict = {}
        for i in range(len(io_str)):
            x = io_str[i].split(":")
            io_dict[x[0]] = {'N': int(x[1]) if len(x) > 1 else 1}
        return io_dict
    # inputs = unpack_io()
    # outputs = unpack_io()

    # def get_state(self, port):
    #     """Returns the current state of the output(s)"""
    #     return getattr(self, port)

    def connect_input(self, input_name: str,
                      input_circuit: 'ElectricComponent'):
        """
        Should be used if not all inputs were available at initialization
        """

        old_input = getattr(self, input_name)
        islist = isinstance(old_input, list)

        if not islist:
            old_input = [old_input]
            input_circuit = [input_circuit]

        for i in range(len(input_circuit)):
            for fc in old_input[i].forward_connections:
                setattr(fc[0], fc[1], input_circuit[i])
                input_circuit[i].add_connection(fc[0], fc[1])
                fc[0].update()

        if not islist:
            input_circuit = input_circuit[0]

        # Not functional, just for tracking
        setattr(self, input_name, input_circuit)

    def __repr__(self):

        def object_to_str(o):
            return str(type(o).__name__) + ' @ ' + hex(id(o))

        def list_item_to_str(item):
            if isinstance(item, ElectricComponent):
                return object_to_str(item)
            elif isinstance(item, tuple):  # forward_connections are stored as tuples
                return object_to_str(item[0]) + ' <--> ' + item[1]
            else:
                raise NotImplementedError('What list is this?')

        selfdict = self.__dict__
        prtl = [object_to_str(self)]
        for k in selfdict.keys():
            if(isinstance(selfdict[k], ElectricComponent)):
                prtl.append(k + ': ' + object_to_str(selfdict[k]))
            elif(isinstance(selfdict[k], list)):
                prtl.append(
                    k + ': [' + ', '.join([list_item_to_str(item) for item in selfdict[k]]) + ']')
            else:
                prtl.append(k + ': ' + str(selfdict[k]))
        return '\n'.join(prtl)
