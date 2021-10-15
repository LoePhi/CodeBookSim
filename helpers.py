import singlestatecomp as ssc


def bit_to_switch_tmp(bit8):
    """doc"""

    return [ssc.Switch(bool(int(b))) for b in bit8]


# Alias
bts8 = bit_to_switch_tmp

