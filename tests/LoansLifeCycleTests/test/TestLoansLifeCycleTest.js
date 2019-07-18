const mochaSteps = require('mocha-steps');

const TestToken = artifacts.require('./utils/test/TestToken.sol');
const LoanManager = artifacts.require('./diaspore/LoanManager.sol');
const DebtEngine = artifacts.require('./diaspore/DebtEngine.sol');
const InstallmentsModel = artifacts.require('./diaspore/model/InstallmentsModel');

const BN = web3.utils.BN;
const expect = require('chai')
    .use(require('bn-chai')(BN))
    .expect;

const api = require('./api.js');
const helper = require('./Helper.js');
const loanHelper = require('./LoanHelper.js');

function bn (number) {
    return new BN(number);
}

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
    const creatorPrivateKey = '0xaf080fd098ca962cc4778758dab7b88b4692afa18a613e7a93b77f8667207dd1';
    const creatorAddress = '0x1B274E25A1B02D77f8de7550daFf58C07A0D12c8';

    const borrowerPrivateKey = '0x9cd9fa19cb2d594f41aa1e89bc6ca3ee8998d405b4f7d096e366fcb59743c277';
    const borrowerAddress = '0x3FaD5afc06e263Ad2E73E82C98377739E746eF15';

    const lenderPrivateKey = '0xda06412214b4901dc170f99a3b51cc36b485bb92d688a449de94638117978c56';
    const lenderAddress = '0xa4D49A5e03c6cEEa80eCC48fBF92835AFd4C37e1';

    const newLenderPrivateKey = '0x1ac6294ae9975943a1917d49d967db683a5755237c626658530a52f2f61209e1';
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
            const expiration = '1578571215';

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
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
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
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
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
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
            const expiration = '1578571215';
            ++saltValue;

            // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
            const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
                cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
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

    // // FLUJO 5 - REQUEST  + APPROVE + CANCEL

    // describe('Flujo 5: REQUEST  + APPROVE + CANCEL', function () {
    //     it('should create a new loan Request, approve and cancel ', async () => {
    //         const cuota = '10000000000000000000';
    //         const punInterestRate = '1555200000000';
    //         const installments = '12';
    //         const duration = '2592000';
    //         const timeUnit = '2592000';
    //         const amount = '100000000000000000000';
    //         const oracle = '0x0000000000000000000000000000000000000000';
    //         const expiration = '1578571215';
    //         ++saltValue;

    //         // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
    //         const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
    //             cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
    //         const id = result.id;
    //         const loanData = result.loanData;

    //         // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
    //         await sleep(5000);
    //         // Query the API for Loan data
    //         const loanApi = (await api.get_loan(id)).content;
    //         const loanEth = await loanManager.requests(id);
    //         // check loan data
    //         const keysTocheck = ['open', 'model', 'borrower', 'creator', 'oracle', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
    //         helper.check_loan(loanEth, loanApi, keysTocheck);

    //         // get descriptor Values from InstallmentModel
    //         const simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
    //         const totalObligation = await installmentModel.simTotalObligation(loanData);
    //         const loanDuration = await installmentModel.simDuration(loanData);
    //         const durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
    //         const interestRate = (durationPercentage * 360 * 86000) / loanDuration;
    //         const frequency = await installmentModel.simFrequency(loanData);
    //         const loanInstallments = await installmentModel.simInstallments(loanData);

    //         assert.equal(loanApi.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
    //         assert.equal(loanApi.descriptor.total_obligation, totalObligation);
    //         assert.equal(loanApi.descriptor.duration, loanDuration);
    //         assert.equal(loanApi.descriptor.interest_rate, interestRate);
    //         assert.equal(loanApi.descriptor.frequency, frequency);
    //         assert.equal(loanApi.descriptor.installments, loanInstallments);

    //         assert.equal(loanApi.lender, null);

    //         await loanManager.approveRequest(id, { from: borrowerAddress });

    //         await sleep(5000);

    //         const loanApi2 = (await api.get_loan(id)).content;
    //         const loanEth2 = await loanManager.requests(id);

    //         const keysTocheck2 = ['approved'];
    //         helper.check_loan(loanEth2, loanApi2, keysTocheck2);

    //         await loanManager.cancel(id, { from: creatorAddress });

    //         await sleep(5000);

    //         const loanApi3 = (await api.get_loan(id)).content;
    //         assert.isTrue(loanApi3.approved, 'loan approved');
    //         assert.isTrue(loanApi3.canceled, 'loan canceled');

    //         let debtExists;
    //         try {
    //             await api.get_debt(id);
    //             debtExists = true;
    //         } catch (error) {
    //             debtExists = false;
    //         } finally {
    //             assert.isFalse(debtExists, 'debt dot exists :)');
    //         }
    //     });
    // });

    // // FLUJO 6 - REQUEST  + APPROVE + LEND + TOTALPAY

    // describe('Flujo 6: REQUEST  + APPROVE + LEND + TOTALPAY', function () {
    //     it('should create a new loan Request, approve, lend, total pay ', async () => {
    //         const cuota = '10000000000000000000';
    //         const punInterestRate = '1555200000000';
    //         const installments = '12';
    //         const duration = '2592000';
    //         const timeUnit = '2592000';
    //         const amount = '100000000000000000000';
    //         const oracle = '0x0000000000000000000000000000000000000000';
    //         const expiration = '1578571215';
    //         ++saltValue;

    //         // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
    //         const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
    //             cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
    //         const id = result.id;
    //         const loanData = result.loanData;

    //         // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
    //         await sleep(5000);
    //         // Query the API for Loan data
    //         const loanApi = (await api.get_loan(id)).content;
    //         const loanEth = await loanManager.requests(id);
    //         // check loan data
    //         const keysToCheck = ['open', 'model', 'borrower', 'creator', 'oracle', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
    //         helper.check_loan(loanEth, loanApi, keysToCheck);

    //         // get descriptor Values from InstallmentModel
    //         const simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
    //         const totalObligation = await installmentModel.simTotalObligation(loanData);
    //         const loanDuration = await installmentModel.simDuration(loanData);
    //         const durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
    //         const interestRate = (durationPercentage * 360 * 86000) / loanDuration;
    //         const frequency = await installmentModel.simFrequency(loanData);
    //         const loanInstallments = await installmentModel.simInstallments(loanData);

    //         assert.equal(loanApi.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
    //         assert.equal(loanApi.descriptor.total_obligation, totalObligation);
    //         assert.equal(loanApi.descriptor.duration, loanDuration);
    //         assert.equal(loanApi.descriptor.interest_rate, interestRate);
    //         assert.equal(loanApi.descriptor.frequency, frequency);
    //         assert.equal(loanApi.descriptor.installments, loanInstallments);

    //         assert.equal(loanApi.lender, null);

    //         await loanManager.approveRequest(id, { from: borrowerAddress });

    //         await sleep(5000);
    //         const loanApi2 = (await api.get_loan(id)).content;
    //         const loanEthBeforeLend = await loanManager.requests(id);

    //         const keysToCheck2 = ['approved'];
    //         helper.check_loan(loanEthBeforeLend, loanApi2, keysToCheck2);

    //         // buy Rcn for lender address
    //         await rcnToken.setBalance(lenderAddress, amount);

    //         await rcnToken.balanceOf(lenderAddress);

    //         await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

    //         await loanManager.lend(
    //             id,                 // Index
    //             [],                 // OracleData
    //             '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
    //             '0', // Cosigner limit
    //             [],                 // Cosigner data
    //             { from: lenderAddress }    // Owner/Lender
    //         );

    //         await sleep(5000);
    //         const loanApi3 = (await api.get_loan(id)).content;

    //         // Query the API for Debt data
    //         const debtApi = (await api.get_debt(id)).content;
    //         const debtEth = await debtEngine.debts(id);

    //         const modelInfo = await api.get_model_debt_info(id);

    //         // Query the API for config data
    //         const configApi = (await api.get_config(id)).content;
    //         const configEth = await installmentModel.configs(id);

    //         // Query the API for state data
    //         const stateApi = (await api.get_state(id)).content;
    //         const stateEth = await installmentModel.states(id);

    //         // call check_status functions
    //         await helper.check_state(stateEth, stateApi);
    //         await helper.check_config(configEth, configApi);
    //         await helper.check_debt(debtEth, debtApi);
    //         const keysToCheck3 = ['approved', 'expiration', 'amount', 'cosigner', 'model', 'creator', 'oracle', 'borrower', 'loanData'];
    //         await helper.check_loan(loanEthBeforeLend, loanApi3, keysToCheck3);

    //         // check model_info.due_time
    //         const dueTime = await loanManager.getDueTime(id);
    //         assert.equal(dueTime, modelInfo.due_time, 'installments_due_time eq model_info.due_time');

    //         // check model_info.balance
    //         assert.equal(parseInt(debtEth.balance), modelInfo.debt_balance, 'debtETH.balance eq model_info.balance');

    //         // estimated_obligation
    //         const estimatedObligationApi = modelInfo.estimated_obligation;
    //         const EstimatedObligationEth = await installmentModel.getEstimateObligation(id);
    //         assert.equal(estimatedObligationApi, EstimatedObligationEth, 'estimated obligation eq');

    //         // next_obligation
    //         const nextObligationApi = modelInfo.next_obligation;
    //         const nextObligationEth = await installmentModel.getObligation(id, dueTime);
    //         assert.equal(nextObligationApi, nextObligationEth[0], 'next_obligation');

    //         // current_obligation
    //         const now = parseInt(Date.now() / 1000);
    //         const currentObligationApi = modelInfo.current_obligation;
    //         const currentObligationEth = await installmentModel.getObligation(id, now);
    //         assert.equal(currentObligationApi, currentObligationEth[0], 'currentObligation');

    //         // Pay loan
    //         await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
    //         await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

    //         await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });

    //         // Test pay
    //         await sleep(5000);
    //         const debtApi2 = (await api.get_debt(id)).content;
    //         const debtEth2 = await debtEngine.debts(id);

    //         const stateApi2 = (await api.get_state(id)).content;
    //         const stateEth2 = await installmentModel.states(id);

    //         const configApi2 = (await api.get_config(id)).content;
    //         const configEth2 = await installmentModel.configs(id);

    //         const modelInfo2 = await api.get_model_debt_info(id);

    //         assert.equal(debtEth2.balance, debtApi2.balance, 'DEBT Balance not eq :(');
    //         assert.equal(stateEth2.paid, stateApi2.paid, 'State paid not eq :(');

    //         helper.check_debt(debtEth2, debtApi2);
    //         helper.check_state(stateEth2, stateApi2);
    //         helper.check_config(configEth2, configApi2);

    //         // check model_info
    //         // check model_info.due_time
    //         const dueTime2 = await loanManager.getDueTime(id);
    //         assert.equal(dueTime2, modelInfo2.due_time, 'installments_due_time eq model_info.due_time');

    //         // check model_info.balance
    //         assert.equal(parseInt(debtEth2.balance), modelInfo2.debt_balance, 'debtETH.balance eq model_info.balance');

    //         // estimated_obligation
    //         const estimatedObligationApi2 = modelInfo2.estimated_obligation;
    //         const EstimatedObligationEth2 = await installmentModel.getEstimateObligation(id);
    //         assert.equal(estimatedObligationApi2, EstimatedObligationEth2, 'estimated obligation eq');

    //         // next_obligation
    //         const nextObligationApi2 = modelInfo2.next_obligation;
    //         const nextObligationEth2 = await installmentModel.getObligation(id, dueTime2);
    //         assert.equal(nextObligationApi2, nextObligationEth2[0], 'next_obligation');

    //         // current_obligation
    //         const now2 = parseInt(Date.now() / 1000);
    //         const currentObligationApi2 = modelInfo2.current_obligation;
    //         const currentObligationEth2 = await installmentModel.getObligation(id, now2);
    //         assert.equal(currentObligationApi2, currentObligationEth2[0], 'currentObligation');

    //         // Test pay, test total pay
    //         await debtEngine.pay(id, web3.utils.toWei('20', 'ether'), borrowerAddress, [], { from: borrowerAddress });

    //         await sleep(5000);
    //         const loanApi4 = (await api.get_loan(id)).content;
    //         const debtApi4 = (await api.get_debt(id)).content;
    //         const stateApi4 = (await api.get_state(id)).content;
    //         const debtEth4 = await debtEngine.debts(id);
    //         const stateEth4 = await installmentModel.states(id);

    //         assert.equal(debtEth4.balance, debtApi4.balance, 'DEBT Balance not eq :(');
    //         assert.equal(stateEth4.paid, stateApi4.paid, 'State paid not eq :(');
    //         assert.equal(loanApi4.status, await loanManager.getStatus(id), 'Status payed');
    //         assert.isAtLeast(parseInt(debtApi4.balance), parseInt(loanApi4.amount), 'balance >= amount');
    //         assert.equal(parseInt(debtApi4.balance), parseInt(loanApi4.descriptor.total_obligation), 'balance eq descriptor total_obligation');
    //     });
    // });

    // // FLUJO 7 - REQUEST  + APPROVE + LEND + TRANSFER

    // describe('Flujo 7: REQUEST  + APPROVE + LEND + TRANSFER', function () {
    //     it('should create a new loan Request, approve, lend and transfer ', async () => {
    //         const cuota = '10000000000000000000';
    //         const punInterestRate = '1555200000000';
    //         const installments = '12';
    //         const duration = '2592000';
    //         const timeUnit = '2592000';
    //         const amount = '100000000000000000000';
    //         const oracle = '0x0000000000000000000000000000000000000000';
    //         const expiration = '1578571215';
    //         ++saltValue;

    //         // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
    //         const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
    //             cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
    //         const id = result.id;
    //         const loanData = result.loanData;

    //         // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
    //         await sleep(5000);
    //         // Query the API for Loan data
    //         const loanApi = (await api.get_loan(id)).content;
    //         const loanEth = await loanManager.requests(id);
    //         // check loan data
    //         const keysToCheck = ['open', 'model', 'borrower', 'creator', 'oracle', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
    //         helper.check_loan(loanEth, loanApi, keysToCheck);

    //         // get descriptor Values from InstallmentModel
    //         const simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
    //         const totalObligation = await installmentModel.simTotalObligation(loanData);
    //         const loanDuration = await installmentModel.simDuration(loanData);
    //         const durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
    //         const interestRate = (durationPercentage * 360 * 86000) / loanDuration;
    //         const frequency = await installmentModel.simFrequency(loanData);
    //         const loanInstallments = await installmentModel.simInstallments(loanData);

    //         assert.equal(loanApi.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
    //         assert.equal(loanApi.descriptor.total_obligation, totalObligation);
    //         assert.equal(loanApi.descriptor.duration, loanDuration);
    //         assert.equal(loanApi.descriptor.interest_rate, interestRate);
    //         assert.equal(loanApi.descriptor.frequency, frequency);
    //         assert.equal(loanApi.descriptor.installments, loanInstallments);

    //         assert.equal(loanApi.lender, null);

    //         await loanManager.approveRequest(id, { from: borrowerAddress });

    //         await sleep(5000);
    //         const loanApi2 = (await api.get_loan(id)).content;
    //         const loanEthBeforeLend = await loanManager.requests(id);

    //         const keysToCheck2 = ['approved'];
    //         helper.check_loan(loanEthBeforeLend, loanApi2, keysToCheck2);

    //         // buy Rcn for lender address
    //         await rcnToken.setBalance(lenderAddress, amount);

    //         await rcnToken.balanceOf(lenderAddress);

    //         await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

    //         await loanManager.lend(
    //             id,                 // Index
    //             [],                 // OracleData
    //             '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
    //             '0', // Cosigner limit
    //             [],                 // Cosigner data
    //             { from: lenderAddress }    // Owner/Lender
    //         );

    //         await sleep(5000);
    //         const loanApi3 = (await api.get_loan(id)).content;

    //         // Query the API for Debt data
    //         const debtApi = (await api.get_debt(id)).content;
    //         const debtEth = await debtEngine.debts(id);

    //         const modelInfo = await api.get_model_debt_info(id);

    //         // Query the API for config data
    //         const configApi = (await api.get_config(id)).content;
    //         const configEth = await installmentModel.configs(id);

    //         // Query the API for state data
    //         const stateApi = (await api.get_state(id)).content;
    //         const stateEth = await installmentModel.states(id);

    //         // call check_status functions
    //         await helper.check_state(stateEth, stateApi);
    //         await helper.check_config(configEth, configApi);
    //         await helper.check_debt(debtEth, debtApi);
    //         const keysToCheck3 = ['approved', 'expiration', 'amount', 'cosigner', 'model', 'creator', 'oracle', 'borrower', 'loanData'];
    //         await helper.check_loan(loanEthBeforeLend, loanApi3, keysToCheck3);

    //         // check model_info.due_time
    //         const dueTime = await loanManager.getDueTime(id);
    //         assert.equal(dueTime, modelInfo.due_time, 'installments_due_time eq model_info.due_time');

    //         // check model_info.balance
    //         assert.equal(parseInt(debtEth.balance), modelInfo.debt_balance, 'debtETH.balance eq model_info.balance');

    //         // estimated_obligation
    //         const estimatedObligationApi = modelInfo.estimated_obligation;
    //         const EstimatedObligationEth = await installmentModel.getEstimateObligation(id);
    //         assert.equal(estimatedObligationApi, EstimatedObligationEth, 'estimated obligation eq');

    //         // next_obligation
    //         const nextObligationApi = modelInfo.next_obligation;
    //         const nextObligationEth = await installmentModel.getObligation(id, dueTime);
    //         assert.equal(nextObligationApi, nextObligationEth[0], 'next_obligation');

    //         // current_obligation
    //         const now = parseInt(Date.now() / 1000);
    //         const currentObligationApi = modelInfo.current_obligation;
    //         const currentObligationEth = await installmentModel.getObligation(id, now);
    //         assert.equal(currentObligationApi, currentObligationEth[0], 'currentObligation');

    //         // Transfer debt
    //         await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });

    //         assert.equal(newLenderAddress, await loanManager.ownerOf(id));

    //         await sleep(5000);
    //         const loanJsonAfterTransfer = await api.get_loan(id);
    //         const loanAfterTransfer = loanJsonAfterTransfer.content;

    //         assert.equal(newLenderAddress, loanAfterTransfer.lender);

    //         // Should not be able to transfer if the sender is not the owner of the debt
    //         let error;
    //         try {
    //             error = await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });
    //         } catch (e) {
    //             error = 'Not the owner of the debt';
    //         }
    //         assert.equal(error, 'Not the owner of the debt');
    //     });
    // });

    // FLUJO 8 - REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW

    // describe('Flujo 8: REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW', function () {
    //     it('should create a new loan Request, approve, lend, total pay and withdraw', async () => {
    //         const cuota = '10000000000000000000';
    //         const punInterestRate = '1555200000000';
    //         const installments = '12';
    //         const duration = '2592000';
    //         const timeUnit = '2592000';
    //         const amount = '100000000000000000000';
    //         const oracle = '0x0000000000000000000000000000000000000000';
    //         const expiration = '1578571215';
    //         ++saltValue;

    //         // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
    //         const result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
    //             cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
    //         const id = result.id;
    //         const loanData = result.loanData;

    //         // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
    //         await sleep(5000);
    //         // Query the API for Loan data
    //         const loanApi = (await api.get_loan(id)).content;
    //         const loanEth = await loanManager.requests(id);
    //         // check loan data
    //         const keysToCheck = ['open', 'model', 'borrower', 'creator', 'oracle', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
    //         helper.check_loan(loanEth, loanApi, keysToCheck);

    //         // get descriptor Values from InstallmentModel
    //         const simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
    //         const totalObligation = await installmentModel.simTotalObligation(loanData);
    //         const loanDuration = await installmentModel.simDuration(loanData);
    //         const durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
    //         const interestRate = (durationPercentage * 360 * 86000) / loanDuration;
    //         const frequency = await installmentModel.simFrequency(loanData);
    //         const loanInstallments = await installmentModel.simInstallments(loanData);

    //         assert.equal(loanApi.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
    //         assert.equal(loanApi.descriptor.total_obligation, totalObligation);
    //         assert.equal(loanApi.descriptor.duration, loanDuration);
    //         assert.equal(loanApi.descriptor.interest_rate, interestRate);
    //         assert.equal(loanApi.descriptor.frequency, frequency);
    //         assert.equal(loanApi.descriptor.installments, loanInstallments);

    //         assert.equal(loanApi.lender, null);

    //         await loanManager.approveRequest(id, { from: borrowerAddress });

    //         await sleep(5000);
    //         co = (await api.get_loan(id)).content;
    //         loan_eth_before_lend = await loanManager.requests(id);

    //         keys_to_check = ['approved'];
    //         helper.check_loan(loan_eth_before_lend, loan_api, keys_to_check);

    //         // buy Rcn for lender address
    //         await rcnToken.setBalance(lenderAddress, amount);

    //         balanceOfLender = await rcnToken.balanceOf(lenderAddress);

    //         await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

    //         await loanManager.lend(
    //             id,                 // Index
    //             [],                 // OracleData
    //             '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
    //             '0', // Cosigner limit
    //             [],                 // Cosigner data
    //             { from: lenderAddress }    // Owner/Lender
    //         );

    //         await sleep(5000);
    //         loan_api = (await api.get_loan(id)).content;

    //         // Query the API for Debt data
    //         debt_api = (await api.get_debt(id)).content;
    //         debt_eth = await debtEngine.debts(id);

    //         model_info = await api.get_model_debt_info(id);

    //         // Query the API for config data
    //         config_api = (await api.get_config(id)).content;
    //         config_eth = await installmentModel.configs(id);

    //         // Query the API for state data
    //         state_api = (await api.get_state(id)).content;
    //         state_eth = await installmentModel.states(id);

    //         // call check_status functions
    //         await helper.check_state(state_eth, state_api);
    //         await helper.check_config(config_eth, config_api);
    //         await helper.check_debt(debt_eth, debt_api);
    //         key_to_check = ['approved', 'expiration', 'amount', 'cosigner', 'model', 'creator', 'oracle', 'borrower', 'loanData'];
    //         await helper.check_loan(loan_eth_before_lend, loan_api, key_to_check);

    //         // check model_info.due_time
    //         due_time = await loanManager.getDueTime(id);
    //         assert.equal(due_time, model_info.due_time, 'installments_due_time eq model_info.due_time');

    //         // check model_info.balance
    //         assert.equal(parseInt(debt_eth.balance), model_info.debt_balance, 'debtETH.balance eq model_info.balance');

    //         // estimated_obligation
    //         estimated_obligation_api = model_info.estimated_obligation;
    //         estimated_obligation_eth = await installmentModel.getEstimateObligation(id);
    //         assert.equal(estimated_obligation_api, estimated_obligation_eth, 'estimated obligation eq');

    //         // next_obligation
    //         next_obligation_api = model_info.next_obligation;
    //         next_obligation_eth = await installmentModel.getObligation(id, due_time);
    //         assert.equal(next_obligation_api, next_obligation_eth[0], 'next_obligation');

    //         // current_obligation
    //         now = parseInt(Date.now() / 1000);
    //         current_obligation_api = model_info.current_obligation;
    //         current_obligation_eth = await installmentModel.getObligation(id, now);

    //         // Pay loan
    //         await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
    //         await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

    //         await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });
    //         // Test pay
    //         await sleep(5000);
    //         debt_api = (await api.get_debt(id)).content;
    //         debt_eth = await debtEngine.debts(id);

    //         state_api = (await api.get_state(id)).content;
    //         state_eth = await installmentModel.states(id);

    //         config_api = (await api.get_config(id)).content;
    //         config_eth = await installmentModel.configs(id);

    //         model_info = await api.get_model_debt_info(id);

    //         assert.equal(debt_eth.balance, debt_api.balance, 'DEBT Balance not eq :(');
    //         assert.equal(state_eth.paid, state_api.paid, 'State paid not eq :(');

    //         helper.check_debt(debt_eth, debt_api);
    //         helper.check_state(state_eth, state_api);
    //         helper.check_config(config_eth, config_api);

    //         // check model_info
    //         // check model_info.due_time
    //         due_time = await loanManager.getDueTime(id);
    //         assert.equal(due_time, model_info.due_time, 'installments_due_time eq model_info.due_time');

    //         // check model_info.balance
    //         assert.equal(parseInt(debt_eth.balance), model_info.debt_balance, 'debtETH.balance eq model_info.balance');

    //         // estimated_obligation
    //         estimated_obligation_api = model_info.estimated_obligation;
    //         estimated_obligation_eth = await installmentModel.getEstimateObligation(id);
    //         assert.equal(estimated_obligation_api, estimated_obligation_eth, 'estimated obligation eq');

    //         // next_obligation
    //         next_obligation_api = model_info.next_obligation;
    //         next_obligation_eth = await installmentModel.getObligation(id, due_time);
    //         assert.equal(next_obligation_api, next_obligation_eth[0], 'next_obligation');

    //         // current_obligation
    //         now = parseInt(Date.now() / 1000);
    //         current_obligation_api = model_info.current_obligation;
    //         current_obligation_eth = await installmentModel.getObligation(id, now);

    //         // Test pay, test total pay
    //         await debtEngine.pay(id, web3.utils.toWei('20', 'ether'), borrowerAddress, [], { from: borrowerAddress });

    //         await sleep(5000);
    //         loan_api = (await api.get_loan(id)).content;
    //         debt_api = (await api.get_debt(id)).content;
    //         state_api = (await api.get_state(id)).content;
    //         debt_eth = await debtEngine.debts(id);
    //         state_eth = await installmentModel.states(id);

    //         assert.equal(debt_eth.balance, debt_api.balance, 'DEBT Balance not eq :(');
    //         assert.equal(state_eth.paid, state_api.paid, 'State paid not eq :(');
    //         assert.equal(loan_api.status, await loanManager.getStatus(id), 'Status payed');
    //         assert.isAtLeast(parseInt(debt_api.balance), parseInt(loan_api.amount), 'balance >= amount');
    //         assert.equal(parseInt(debt_api.balance), parseInt(loan_api.descriptor.total_obligation), 'balance eq descriptor total_obligation');

    //         // withdraw
    //         balance_lender_before_withdraw = await rcnToken.balanceOf(lenderAddress);
    //         await debtEngine.withdrawPartial(id, lenderAddress, web3.utils.toWei('120', 'ether'), { from: lenderAddress });
    //         await sleep(5000);

    //         debt_api = (await api.get_debt(id)).content;
    //         debt_eth = await debtEngine.debts(id);

    //         balance_lender_after_withdraw = parseInt(await rcnToken.balanceOf(lenderAddress));
    //         total_balance = balance_lender_before_withdraw + parseInt(web3.utils.toWei('120', 'ether'));

    //         assert.equal(parseInt(debt_api.balance), parseInt(debt_eth.balance), 'balance eq');
    //         assert.equal(total_balance, balance_lender_after_withdraw, 'balance lender eq');
    //     });
    // });

