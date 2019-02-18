
const TestToken = artifacts.require('./utils/test/TestToken.sol');
const LoanManager = artifacts.require('./diaspore/LoanManager.sol');
const DebtEngine = artifacts.require('./diaspore/DebtEngine.sol');
const InstallmentsModel = artifacts.require('./diaspore/model/InstallmentsModel');

const BN = web3.utils.BN;
const expect = require('chai')
  .use(require('bn-chai')(BN))
  .expect;

const api = require("./api.js");

function bn(number) {
  return new BN(number);
}

contract("Loans Life Cycle Tests", async accounts => {

  // Global instances variables
  let rcnToken;
  let debtEngine;
  let loanManager;
  let installmentModel;
  let saltValue = 0;

  // Static Contract Addresses for backend
  const rcnTokenAddress = "0xe5EA9D03D391d86933277c69ce6d2c3f073c4819"
  const debtEngineAddress = "0xdC8Dd86b3337A8EB4B1955DfF4B79676c9A40991"
  const loanManagerAddress = "0x275b0DC17674e02a8a434689A638E98D9aCd417a"
  const installmentModelAddress = "0xf1d88d1a22AD6D4A56137761e8df4aa68eDa3A11"

  //mnemonic used to create accounts
  // "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"
  // command: ganache-cli -m "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"

  // Accounts 
  const creatorPrivateKey = '0xaf080fd098ca962cc4778758dab7b88b4692afa18a613e7a93b77f8667207dd1';
  const creatorAddress = '0x1B274E25A1B02D77f8de7550daFf58C07A0D12c8';

  const borrowerPrivateKey = '0x9cd9fa19cb2d594f41aa1e89bc6ca3ee8998d405b4f7d096e366fcb59743c277';
  const borrowerAddress = '0x3FaD5afc06e263Ad2E73E82C98377739E746eF15';

  const lenderPrivateKey = '0xda06412214b4901dc170f99a3b51cc36b485bb92d688a449de94638117978c56';
  const lenderAddress = '0xa4D49A5e03c6cEEa80eCC48fBF92835AFd4C37e1';

  function sleep(millis) {
    return new Promise(resolve => setTimeout(resolve, millis));
  }

  // Function to calculate the id of a Loan
  async function calcId(_amount, _borrower, _creator, _model, _oracle, _salt, _expiration, _data) {
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
  }

  // Function creates a new loan request
  async function requestLoan(_cuota, _interestRate, _installments, _duration, _timeUnit, _amount, _oracle, _expiration) {
    // Set loan data parameters
    const cuota = _cuota;
    const interestRate = _interestRate;  //punitive interest rate 
    const installments = _installments;
    const duration = _duration;
    const timeUnit = _timeUnit;

    // Endode Loan data
    const loanData = await installmentModel.encodeData(cuota, interestRate, installments, duration, timeUnit);

    // Set other parameters to request a Loan
    const amount = _amount;        //amount in RCN 
    const modelAddress = installmentModel.address;
    let oracle = _oracle;
    let borrower = borrowerAddress;
    let salt = saltValue++;
    let expiration = _expiration;

    request = await loanManager.requestLoan(amount, modelAddress, oracle, borrower, salt, expiration, loanData);

    id = await calcId(amount, borrower, creatorAddress, installmentModel, oracle, salt, expiration, loanData);

    // Obtains loanId from logs of the transaction receipt
    const loanId = request.logs[0].args[0];

    return [id, loanData];
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

    it(" Should use the defined contracs Addresses  ", async () => {
      assert.equal(rcnToken.address, rcnTokenAddress);
      assert.equal(debtEngine.address, debtEngineAddress);
      assert.equal(loanManager.address, loanManagerAddress);
      assert.equal(installmentModel.address, installmentModelAddress);
    });
  });

  // FLUJO 1 - REQUEST  

  describe('Flujo 1: REQUEST LOAN', function () {

    it("should create a new loan Request ", async () => {
      cuota = '10000000000000000000';
      punInterestRate = '1555200000000';
      installments = '12';
      duration = '2592000';
      timeUnit = '2592000';
      amount = '100000000000000000000';
      oracle = '0x0000000000000000000000000000000000000000';
      expiration = '1578571215';

      // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
      loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
      id = loanIdandData[0];
      loanData = loanIdandData[1];

      // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
      await sleep(5000);
      // Query the API for Loan data
      loanJson = await api.get_loan(id);
      loan = loanJson.content;

      // Query blockchain for loan data 
      getRequestId = await loanManager.requests(id);
      getBorrower = await loanManager.getBorrower(id);
      getCreator = await loanManager.getCreator(id);
      getOracle = await loanManager.getOracle(id);
      getCosigner = await loanManager.getCosigner(id);
      getCurrency = await loanManager.getCurrency(id);
      getAmount = await loanManager.getAmount(id);
      getExpirationRequest = await loanManager.getExpirationRequest(id);
      getApproved = await loanManager.getApproved(id);
      // getDueTime = await loanManager.getDueTime(id);
      getLoanData = await loanManager.getLoanData(id);
      getStatus = await loanManager.getStatus(id);

      // get descriptor Values from InstallmentModel
      simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
      totalObligation = await installmentModel.simTotalObligation(loanData);
      duration = await installmentModel.simDuration(loanData);
      durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
      interestRate = (durationPercentage * 360 * 86000) / duration;
      frequency = await installmentModel.simFrequency(loanData);
      installments = await installmentModel.simInstallments(loanData);


      // Compare both results (API and blockchain) and validate consistency
      assert.equal(loan.id, id);
      assert.equal(loan.open, getRequestId.open);
      assert.equal(loan.approved, getApproved);
      assert.equal(loan.position, getRequestId.position);
      assert.equal(loan.expiration, getExpirationRequest);
      assert.equal(loan.amount, getAmount);
      // assert.equal(loan.cosigner, getCosigner);
      assert.equal(loan.model, getRequestId.model);
      assert.equal(loan.creator, getCreator);
      assert.equal(loan.oracle, getOracle);
      assert.equal(loan.borrower, getBorrower);
      assert.equal(loan.salt, getRequestId.salt)
      assert.equal(loan.loanData, getLoanData);
      //loan.created time value only in API
      assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
      assert.equal(loan.descriptor.total_obligation, totalObligation);
      assert.equal(loan.descriptor.duration, duration);
      assert.equal(loan.descriptor.interest_rate, interestRate);
      assert.equal(loan.descriptor.frequency, frequency);
      assert.equal(loan.descriptor.installments, installments);

      //assert.equal(loan.currency, getCurrency);
      assert.equal(loan.lender, null);
      assert.equal(loan.status, getStatus);
      //assert.equal(loan.canceled, );
    });
  });

    // FLUJO 3 - REQUEST  + APPROVE + LEND

    describe('Flujo 3: REQUEST  + APPROVE + LEND', function () {

      it("should create a new loan Request, approved and lend it ", async () => {
        cuota = '10000000000000000000';
        punInterestRate = '1555200000000';
        installments = '12';
        duration = '2592000';
        timeUnit = '2592000';
        amount = '100000000000000000000';
        oracle = '0x0000000000000000000000000000000000000000';
        expiration = '1578571215';
  
        // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
        loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
        id = loanIdandData[0];
        loanData = loanIdandData[1];
  
        // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
        await sleep(5000);
        // Query the API for Loan data
        loanJson = await api.get_loan(id);
        loan = loanJson.content;
        console.log(loan);
  
        // Query blockchain for loan data 
        getRequestId = await loanManager.requests(id);
        getBorrower = await loanManager.getBorrower(id);
        getCreator = await loanManager.getCreator(id);
        getOracle = await loanManager.getOracle(id);
        getCosigner = await loanManager.getCosigner(id);
        getCurrency = await loanManager.getCurrency(id);
        getAmount = await loanManager.getAmount(id);
        getExpirationRequest = await loanManager.getExpirationRequest(id);
        getApproved = await loanManager.getApproved(id);
        // getDueTime = await loanManager.getDueTime(id);
        getLoanData = await loanManager.getLoanData(id);
        getStatus = await loanManager.getStatus(id);
  
        // get descriptor Values from InstallmentModel
        simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
        totalObligation = await installmentModel.simTotalObligation(loanData);
        duration = await installmentModel.simDuration(loanData);
        durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
        interestRate = (durationPercentage * 360 * 86000) / duration;
        frequency = await installmentModel.simFrequency(loanData);
        installments = await installmentModel.simInstallments(loanData);
  
  
        // Compare both results (API and blockchain) and validate consistency
        assert.equal(loan.id, id);
        assert.equal(loan.open, getRequestId.open);
        assert.equal(loan.approved, getApproved);
        assert.equal(loan.position, getRequestId.position);
        assert.equal(loan.expiration, getExpirationRequest);
        assert.equal(loan.amount, getAmount);
        // assert.equal(loan.cosigner, getCosigner);
        assert.equal(loan.model, getRequestId.model);
        assert.equal(loan.creator, getCreator);
        assert.equal(loan.oracle, getOracle);
        assert.equal(loan.borrower, getBorrower);
        assert.equal(loan.salt, getRequestId.salt)
        assert.equal(loan.loanData, getLoanData);
        //loan.created time value only in API
        assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
        assert.equal(loan.descriptor.total_obligation, totalObligation);
        assert.equal(loan.descriptor.duration, duration);
        assert.equal(loan.descriptor.interest_rate, interestRate);
        assert.equal(loan.descriptor.frequency, frequency);
        assert.equal(loan.descriptor.installments, installments);
  
        //assert.equal(loan.currency, getCurrency);
        assert.equal(loan.lender, null);
        assert.equal(loan.status, getStatus, 'status not equal');
        //assert.equal(loan.canceled, )
  
        // Approve Loan by borower
        await loanManager.approveRequest(id, { from: borrowerAddress });
  
      // Lend Loan  
        // buy Rcn for lender address 
        await rcnToken.setBalance(lenderAddress, amount);
  
        balanceOfLender = await rcnToken.balanceOf(lenderAddress);
        console.log('BALANCE OF LENDER');
        console.log(balanceOfLender.toString());
  
        await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });
  
        await loanManager.lend(
            id,                 // Index
            [],                 // OracleData
            '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
            '0', // Cosigner limit
            [],                 // Cosigner data
            { from: lenderAddress }    // Owner/Lender
        );
  
        await sleep(10000);
        // Query the API for Loan data
        debtJson = await api.get_debt(id);
        debt = debtJson.content;
        console.log(debt);
  
      
  
      });
    });


});