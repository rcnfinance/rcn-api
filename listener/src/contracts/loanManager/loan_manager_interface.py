from models import Descriptor
import os
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection


ABI_PATH = os.path.join(
    "/project/contracts/installmentsModel",
    "abi.json"
)
URL_NODE = "https://ropsten.node.rcn.loans:8545/"

eth_conn = EthereumConnection(URL_NODE)


class LoanManagerInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_request_data(self, _id):
        request_data = self.fn.requests(_id).call()
        print(request_data);
        print("loanID=",_id)
        parsed_request_data = self.__parse_data(request_data)
        parsed_request_data["currency"] = self.get_currency(int(_id, 16))
        parsed_request_data["status"] = self.get_status(int(_id, 16))
        parsed_request_data["descriptor"] = self.get_descriptor(parsed_request_data)

        return parsed_request_data

    def __parse_data(self, request_data):
        parsed_data = {}
        parsed_data["open"] = request_data[0]
        parsed_data["approved"] = request_data[1]
        parsed_data["currency"] = request_data[2].hex()
        parsed_data["position"] = request_data[3]
        parsed_data["expiration"] = request_data[4]
        parsed_data["amount"] = request_data[5]
        parsed_data["cosigner"] = request_data[6]
        parsed_data["model"] = request_data[7]
        parsed_data["creator"] = request_data[8]
        parsed_data["oracle"] = request_data[9]
        parsed_data["borrower"] = request_data[10]
        parsed_data["nonce"] = request_data[11]
        parsed_data["loanData"] = request_data[12].hex()

        return parsed_data

    def get_directory(self):
        return self.fn.getDirectory().call()

    def get_currency(self, _id):
        return self.fn.getCurrency(_id).call().hex()

    def get_due_time(self, _id):
        return self.fn.getDueTime(_id).call()

    def get_status(self, _id):
        return self.fn.getStatus(_id).call()

    def get_descriptor(self, parsed_request_data):
    
        contract_connectionModel = ContractConnection(eth_conn, parsed_request_data["model"], ABI_PATH)
        contractModel = contract_connectionModel.contract.functions   
        loanData = parsed_request_data["loanData"]
        print("abi-path",ABI_PATH)
        print("model=",parsed_request_data["model"])
        print("contractModel=",contractModel) 
        print("loanData",loanData)

        validate = contractModel.validate(loanData).call()
        print("esDataLoanValida:",validate)

        descriptor = Descriptor()

        (firstObligationAmount, firstObligationTime) = contractModel.simFirstObligation(loanData).call()

        totalObligation = contractModel.simTotalObligation(loanData).call()
        duration = contractModel.simDuration(loanData).call()

        yearAccrued = (totalObligation * 86400 * 360) / duration;
        interestRate = ((yearAccrued / parsed_request_data["amount"]) - 1) * 100;

        descriptor.firstObligation = firstObligationAmount
        descriptor.totalObligation = totalObligation
        descriptor.duration = duration
        descriptor.interestRate = interestRate
        descriptor.punitiveInterestRate = contractModel.simPunitiveInterestRate(loanData).call()
        descriptor.frequency = contractModel.simFrequency(loanData).call()
        descriptor.installments = contractModel.simInstallments(loanData).call()
 

        print("firstObligation=",descriptor.firstObligation)
        print("totalObligation=",descriptor.totalObligation)
        print("duration=",descriptor.duration)
        print("interestRate=",descriptor.interestRate)
        print("punitiveInterestRate=",descriptor.punitiveInterestRate)
        print("frequency=",descriptor.frequency)
        print("installments=",descriptor.installments)

        return descriptor


