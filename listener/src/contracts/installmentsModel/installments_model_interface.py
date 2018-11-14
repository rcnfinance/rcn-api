class InstallmentsModelInterface():
    def __init__(self, contract_connection):
        self.contract = contract_connection

    def get_config_by_id(self, id_):
        return self.contract.contract.functions.configs(id_).call()
