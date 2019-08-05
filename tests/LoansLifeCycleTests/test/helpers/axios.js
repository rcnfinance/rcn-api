// axios.js
const axios = require('axios');
const JSONBigInt = require('json-bigint');
// Add a request interceptor
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    // console.log(config);
    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
});

// Add a response interceptor
axios.interceptors.response.use(function (response) {
    response.data = JSONBigInt.parse(response.data);

    return response;
}, function (error) {
    // Do something with response error
    return Promise.reject(error);
});

module.exports = axios;
