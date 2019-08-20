import glob
import json
import os

from .interface_blocklogs_service import IBlockLogsService


class MockNewBlocksService(IBlockLogsService):
    BKUP_PATH = "data/new_blocks/"
    def __init__(self):
        self.__init_data()

    def __init_data(self):
        data_path = os.path.abspath(self.BKUP_PATH)
        pattern = "*.json"
        list_dumps = glob.glob1(data_path, pattern)
        print("Encontre {} archivos backup".format(len(list_dumps)))
        print(list_dumps)
        self._data = []
        for json_file in list_dumps:
            self._data.extend(json.load(open(os.path.join(self.BKUP_PATH, json_file))))

        print("Num blocks: {}".format(len(self._data)))
        self._data.sort(
            key=lambda block: block.get("number"),
            reverse=True
        )

        self._last_block_mined = self._data[0].get("number")

    def get_last_nth_blocks(self, num):
        return self._data[:num]

    def get_range_blocks(self, from_block, to_block):
        blocks = list(filter(lambda block: from_block <= int(block.get("number")) <= to_block, self._data))
        return blocks

    @property
    def last_block_mined(self):
        return int(self._last_block_mined)


class MockForkBlocksService(MockNewBlocksService):
    def get_last_nth_blocks(self, num):
        BKUP_PATH = "data/fork/"
        fork_file = "last_32_blocks.json"
        fork_path = os.path.abspath(os.path.join(BKUP_PATH, fork_file))
        data = json.load(open(fork_path))
        data.sort(
            key=lambda block: block.get("number"),
            reverse=True
        )
        return data[:num]
