import corecomponents as cc
from corecomponents import LooseWire
from functools import wraps
import inspect


def bin_to_switch(bin_str):
    return [cc.Switch(bool(int(b))) for b in bin_str]


def int_to_switch(dec_int):
    return bin_to_switch(bin(dec_int)[2:])


def bool_to_int(bin_bool):
    if len(bin_bool) == 1:
        return(int(bin_bool))
    else:
        bin_str = ''.join(['1' if b else '0' for b in bin_bool])
        return int(bin_str, 2)


def bool_to_bin(bin_bool):
    if len(bin_bool) == 1:
        return(str(int(bin_bool)))
    else:
        bin_str = ''.join(['1' if b else '0' for b in bin_bool])
        return bin_str


# TODO: better names
bts = bin_to_switch
its = int_to_switch
bti = bool_to_int
btb = bool_to_bin


def bit_to_switch_tmp(bit8):
    """
    doc
    this is description
    """

    return [cc.Switch(bool(int(b))) for b in bit8]


def _lwd(n: int = 1):
    """
    ONLY for use with the @autoparse decorator.
    LooseWires are temporary and will be exchanged by the decorator.
    """
    if n == 1:
        return LooseWire()
    else:
        return [LooseWire() for _ in range(n)]


def autoparse(init):
    inispec = inspect.getfullargspec(init)
    parnames = inispec.args[1:]
    defaults = inispec.defaults

    @wraps(init)
    def wrapped_init(self, *args, **kwargs):
        print(args)
        print(kwargs)
        print(parnames)
        print(defaults)
        # Turn args into kwargs
        kwargs.update(zip(parnames[:len(args)], args))

        # apply default parameter values
        default_start = len(parnames) - len(defaults)
        for i in range(len(defaults)):
            if parnames[default_start + i] not in kwargs:
                kwargs[parnames[default_start + i]] = defaults[i]

        # generate new instance for each LooseWire
        for arg in kwargs:
            if isinstance(kwargs[arg], LooseWire):
                kwargs[arg] = LooseWire()
            if isinstance(kwargs[arg], list):
                for i in range(len(kwargs[arg])):
                    if isinstance(kwargs[arg][i], LooseWire):
                        kwargs[arg][i] = LooseWire()

        # attach parameters to instance
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

        init(self, **kwargs)

    return wrapped_init
