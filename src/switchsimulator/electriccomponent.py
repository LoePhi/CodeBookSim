from typing import Union, List


class ElectricComponent():
    """
    Parent class for all components of the electric circuit
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def add_connection(self, con, port):
        raise NotImplementedError

    def get_state(self):
        raise NotImplementedError

    def connect_input(self,
                      port: str,
                      component: Union['ElectricComponent',
                                       List['ElectricComponent']]):
        """
        Should be used if not all inputs were available at initialization
        """

        old_input = getattr(self, port)

        old_input = old_input if isinstance(old_input, list) else [old_input]
        component = component if isinstance(component, list) else [component]

        if len(old_input) != len(component):
            raise ValueError("New input has wrong size")

        for i in range(len(component)):
            for fc in old_input[i].forward_connections:
                setattr(fc[0], fc[1], component[i])
                component[i].add_connection(fc[0], fc[1])
                fc[0].update()

        # Not functional, just for tracking
        component = component[0] if len(component) == 1 else component
        setattr(self, port, component)

    # def __repr__(self):

    #     def object_to_str(o):
    #         return str(type(o).__name__) + ' @ ' + hex(id(o))

    #     def list_item_to_str(item):
    #         if isinstance(item, ElectricComponent):
    #             return object_to_str(item)
    #         elif isinstance(item, tuple):  # forward_con stored as tuples
    #             return object_to_str(item[0]) + ' <--> ' + item[1]
    #         else:
    #             raise NotImplementedError('What list is this?')

    #     selfdict = self.__dict__
    #     prtl = [object_to_str(self)]
    #     for k in selfdict.keys():
    #         if(isinstance(selfdict[k], ElectricComponent)):
    #             prtl.append(k + ': ' + object_to_str(selfdict[k]))
    #         elif(isinstance(selfdict[k], list)):
    #             prtl.append(k + ': [' + ', '.join(
    #                 [list_item_to_str(item) for item in selfdict[k]]
    #             ) + ']')
    #         else:
    #             prtl.append(k + ': ' + str(selfdict[k]))
    #     return '\n'.join(prtl)
