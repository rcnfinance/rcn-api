import web3
from contracts.event import EventHandler
from utils import split_every
from models import Commit


class Cosigned(EventHandler):
    signature = "Cosigned(bytes32,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        self._id = self._event.get("topics")[1].hex()
        data = self._event.get("data")
        splited_data = split_every(64, data)
        self._cosigner = splited_data[0]
        self._amount = splited_data[1]
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "cosigned_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._id,
            "cosigner": self._cosigner
        }

        commit.data = data

        return [commit]
