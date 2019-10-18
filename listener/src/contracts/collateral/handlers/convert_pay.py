import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class ConvertPay(EventHandler):
    signature = "ConvertPay(uint256,uint256,uint256,bytes)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_entryId"] = utils.add_0x_prefix(self._args["_entryId"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "convert_pay_collateral"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        data = {
            "id": str(self._args.get("_entryId")),
            "fromAmount": str(self._args.get("_fromAmount")),
            "toAmount": str(self._args.get("_toAmount")),
            "oracleData": str(self._args.get("_oracleData")),
        }

        commit.data = data

        return [commit]
