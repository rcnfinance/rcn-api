const BN = web3.utils.BN;
const expect = require('chai')
    .use(require('bn-chai')(BN))
    .expect;

// Function to calculate the id of a Loan
async function calcId (loanManager, debtEngine, _amount, _borrower, _creator, _model, _oracle, _salt, _expiration, _data) {
    const _two = '0x02';
    const controlId = await loanManager.calcId(
        _amount,
        _borrower,
        _creator,
        _model.address,
        _oracle,
        _salt,
        _expiration,
        _data
    );

    const controlInternalSalt = await loanManager.buildInternalSalt(
        _amount,
        _borrower,
        _creator,
        _salt,
        _expiration
    );

    const internalSalt = web3.utils.hexToNumberString(
        web3.utils.soliditySha3(
            { t: 'uint128', v: _amount },
            { t: 'address', v: _borrower },
            { t: 'address', v: _creator },
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
    _cuota, _interestRate, _installments, _duration, _timeUnit, _amount, _oracle, _expiration) {
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
    const salt = saltValue;
    const expiration = _expiration;

    await loanManager.requestLoan(amount, modelAddress, oracle, borrower, salt, expiration, loanData);

    const id = await calcId(loanManager, debtEngine, amount, borrower, creatorAddress, installmentsModel, oracle, salt, expiration, loanData);

    // Obtains loanId from logs of the transaction receipt
    // const loanId = request.logs[0].args[0];

    const _loanData = {
        id: id,
        loanData: loanData,
    };
    return _loanData;
};

module.exports = {
    requestLoan: requestLoan,
};
