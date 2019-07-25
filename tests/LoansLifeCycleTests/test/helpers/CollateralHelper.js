const Helper = require('./Helper.js');
const BN = web3.utils.BN;
const expect = require('chai')
    .use(require('bn-chai')(BN))
    .expect;

function bn (number) {
    if (!(number instanceof String)) {
        number.toString();
    }
    return new BN(number);
}

function divceil (x, y) {
    if (x.mod(y).eq(bn(0))) {
        return x.div(y);
    } else {
        return x.div(y).add(bn(1));
    }
}

function rand (min = 0, max = 2 ** 53) {
    if (min instanceof BN) {
        min = min.toNumber();
    }
    if (max instanceof BN) {
        max = max.toNumber();
    }
    assert.isAtMost(min, max);
    return bn(Math.floor(Math.random() * (max + 1 - min)) + min);
}

const WEI = bn(10).pow(bn(18));
const BASE = bn(10000);

class EntryBuilder {
    constructor (creator, auxToken) {
        this.oracle = { address: Helper.address0x };
        // Loan
        this.loanId = undefined;
        this.loanAmount = rand(1, 200000000);
        this.loanAmountRcn = this.loanAmount;
        this.expirationDelta = rand(1000, BASE);
        this.durationDelta = rand(1000, BASE);
        // To oracle
        this.oracleData = [];
        this.tokens = WEI;
        this.equivalent = WEI;
        // To converter
        this.rateFromRCN = WEI;
        this.rateToRCN = WEI;
        // Entry
        this.createFrom = creator;
        this.burnFee = rand(0, BASE);
        this.rewardFee = rand(0, BASE.sub(this.burnFee).sub(bn(1)));
        this.liquidationRatio = rand(BASE, 20000);
        this.balanceRatio = rand(this.liquidationRatio.add(this.burnFee).add(this.rewardFee), 30000);
        this.collateralToken = auxToken;
    }

    with (attr, value) {
        this[attr] = value;
        return this;
    }

    async build (rcn, converter, model, loanManager, borrower, collateral, creator) {
        if (rcn.address !== this.collateralToken.address) {
            await converter.setRate(rcn.address, this.collateralToken.address, this.rateFromRCN);
            await converter.setRate(this.collateralToken.address, rcn.address, this.rateToRCN);
        }

        const salt = bn(web3.utils.randomHex(32));
        const now = bn(await Helper.getBlockTime());
        const expiration = now.add(this.expirationDelta);
        const duration = now.add(this.durationDelta);

        const loanData = await model.encodeData(this.loanAmount, duration);

        if (this.loanId === undefined) {
            this.loanId = await getId(loanManager.requestLoan(
                this.loanAmount,     // Amount
                model.address,       // Model
                this.oracle.address, // Oracle
                borrower,            // Borrower
                salt,                // salt
                expiration,          // Expiration
                loanData,            // Loan data
                { from: borrower }   // Creator
            ));
            if (this.oracle.address !== Helper.address0x) {
                this.oracleData = await this.oracle.encodeRate(this.tokens, this.equivalent);
                this.loanAmountRcn = await this.currencyToRCN();
            }
            if (this.onlyTakeALoan) {
                return this.loanId;
            }
        }

        if (this.entryAmount === undefined) {
            const loanAmountInColl = await this.RCNToCollateral(this.loanAmountRcn);
            const minEntryAmount = divceil(loanAmountInColl.mul(this.balanceRatio.add(BASE)), BASE);
            this.entryAmount = rand(minEntryAmount, 40000000000);
        }

        this.id = await collateral.getEntriesLength();

        await this.collateralToken.setBalance(creator, this.entryAmount);
        await this.collateralToken.approve(collateral.address, this.entryAmount, { from: creator });

        const collateralSnap = await Helper.balanceSnap(this.collateralToken, collateral.address);
        const creatorSnap = await Helper.balanceSnap(this.collateralToken, this.createFrom);

        const createdEvent = await Helper.toEvents(
            collateral.create(
                this.loanId,                  // debtId
                this.collateralToken.address, // token
                this.entryAmount,             // amount
                this.liquidationRatio,        // liquidationRatio
                this.balanceRatio,            // balanceRatio
                this.burnFee,                 // burnFee
                this.rewardFee,               // rewardFee
                { from: this.createFrom }     // sender
            ),
            'Created'
        );

        // Control collateral creation event
        expect(createdEvent._id).to.eq.BN(this.id);
        assert.equal(createdEvent._debtId, this.loanId);
        assert.equal(createdEvent._token, this.collateralToken.address);
        expect(createdEvent._amount).to.eq.BN(this.entryAmount);
        expect(createdEvent._liquidationRatio).to.eq.BN(this.liquidationRatio);
        expect(createdEvent._balanceRatio).to.eq.BN(this.balanceRatio);
        expect(createdEvent._burnFee).to.eq.BN(this.burnFee);
        expect(createdEvent._rewardFee).to.eq.BN(this.rewardFee);

        // Expect entry creation
        const entry = await collateral.entries(this.id);
        expect(entry.liquidationRatio).to.eq.BN(this.liquidationRatio);
        expect(entry.balanceRatio).to.eq.BN(this.balanceRatio);
        expect(entry.burnFee).to.eq.BN(this.burnFee);
        expect(entry.rewardFee).to.eq.BN(this.rewardFee);
        assert.equal(entry.token, this.collateralToken.address);
        assert.equal(entry.debtId, this.loanId);
        expect(entry.amount).to.eq.BN(this.entryAmount);

        // Owner and balance of colalteral
        await creatorSnap.requireDecrease(this.entryAmount);
        await collateralSnap.requireIncrease(this.entryAmount);
        assert.equal(await collateral.ownerOf(this.id), creator);

        return this;
    }

