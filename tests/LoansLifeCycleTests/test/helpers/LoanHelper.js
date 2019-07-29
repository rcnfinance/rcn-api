const api = require('./api.js');
const helper = require('./Helper.js');
const BN = web3.utils.BN;
const expect = require('chai')
    .use(require('bn-chai')(BN))
    .expect;

// Function to calculate the id of a Loan
async function calcId (loanManager, debtEngine, _amount, _borrower, _creator, _model, _oracle, _callback, _salt, _expiration, _data) {
    const _two = '0x02';
    const controlId = await loanManager.calcId(
        _amount,
        _borrower,
        _creator,
        _model.address,
        _oracle,
        _callback,
        _salt,
        _expiration,
        _data
    );

    const controlInternalSalt = await loanManager.buildInternalSalt(
        _amount,
        _borrower,
        _creator,
        _callback,
        _salt,
        _expiration
    );

    const internalSalt = web3.utils.hexToNumberString(
        web3.utils.soliditySha3(
            { t: 'uint128', v: _amount },
            { t: 'address', v: _borrower },
            { t: 'address', v: _creator },
            { t: 'address', v: _callback },
            { t: 'uint256', v: _salt },
            { t: 'uint64', v: _expiration }
        )
    );

    const id = web3.utils.soliditySha3(
        { t: 'uint8', v: _two },
        { t: 'address', v: debtEngine.address },
        { t: 'address', v: loanManager.address },
        { t: 'address', v: _model.address },
        { t: 'address', v: _oracle },
        { t: 'uint256', v: internalSalt },
        { t: 'bytes', v: _data }
    );

    expect(internalSalt).to.eq.BN(controlInternalSalt, 'bug internalSalt');
    assert.equal(id, controlId, 'bug calcId');
    return id;
};

// Function creates a new loan request
const requestLoan = async function (installmentsModel, borrowerAddress, saltValue, loanManager, debtEngine, creatorAddress,
    _cuota, _interestRate, _installments, _duration, _timeUnit, _amount, _oracle, _callback, _expiration) {
    // Set loan data parameters
    const cuota = _cuota;
    const interestRate = _interestRate;  // punitive interest rate
    const installments = _installments;
    const duration = _duration;
    const timeUnit = _timeUnit;

    // Endode Loan data
    const loanData = await installmentsModel.encodeData(cuota, interestRate, installments, duration, timeUnit);

    // Set other parameters to request a Loan
    const amount = _amount;        // amount in RCN
    const modelAddress = installmentsModel.address;
    const oracle = _oracle;
    const borrower = borrowerAddress;
    const callback = _callback;
    const salt = saltValue;
    const expiration = _expiration;

    await loanManager.requestLoan(amount, modelAddress, oracle, borrower, callback, salt, expiration, loanData);

    const id = await calcId(loanManager, debtEngine, amount, borrower, creatorAddress, installmentsModel, oracle, callback, salt, expiration, loanData);

    // Obtains loanId from logs of the transaction receipt
    // const loanId = request.logs[0].args[0];

    const _loanData = {
        id: id,
        loanData: loanData,
    };
    return _loanData;
};

