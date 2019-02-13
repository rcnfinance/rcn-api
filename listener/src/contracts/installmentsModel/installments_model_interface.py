class InstallmentsModelInterface():
    def __init__(self, contract_connection):
        self.contract = contract_connection

    def get_config_by_id(self, id_):
        config = self.contract.contract.functions.configs(id_).call()

        config_data = dict()
        config_data["installments"] = config[0]
        config_data["time_unit"] = config[1]
        config_data["duration"] = config[2]
        config_data["lent_time"] = config[3]
        config_data["cuota"] = config[4]
        config_data["interest_rate"] = config[5]
        config_data["id"] = config[6]

        return config_data
