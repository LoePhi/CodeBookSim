from basic_components import Switch


def bit_to_switch_tmp(bit8):
    return [Switch(bool(int(b))) for b in bit8]


bts8 = bit_to_switch_tmp
