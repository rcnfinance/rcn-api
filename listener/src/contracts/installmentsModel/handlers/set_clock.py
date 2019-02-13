from contracts.event import EventHandler
import web3
import utils
from models import Commit


class SetClock(EventHandler):
    signature = "_setClock(bytes32,uint64)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    # def _parse(self):
    #     data = self._event.get("data")[2:]
    #     splited_args = utils.split_every(64, data)
    #
    #     self._id = "0x" + splited_args[0]
    #     self._duration = splited_args[1]
    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_clock_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "duration": str(self._args.get("_to"))
        }

        commit.data = data

        return [commit]
