import web3
from contracts.event import EventHandler
from models import Commit
import utils


class Paid(EventHandler):
    signature = "Paid(bytes32,address,address,uint256,uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _parse(self):
    #     data = self._event.get("data")[2:]
    #     splited_args = utils.split_every(64, data)

    #     self._id = self._event.get("topics")[1].hex()

    #     self._sender = "0x" + splited_args[0][24:]
    #     self._origin = "0x" + splited_args[1][24:]
    #     self._requested = int(splited_args[2], 16)
    #     self._requested_tokens = int(splited_args[3], 16)
    #     self._paid = int(splited_args[4], 16)
    #     self._tokens = int(splited_args[5], 16)

    #     self._block_number = self._event.get('blockNumber')
    #     self._transaction = self._event.get('transactionHash').hex()

    def _normalize(self):
        self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "paid_debt_engine"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        data = {
            "id": self._args.get("_id"),
            "sender": self._args.get("_sender"),
            "origin": self._args.get("_origin"),
            "requested": str(self._args.get("_requested")),
            "requested_tokens": str(self._args.get("_requestedTokens")),
            "paid": str(self._args.get("_paid")),
            "tokens": str(self._args.get("_tokens"))
        }

        commit.data = data

        return [commit]