//     // FLUJO 9 - EXPIRED

//     describe('Flujo 9: REQUEST LOAN EXPIRED', function () {
//         it('should check if a loan is expired ', async () => {
//             delta = 2;
//             cuota = '10000000000000000000';
//             punInterestRate = '1555200000000';
//             installments = '12';
//             duration = '2592000';
//             timeUnit = '2592000';
//             amount = '100000000000000000000';
//             oracle = '0x0000000000000000000000000000000000000000';
//             expiration = (await helper.getBlockTime()) + delta;
//             ++saltValue;

//             // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
//             result = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
//                 cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
//             id = result.id;
//             loanData = result.loanData;

//             // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
//             await sleep(5000);
//             // Query the API for Loan data
//             loan_api = (await api.get_loan(id)).content;
//             loan_eth = await loanManager.requests(id);
//             // check loan data
//             keys_to_check = ['open', 'model', 'borrower', 'creator', 'oracle', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
//             helper.check_loan(loan_eth, loan_api, keys_to_check);

//             // get descriptor Values from InstallmentModel
//             simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
//             totalObligation = await installmentModel.simTotalObligation(loanData);
//             duration = await installmentModel.simDuration(loanData);
//             durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
//             interestRate = (durationPercentage * 360 * 86000) / duration;
//             frequency = await installmentModel.simFrequency(loanData);
//             installments = await installmentModel.simInstallments(loanData);

