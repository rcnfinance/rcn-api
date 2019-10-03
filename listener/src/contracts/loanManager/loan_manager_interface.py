from __future__ import division
import os
import numpy as np
from ethereum_connection import EthereumConnection
from ethereum_connection import ContractConnection

MODEL_ADDRESS = os.environ.get("INSTALLMENTS_ADDRESS")

ABI_PATH = os.path.join(
    "/project/contracts/installmentsModel",
    "abi.json"
)
URL_NODE = os.environ.get("URL_NODE")

eth_conn = EthereumConnection(URL_NODE)


class LoanManagerInterface():
    def __init__(self, contract_connection):
        self.__contract_connection = contract_connection
        self.fn = self.__contract_connection.contract.functions

    def get_directory(self):
        return self.fn.getDirectory().call()

    def get_currency(self, _id):
        try:
            currency = self.fn.getCurrency(_id).call().hex()
        except Exception:
            currency = None

        return currency

    def get_due_time(self, _id):
        return self.fn.getDueTime(_id).call()

    def get_status(self, _id):
        return self.fn.getStatus(_id).call()

    def get_descriptor(self, data):

        contract_connection_model = ContractConnection(eth_conn, MODEL_ADDRESS, ABI_PATH)
        contract_model = contract_connection_model.contract.functions
        loan_data = data.get("loanData")

        descriptor = {}

        descriptor["first_obligation"] = "0"
        descriptor["total_obligation"] = "0"
        descriptor["duration"] = "0"
        descriptor["interest_rate"] = "0"
        descriptor["punitive_interest_rate"] = "0"
        descriptor["frequency"] = "0"
        descriptor["installments"] = "0"

        if loan_data:
            contract_model.validate(loan_data).call()

            first_obligation_amount, first_obligation_time = contract_model.simFirstObligation(loan_data).call()
            total_obligation = contract_model.simTotalObligation(loan_data).call()
            duration = contract_model.simDuration(loan_data).call()

            descriptor["first_obligation"] = str(first_obligation_amount)
            descriptor["total_obligation"] = str(total_obligation)

            descriptor["duration"] = str(duration)
            descriptor["punitive_interest_rate"] = str(contract_model.simPunitiveInterestRate(loan_data).call())
            descriptor["frequency"] = str(contract_model.simFrequency(loan_data).call())
            descriptor["installments"] = str(contract_model.simInstallments(loan_data).call())

            periodic_rate = np.rate(
                int(descriptor["installments"]),
                int(descriptor["first_obligation"]),
                -int(data["amount"]),
                0,
                maxiter=9999999999999
            )

            annual_rate = float(periodic_rate) * (86400 * 360) / int(descriptor["frequency"])
            perc_rate = annual_rate * 100
            perc_rate_round = round(perc_rate, 2)

            descriptor["interest_rate"] = str(perc_rate_round)
        return descriptor
