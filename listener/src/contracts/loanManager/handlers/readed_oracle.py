import web3
from contracts.event import EventHandler
from utils import split_every
from models import Commit


class ReadedOracle(EventHandler):
    signature = "ReadedOracle(address,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        # data = self._event.get("data")
        # splited_data = split_every(64, data)
        #
        # self._id = splited_data[0]
        # self._tokens = splited_data[1]
        # self._equivalent = splited_data[2]
        #
        # self._block_number = self._event.get('blockNumber')
        # self._transaction = self._event.get('transactionHash').hex()
        pass

    def handle(self):
        return []
        # commit = Commit()
        #
        # commit.opcode = "readed_oracle_loan_manager"
        # commit.timestamp = self._block_timestamp()
        # commit.proof = self._transaction
        #
        # data = {
        #     "id": self._id,
        #     "tokens": self._tokens,
        #     "equivalent": self._equivalent,
        #     "timestamp": str(self._block_timestamp())
        # }
        #
        # commit.data = data
        #
        # return [commit]