//             assert.equal(loan_api.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
//             assert.equal(loan_api.descriptor.total_obligation, totalObligation);
//             assert.equal(loan_api.descriptor.duration, duration);
//             assert.equal(loan_api.descriptor.interest_rate, interestRate);
//             assert.equal(loan_api.descriptor.frequency, frequency);
//             assert.equal(loan_api.descriptor.installments, installments);

//             assert.equal(loan_api.lender, null);

//             await helper.increaseTime(5);

//             await loanManager.approveRequest(id, { from: borrowerAddress });

//             // buy Rcn for lender address
//             await rcnToken.setBalance(lenderAddress, amount);

//             await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

//             try {
//                 await loanManager.lend(
//                     id,
//                     [],
//                     '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
//                     '0', // Cosigner limit
//                     [],                 // Cosigner data
//                     { from: lenderAddress }
//                 );
//                 error = false;
//             } catch (e) {
//                 error = true;
//             }
//             assert.isTrue(error, 'lend expired');
//         });
//     });

//     // E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW

//     describe(' E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW', function () {
//         // CREATE A REQUEST

//         step('should create a new loan Request', async () => {
//             cuota = '10000000000000000000';
//             punInterestRate = '1555200000000';
//             installments = '12';
//             duration = '2592000';
//             timeUnit = '2592000';
//             amount = '100000000000000000000';
//             oracle = '0x0000000000000000000000000000000000000000';
//             expiration = '1578571215';
//             ++saltValue;

