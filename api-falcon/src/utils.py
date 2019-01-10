import web3
import os
import falcon
from models import Debt
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

URL_NODE = "https://ropsten.node.rcn.loans:8545/"
eth_conn = EthereumConnection(URL_NODE)

LOAN_MANAGER_ADDRESS = "0xbF77a4061eB243d38BaCBD684f0c3124eefE6E91"
MODEL_ADDRESS = "0xE3633E63Da6154D9450e34F0d4c64c6A51f6918e"

LOAN_MANAGER_ABI_PATH = os.path.join(
 os.path.dirname(os.path.realpath(__file__)),
    "loanManagerABI.json"
)

MODEL_ABI_PATH = os.path.join(
 os.path.dirname(os.path.realpath(__file__)),
    "modelABI.json"
)

loan_manager_connection = ContractConnection(eth_conn, LOAN_MANAGER_ADDRESS, LOAN_MANAGER_ABI_PATH)
model_connection = ContractConnection(eth_conn, MODEL_ADDRESS, MODEL_ABI_PATH)

loanManagerContract = loan_manager_connection.contract.functions
modelContract = model_connection.contract.functions

class ModelAndDebtData:

    def getData(self, id_loan):

        block = loan_manager_connection.w3.eth.getBlock('latest')
        debt = Debt.objects.get(id=id_loan)

        paid = modelContract.getPaid(id_loan).call()
        dueTime = modelContract.getDueTime(id_loan).call()
        estimatedObligation = modelContract.getEstimateObligation(id_loan).call()
        nextObligation = modelContract.getObligation(id_loan, dueTime).call()[0]
        currentObligation = modelContract.getObligation(id_loan, block.timestamp).call()[0]


        debtBalance = debt.balance
        owner = loanManagerContract.ownerOf(int(id_loan, 16)).call()

        data = {
            "paid": paid,
            "dueTime": dueTime,
            "estimatedObligation": estimatedObligation,
            "nextObligation": nextObligation,
            "currentObligation": currentObligation,
            "debtBalance": debtBalance,
            "owner": owner
        }
        return data
