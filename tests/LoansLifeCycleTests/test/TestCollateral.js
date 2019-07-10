const Collateral = artifacts.require('Collateral');
const TestModel = artifacts.require('TestModel');
const LoanManager = artifacts.require('LoanManager');
const DebtEngine = artifacts.require('DebtEngine');
const TestToken = artifacts.require('TestToken');
const TestConverter = artifacts.require('TestConverter');
const TestRateOracle = artifacts.require('TestRateOracle');

const api = require('./api.js');

const Helper = require('./Helper.js');
const BN = web3.utils.BN;
const expect = require('chai')
  .use(require('bn-chai')(BN))
  .expect;

function bn (number) {
  return new BN(number);
}

function rand (min = 0, max = 2 ** 53) {
  return Math.floor(Math.random() * (max + 1 - min)) + min;
}

function min (x, y, z) {
  if (x.lte(y) && x.lte(z)) {
    return x;
  } else {
    return y.lte(z) ? y : x;
  }
}

function divceil (x, y) {
  if (x.mod(y).eq(bn('0'))) {
    return x.div(y);
  } else {
    return x.div(y).add(bn('1'));
  }
}

const WEI = bn('10').pow(bn('18'));
const BASE = bn('10000');

contract('Test Collateral API', function (accounts) {
  let rcn;
  let auxToken;
  let loanManager;
  let debtEngine;
  let model;
  let collateral;
  let converter;
  let oracle;

  // Random Loan
  async function randParams () {
    const BASE_INT = 10000;

    const salt = bn(web3.utils.randomHex(32));
    const loanAmount = rand();
    const expiration = (await Helper.getBlockTime()) + rand(BASE_INT);

    const entryAmount = rand();
    const burnFee = rand(0, BASE_INT);
    const rewardFee = rand(0, BASE_INT - burnFee);
    const liquidationRatio = rand(BASE_INT, 20000);
    const balanceRatio = rand(liquidationRatio + burnFee + rewardFee, 30000);

    return {
      loan: {
        salt: salt,
        borrower: Helper.borrower,
        model: model.address,
        oracle: Helper.address0x,
        amount: loanAmount,
        expiration: expiration,
        loanData: await model.encodeData(loanAmount, expiration),
      },
      entry: {
        amount: entryAmount,
        liquidationRatio: liquidationRatio,
        balanceRatio: balanceRatio,
        burnFee: burnFee,
        rewardFee: rewardFee,
        creator: Helper.creator,
      },
    };
  };

  async function getId (promise) {
    const receipt = await promise;
    const event = receipt.logs.find(l => l.event === 'Requested');
    assert.ok(event);
    return event.args._id;
  }

  function roundCompare (x, y) {
    const z = x.sub(y).abs();
    assert.isTrue(z.gte(bn('0')) || z.lte(bn('2')),
      'Diff between ' +
            x.toString() +
            ' to ' +
            y.toString() +
            ' should be less than 1 and is ' +
            z.toString()
    );
  }

  async function requestLoan (params) {
    return getId(loanManager.requestLoan(
      params.loan.amount,            // Amount
      params.loan.model,             // Model
      params.loan.oracle,            // Oracle
      params.loan.borrower,          // Borrower
      params.loan.salt,              // salt
      params.loan.expiration,        // Expiration
      params.loan.loanData,          // Loan data
      { from: params.loan.borrower } // Creator
    ));
  }

  before('Create contracts', async function () {
    converter = await TestConverter.new({ from: Helper.creator });
    oracle = await TestRateOracle.new({ from: Helper.creator });
    rcn = await TestToken.new({ from: Helper.creator });
    auxToken = await TestToken.new({ from: Helper.creator });
    debtEngine = await DebtEngine.new(rcn.address, { from: Helper.creator });
    loanManager = await LoanManager.new(debtEngine.address, { from: Helper.creator });
    model = await TestModel.new({ from: Helper.creator });
    await model.setEngine(debtEngine.address, { from: Helper.creator });
    // Collateral deploy
    collateral = await Collateral.new(loanManager.address, { from: Helper.creator });
    await collateral.setConverter(converter.address, { from: Helper.creator });

    // Log contracts addreses
    console.log('converter: ' + converter.address);
    console.log('oracle: ' + oracle.address);
    console.log('rcn: ' + rcn.address);
    console.log('auxToken: ' + auxToken.address);
    console.log('debtEngine: ' + debtEngine.address);
    console.log('loanManager: ' + loanManager.address);
    console.log('model: ' + model.address);
    console.log('collateral: ' + collateral.address);
    console.log();
  });

  async function setApprove (amount, from, to) {
    await auxToken.setBalance(from, amount);
    await auxToken.approve(to, amount, { from: from });
  };

  describe('Function create', function () {
    it('Should create a new collateral', async function () {
      const params = await randParams();
      const loanId = await requestLoan(params);
      console.log(params);
      await setApprove(params.entry.amount, params.entry.creator, collateral.address);
      //console.log(await api.getLoan(loanId));

      const Created = await Helper.toEvents(
        collateral.create(
          loanId,                             // debtId
          auxToken.address,                   // token
          params.entry.amount,           // amount
          params.entry.liquidationRatio, // liquidationRatio
          params.entry.balanceRatio,     // balanceRatio
          params.entry.burnFee,          // burnFee
          params.entry.rewardFee,        // rewardFee
          { from: params.entry.creator }
        ),
        'Created'
      );

      const entryApi = (await api.getEntry(Created._id)).content;
      console.log(entryApi);
/*
      expect(Created._id).to.eq.BN(collateralId);
      assert.equal(Created._debtId, loanId);
      assert.equal(Created._token, auxToken.address);
      expect(Created._amount).to.eq.BN(collateralAmount);
      expect(Created._liquidationRatio).to.eq.BN(liquidationRatio);
      expect(Created._balanceRatio).to.eq.BN(balanceRatio);
      expect(Created._burnFee).to.eq.BN(burnFee);
      expect(Created._rewardFee).to.eq.BN(rewardFee);

      const entry = await collateral.entries(collateralId);
      expect(entry.liquidationRatio).to.eq.BN(liquidationRatio);
      expect(entry.balanceRatio).to.eq.BN(balanceRatio);
      expect(entry.burnFee).to.eq.BN(burnFee);
      expect(entry.rewardFee).to.eq.BN(rewardFee);
      assert.equal(entry.token, auxToken.address);
      assert.equal(entry.debtId, loanId);
      expect(entry.amount).to.eq.BN(collateralAmount);

      expect(await auxToken.balanceOf(collateral.address)).to.eq.BN(prevAuxTokenBal.add(collateralAmount));
      assert.equal(await collateral.ownerOf(collateralId), creator);*/
    });
  });
});