//             // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
//             loanIdandData = await loanHelper.requestLoan(installmentModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
//                 cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
//             id = loanIdandData.id;
//             loanData = loanIdandData.loanData;

//             // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
//             await sleep(5000);
//             // Query the API for Loan data
//             loanJson = await api.get_loan(id);
//             loan = loanJson.content;

//             // Query blockchain for loan data
//             getRequestId = await loanManager.requests(id);
//             getBorrower = await loanManager.getBorrower(id);
//             getCreator = await loanManager.getCreator(id);
//             getOracle = await loanManager.getOracle(id);
//             getCosigner = await loanManager.getCosigner(id);
//             getCurrency = await loanManager.getCurrency(id);
//             getAmount = await loanManager.getAmount(id);
//             getExpirationRequest = await loanManager.getExpirationRequest(id);
//             getApproved = await loanManager.getApproved(id);
//             // getDueTime = await loanManager.getDueTime(id);
//             getLoanData = await loanManager.getLoanData(id);
//             getStatus = await loanManager.getStatus(id);

//             // get descriptor Values from InstallmentModel
//             simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
//             totalObligation = await installmentModel.simTotalObligation(loanData);
//             duration = await installmentModel.simDuration(loanData);
//             durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100;
//             interestRate = (durationPercentage * 360 * 86000) / duration;
//             frequency = await installmentModel.simFrequency(loanData);
//             installments = await installmentModel.simInstallments(loanData);

