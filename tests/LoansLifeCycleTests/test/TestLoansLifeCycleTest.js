
const TestToken = artifacts.require('./utils/test/TestToken.sol');
const LoanManager = artifacts.require('./diaspore/LoanManager.sol');
const DebtEngine = artifacts.require('./diaspore/DebtEngine.sol');
const InstallmentsModel = artifacts.require('./diaspore/model/InstallmentsModel');

const api = require('./api.js');
const helper = require('./Helper.js');
const loanHelper = require('./LoanHelper.js');

contract('Loans Life Cycle Tests', async accounts => {
    // Global instances variables
    let rcnToken;
    let debtEngine;
    let loanManager;
    let installmentModel;
    let saltValue = 100;

    // Static Contract Addresses for backend
    const rcnTokenAddress = '0xe5EA9D03D391d86933277c69ce6d2c3f073c4819';
    const debtEngineAddress = '0xdC8Dd86b3337A8EB4B1955DfF4B79676c9A40991';
    const loanManagerAddress = '0x275b0DC17674e02a8a434689A638E98D9aCd417a';
    const installmentModelAddress = '0xf1d88d1a22AD6D4A56137761e8df4aa68eDa3A11';

    // mnemonic used to create accounts
    // "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"
    // command: ganache-cli -m "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"

    // Accounts
    // const creatorPrivateKey = '0xaf080fd098ca962cc4778758dab7b88b4692afa18a613e7a93b77f8667207dd1';
    const creatorAddress = '0x1B274E25A1B02D77f8de7550daFf58C07A0D12c8';

    // const borrowerPrivateKey = '0x9cd9fa19cb2d594f41aa1e89bc6ca3ee8998d405b4f7d096e366fcb59743c277';
    const borrowerAddress = '0x3FaD5afc06e263Ad2E73E82C98377739E746eF15';

    // const lenderPrivateKey = '0xda06412214b4901dc170f99a3b51cc36b485bb92d688a449de94638117978c56';
    const lenderAddress = '0xa4D49A5e03c6cEEa80eCC48fBF92835AFd4C37e1';

    // const newLenderPrivateKey = '0x1ac6294ae9975943a1917d49d967db683a5755237c626658530a52f2f61209e1';
    const newLenderAddress = '0x060a109b32d70e58e39376516b2f97E9346939a9';

    function sleep (millis) {
        return new Promise(resolve => setTimeout(resolve, millis));
    }

    before('Create Token, Debt Engine , Loan Manager and Model instances', async function () {
        // Create contracts (Token RCN , Debt Engine, Loan Manager, Installments Model) and set engine in model
        rcnToken = await TestToken.new();
        debtEngine = await DebtEngine.new(rcnToken.address);
        loanManager = await LoanManager.new(debtEngine.address);
        installmentModel = await InstallmentsModel.new();
        await installmentModel.setEngine(debtEngine.address);
    });

    describe('Use Static contracts', function () {
        it(' Should use the defined contracs Addresses  ', async () => {
            assert.equal(rcnToken.address, rcnTokenAddress);
            assert.equal(debtEngine.address, debtEngineAddress);
            assert.equal(loanManager.address, loanManagerAddress);
            assert.equal(installmentModel.address, installmentModelAddress);
        });
    });

    // FLUJO 1 - REQUEST

    describe('Flujo 1: REQUEST LOAN', function () {
        it('should create a new loan Request ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;
            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);

            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);
        });
    });

    // FLUJO 2 - REQUEST + APPROVE
    describe('Flujo 2: REQUEST AND APPROVE LOAN', function () {
        it('should create a new loan Request and approve the request by the borrower ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });
            await sleep(5000);

            loanHelper.checkApprove(loanManager, id);
        });
    });

    // FLUJO 3 - REQUEST + APPROVE + LEND

    describe('Flujo 3: REQUEST + APPROVE + LEND', function () {
        it('should create a new loan Request and approve and lend ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });
            await sleep(5000);

            await loanHelper.checkApprove(loanManager, id);

            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );
            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);
        });
    });

    // FLUJO 4 - REQUEST  + APPROVE + LEND + PAY

    describe('Flujo 4: REQUEST  + APPROVE + LEND + PAY', function () {
        it('should create a new loan Request, approve and lend ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });

            await sleep(5000);
            await loanHelper.checkApprove(loanManager, id);

            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );

            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);

            // Pay loan
            await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
            await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

            await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });
            // Test pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);
        });
    });

    // FLUJO 5 - REQUEST  + APPROVE + CANCEL

    describe('Flujo 5: REQUEST  + APPROVE + CANCEL', function () {
        it('should create a new loan Request, approve and cancel ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });

            await sleep(5000);
            await loanHelper.checkApprove(loanManager, id);

            await loanManager.cancel(id, { from: creatorAddress });

            await sleep(5000);

            await loanHelper.checkCancel(id);
        });
    });

    // FLUJO 6 - REQUEST  + APPROVE + LEND + TOTALPAY

    describe('Flujo 6: REQUEST  + APPROVE + LEND + TOTALPAY', function () {
        it('should create a new loan Request, approve, lend, total pay ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });

            await sleep(5000);
            await loanHelper.checkApprove(loanManager, id);

            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );

            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);

            // Pay loan
            await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
            await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

            await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });

            // Test pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);

            // Pay total
            await debtEngine.pay(id, web3.utils.toWei('20', 'ether'), borrowerAddress, [], { from: borrowerAddress });

            // Test pay, test total pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);
            const loanApi4 = (await api.getLoan(id)).content;
            const debtApi4 = (await api.getDebt(id)).content;

            assert.equal(loanApi4.status, await loanManager.getStatus(id), 'Status payed');
            assert.isAtLeast(parseInt(debtApi4.balance), parseInt(loanApi4.amount), 'balance >= amount');
            assert.equal(parseInt(debtApi4.balance), parseInt(loanApi4.descriptor.total_obligation), 'balance eq descriptor total_obligation');
        });
    });

    // FLUJO 7 - REQUEST  + APPROVE + LEND + TRANSFER

    describe('Flujo 7: REQUEST  + APPROVE + LEND + TRANSFER', function () {
        it('should create a new loan Request, approve, lend and transfer ', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });

            await sleep(5000);
            await loanHelper.checkApprove(loanManager, id);

            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );

            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);

            // Transfer debt
            await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });

            await sleep(5000);
            await loanHelper.checkTransfer(loanManager, debtEngine, newLenderAddress, lenderAddress, id);
        });
    });

    // FLUJO 8 - REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW

    describe('Flujo 8: REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW', function () {
        it('should create a new loan Request, approve, lend, total pay and withdraw', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await loanManager.approveRequest(id, { from: borrowerAddress });
            await sleep(5000);

            await loanHelper.checkApprove(loanManager, id);

            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );
            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);

            // Pay loan
            await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
            await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

            await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });

            // Test pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);

            // Pay total
            await debtEngine.pay(id, web3.utils.toWei('20', 'ether'), borrowerAddress, [], { from: borrowerAddress });

            // Test pay, test total pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);
            const loanApi4 = (await api.getLoan(id)).content;
            const debtApi4 = (await api.getDebt(id)).content;

            assert.equal(loanApi4.status, await loanManager.getStatus(id), 'Status payed');
            assert.isAtLeast(parseInt(debtApi4.balance), parseInt(loanApi4.amount), 'balance >= amount');
            assert.equal(parseInt(debtApi4.balance), parseInt(loanApi4.descriptor.total_obligation), 'balance eq descriptor total_obligation');

            // withdraw
            const balanceLenderBeforeWithdraw = await rcnToken.balanceOf(lenderAddress);
            await debtEngine.withdrawPartial(id, lenderAddress, web3.utils.toWei('120', 'ether'), { from: lenderAddress });
            await sleep(5000);
            await loanHelper.checkWithdraw(debtEngine, rcnToken, lenderAddress, id, balanceLenderBeforeWithdraw);
        });
    });

    // FLUJO 9 - EXPIRED

    describe('Flujo 9: REQUEST LOAN EXPIRED', function () {
        it('should check if a loan is expired ', async () => {
            const delta = 2;
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            const amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = (await helper.getBlockTime()) + delta;
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            const id = result.id;
            const loanData = result.loanData;

            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);
            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);

            await helper.increaseTime(5);

            await loanManager.approveRequest(id, { from: borrowerAddress });

            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            let error;
            try {
                await loanManager.lend(
                    id,
                    [],
                    '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                    '0', // Cosigner limit
                    [],                 // Cosigner data
                    [],                 // Callback data
                    { from: lenderAddress }
                );
                error = false;
            } catch (e) {
                error = true;
            }
            assert.isTrue(error, 'lend expired');
        });
    });

    // E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW

    describe(' E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW', function () {
        // CREATE A REQUEST
        let id;
        let amount;

        it('should create a new loan Request', async () => {
            const cuota = '10000000000000000000';
            const punInterestRate = '1555200000000';
            const installments = '12';
            const duration = '2592000';
            const timeUnit = '2592000';
            amount = '100000000000000000000';
            const oracle = '0x0000000000000000000000000000000000000000';
            const callback = '0x0000000000000000000000000000000000000000';
            const expiration = '1578571215';

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, callback, expiration);
            id = result.id;
            const loanData = result.loanData;
            // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
            await sleep(5000);

            await loanHelper.checkRequestLoan(loanManager, installmentModel, id, loanData);
        });

        // APPROVE

        it('should approve the loan request by the borrower', async () => {
            await loanManager.approveRequest(id, { from: borrowerAddress });
            await sleep(5000);

            loanHelper.checkApprove(loanManager, id);
        });

        // LEND

        it('should lend', async () => {
            const loanEthBeforeLend = await loanManager.requests(id);
            // buy Rcn for lender address
            await rcnToken.setBalance(lenderAddress, amount);

            await rcnToken.balanceOf(lenderAddress);

            await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

            await loanManager.lend(
                id,                 // Index
                [],                 // OracleData
                '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
                '0', // Cosigner limit
                [],                 // Cosigner data
                [],                 // Callback data
                { from: lenderAddress }    // Owner/Lender
            );
            await sleep(5000);
            await loanHelper.checkLend(loanManager, debtEngine, installmentModel, loanEthBeforeLend, id);
        });

        // TRANSFER DEBT

        it('should transfer the lender debt to another address', async () => {
            // Transfer debt
            await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });

            await sleep(5000);
            await loanHelper.checkTransfer(loanManager, debtEngine, newLenderAddress, lenderAddress, id);
        });

        // TOTAL PAY

        it('should pay the total of the debt', async () => {
            // Pay loan
            await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
            await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

            await debtEngine.pay(id, web3.utils.toWei('120', 'ether'), borrowerAddress, [], { from: borrowerAddress });
            // Test pay
            await sleep(5000);
            await loanHelper.checkPay(loanManager, debtEngine, installmentModel, id);
        });

        // WITHDRAW

        it('should withdraw funds for lender', async () => {
            // withdraw
            const balanceLenderBeforeWithdraw = await rcnToken.balanceOf(newLenderAddress);
            await debtEngine.withdrawPartial(id, newLenderAddress, web3.utils.toWei('120', 'ether'), { from: newLenderAddress });
            await sleep(5000);
            await loanHelper.checkWithdraw(debtEngine, rcnToken, newLenderAddress, id, balanceLenderBeforeWithdraw);
        });
    });
});
