import utils


class InstallmentsModelInterface():
    def __init__(self, contract_connection):
        self.contract = contract_connection

    def get_config_by_id(self, id_):
        config = self.contract.contract.functions.configs(id_).call()

        config_data = dict()
        config_data["installments"] = str(config[0])
        config_data["time_unit"] = str(config[1])
        config_data["duration"] = str(config[2])
        config_data["lent_time"] = str(config[3])
        config_data["cuota"] = str(config[4])
        config_data["interest_rate"] = str(config[5])
        config_data["id"] = utils.add_0x_prefix(config[6].hex())

        return config_data