//             // Compare both results (API and blockchain) and validate consistency
//             assert.equal(loan.id, id);
//             assert.equal(loan.open, getRequestId.open);
//             assert.equal(loan.approved, getApproved);
//             assert.equal(loan.position, getRequestId.position);
//             assert.equal(loan.expiration, getExpirationRequest);
//             assert.equal(loan.amount, getAmount);
//             // assert.equal(loan.cosigner, getCosigner);
//             assert.equal(loan.model, getRequestId.model);
//             assert.equal(loan.creator, getCreator);
//             assert.equal(loan.oracle, getOracle);
//             assert.equal(loan.borrower, getBorrower);
//             assert.equal(loan.salt, getRequestId.salt);
//             assert.equal(loan.loanData, getLoanData);
//             // loan.created time value only in API
//             assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
//             assert.equal(loan.descriptor.total_obligation, totalObligation);
//             assert.equal(loan.descriptor.duration, duration);
//             assert.equal(loan.descriptor.interest_rate, interestRate);
//             assert.equal(loan.descriptor.frequency, frequency);
//             assert.equal(loan.descriptor.installments, installments);

//             // assert.equal(loan.currency, getCurrency);
//             assert.equal(loan.lender, null);
//             assert.equal(loan.status, getStatus, 'status not equal');
//             // assert.equal(loan.canceled, )
//         });

