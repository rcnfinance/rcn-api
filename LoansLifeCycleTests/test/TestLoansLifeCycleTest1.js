
const TestToken = artifacts.require('./utils/test/TestToken.sol');
const LoanManager = artifacts.require('./diaspore/LoanManager.sol');
const DebtEngine = artifacts.require('./diaspore/DebtEngine.sol');
const InstallmentsModel = artifacts.require('./diaspore/model/InstallmentsModel');

const BN = web3.utils.BN;
const expect = require('chai')
    .use(require('bn-chai')(BN))
    .expect;

function bn (number) {
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

      // Set loan data parameters
      const cuota = '10000000000000000000';
      const interestRate = '1555200000000';  //punitive interest rate 
      const installments = '12';
      const duration = '2592000';
      const timeUnit = '2592000';

      // Endode Loan data
      const loanData = await installmentModel.encodeData(cuota, interestRate, installments, duration, timeUnit);

      // Set other parameters to request a Loan
      const amount = '100000000000000000000';        //amount in RCN 
      const modelAddress = installmentModel.address;
      let oracle = '0x0000000000000000000000000000000000000000';
      let borrower = borrowerAddress;
      let salt = saltValue++;
      let expiration = '1578571215';

      console.log('salt');
      console.log(salt);

      // Request Loan 
      request = await loanManager.requestLoan(amount, modelAddress, oracle, borrower, salt, expiration, loanData);
      
      const loanId = request.logs[0].args[0];
      console.log('Loan id from result');
      console.log(loanId);

      const id = await calcId(amount, borrower, creatorAddress, installmentModel, oracle, salt, expiration, loanData);
      console.log('CALC ID');
      console.log(id);

      const getBorrower = await loanManager.getBorrower(request.logs[0].args[0]);

      assert.equal(borrower, getBorrower);
      assert.equal(loanId, id);
    });
  });


  //FLUJO 2 - REQUEST + APPROVE  

  describe('Flujo 2: REQUEST AND APPROVE LOAN', function () {

    it("should create a new loan Request and approve the  ", async () => {

      // Set loan data parameters
      const cuota = '10000000000000000000';
      const interestRate = '1555200000000';  //punitive interest rate 
      const installments = '12';
      const duration = '2592000';
      const timeUnit = '2592000';

      // Endode Loan data
      const loanData = await installmentModel.encodeData(cuota, interestRate, installments, duration, timeUnit);

      // Set other parameters to request a Loan
      //amount in RCN 
      const amount = '100000000000000000000';
      const modelAddress = installmentModel.address;
      let oracle = '0x0000000000000000000000000000000000000000';
      let borrower = borrowerAddress;
      let salt = saltValue++;
      let expiration = '1578571215';

      // Request Loan 
      request = await loanManager.requestLoan(amount, modelAddress, oracle, borrower, salt, expiration, loanData);
      
      const loanId = request.logs[0].args[0];
      console.log('Loan id from result');
      console.log(loanId);

      const id = await calcId(amount, borrower, creatorAddress, installmentModel, oracle, salt, expiration, loanData);
      console.log('CALC ID');
      console.log(id);

      const approved = await loanManager.approveRequest(id ,{from: borrowerAddress });

      const getBorrower = await loanManager.getBorrower(id);
      const getApproved = await loanManager.getApproved(id);

      assert.equal(borrower, getBorrower);
      assert.equal(true, getApproved);
      assert.equal(loanId, id);
    });
  });


});
