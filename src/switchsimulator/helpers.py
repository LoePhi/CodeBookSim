from switchsimulator.corecomponents import Switch


def bin_to_switch(bin_str):
    return [Switch(bool(int(b))) for b in bin_str]


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

    return [Switch(bool(int(b))) for b in bit8]