//         // APPROVE

//         step('should approve the loan request by the borrower', async () => {
//             await loanManager.approveRequest(id, { from: borrowerAddress });

//             // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
//             await sleep(5000);
//             // Query the API for Loan data
//             loanJsonAfterRequest = await api.get_loan(id);
//             loanAfterRequest = loanJsonAfterRequest.content;

//             const getApproved = await loanManager.getApproved(id);

//             assert.equal(true, loanAfterRequest.approved);
//             assert.equal(true, getApproved);
//         });

//         // LEND

//         step('should lend', async () => {
//             // buy Rcn for lender address
//             await rcnToken.setBalance(lenderAddress, amount);

//             balanceOfLender = await rcnToken.balanceOf(lenderAddress);

//             await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

//             await loanManager.lend(
//                 id,                 // Index
//                 [],                 // OracleData
//                 '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
//                 '0', // Cosigner limit
//                 [],                 // Cosigner data
//                 { from: lenderAddress }    // Owner/Lender
//             );

//             await sleep(5000);
//             // Query the API for Debt data
//             debtJson = await api.get_debt(id);
//             debt = debtJson.content;

//             // Query the API for config data
//             configJson = await api.get_config(id);
//             config = configJson.content;

//             // Query the API for Loan data
//             loanJsonAfterLend = await api.get_loan(id);
//             loanAfterLend = loanJsonAfterLend.content;