    totalFee () {
        return this.burnFee.add(this.rewardFee);
    }

    toRewardFee (amount) {
        return amount.mul(BASE.add(this.rewardFee)).div(BASE).sub(amount);
    }

    toBurnFee (amount) {
        return amount.mul(BASE.add(this.burnFee)).div(BASE).sub(amount);
    }

    withFee (amount) {
        return this.toRewardFee(amount).add(this.toBurnFee(amount)).add(amount);
    }

    async currencyToRCN (amount = this.loanAmount) {
        return this.oracle.getReturn(amount, this.oracleData);
    }

    async collateralToRCN (amount = this.entryAmount, converter, auxToken, rcn) {
        return converter.getReturn(auxToken.address, rcn.address, amount);
    }

    async RCNToCollateral (amount, converter, auxToken, rcn) {
        return converter.getReturn(rcn.address, auxToken.address, amount);
    }
}

const deposit = async function (tok, col, id, amount, from, collateral, auxToken) {
    const prevEntry = await collateral.entries(id);
    await tok.setBalance(from, amount);
    await tok.approve(col.address, amount, { from: from });

    const collateralSnap = await Helper.balanceSnap(auxToken, collateral.address);
    const fromSnap = await Helper.balanceSnap(auxToken, from);
    const Deposited = await Helper.toEvents(
        col.deposit(
            id,
            amount,
            { from: from }
        ),
        'Deposited'
    );

    // Test events
    expect(Deposited._id).to.eq.BN(id);
    expect(Deposited._amount).to.eq.BN(amount);

    // Test collateral entry
    const entry = await collateral.entries(id);
    // Should remain the same
    expect(entry.liquidationRatio).to.eq.BN(prevEntry.liquidationRatio);
    expect(entry.balanceRatio).to.eq.BN(prevEntry.balanceRatio);
    expect(entry.burnFee).to.eq.BN(prevEntry.burnFee);
    expect(entry.rewardFee).to.eq.BN(prevEntry.rewardFee);
    expect(entry.token).to.equal(prevEntry.token);
    expect(entry.debtId).to.equal(prevEntry.debtId);

    // Should increase by amount
    expect(entry.amount).to.eq.BN(amount.add(prevEntry.amount));
    await collateralSnap.requireIncrease(amount);

    // Should decreae by amount
    await fromSnap.requireDecrease(amount);

    // Restore balance
    await fromSnap.restore();
};

