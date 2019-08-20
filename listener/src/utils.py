# import itertools
from itertools import tee
# import re
import web3
# from web3.exceptions import MismatchedABI

def same_block(block1, block2):
    print("{} == {} --> {}".format(
        block1.get("number"),
        block2.get("number"),
        block1.get("number") == block2.get("number")
    ))
    return block1.get("number") == block2.get("number")


def same_hash(block1, block2):
    print("{} == {} --> {}".format(
        block1.get("hash"),
        block2.get("hash"),
        block1.get("hash") == block2.get("hash")
    ))
    return block1.get("hash") == block2.get("hash")


def pairwise(iterable):
    a, b = tee(iterable)
    next(a, None)
    return list(zip(a, b))


def is_prev(b1, b2):
    return b1["hash"] == b2["parentHash"]


def is_valid_chain(chain):
    return all(map(lambda pair: is_prev(pair[0], pair[1]), pairwise(chain)))


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

# def collapse_if_tuple(abi):
#     """Converts a tuple from a dict to a parenthesized list of its types.
#
#     >>> from eth_utils.abi import collapse_if_tuple
#     >>> collapse_if_tuple(
#     ...     {
#     ...         'components': [
#     ...             {'name': 'anAddress', 'type': 'address'},
#     ...             {'name': 'anInt', 'type': 'uint256'},
#     ...             {'name': 'someBytes', 'type': 'bytes'},
#     ...         ],
#     ...         'type': 'tuple',
#     ...     }
#     ... )
#     '(address,uint256,bytes)'
#     """
#     typ = abi["type"]
#     if not typ.startswith("tuple"):
#         return typ
#
#     delimited = ",".join(collapse_if_tuple(c) for c in abi["components"])
#     # Whatever comes after "tuple" is the array dims.  The ABI spec states that
#     # this will have the form "", "[]", or "[k]".
#     array_dim = typ[5:]
#     collapsed = "({}){}".format(delimited, array_dim)
#
#     return collapsed
#
# def _abi_to_signature(abi):
#     function_signature = "{fn_name}({fn_input_types})".format(
#         fn_name=abi["name"],
#         fn_input_types=",".join(
#             [collapse_if_tuple(abi_input) for abi_input in abi.get("inputs", [])]
#         ),
#     )
#     return function_signature
#
# def event_signature_to_log_topic(event_signature):
#     return web3.Web3.sha3(text=event_signature).hex()
#
# def event_abi_to_log_topic(event_abi):
#     event_signature = _abi_to_signature(event_abi)
#     return event_signature_to_log_topic(event_signature)
#
# def get_indexed_event_inputs(event_abi):
#     return [arg for arg in event_abi['inputs'] if arg['indexed'] is True]
#
# DYNAMIC_TYPES = ['bytes', 'string']
#
# INT_SIZES = range(8, 257, 8)
# BYTES_SIZES = range(1, 33)
# UINT_TYPES = ['uint{0}'.format(i) for i in INT_SIZES]
# INT_TYPES = ['int{0}'.format(i) for i in INT_SIZES]
# BYTES_TYPES = ['bytes{0}'.format(i) for i in BYTES_SIZES] + ['bytes32.byte']
#
# STATIC_TYPES = list(itertools.chain(
#     ['address', 'bool'],
#     UINT_TYPES,
#     INT_TYPES,
#     BYTES_TYPES,
# ))
#
# BASE_TYPE_REGEX = '|'.join((
#     _type + '(?![a-z0-9])'
#     for _type
#     in itertools.chain(STATIC_TYPES, DYNAMIC_TYPES)
# ))
#
# SUB_TYPE_REGEX = (
#     r'\['
#     '[0-9]*'
#     r'\]'
# )
#
# TYPE_REGEX = (
#     '^'
#     '(?:{base_type})'
#     '(?:(?:{sub_type})*)?'
#     '$'
# ).format(
#     base_type=BASE_TYPE_REGEX,
#     sub_type=SUB_TYPE_REGEX,
# )
#
#
# def is_recognized_type(abi_type):
#     return bool(re.match(TYPE_REGEX, abi_type))
#
# NAME_REGEX = (
#     '[a-zA-Z_]'
#     '[a-zA-Z0-9_]*'
# )
#
#
# ENUM_REGEX = (
#     '^'
#     '{lib_name}'
#     r'\.'
#     '{enum_name}'
#     '$'
# ).format(lib_name=NAME_REGEX, enum_name=NAME_REGEX)
#
# def is_probably_enum(abi_type):
#     return bool(re.match(ENUM_REGEX, abi_type))
#
# def normalize_event_input_types(abi_args):
#     for arg in abi_args:
#         if is_recognized_type(arg['type']):
#             yield arg
#         elif is_probably_enum(arg['type']):
#             yield {k: 'uint8' if k == 'type' else v for k, v in arg.items()}
#         else:
#             yield arg
#
# def get_event_data(event_abi, log_entry):
#     """
#     Given an event ABI and a log entry for that event, return the decoded
#     event data
#     """
#     # if event_abi['anonymous']:
#     #     log_topics = log_entry['topics']
#     # elif not log_entry['topics']:
#     #     raise MismatchedABI("Expected non-anonymous event to have 1 or more topics")
#     # elif event_abi_to_log_topic(event_abi) != log_entry['topics'][0]:
#     #     raise MismatchedABI("The event signature did not match the provided ABI")
#     # else:
#     #     log_topics = log_entry['topics'][1:]
#
#     if event_abi_to_log_topic(event_abi) != log_entry.get('topic0'):
#         raise MismatchedABI("The event signature did not match the provided ABI")
#
#
#     log_topics_abi = get_indexed_event_inputs(event_abi)
#     log_topic_normalized_inputs = normalize_event_input_types(log_topics_abi)
#     log_topic_types = get_event_abi_types_for_decoding(log_topic_normalized_inputs)
#     log_topic_names = get_abi_input_names({'inputs': log_topics_abi})
#
#     if len(log_topics) != len(log_topic_types):
#         raise ValueError("Expected {0} log topics.  Got {1}".format(
#             len(log_topic_types),
#             len(log_topics),
#         ))
#
#     log_data = hexstr_if_str(to_bytes, log_entry['data'])
#     log_data_abi = exclude_indexed_event_inputs(event_abi)
#     log_data_normalized_inputs = normalize_event_input_types(log_data_abi)
#     log_data_types = get_event_abi_types_for_decoding(log_data_normalized_inputs)
#     log_data_names = get_abi_input_names({'inputs': log_data_abi})
#
#     # sanity check that there are not name intersections between the topic
#     # names and the data argument names.
#     duplicate_names = set(log_topic_names).intersection(log_data_names)
#     if duplicate_names:
#         raise ValueError(
#             "Invalid Event ABI:  The following argument names are duplicated "
#             "between event inputs: '{0}'".format(', '.join(duplicate_names))
#         )
#
#     decoded_log_data = decode_abi(log_data_types, log_data)
#     normalized_log_data = map_abi_data(
#         BASE_RETURN_NORMALIZERS,
#         log_data_types,
#         decoded_log_data
#     )
#
#     decoded_topic_data = [
#         decode_single(topic_type, topic_data)
#         for topic_type, topic_data
#         in zip(log_topic_types, log_topics)
#     ]
#     normalized_topic_data = map_abi_data(
#         BASE_RETURN_NORMALIZERS,
#         log_topic_types,
#         decoded_topic_data
#     )
#
#     event_args = dict(itertools.chain(
#         zip(log_topic_names, normalized_topic_data),
#         zip(log_data_names, normalized_log_data),
#     ))
#
#     event_data = {
#         'args': event_args,
#         'event': event_abi['name'],
#         'logIndex': log_entry['logIndex'],
#         'transactionIndex': log_entry['transactionIndex'],
#         'transactionHash': log_entry['transactionHash'],
#         'address': log_entry['address'],
#         'blockHash': log_entry['blockHash'],
#         'blockNumber': log_entry['blockNumber'],
#     }
#
#     return AttributeDict.recursive(event_data)