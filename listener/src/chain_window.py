import logging
import os

from utils import is_valid_chain
from utils import same_block
from utils import same_hash

logger = logging.getLogger(__name__)
MAGIC_NUMBER = int(os.environ.get("MAGIC_NUMBER_WINDOW"))


class InvalidChain(Exception):
    pass


class ChainWindow:
    def __init__(self, origin_block, block_logs_service):
        self.__origin_block = origin_block
        self.__block_logs_service = block_logs_service
        self.old_chain = []
        self.new_chain = []

    @property
    def last_block_mined(self):
        return self.__block_logs_service.last_block_mined

    @property
    def last_block(self):
        if self.old_chain:
            last_block = self.old_chain[0].get("number")
        else:
            last_block = self.__origin_block
        return int(last_block)

    def sync(self):
        if self.last_block_mined - self.last_block <= MAGIC_NUMBER:
            logger.info("get_last_n_blocks")
            new_chain = self.__block_logs_service.get_last_nth_blocks(MAGIC_NUMBER)
            if not is_valid_chain(new_chain):
                raise InvalidChain("Invalid chain wachin")
        else:
            from_block = self.last_block + 1
            to_block = from_block + 500
            logger.info("get_range_blocks: {}-{}".format(from_block, to_block))
            new_chain = self.__block_logs_service.get_range_blocks(from_block, to_block)

        self.old_chain = self.new_chain
        self.new_chain = new_chain
        # self.__last_block = new_chain[0].get("block_number")

    def check_fork(self):
        old_chain = self.old_chain[::-1]
        new_chain = self.new_chain[::-1]
        i, j = 0, 0
        len_new_chain = len(new_chain) - 1

        while i <= len_new_chain:
            if same_block(new_chain[i], old_chain[j]):
                if not same_hash(new_chain[i], old_chain[j]):
                    return old_chain[j:][::-1]
                else:
                    i += 1
                    j += 1
            elif new_chain[i].get("number") > old_chain[j].get("number"):
                j += 1
        return []

    def check_new_blocks(self):
        last_block_processed = self.old_chain[0]
        for i, block in enumerate(self.new_chain):
            if same_block(self.new_chain[i], last_block_processed) and same_hash(self.new_chain[i], last_block_processed):
                return self.new_chain[:i]
        return []



# class ChainWindow:
#     def __init__(self, origin_block, block_logs_service):
#         self.__origin_block = origin_block
#         self.__block_logs_service = block_logs_service
#         self.__old_chain = []
#         self.__new_chain = []
#         self.__on_new_blocks_callbacks = []
#         self.__on_fork_callbacks = []
#
#     @property
#     def last_block_mined(self):
#         return self.__block_logs_service.last_block_mined
#
#     @property
#     def last_block(self):
#         if self.__old_chain:
#             last_block = self.__old_chain[0].get("number")
#         else:
#             last_block = self.__origin_block
#         return int(last_block)
#
#     def refresh(self):
#         if self.last_block_mined - self.last_block <= MAGIC_NUMBER:
#             logger.info("get_last_n_blocks")
#             new_chain = self.__block_logs_service.get_last_nth_blocks(MAGIC_NUMBER)
#             if not is_valid_chain(new_chain):
#                 raise InvalidChain("Invalid chain wachin")
#             self.__check_fork(new_chain, self.__old_chain)
#             self.__check_new_blocks(new_chain, self.__old_chain)
#             # self.__sarlanga(self.__old_chain, new_chain)
#         else:
#             from_block = self.last_block + 1
#             to_block = from_block + 500
#             logger.info("get_range_blocks: {}-{}".format(from_block, to_block))
#             new_chain = self.__block_logs_service.get_range_blocks(from_block, to_block)
#             self.__on_new_blocks(new_chain[::-1])
#
#         self.__old_chain = new_chain
#         self.__last_block = new_chain[0].get("block_number")
#
#
#     # def __sarlanga(self, old_chain, new_chain):
#     #     i, j = 0, 0
#     #     old_chain = old_chain[::-1]
#     #     while True:
#     #         if same_block(new_chain[i], old_chain[j]):
#     #             if not same_hash(new_chain[i], old_chain[j]):
#     #                 # restore_to_block(old_chain[j])
#     #                 self.__on_fork(old_chain[j:])
#     #             else:
#     #                 break
#     #             i += 1
#     #             j += 1
#     #         elif new_chain[i].get("number") > old_chain[j].get("number"):
#     #             j += 1
#     #     self.__on_new_blocks(new_chain[:i])
#
#     def __check_fork(self, new_chain, old_chain):
#         old_chain = old_chain[::-1]
#         new_chain = new_chain[::-1]
#         i, j = 0, 0
#         len_new_chain = len(new_chain) - 1
#
#         while i <= len_new_chain:
#             if same_block(new_chain[i], old_chain[j]):
#                 if not same_hash(new_chain[i], old_chain[j]):
#                     # return old_chain[:j]
#                     self.__on_fork(old_chain[j:][::-1])
#                 else:
#                     i += 1
#                     j += 1
#             elif new_chain[i].get("number") > old_chain[j].get("number"):
#                 j += 1
#
#     def __check_new_blocks(self, new_chain, old_chain):
#         last_block_processed = old_chain[0]
#         for i, block in enumerate(new_chain):
#             if same_block(new_chain[i], last_block_processed) and same_hash(new_chain[i], last_block_processed):
#                 self.__on_new_blocks(new_chain[:i])
#
#     def __sarlanga(self, old_chain, new_chain):
#
#         old_chain = old_chain[::-1]
#         new_chain = new_chain[::-1]
#         i, j = 0, 0
#         while True:
#             if same_block(new_chain[i], old_chain[j]):
#                 if not same_hash(new_chain[i], old_chain[j]):
#                     # restore_to_block(old_chain[j])
#                     self.__on_fork(old_chain[j:])
#                     break
#                 i += 1
#                 j += 1
#             elif new_chain[i].get("number") > old_chain[j].get("number"):
#                 j += 1
#         self.__on_new_blocks(new_chain[:i])
#
#     def subscribe_on_new_blocks(self, fn):
#         if fn not in self.__on_new_blocks_callbacks:
#             self.__on_new_blocks_callbacks.append(fn)
#
#     def subscribe_on_fork(self, fn):
#         if fn not in self.__on_fork_callbacks:
#             self.__on_fork_callbacks.append(fn)
#
#     def __on_new_blocks(self, new_blocks):
#         for callback in self.__on_new_blocks_callbacks:
#             callback(new_blocks)
#
#     def __on_fork(self, blocks):
#         for callback in self.__on_fork_callbacks:
#             callback(blocks)