const withdraw = async function (id, to, amount, from, data = [], collateral, auxToken) {
    const prevEntry = await collateral.entries(id);

    const collateralSnap = await Helper.balanceSnap(auxToken, collateral.address);
    const toSnap = await Helper.balanceSnap(auxToken, to);

    const Withdrawed = await Helper.toEvents(
        collateral.withdraw(
            id,
            to,
            amount,
            data,
            { from: from }
        ),
        'Withdrawed'
    );

    // Assert events
    expect(Withdrawed._id).to.eq.BN(id);
    expect(Withdrawed._to).to.equal(from);
    expect(Withdrawed._amount).to.eq.BN(amount);

    // Validate entry
    const entry = await collateral.entries(id);
    // Should remain the same
    expect(entry.liquidationRatio).to.eq.BN(prevEntry.liquidationRatio);
    expect(entry.balanceRatio).to.eq.BN(prevEntry.balanceRatio);
    expect(entry.burnFee).to.eq.BN(prevEntry.burnFee);
    expect(entry.rewardFee).to.eq.BN(prevEntry.rewardFee);
    expect(entry.token).to.equal(prevEntry.token);
    expect(entry.debtId).to.equal(prevEntry.debtId);

    // Should decrease by amount
    expect(entry.amount).to.eq.BN(prevEntry.amount.sub(amount));
    await collateralSnap.requireDecrease(amount);

    // Shoud increase by amount
    await toSnap.requireIncrease(amount);
    await toSnap.restore();
};

const lend = async function (entry, expectLoanAmount, rcn, lender, loanManager, collateral, model) {
    const lenderSnap = await Helper.balanceSnap(rcn, lender);

    await rcn.setBalance(lender, entry.loanAmountRcn);
    await rcn.approve(loanManager.address, entry.loanAmountRcn, { from: lender });

    await loanManager.lend(
        entry.loanId,               // Loan ID
        entry.oracleData,           // Oracle data
        collateral.address,         // Collateral cosigner address
        bn(0),                      // Collateral cosigner cost
        Helper.toBytes32(entry.id), // Collateral ID reference
        { from: lender }
    );

    if (expectLoanAmount !== undefined) {
        assert.isTrue(expectLoanAmount.gt(entry.loanAmount), 'The new amount should be greater');
        await model.addDebt(entry.loanId, expectLoanAmount.sub(entry.loanAmount));
        entry.loanAmount = entry.loanAmount.add(expectLoanAmount.sub(entry.loanAmount));
        entry.loanAmountRcn = await entry.currencyToRCN();
    }

    // TODO Check entry status change
    await lenderSnap.restore();
};

const requireDeleted = async function (entryId, loanId, collateral) {
    const entry = await collateral.entries(entryId);
    expect(entry.liquidationRatio).to.eq.BN(0);
    expect(entry.balanceRatio).to.eq.BN(0);
    expect(entry.burnFee).to.eq.BN(0);
    expect(entry.rewardFee).to.eq.BN(0);
    assert.equal(entry.token, Helper.address0x);
    assert.equal(entry.debtId, Helper.bytes320x);
    expect(entry.amount).to.eq.BN(0);

    expect(await collateral.debtToEntry(loanId)).to.eq.BN(0);
};

const getId = async function (promise) {
    const receipt = await promise;
    const event = receipt.logs.find(l => l.event === 'Requested');
    assert.ok(event);
    return event.args._id;
};

const roundCompare = function (x, y) {
    const z = x.sub(y).abs();
    assert.isTrue(z.gte(bn(0)) || z.lte(bn(2)),
        'Diff between ' +
        x.toString() +
        ' to ' +
        y.toString() +
        ' should be less than 1 and is ' +
        z.toString()
    );
};

module.exports = {
    deposit: deposit,
    withdraw: withdraw,
    lend: lend,
    requireDeleted: requireDeleted,
    roundCompare: roundCompare,
    EntryBuilder: EntryBuilder,
};
