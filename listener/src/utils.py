import web3


def split_every(n, string):
    return [string[i:i + n] for i in range(0, len(string), n)]


def to_address(hex_string):
    return '0x' + hex_string[-40:]


def to_int(hex_string):
    return web3.Web3.toInt(hexstr=hex_string)


def to_bool(hex_string):
    # TODO: fix this
    return hex_string


def add_0x_prefix(string):
    return web3.utils.contracts.add_0x_prefix(string)
