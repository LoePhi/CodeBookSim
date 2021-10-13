def ipp(inp):
    """
    Input parser
    Converts input to bool or list of bool
    Input -> Output:
    List -> List (unchecked)
    bool -> bool
    single int (0,1) -> bool
    ...
    """

    # int: 101 -> ['1', '0', '1'] ->
    # str: '101' -> ['1', '0', '1']
    # bool: True ->

    if isinstance(inp, (bool, list)):
        return inp
    if isinstance(inp, (int)):
        inp = str(inp)
    if isinstance(inp, str):
        inp = list(inp)
    out = []
    for i in inp:
        if i not in ('0', '1'):
            raise ValueError("bad input")
        out = [bool(int(i)) for i in inp]
    if len(out) == 1:
        return out[0]
    else:
        return out

# Tests

# 12 -> error
# 10 -> [True, False]
# '10' -> [True, False]
# '12' -> Error
# True -> True
# True, False -> True, False

# ipp(12)
# ipp(10)
# ipp(1)
# ipp(0)
# ipp('12')
# ipp('10')
# ipp(True)
# ipp([True, False])