def unpack_io(*io_str):
    io_dict = {}
    for i in range(len(io_str)):
        x = io_str[i].split(":")
        io_dict[x[0]] = {'N': x[1] if len(x) > 1 else 1}
    return io_dict
