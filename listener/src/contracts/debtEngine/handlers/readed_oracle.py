import web3
from contracts.event import EventHandler
from models import Commit
import utils


class ReadedOracle(EventHandler):
    signature = "ReadedOracle(bytes32,bytes32,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        data = self._event.get("data")
        splited_args = utils.split_every(64, data)
        self._tokens = splited_args[0]
        self._equivalent = splited_args[1]

        self._id = self._event.get("topics")[1].hex()
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "readed_oracle_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._id,
            "timestamp": self._block_timestamp(),
            "tokens": self._tokens,
            "equivalent": self._equivalent
        }

        commit.data = data

        return [commit]
