const axios = require('axios');
const baseUrl = process.env.BASE_URL;

async function getLoan (idLoan) {
    const endPointResource = 'loans/';
    const url = baseUrl + endPointResource + idLoan;

    const response = await axios.get(url, { transformResponse: [data => data] });
    return response.data;
};

async function getDebt (idDebt) {
    const endPointResource = 'debts/';
    const url = baseUrl + endPointResource + idDebt;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

async function getConfig (isConfig) {
    const endPointResource = 'configs/';
    const url = baseUrl + endPointResource + isConfig;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

async function getState (idState) {
    const endPointResource = 'states/';
    const url = baseUrl + endPointResource + idState;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

async function getModelDebtInfo (idLoan) {
    const endPointResource = 'model_debt_info/';
    const url = baseUrl + endPointResource + idLoan;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

async function getCollateralByLoanId (idLoan) {
    const endPointResource = 'collaterals?debt_id=' + idLoan;
    const url = baseUrl + endPointResource;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

async function getCollateralByEntryId (idEntry) {
    const endPointResource = 'collaterals/';
    const url = baseUrl + endPointResource + idEntry;

    const response = await axios.get(url, { transformResponse: [data => data] });

    return response.data;
};

module.exports = {
    getLoan: getLoan,
    getDebt: getDebt,
    getConfig: getConfig,
    getState: getState,
    getModelDebtInfo: getModelDebtInfo,
    getCollateralByLoanId: getCollateralByLoanId,
    getCollateralByEntryId: getCollateralByEntryId,
};