//             // Check Debt endpoint
//             loanDebt = await debtEngine.debts(id);

//             assert.equal(debt.error, loanDebt.error);
//             assert.equal(debt.balance, loanDebt.balance);
//             assert.equal(debt.model, loanDebt.model);
//             assert.equal(debt.creator, loanDebt.creator);
//             assert.equal(debt.oracle, loanDebt.oracle);

//             // Check config endPoint
//             loanConfigs = await installmentModel.configs(id);
//             assert.equal(config.data.installments, loanConfigs.installments);
//             assert.equal(config.data.time_unit, loanConfigs.timeUnit);
//             assert.equal(config.data.duration, loanConfigs.duration);
//             assert.equal(config.data.lent_time, loanConfigs.lentTime);
//             assert.equal(config.data.cuota, loanConfigs.cuota);
//             assert.equal(config.data.interest_rate, loanConfigs.interestRate);

//             // Check loan endPoint
//             assert.equal(loanAfterLend.open, false);
//             assert.equal(loanAfterLend.approved, true);
//             assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
//             assert.equal(loanAfterLend.status, await loanManager.getStatus(id));
//         });

//         // TRANSFER DEBT

//         step('should transfer the lender debt to another address', async () => {
//             // Transfer debt
//             await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });

//             assert.equal(newLenderAddress, await loanManager.ownerOf(id));

