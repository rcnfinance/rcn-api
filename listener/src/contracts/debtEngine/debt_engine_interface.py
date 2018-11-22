class DebtEngineInterface():
    def __init__(self, contract_connection):
        self.contract = contract_connection

    def get_debt_by_id(self, id_):
        return self.contract.contract.functions.debts(id_).call()

    def get_model_by_id(self, id_):
        model = self.get_debt_by_id(id_)[4]
        return model

    def get_state_by_id(self, id_):
        state = self.contract.coontract.functions.states(id_).call()
        return state
