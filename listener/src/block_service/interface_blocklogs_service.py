from abc import ABC


class IBlockLogsService(ABC):
    def get_last_nth_blocks(cls, num):
        pass

    def get_range_blocks(cls, from_block, to_block):
        pass

    def last_block_mined(cls):
        pass