//             await sleep(5000);
//             loanJsonAfterTransfer = await api.get_loan(id);
//             loanAfterTransfer = loanJsonAfterTransfer.content;

//             assert.equal(newLenderAddress, loanAfterTransfer.lender);

//             // Should not be able to transfer if the sender is not the owner of the debt
//             try {
//                 error = await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });
//             } catch (e) {
//                 error = 'Not the owner of the debt';
//             }
//             assert.equal(error, 'Not the owner of the debt');
//         });

//         // TOTAL PAY

//         step('should pay the total of the debt', async () => {
//             // Pay loan
//             await rcnToken.setBalance(borrowerAddress, web3.utils.toWei('120', 'ether'));
//             await rcnToken.approve(debtEngine.address, web3.utils.toWei('120', 'ether'), { from: borrowerAddress });

//             await debtEngine.pay(id, web3.utils.toWei('100', 'ether'), borrowerAddress, [], { from: borrowerAddress });
//             // Test pay
//             await sleep(5000);
//             debtAPI = (await api.get_debt(id)).content;
//             stateAPI = (await api.get_state(id)).content;
//             debtETH = await debtEngine.debts(id);
//             stateETH = await installmentModel.states(id);

//             assert.equal(debtETH.balance, debtAPI.balance, 'DEBT Balance not eq :(');
//             assert.equal(stateETH.paid, stateAPI.paid, 'State paid not eq :(');

//             // Test pay, test total pay
//             await debtEngine.pay(id, web3.utils.toWei('20', 'ether'), borrowerAddress, [], { from: borrowerAddress });

//             await sleep(5000);
//             loanAPI = (await api.get_loan(id)).content;
//             debtAPI = (await api.get_debt(id)).content;
//             stateAPI = (await api.get_state(id)).content;
//             debtETH = await debtEngine.debts(id);
//             stateETH = await installmentModel.states(id);

//             assert.equal(debtETH.balance, debtAPI.balance, 'DEBT Balance not eq :(');
//             assert.equal(stateETH.paid, stateAPI.paid, 'State paid not eq :(');
//             assert.equal(loanAPI.status, await loanManager.getStatus(id), 'Status payed');
//             assert.isAtLeast(parseInt(debtAPI.balance), parseInt(loanAPI.amount), 'balance >= amount');
//             assert.equal(parseInt(debtAPI.balance), parseInt(loan.descriptor.total_obligation), 'balance eq descriptor total_obligation');
//         });

//         // WITHDRAW

//         step('should withdraw funds for lender', async () => {
//             // withdraw
//             balance_lender_before_withdraw = await rcnToken.balanceOf(newLenderAddress);
//             await debtEngine.withdrawPartial(id, newLenderAddress, web3.utils.toWei('120', 'ether'), { from: newLenderAddress });
//             await sleep(5000);

//             debtAPI = (await api.get_debt(id)).content;
//             debtETH = await debtEngine.debts(id);

//             balance_lender_after_withdraw = parseInt(await rcnToken.balanceOf(newLenderAddress));
//             total_balance = balance_lender_before_withdraw + parseInt(web3.utils.toWei('120', 'ether'));

//             assert.equal(parseInt(debtAPI.balance), parseInt(debtETH.balance), 'balance eq');
//             assert.equal(total_balance, balance_lender_after_withdraw, 'balance lender eq');
//         });
//     });
});
