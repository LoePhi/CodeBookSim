from typing import Any, Iterable, Union, List


class ElectricComponent():
    """
    Parent class for all components of the electric circuit
    """

    def __init__(self) -> None:
        raise NotImplementedError

    # type cheat
    # add_connection ist hier nur, weil
    # connect_input sich sonst beschwert
    # -> connect_input in kinder packen, aber die
    # gleich bleibenden elemente wieder hier hoch verlagern
    def add_connection(self, con: 'ElectricComponent', port: str) -> None:
        raise NotImplementedError

    def get_state(self) -> bool:
        raise NotImplementedError

    def connect_input(self,
                      port: str,
                      component: Union['ElectricComponent',
                                       List['ElectricComponent']]) -> None:
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

    @staticmethod
    def _prt_dict_atom(a: Any) -> str:
        if isinstance(a, ElectricComponent):
            retstr = a.__class__.__name__ + ' at ' + hex(id(a))
        else:
            retstr = str(a)
        return retstr

    @staticmethod
    def _prt_collection(c: Iterable[Any]) -> str:
        str_list = []
        for a in c:
            str_list.append(ElectricComponent._prt_dict_elem(a))
        return ', '.join(str_list)

    @staticmethod
    def _prt_dict_elem(e: Any) -> str:
        if isinstance(e, list):
            retstr = "[" + ElectricComponent._prt_collection(e) + "]"
        elif isinstance(e, tuple):
            retstr = "(" + ElectricComponent._prt_collection(e) + ")"
        else:
            retstr = ElectricComponent._prt_dict_atom(e)
        return retstr

    def __repr__(self) -> str:
        """
        Mea culpa
        """
        retstr = ElectricComponent._prt_dict_atom(self) + ' '
        retstr = retstr + str(self.__class__.__base__) + '\n'
        sd = self.__dict__
        for k in sd:
            retstr = retstr + str(k) + ': ' + self._prt_dict_elem(sd[k]) + '\n'
        return retstr
