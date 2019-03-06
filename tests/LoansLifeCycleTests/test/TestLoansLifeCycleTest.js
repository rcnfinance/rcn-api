var mochaSteps = require("mocha-steps");

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

function increaseTime(duration) {
    const id = Date.now();

    return new Promise((resolve, reject) => {
        web3.currentProvider.send({
            jsonrpc: "2.0",
            method: "evm_increaseTime",
            params: [duration],
            id: id
        },
        err1 => {
            if (err1) return reject(err1);

            web3.currentProvider.send({
                jsonrpc: "2.0",
                method: "evm_mine",
                id: id + 1
            },
            (err2, res) => {
                return err2 ? reject(err2) : resolve(res);
            });
        });
    });
};

async function getBlockTime() {
  return (await web3.eth.getBlock(await web3.eth.getBlockNumber())).timestamp;
};

async function tryCatchRevert(promise, message) {
    let headMsg = 'revert ';
    if (message === '') {
        headMsg = headMsg.slice(0, headMsg.length - 1);
        console.warn('    \u001b[93m\u001b[2m\u001b[1m⬐ Warning:\u001b[0m\u001b[30m\u001b[1m There is an empty revert/require message');
    }
    try {
        if (promise instanceof Function) {
            await promise();
        } else {
            await promise;
        }
    } catch (error) {
        assert(
            error.message.search(headMsg + message) >= 0 || process.env.SOLIDITY_COVERAGE,
            'Expected a revert \'' + headMsg + message + '\', got ' + error.message + '\' instead'
        );
        return;
    }
    assert.fail('Expected throw not received');
};

async function check_state(state_eth, state_api) {

  assert.equal(state_eth.status, state_api.status, "state.status eq");
  assert.equal(state_eth.clock, state_api.clock, "state.clock eq");
  assert.equal(state_eth.lastPayment, state_api.last_payment, "state.last_payment eq");
  assert.equal(state_eth.paid, state_api.paid, "state.paid eq");
  assert.equal(state_eth.paidBase, state_api.paid_base, "state.paid_base eq");
  assert.equal(state_eth.interest, state_api.interest, "state.interest eq");

  return;
}

async function check_config(config_eth, config_api) {

  assert.equal(config_eth.installments, config_api.data.installments, "config.installments eq")
  assert.equal(config_eth.timeUnit, config_api.data.time_unit, "config.time_unit eq")
  assert.equal(config_eth.duration, config_api.data.duration, "config.duration eq")
  assert.equal(config_eth.lentTime, config_api.data.lent_time, "config.lent_time eq")
  assert.equal(config_eth.cuota, config_api.data.cuota, "config.cuota eq")
  assert.equal(config_eth.interestRate, config_api.data.interest_rate, "config.interest_rate eq")

  return
}

async function check_debt(debt_eth, debt_api) {

  assert.equal(debt_eth.error, debt_api.error, "debt.error eq");
  assert.equal(debt_eth.balance, debt_api.balance, "debt.balance eq");
  assert.equal(debt_eth.model, debt_api.model, "debt.model eq");
  assert.equal(debt_eth.creator, debt_api.creator, "debt.creator eq");
  assert.equal(debt_eth.oracle, debt_api.oracle, "debt.oracle eq");

  return
}

async function check_loan(loan_eth, loan_api, check_keys) {

  if (check_keys.includes("open") ) {
    assert.equal(loan_eth.open, loan_api.open, "loan.open");
  }
  if (check_keys.includes("approved")) {
    assert.equal(loan_eth.approved, loan_api.approved, "loan.approved");
  }
  if (check_keys.includes("position")) {
    assert.equal(loan_eth.position, loan_api.position, "loan.position");
  }
  if (check_keys.includes("expiration")) {
    assert.equal(loan_eth.expiration, loan_api.expiration, "loan.expiration");
  }
  if (check_keys.includes("amount")) {
    assert.equal(loan_eth.amount, loan_api.amount, "loan.amount");
  }  
  if (check_keys.includes("cosigner")) {
    assert.equal(loan_eth.cosigner, loan_api.cosigner, "loan.cosigner");
  }
  if (check_keys.includes("model")) {
    assert.equal(loan_eth.model, loan_api.model, "loan.model");
  }
  if (check_keys.includes("creator")) {
    assert.equal(loan_eth.creator, loan_api.creator, "loan.creator");
  }
  if (check_keys.includes("oracle")) {
    assert.equal(loan_eth.oracle, loan_api.oracle, "loan.oracle");
  }
  if (check_keys.includes("borrower")) {
    assert.equal(loan_eth.borrower, loan_api.borrower, "loan.borrower");
  }
  if (check_keys.includes("salt")) {
    assert.equal(loan_eth.salt, loan_api.salt, "loan.salt");
  }
  if (check_keys.includes("loanData")) {
    assert.equal(loan_eth.loanData, loan_api.loanData, "loan.loanData");
  }

  return
}

