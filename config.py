
def read_config():
    args_dict = {}

    with open('CONFIG.txt', 'r') as fp:
        args = [u for u in fp.readlines() if u.strip()[0] != '#']
        for arg in args:
            arg_pair = [u.strip() for u in arg.split(':')]
            args_dict[arg_pair[0]] = float(arg_pair[1])

    return args_dict
