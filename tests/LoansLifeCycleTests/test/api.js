const axios = require("axios");
const base_url = process.env.BASE_URL;

async function get_loan(id_loan) {
    const endpoint_resource = "loans/";
    const url = base_url + endpoint_resource + id_loan;
    
    response = await axios.get(url);
    return response.data;
};

async function get_debt(id_debt) {
    const endpoint_resource = "debts/"
    const url = base_url + endpoint_resource + id_debt;

    response = await axios.get(url);

    return response.data;
};

async function get_config(id_config) {
    const endpoint_resource = "configs/"
    const url = base_url + endpoint_resource + id_config;

    response = await axios.get(url);

    return response.data;
};

async function get_state(id_state) {
    const endpoint_resource = "states/"
    const url = base_url + endpoint_resource + id_state;

    response = await axios.get(url);

    return response.data;
};

async function get_model_debt_info(id_loan) {
    const endpoint_resource = "model_debt_info/"
    const url = base_url + endpoint_resource + id_loan;

    response = await axios.get(url);

    return response.data;
};

module.exports = {
  get_loan: get_loan,
  get_debt: get_debt,
  get_config: get_config,
  get_state: get_state,
  get_model_debt_info: get_model_debt_info
};
