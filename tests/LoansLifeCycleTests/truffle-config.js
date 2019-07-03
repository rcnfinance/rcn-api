module.exports = {
  compilers: {
    solc: {
      version: '0.5.6',
      docker: false,
      settings: {
        optimizer: {
          enabled: true,
          runs: 200,
        },
        evmVersion: 'constantinople',
      },
    },
  },
  networks: {
    development: {
      host: 'ganachecli',
      port: 8545,
      network_id: '*', // eslint-disable-line camelcase
      from: '0x1B274E25A1B02D77f8de7550daFf58C07A0D12c8',
    },
  },
};
