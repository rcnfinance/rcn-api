class DebtEngineInterface():
    def __init__(self, contract_connection):
        self.contract = contract_connection

    def get_debt_by_id(self, id_):
        debt_data = self.contract.contract.functions.debts(id_).call()

        debt = {}
        debt["error"] = debt_data[0]
        debt["balance"] = debt_data[1]
        debt["model"] = debt_data[2]
        debt["creator"] = debt_data[3]
        debt["oracle"] = debt_data[4]

        return debt

    def get_model_by_id(self, id_):
        model = self.get_debt_by_id(id_)[4]
        return model

    def get_state_by_id(self, id_):
        state = self.contract.coontract.functions.states(id_).call()
        return state
