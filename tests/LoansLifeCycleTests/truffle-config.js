module.exports = {
    compilers: {
        solc: {
            version: '0.5.10',
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
    dependencies: {
        'axios': '^0.18.0',
        'chai': '^4.2.0',
        'bn-chai': '^1.0.1',
        'solc': '0.5.8',
    },

};
