from contracts.event import EventHandler
import web3
import utils
from models import Commit


class SetPaidBase(EventHandler):
    signature = "_setPaidBase(bytes32,uint128)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    # def _parse(self):
    #     data = self._event.get("data")[2:]
    #     splited_args = utils.split_every(64, data)
    #     self._id = "0x" + splited_args[0]
    #     self._paid_base = int(splited_args[1], 16)
    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "set_paid_base_installments"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "paid_base": str(self._args.get("_paidBase"))
        }

        commit.data = data

        return [commit]
