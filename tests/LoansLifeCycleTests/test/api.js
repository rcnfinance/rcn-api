const axios = require('axios');
const baseUrl = process.env.BASE_URL;

module.exports.getLoan = async (idLoan) => {
  const endpointResource = 'loans/';
  return this.get(endpointResource + idLoan);
};

module.exports.getDebt = async (idDebt) => {
  const endpointResource = 'debts/';
  return this.get(endpointResource + idDebt);
};

module.exports.getConfig = async (idLoan) => {
  const endpointResource = 'configs/';
  return this.get(endpointResource + idLoan);
};

module.exports.getState = async (idLoan) => {
  const endpointResource = 'states/';
  return this.get(endpointResource + idLoan);
};

module.exports.getModelDebtInfo = async (idLoan) => {
  const endpointResource = 'model_debt_info/';
  return this.get(endpointResource + idLoan);
};

module.exports.get = async (endpointResource) => {
  const response = await axios.get(baseUrl + endpointResource);
  return response.data;
};
