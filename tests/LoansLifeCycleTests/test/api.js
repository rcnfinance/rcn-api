const axios = require("axios");
const base_url = process.env.BASE_URL;

module.exports.get_loan = async (id_loan) => {
    const endpoint_resource = "loans/";
    const url = base_url + endpoint_resource + id_loan;

    response = await axios.get(url);
    return response.data;
};

module.exports.get_debt = async (id_loan) => {
    const endpoint_resource = "debts/"
    const url = base_url + endpoint_resource + id_debt;

    response = await axios.get(url);

    return response.data;
};

module.exports.get_config = async (id_loan) => {
    const endpoint_resource = "configs/"
    const url = base_url + endpoint_resource + id_config;

    response = await axios.get(url);

    return response.data;
};

module.exports.get_state = async (id_loan) => {
    const endpoint_resource = "states/"
    const url = base_url + endpoint_resource + id_state;

    response = await axios.get(url);

    return response.data;
};

module.exports.get_model_debt_info = async (id_loan) => {
    const endpoint_resource = "model_debt_info/"
    const url = base_url + endpoint_resource + id_loan;

    response = await axios.get(url);

    return response.data;
};