// Function which checks requestLoan consistency Api and Eth
const checkRequestLoan = async function (loanManager, installmentModel, id, loanData) {
    // Query the API for Loan data
    const loanApi = (await api.getLoan(id)).content;
    const loanEth = await loanManager.requests(id);
    // check loan data
    const keysToCheck = ['open', 'model', 'borrower', 'creator', 'oracle', 'callback', 'cosigner', 'currency', 'amount', 'expiration', 'approved', 'loanData', 'status'];
    helper.checkLoan(loanEth, loanApi, keysToCheck);

    // get descriptor Values from InstallmentModel
    const simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
    const totalObligation = await installmentModel.simTotalObligation(loanData);
    const loanDuration = await installmentModel.simDuration(loanData);
    const durationPercentage = ((totalObligation / parseInt(loanEth.amount)) - 1) * 100;
    const interestRate = (durationPercentage * 360 * 86000) / loanDuration;
    const frequency = await installmentModel.simFrequency(loanData);
    const loanInstallments = await installmentModel.simInstallments(loanData);

    assert.equal(loanApi.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
    assert.equal(loanApi.descriptor.total_obligation, totalObligation);
    assert.equal(loanApi.descriptor.duration, loanDuration);
    assert.equal(loanApi.descriptor.interest_rate, interestRate);
    assert.equal(loanApi.descriptor.frequency, frequency);
    assert.equal(loanApi.descriptor.installments, loanInstallments);

    assert.equal(loanApi.lender, null);
};

const checkApprove = async function (loanManager, id) {
    const loanApiAfter = (await api.getLoan(id)).content;
    const loanEthAfter = await loanManager.requests(id);

    const keysToCheckAfter = ['approved'];
    helper.checkLoan(loanEthAfter, loanApiAfter, keysToCheckAfter);
};

const checkLend = async function (loanManager, debtEngine, installmentModel, loanEthBeforeLend, id) {
    const loanApi = (await api.getLoan(id)).content;
    const loanEthAfterLend = await loanManager.requests(id);

    // Query the API for Debt data
    const debtApi = (await api.getDebt(id)).content;
    const debtEth = await debtEngine.debts(id);

    const modelInfo = await api.getModelDebtInfo(id);

    // Query the API for config data
    const configApi = (await api.getConfig(id)).content;
    const configEth = await installmentModel.configs(id);

    // Query the API for state data
    const stateApi = (await api.getState(id)).content;
    const stateEth = await installmentModel.states(id);

    // call check_status functions
    await helper.checkState(stateEth, stateApi);
    await helper.checkConfig(configEth, configApi);
    await helper.checkDebt(debtEth, debtApi);
    const keyToCheck3 = ['approved', 'expiration', 'amount', 'model', 'creator', 'oracle', 'borrower', 'loanData'];
    await helper.checkLoan(loanEthBeforeLend, loanApi, keyToCheck3);
    assert.equal(loanEthAfterLend.cosigner, loanApi.cosigner);

    assert.equal(loanApi.open, false);
    assert.equal(loanApi.approved, true);
    assert.equal(loanApi.lender, await loanManager.ownerOf(id));
    assert.equal(loanApi.status, await loanManager.getStatus(id));

    // check model_info.due_time
    const dueTime = await loanManager.getDueTime(id);
    assert.equal(dueTime, modelInfo.due_time, 'installments_due_time eq model_info.due_time');

    // check model_info.balance
    assert.equal(parseInt(debtEth.balance), modelInfo.debt_balance, 'debtETH.balance eq model_info.balance');

    // estimated_obligation
    const estimatedObligationApi = modelInfo.estimated_obligation;
    const estimatedObligationEth = await installmentModel.getEstimateObligation(id);
    assert.equal(estimatedObligationApi, estimatedObligationEth, 'estimated obligation eq');

    // next_obligation
    const nextObligationApi = modelInfo.next_obligation;
    const nextObligationEth = await installmentModel.getObligation(id, dueTime);
    assert.equal(nextObligationApi, nextObligationEth[0], 'next_obligation');

    // current_obligation
    const now = parseInt(Date.now() / 1000);
    const currentObligationApi = modelInfo.current_obligation;
    const currentObligationEth = await installmentModel.getObligation(id, now);
    assert.equal(currentObligationApi, currentObligationEth[0], 'currentObligation');
};

const checkPay = async function (loanManager, debtEngine, installmentModel, id) {
    const debtApi = (await api.getDebt(id)).content;
    const debtEth = await debtEngine.debts(id);

    const stateApi = (await api.getState(id)).content;
    const stateEth = await installmentModel.states(id);

    const configApi = (await api.getConfig(id)).content;
    const configEth = await installmentModel.configs(id);

    const modelInfo = await api.getModelDebtInfo(id);

    assert.equal(debtEth.balance, debtApi.balance, 'DEBT Balance not eq :(');
    assert.equal(stateEth.paid, stateApi.paid, 'State paid not eq :(');

    helper.checkDebt(debtEth, debtApi);
    helper.checkState(stateEth, stateApi);
    helper.checkConfig(configEth, configApi);

    // check model_info
    // check model_info.due_time
    const dueTime = await loanManager.getDueTime(id);
    assert.equal(dueTime, modelInfo.due_time, 'installments_due_time eq model_info.due_time');

    // check model_info.balance
    assert.equal(parseInt(debtEth.balance), modelInfo.debt_balance, 'debtETH.balance eq model_info.balance');

    // estimated_obligation
    const estimatedObligationApi = modelInfo.estimated_obligation;
    const estimatedObligationEth = await installmentModel.getEstimateObligation(id);
    assert.equal(estimatedObligationApi, estimatedObligationEth, 'estimated obligation eq');

    // next_obligation
    const nextObligationApi = modelInfo.next_obligation;
    const nextObligationEth = await installmentModel.getObligation(id, dueTime);
    assert.equal(nextObligationApi, nextObligationEth[0], 'next_obligation');

    // current_obligation
    const now = parseInt(Date.now() / 1000);
    const currentObligationApi = modelInfo.current_obligation;
    const currentObligationEth = await installmentModel.getObligation(id, now);
    assert.equal(currentObligationApi, currentObligationEth[0], 'currentObligation');
};

const checkCancel = async function (id) {
    const loanApi = (await api.getLoan(id)).content;
    assert.isTrue(loanApi.approved, 'loan approved');
    assert.isTrue(loanApi.canceled, 'loan canceled');

    let debtExists;
    try {
        await api.getDebt(id);
        debtExists = true;
    } catch (error) {
        debtExists = false;
    } finally {
        assert.isFalse(debtExists, 'debt dot exists :)');
    }
};

const checkTransfer = async function (loanManager, debtEngine, newLenderAddress, lenderAddress, id) {
    assert.equal(newLenderAddress, await loanManager.ownerOf(id));

    const loanJsonAfterTransfer = await api.getLoan(id);
    const loanAfterTransfer = loanJsonAfterTransfer.content;

    assert.equal(newLenderAddress, loanAfterTransfer.lender);

    // Should not be able to transfer if the sender is not the owner of the debt
    let error;
    try {
        error = await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });
    } catch (e) {
        error = 'Not the owner of the debt';
    }
    assert.equal(error, 'Not the owner of the debt');
};

const checkWithdraw = async function (debtEngine, rcnToken, lenderAddress, id, balanceLenderBeforeWithdraw) {
    const debtApi = (await api.getDebt(id)).content;
    const debtEth = await debtEngine.debts(id);

    const balanceLenderAfterWithdraw = parseInt(await rcnToken.balanceOf(lenderAddress));
    const totalBalance = balanceLenderBeforeWithdraw + parseInt(web3.utils.toWei('120', 'ether'));

    assert.equal(parseInt(debtApi.balance), parseInt(debtEth.balance), 'balance eq');
    assert.equal(totalBalance, balanceLenderAfterWithdraw, 'balance lender eq');
};

module.exports = {
    requestLoan: requestLoan,
    checkRequestLoan: checkRequestLoan,
    checkApprove: checkApprove,
    checkLend: checkLend,
    checkPay: checkPay,
    checkCancel: checkCancel,
    checkTransfer: checkTransfer,
    checkWithdraw: checkWithdraw,
};