contract("Loans Life Cycle Tests", async accounts => {

  // Global instances variables
  let rcnToken;
  let debtEngine;
  let loanManager;
  let installmentModel;
  let saltValue = 100;

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

  const newLenderPrivateKey = '0x1ac6294ae9975943a1917d49d967db683a5755237c626658530a52f2f61209e1';
  const newLenderAddress = '0x060a109b32d70e58e39376516b2f97E9346939a9';

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
    let salt = ++saltValue;
    let expiration = _expiration;

    request = await loanManager.requestLoan(amount, modelAddress, oracle, borrower, salt, expiration, loanData);

    id = await calcId(amount, borrower, creatorAddress, installmentModel, oracle, salt, expiration, loanData);

    // Obtains loanId from logs of the transaction receipt
    const loanId = request.logs[0].args[0];

    loan_data = {
      id: id,
      loanData: loanData
    }

    return loan_data;
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

  // describe('Flujo 1: REQUEST LOAN', function () {

  //   it("should create a new loan Request ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     result = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = result.id;
  //     loanData = result.loanData;

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loan_api = (await api.get_loan(id)).content;
  //     loan_eth = await loanManager.requests(id);
  //     //check loan data
  //     keys_to_check = ["open", "model", "borrower", "creator", "oracle", "cosigner", "currency", "amount", "expiration", "approved", "loanData", "status"]
  //     check_loan(loan_eth, loan_api, keys_to_check)

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);

  //     assert.equal(loan_api.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan_api.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan_api.descriptor.duration, duration);
  //     assert.equal(loan_api.descriptor.interest_rate, interestRate);
  //     assert.equal(loan_api.descriptor.frequency, frequency);
  //     assert.equal(loan_api.descriptor.installments, installments);

  //     assert.equal(loan_api.lender, null);
  //   });
  // });

  // // // FLUJO 2 - REQUEST + APPROVE

  // describe('Flujo 2: REQUEST AND APPROVE LOAN', function () {

  //   it("should create a new loan Request and approve the request by the borrower ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     result = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = result.id;
  //     loanData = result.loanData;

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loan_api = (await api.get_loan(id)).content;
  //     loan_eth = await loanManager.requests(id);
  //     //check loan data
  //     keys_to_check = ["open", "model", "borrower", "creator", "oracle", "cosigner", "currency", "amount", "expiration", "approved", "loanData", "status"]
  //     check_loan(loan_eth, loan_api, keys_to_check)

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);

  //     assert.equal(loan_api.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan_api.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan_api.descriptor.duration, duration);
  //     assert.equal(loan_api.descriptor.interest_rate, interestRate);
  //     assert.equal(loan_api.descriptor.frequency, frequency);
  //     assert.equal(loan_api.descriptor.installments, installments);

  //     assert.equal(loan_api.lender, null);
      
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     loan_api = (await api.get_loan(id)).content;
  //     loan_eth = await loanManager.requests(id);

  //     keys_to_check = ["approved"]
  //     check_loan(loan_eth, loan_api, keys_to_check)
  //   });
  // });

  // FLUJO 3 - REQUEST  + APPROVE + LEND

  describe('Flujo 3: REQUEST  + APPROVE + LEND', function () {

    it("should create a new loan Request, approve and lend ", async () => {
      cuota = '10000000000000000000';
      punInterestRate = '1555200000000';
      installments = '12';
      duration = '2592000';
      timeUnit = '2592000';
      amount = '100000000000000000000';
      oracle = '0x0000000000000000000000000000000000000000';
      expiration = '1578571215';

      // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
      result = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
      id = result.id;
      loanData = result.loanData;

      // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
      await sleep(5000);
      // Query the API for Loan data
      loan_api = (await api.get_loan(id)).content;
      loan_eth = await loanManager.requests(id);
      //check loan data
      keys_to_check = ["open", "model", "borrower", "creator", "oracle", "cosigner", "currency", "amount", "expiration", "approved", "loanData", "status"]
      check_loan(loan_eth, loan_api, keys_to_check)

      // get descriptor Values from InstallmentModel
      simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
      totalObligation = await installmentModel.simTotalObligation(loanData);
      duration = await installmentModel.simDuration(loanData);
      durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
      interestRate = (durationPercentage * 360 * 86000) / duration;
      frequency = await installmentModel.simFrequency(loanData);
      installments = await installmentModel.simInstallments(loanData);

      assert.equal(loan_api.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
      assert.equal(loan_api.descriptor.total_obligation, totalObligation);
      assert.equal(loan_api.descriptor.duration, duration);
      assert.equal(loan_api.descriptor.interest_rate, interestRate);
      assert.equal(loan_api.descriptor.frequency, frequency);
      assert.equal(loan_api.descriptor.installments, installments);

      assert.equal(loan_api.lender, null);
      
      await loanManager.approveRequest(id, { from: borrowerAddress });

      await sleep(5000)
      loan_api = (await api.get_loan(id)).content;
      loan_eth_before_lend = await loanManager.requests(id);

      keys_to_check = ["approved"]
      check_loan(loan_eth_before_lend, loan_api, keys_to_check)

      // buy Rcn for lender address 
      await rcnToken.setBalance(lenderAddress, amount);

      balanceOfLender = await rcnToken.balanceOf(lenderAddress);

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
      loan_api = (await api.get_loan(id)).content;

      // Query the API for Debt data
      debt_api = (await api.get_debt(id)).content;
      debt_eth = await debtEngine.debts(id);

      model_info = await api.get_model_debt_info(id);

      // Query the API for config data
      config_api = (await api.get_config(id)).content;
      config_eth = await installmentModel.configs(id);

      // Query the API for state data
      state_api = (await api.get_state(id)).content;
      state_eth = await installmentModel.states(id);

      // call check_status functions
      await check_state(state_eth, state_api);
      await check_config(config_eth, config_api)
      await check_debt(debt_eth, debt_api)
      key_to_check = ["approved", "expiration", "amount", "cosigner", "model", "creator", "oracle", "borrower", "loanData"]
      await check_loan(loan_eth_before_lend, loan_api, key_to_check)

      // check model_info.due_time
      due_time = await loanManager.getDueTime(id);
      assert.equal(due_time, model_info.due_time, "installments_due_time eq model_info.due_time");

      // check model_info.balance
      assert.equal(parseInt(debt_eth.balance), model_info.debt_balance, "debtETH.balance eq model_info.balance");

      // estimated_obligation
      estimated_obligation_api = model_info.estimated_obligation
      estimated_obligation_eth = await installmentModel.getEstimateObligation(id);
      console.log("estimated_obligation_api", estimated_obligation_api)
      console.log("estimated_obligation_eth", estimated_obligation_eth)
      assert.equal(estimated_obligation_api, estimated_obligation_eth, "estimated obligation eq")

      // next_obligation
      next_obligation_api = model_info.next_obligation
      next_obligation_eth = await installmentModel.getObligation(id, due_time)
      console.log("next_obligation_api", next_obligation_api)
      console.log("next_obligation_eth", next_obligation_eth)
      assert.equal(next_obligation_api, next_obligation_eth, "next_obligation")

      assert.equal(false, true, "asd");

      // console.log("due_time:", parseInt(due_time))
      // console.log("next_obligation_api: ", next_obligation_api)
      // console.log("state", stateETH);
      // console.log("debt", debtETH);
      // console.log("debt_api:", debt)
      console.log("config", config_eth)
      console.log()

      console.log("config.lentTime:", parseInt(config_eth.lentTime));
      console.log("timestamp < lenttime:", 1553948891 < parseInt(config_eth.lentTime))
      console.log("next_obligation_eth: ", next_obligation_eth)
      // console.log("config;", parseInt(config_eth[3]))
      // console.log("timestamp:", 1553948891)
      assert.equal(next_obligation_api, next_obligation_eth, "next_obligation eq?");


      // Query the API for Loan data
      loanJsonAfterLend = await api.get_loan(id);
      loanAfterLend = loanJsonAfterLend.content;

      //Check Debt endpoint
      loanDebt = await debtEngine.debts(id);

      assert.equal(debt.error, loanDebt.error);
      assert.equal(debt.balance, loanDebt.balance);
      assert.equal(debt.model, loanDebt.model);
      assert.equal(debt.creator, loanDebt.creator);
      assert.equal(debt.oracle, loanDebt.oracle);

      //Check config endPoint
      loanConfigs = await installmentModel.configs(id);
      assert.equal(config.data.installments, loanConfigs.installments);
      assert.equal(config.data.time_unit, loanConfigs.timeUnit);
      assert.equal(config.data.duration, loanConfigs.duration);
      assert.equal(config.data.lent_time, loanConfigs.lentTime); 
      assert.equal(config.data.cuota, loanConfigs.cuota);    
      assert.equal(config.data.interest_rate, loanConfigs.interestRate);

      // Check loan endPoint
      assert.equal(loanAfterLend.open, false);
      assert.equal(loanAfterLend.approved, true);
      assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
      assert.equal(loanAfterLend.status, await loanManager.getStatus(id));
    });
  });

  // FLUJO 4 - REQUEST  + APPROVE + LEND + PAY

  // describe('Flujo 4: REQUEST  + APPROVE + LEND + PAY', function () {

  //   it("should create a new loan Request, approve, lend and pay ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;
  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //     // Approve Loan by borower
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.lend(
  //         id,                 // Index
  //         [],                 // OracleData
  //         '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //         '0', // Cosigner limit
  //         [],                 // Cosigner data
  //         { from: lenderAddress }    // Owner/Lender
  //     );

  //     await sleep(5000);
  //     // Query the API for Debt data
  //     debtJson = await api.get_debt(id);
  //     debt = debtJson.content;

  //     // Query the API for config data
  //     configJson = await api.get_config(id);
  //     config = configJson.content;

  //     // Query the API for Loan data
  //     loanJsonAfterLend = await api.get_loan(id);
  //     loanAfterLend = loanJsonAfterLend.content;

  //     //Check Debt endpoint
  //     loanDebt = await debtEngine.debts(id);

  //     assert.equal(debt.error, loanDebt.error);
  //     assert.equal(debt.balance, loanDebt.balance);
  //     assert.equal(debt.model, loanDebt.model);
  //     assert.equal(debt.creator, loanDebt.creator);
  //     assert.equal(debt.oracle, loanDebt.oracle);

  //     //Check config endPoint
  //     loanConfigs = await installmentModel.configs(id);
  //     assert.equal(config.data.installments, loanConfigs.installments);
  //     assert.equal(config.data.time_unit, loanConfigs.timeUnit);
  //     assert.equal(config.data.duration, loanConfigs.duration);
  //     assert.equal(config.data.lent_time, loanConfigs.lentTime); 
  //     assert.equal(config.data.cuota, loanConfigs.cuota);    
  //     assert.equal(config.data.interest_rate, loanConfigs.interestRate);

  //     // Check loan endPoint
  //     assert.equal(loanAfterLend.open, false);
  //     assert.equal(loanAfterLend.approved, true);
  //     assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
  //     assert.equal(loanAfterLend.status, await loanManager.getStatus(id));

  //     // Pay loan
  //     await rcnToken.setBalance(borrowerAddress, web3.utils.toWei("120", "ether"));
  //     await rcnToken.approve(debtEngine.address, web3.utils.toWei("120", "ether"), { from: borrowerAddress });


  //     await debtEngine.pay(id, web3.utils.toWei("100", "ether"), borrowerAddress, [], { from: borrowerAddress });
  //     // Test pay
  //     await sleep(10000);
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");


  //     // await debtEngine.pay(id, web3.utils.toWei("20", "ether"), borrowerAddress, [], { from: borrowerAddress });
  //     // Test pay, test total pay


  //   });
  // });

  // // FLUJO 5 - REQUEST  + APPROVE + CANCEL

  // describe('Flujo 5: REQUEST  + APPROVE + CANCEL', function () {

  //   it("should create a new loan Request, approve and cancel ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;
  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //     // Approve Loan by borower
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.cancel(id, { from: creatorAddress });
      
  //     await sleep(5000);
      
  //     loanAPI = (await api.get_loan(id)).content;
  //     assert.isTrue(loanAPI.approved, "loan approved");
  //     assert.isTrue(loanAPI.canceled, "loan canceled");

  //     // let debt_exists;
  //     try {
  //       await api.get_debt(id);
  //       debt_exists = true;
  //     } catch (error) {
  //       debt_exists = false;
  //     } finally {
  //       assert.isFalse(debt_exists, "debt dot exists :)");
  //     }
  //   });
  // });

  // // FLUJO 6 - REQUEST  + APPROVE + LEND + TOTALPAY

  // describe('Flujo 6: REQUEST  + APPROVE + LEND + TOTALPAY', function () {

  //   it("should create a new loan Request, approve, lend, total pay ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;
  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //     // Approve Loan by borower
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.lend(
  //         id,                 // Index
  //         [],                 // OracleData
  //         '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //         '0', // Cosigner limit
  //         [],                 // Cosigner data
  //         { from: lenderAddress }    // Owner/Lender
  //     );

  //     await sleep(5000);
  //     // Query the API for Debt data
  //     debtJson = await api.get_debt(id);
  //     debt = debtJson.content;

  //     // Query the API for config data
  //     configJson = await api.get_config(id);
  //     config = configJson.content;

  //     // Query the API for Loan data
  //     loanJsonAfterLend = await api.get_loan(id);
  //     loanAfterLend = loanJsonAfterLend.content;

  //     //Check Debt endpoint
  //     loanDebt = await debtEngine.debts(id);

  //     assert.equal(debt.error, loanDebt.error);
  //     assert.equal(debt.balance, loanDebt.balance);
  //     assert.equal(debt.model, loanDebt.model);
  //     assert.equal(debt.creator, loanDebt.creator);
  //     assert.equal(debt.oracle, loanDebt.oracle);

  //     //Check config endPoint
  //     loanConfigs = await installmentModel.configs(id);
  //     assert.equal(config.data.installments, loanConfigs.installments);
  //     assert.equal(config.data.time_unit, loanConfigs.timeUnit);
  //     assert.equal(config.data.duration, loanConfigs.duration);
  //     assert.equal(config.data.lent_time, loanConfigs.lentTime); 
  //     assert.equal(config.data.cuota, loanConfigs.cuota);    
  //     assert.equal(config.data.interest_rate, loanConfigs.interestRate);

  //     // Check loan endPoint
  //     assert.equal(loanAfterLend.open, false);
  //     assert.equal(loanAfterLend.approved, true);
  //     assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
  //     assert.equal(loanAfterLend.status, await loanManager.getStatus(id));

  //     // Pay loan
  //     await rcnToken.setBalance(borrowerAddress, web3.utils.toWei("120", "ether"));
  //     await rcnToken.approve(debtEngine.address, web3.utils.toWei("120", "ether"), { from: borrowerAddress });


  //     await debtEngine.pay(id, web3.utils.toWei("100", "ether"), borrowerAddress, [], { from: borrowerAddress });
  //     // Test pay
  //     await sleep(5000);
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");

  //     // Test pay, test total pay
  //     await debtEngine.pay(id, web3.utils.toWei("20", "ether"), borrowerAddress, [], { from: borrowerAddress });

  //     await sleep(5000)
  //     loanAPI = (await api.get_loan(id)).content;
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");
  //     assert.equal(loanAPI.status, await loanManager.getStatus(id), "Status payed")
  //     assert.isAtLeast(parseInt(debtAPI.balance), parseInt(loanAPI.amount), "balance >= amount");
  //     assert.equal(parseInt(debtAPI.balance), parseInt(loan.descriptor.total_obligation), "balance eq descriptor total_obligation");
  //   });
  // });

  // // FLUJO 7 - REQUEST  + APPROVE + LEND + TRANSFER

  // describe('Flujo 7: REQUEST  + APPROVE + LEND + TRANSFER', function () {

  //   it("should create a new loan Request, approve, lend and transfer ", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;
  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //     // Approve Loan by borower
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.lend(
  //         id,                 // Index
  //         [],                 // OracleData
  //         '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //         '0', // Cosigner limit
  //         [],                 // Cosigner data
  //         { from: lenderAddress }    // Owner/Lender
  //     );

  //     await sleep(5000);
  //     // Query the API for Debt data
  //     debtJson = await api.get_debt(id);
  //     debt = debtJson.content;

  //     // Query the API for config data
  //     configJson = await api.get_config(id);
  //     config = configJson.content;

  //     // Query the API for Loan data
  //     loanJsonAfterLend = await api.get_loan(id);
  //     loanAfterLend = loanJsonAfterLend.content;

  //     //Check Debt endpoint
  //     loanDebt = await debtEngine.debts(id);

  //     assert.equal(debt.error, loanDebt.error);
  //     assert.equal(debt.balance, loanDebt.balance);
  //     assert.equal(debt.model, loanDebt.model);
  //     assert.equal(debt.creator, loanDebt.creator);
  //     assert.equal(debt.oracle, loanDebt.oracle);

  //     //Check config endPoint
  //     loanConfigs = await installmentModel.configs(id);
  //     assert.equal(config.data.installments, loanConfigs.installments);
  //     assert.equal(config.data.time_unit, loanConfigs.timeUnit);
  //     assert.equal(config.data.duration, loanConfigs.duration);
  //     assert.equal(config.data.lent_time, loanConfigs.lentTime); 
  //     assert.equal(config.data.cuota, loanConfigs.cuota);    
  //     assert.equal(config.data.interest_rate, loanConfigs.interestRate);

  //     // Check loan endPoint
  //     assert.equal(loanAfterLend.open, false);
  //     assert.equal(loanAfterLend.approved, true);
  //     assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
  //     assert.equal(loanAfterLend.status, await loanManager.getStatus(id));

  //     // Transfer debt 
  //     await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, {from: lenderAddress });

  //     assert.equal(newLenderAddress, await loanManager.ownerOf(id));

  //     await sleep(5000);
  //     loanJsonAfterTransfer = await api.get_loan(id);
  //     loanAfterTransfer = loanJsonAfterTransfer.content;

  //     assert.equal(newLenderAddress, loanAfterTransfer.lender);

  //     // Should not be able to transfer if the sender is not the owner of the debt
  //     try {
  //     error = await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, {from: lenderAddress });
  //     } catch (e) {
  //       error = 'Not the owner of the debt';
  //     }
  //     assert.equal(error, 'Not the owner of the debt');

  //   });
  // });

  // // FLUJO 8 - REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW

  // describe('Flujo 8: REQUEST  + APPROVE + LEND + TOTALPAY + WITHDRAW', function () {

  //   it("should create a new loan Request, approve, lend, total pay and withdraw", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;
    
  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //     // Approve Loan by borower
  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.lend(
  //         id,                 // Index
  //         [],                 // OracleData
  //         '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //         '0', // Cosigner limit
  //         [],                 // Cosigner data
  //         { from: lenderAddress }    // Owner/Lender
  //     );

  //     await sleep(5000);
  //     // Query the API for Debt data
  //     debtJson = await api.get_debt(id);
  //     debt = debtJson.content;

  //     // Query the API for config data
  //     configJson = await api.get_config(id);
  //     config = configJson.content;

  //     // Query the API for Loan data
  //     loanJsonAfterLend = await api.get_loan(id);
  //     loanAfterLend = loanJsonAfterLend.content;

  //     //Check Debt endpoint
  //     loanDebt = await debtEngine.debts(id);
  //     assert.equal(debt.error, loanDebt.error);
  //     assert.equal(debt.balance, loanDebt.balance);
  //     assert.equal(debt.model, loanDebt.model);
  //     assert.equal(debt.creator, loanDebt.creator);
  //     assert.equal(debt.oracle, loanDebt.oracle);

  //     //Check config endPoint
  //     loanConfigs = await installmentModel.configs(id);
  //     assert.equal(config.data.installments, loanConfigs.installments);
  //     assert.equal(config.data.time_unit, loanConfigs.timeUnit);
  //     assert.equal(config.data.duration, loanConfigs.duration);
  //     assert.equal(config.data.lent_time, loanConfigs.lentTime); 
  //     assert.equal(config.data.cuota, loanConfigs.cuota);    
  //     assert.equal(config.data.interest_rate, loanConfigs.interestRate);

  //     // Check loan endPoint
  //     assert.equal(loanAfterLend.open, false);
  //     assert.equal(loanAfterLend.approved, true);
  //     assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
  //     assert.equal(loanAfterLend.status, await loanManager.getStatus(id));

  //     // Pay loan
  //     await rcnToken.setBalance(borrowerAddress, web3.utils.toWei("120", "ether"));
  //     await rcnToken.approve(debtEngine.address, web3.utils.toWei("120", "ether"), { from: borrowerAddress });


  //     await debtEngine.pay(id, web3.utils.toWei("100", "ether"), borrowerAddress, [], { from: borrowerAddress });
  //     // Test pay
  //     await sleep(5000);
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");

  //     // Test pay, test total pay
  //     await debtEngine.pay(id, web3.utils.toWei("20", "ether"), borrowerAddress, [], { from: borrowerAddress });

  //     await sleep(5000)
  //     loanAPI = (await api.get_loan(id)).content;
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");
  //     assert.equal(loanAPI.status, await loanManager.getStatus(id), "Status payed")
  //     assert.isAtLeast(parseInt(debtAPI.balance), parseInt(loanAPI.amount), "balance >= amount");
  //     assert.equal(parseInt(debtAPI.balance), parseInt(loan.descriptor.total_obligation), "balance eq descriptor total_obligation");

  //     // withdraw
  //     balance_lender_before_withdraw = await rcnToken.balanceOf(lenderAddress);
  //     await debtEngine.withdrawPartial(id, lenderAddress, web3.utils.toWei("120", "ether"), { from: lenderAddress });
  //     await sleep(5000);

  //     debtAPI = (await api.get_debt(id)).content;
  //     debtETH = await debtEngine.debts(id);

  //     balance_lender_after_withdraw = parseInt(await rcnToken.balanceOf(lenderAddress));
  //     total_balance = balance_lender_before_withdraw + parseInt(web3.utils.toWei("120", "ether"));
      
  //     assert.equal(parseInt(debtAPI.balance), parseInt(debtETH.balance), "balance eq");
  //     assert.equal(total_balance, balance_lender_after_withdraw, "balance lender eq");
  //   });
  // });

  // // FLUJO 9 - EXPIRED

  // describe('Flujo 9: REQUEST LOAN EXPIRED', function () {

  //   it("should check if a loan is expired ", async () => {
  //     delta = 2

  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = (await getBlockTime()) + delta;

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;

  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus);
      
  //     await increaseTime(5);


  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     try {
  //       await loanManager.lend(
  //         id,
  //         [],
  //         '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //         '0', // Cosigner limit
  //         [],                 // Cosigner data
  //         { from: lenderAddress }
  //       );
  //       error = false;
  //     } catch (e){
  //       error = true;
  //     }
  //     assert.isTrue(error, "lend expired");

  //   });
  // });

  // E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW

  // describe(' E2E integration Test - REQUEST  + APPROVE + LEND + TRANSFER + TOTALPAY + WITHDRAW', function () {

  //   // CREATE A REQUEST

  //   step("should create a new loan Request", async () => {
  //     cuota = '10000000000000000000';
  //     punInterestRate = '1555200000000';
  //     installments = '12';
  //     duration = '2592000';
  //     timeUnit = '2592000';
  //     amount = '100000000000000000000';
  //     oracle = '0x0000000000000000000000000000000000000000';
  //     expiration = '1578571215';

  //     // Brodcast transaction to the network -Request Loan  and  Calculate the Id of the loan with helper function
  //     loanIdandData = await requestLoan(cuota, punInterestRate, installments, duration, timeUnit, amount, oracle, expiration);
  //     id = loanIdandData[0];
  //     loanData = loanIdandData[1];

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJson = await api.get_loan(id);
  //     loan = loanJson.content;

  //     // Query blockchain for loan data 
  //     getRequestId = await loanManager.requests(id);
  //     getBorrower = await loanManager.getBorrower(id);
  //     getCreator = await loanManager.getCreator(id);
  //     getOracle = await loanManager.getOracle(id);
  //     getCosigner = await loanManager.getCosigner(id);
  //     getCurrency = await loanManager.getCurrency(id);
  //     getAmount = await loanManager.getAmount(id);
  //     getExpirationRequest = await loanManager.getExpirationRequest(id);
  //     getApproved = await loanManager.getApproved(id);
  //     // getDueTime = await loanManager.getDueTime(id);
  //     getLoanData = await loanManager.getLoanData(id);
  //     getStatus = await loanManager.getStatus(id);

  //     // get descriptor Values from InstallmentModel
  //     simFirstObligationTimeAndAmount = await installmentModel.simFirstObligation(loanData);
  //     totalObligation = await installmentModel.simTotalObligation(loanData);
  //     duration = await installmentModel.simDuration(loanData);
  //     durationPercentage = ((totalObligation / parseInt(amount)) - 1) * 100
  //     interestRate = (durationPercentage * 360 * 86000) / duration;
  //     frequency = await installmentModel.simFrequency(loanData);
  //     installments = await installmentModel.simInstallments(loanData);


  //     // Compare both results (API and blockchain) and validate consistency
  //     assert.equal(loan.id, id);
  //     assert.equal(loan.open, getRequestId.open);
  //     assert.equal(loan.approved, getApproved);
  //     assert.equal(loan.position, getRequestId.position);
  //     assert.equal(loan.expiration, getExpirationRequest);
  //     assert.equal(loan.amount, getAmount);
  //     // assert.equal(loan.cosigner, getCosigner);
  //     assert.equal(loan.model, getRequestId.model);
  //     assert.equal(loan.creator, getCreator);
  //     assert.equal(loan.oracle, getOracle);
  //     assert.equal(loan.borrower, getBorrower);
  //     assert.equal(loan.salt, getRequestId.salt)
  //     assert.equal(loan.loanData, getLoanData);
  //     //loan.created time value only in API
  //     assert.equal(loan.descriptor.first_obligation, simFirstObligationTimeAndAmount.amount);
  //     assert.equal(loan.descriptor.total_obligation, totalObligation);
  //     assert.equal(loan.descriptor.duration, duration);
  //     assert.equal(loan.descriptor.interest_rate, interestRate);
  //     assert.equal(loan.descriptor.frequency, frequency);
  //     assert.equal(loan.descriptor.installments, installments);

  //     //assert.equal(loan.currency, getCurrency);
  //     assert.equal(loan.lender, null);
  //     assert.equal(loan.status, getStatus, 'status not equal');
  //     //assert.equal(loan.canceled, )

  //   });

  //   // APPROVE 

  //   step("should approve the loan request by the borrower", async () => {

  //     await loanManager.approveRequest(id, { from: borrowerAddress });

  //     // sleep 5 seconds for the listener to capture the event , process, saved it database and resourse should be available in API
  //     await sleep(5000);
  //     // Query the API for Loan data
  //     loanJsonAfterRequest = await api.get_loan(id);
  //     loanAfterRequest = loanJsonAfterRequest.content;

  //     const getApproved = await loanManager.getApproved(id);

  //     assert.equal(true, loanAfterRequest.approved);
  //     assert.equal(true, getApproved);
  //   });

  //   // LEND

  //   step("should lend", async () => {

  //     // buy Rcn for lender address 
  //     await rcnToken.setBalance(lenderAddress, amount);

  //     balanceOfLender = await rcnToken.balanceOf(lenderAddress);

  //     await rcnToken.approve(loanManager.address, amount, { from: lenderAddress });

  //     await loanManager.lend(
  //       id,                 // Index
  //       [],                 // OracleData
  //       '0x0000000000000000000000000000000000000000',   // Cosigner  0x address
  //       '0', // Cosigner limit
  //       [],                 // Cosigner data
  //       { from: lenderAddress }    // Owner/Lender
  //     );

  //     await sleep(5000);
  //     // Query the API for Debt data
  //     debtJson = await api.get_debt(id);
  //     debt = debtJson.content;

  //     // Query the API for config data
  //     configJson = await api.get_config(id);
  //     config = configJson.content;

  //     // Query the API for Loan data
  //     loanJsonAfterLend = await api.get_loan(id);
  //     loanAfterLend = loanJsonAfterLend.content;

  //     //Check Debt endpoint
  //     loanDebt = await debtEngine.debts(id);

  //     assert.equal(debt.error, loanDebt.error);
  //     assert.equal(debt.balance, loanDebt.balance);
  //     assert.equal(debt.model, loanDebt.model);
  //     assert.equal(debt.creator, loanDebt.creator);
  //     assert.equal(debt.oracle, loanDebt.oracle);

  //     //Check config endPoint
  //     loanConfigs = await installmentModel.configs(id);
  //     assert.equal(config.data.installments, loanConfigs.installments);
  //     assert.equal(config.data.time_unit, loanConfigs.timeUnit);
  //     assert.equal(config.data.duration, loanConfigs.duration);
  //     assert.equal(config.data.lent_time, loanConfigs.lentTime);
  //     assert.equal(config.data.cuota, loanConfigs.cuota);
  //     assert.equal(config.data.interest_rate, loanConfigs.interestRate);

  //     // Check loan endPoint
  //     assert.equal(loanAfterLend.open, false);
  //     assert.equal(loanAfterLend.approved, true);
  //     assert.equal(loanAfterLend.lender, await loanManager.ownerOf(id));
  //     assert.equal(loanAfterLend.status, await loanManager.getStatus(id));
  //   });

  //   // TRANSFER DEBT 

  //   step("should transfer the lender debt to another address", async () => {

  //     // Transfer debt 
  //     await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });

  //     assert.equal(newLenderAddress, await loanManager.ownerOf(id));

  //     await sleep(5000);
  //     loanJsonAfterTransfer = await api.get_loan(id);
  //     loanAfterTransfer = loanJsonAfterTransfer.content;

  //     assert.equal(newLenderAddress, loanAfterTransfer.lender);

  //     // Should not be able to transfer if the sender is not the owner of the debt
  //     try {
  //       error = await debtEngine.safeTransferFrom(lenderAddress, newLenderAddress, id, { from: lenderAddress });
  //     } catch (e) {
  //       error = 'Not the owner of the debt';
  //     }
  //     assert.equal(error, 'Not the owner of the debt');

  //   });

  //   // TOTAL PAY 

  //   step("should pay the total of the debt", async () => {

  //     // Pay loan
  //     await rcnToken.setBalance(borrowerAddress, web3.utils.toWei("120", "ether"));
  //     await rcnToken.approve(debtEngine.address, web3.utils.toWei("120", "ether"), { from: borrowerAddress });


  //     await debtEngine.pay(id, web3.utils.toWei("100", "ether"), borrowerAddress, [], { from: borrowerAddress });
  //     // Test pay
  //     await sleep(5000);
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");

  //     // Test pay, test total pay
  //     await debtEngine.pay(id, web3.utils.toWei("20", "ether"), borrowerAddress, [], { from: borrowerAddress });

  //     await sleep(5000)
  //     loanAPI = (await api.get_loan(id)).content;
  //     debtAPI = (await api.get_debt(id)).content;
  //     stateAPI = (await api.get_state(id)).content;
  //     debtETH = await debtEngine.debts(id);
  //     stateETH = await installmentModel.states(id);

  //     assert.equal(debtETH.balance, debtAPI.balance, "DEBT Balance not eq :(");
  //     assert.equal(stateETH.paid, stateAPI.paid, "State paid not eq :(");
  //     assert.equal(loanAPI.status, await loanManager.getStatus(id), "Status payed")
  //     assert.isAtLeast(parseInt(debtAPI.balance), parseInt(loanAPI.amount), "balance >= amount");
  //     assert.equal(parseInt(debtAPI.balance), parseInt(loan.descriptor.total_obligation), "balance eq descriptor total_obligation");
  //   });

  //   // WITHDRAW 

  //   step("should withdraw funds for lender", async () => {

  //     // withdraw
  //     balance_lender_before_withdraw = await rcnToken.balanceOf(newLenderAddress);
  //     await debtEngine.withdrawPartial(id, newLenderAddress, web3.utils.toWei("120", "ether"), { from: newLenderAddress });
  //     await sleep(5000);

  //     debtAPI = (await api.get_debt(id)).content;
  //     debtETH = await debtEngine.debts(id);

  //     balance_lender_after_withdraw = parseInt(await rcnToken.balanceOf(newLenderAddress));
  //     total_balance = balance_lender_before_withdraw + parseInt(web3.utils.toWei("120", "ether"));

  //     assert.equal(parseInt(debtAPI.balance), parseInt(debtETH.balance), "balance eq");
  //     assert.equal(total_balance, balance_lender_after_withdraw, "balance lender eq");
  //   });



  // });


});
