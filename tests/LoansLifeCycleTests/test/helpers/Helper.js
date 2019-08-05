module.exports.address0x = '0x0000000000000000000000000000000000000000';
module.exports.bytes320x = '0x0000000000000000000000000000000000000000000000000000000000000000';

module.exports.STATUS_ONGOING = '1';
module.exports.STATUS_PAID = '2';
module.exports.STATUS_ERROR = '4';

module.exports.arrayToBytesOfBytes32 = (array) => {
    let bytes = '0x';
    for (let i = 0; i < array.length; i++) {
        let bytes32 = module.exports.toBytes32(array[i]).toString().replace('0x', '');
        if (bytes32.length < 64) {
            const diff = 64 - bytes32.length;
            bytes32 = '0'.repeat(diff) + bytes32;
        }
        bytes += bytes32;
    }

    return bytes;
};

module.exports.toBytes32 = (source) => {
    source = web3.utils.toHex(source);
    const rl = 64;
    source = source.toString().replace('0x', '');
    if (source.length < rl) {
        const diff = 64 - source.length;
        source = '0'.repeat(diff) + source;
    }
    return '0x' + source;
};

module.exports.increaseTime = function increaseTime (duration) {
    const id = Date.now();

    return new Promise((resolve, reject) => {
        web3.currentProvider.send({
            jsonrpc: '2.0',
            method: 'evm_increaseTime',
            params: [duration],
            id: id,
        },
        err1 => {
            if (err1) return reject(err1);

            web3.currentProvider.send({
                jsonrpc: '2.0',
                method: 'evm_mine',
                id: id + 1,
            },
            (err2, res) => {
                return err2 ? reject(err2) : resolve(res);
            });
        });
    });
};

module.exports.isRevertErrorMessage = (error) => {
    if (error.message.search('invalid opcode') >= 0) return true;
    if (error.message.search('revert') >= 0) return true;
    if (error.message.search('out of gas') >= 0) return true;
    return false;
};

module.exports.getBlockTime = async () => {
    return (await web3.eth.getBlock(await web3.eth.getBlockNumber())).timestamp;
};

module.exports.assertThrow = async (promise) => {
    try {
        await promise;
    } catch (error) {
        const invalidJump = error.message.search('invalid JUMP') >= 0;
        const revert = error.message.search('revert') >= 0;
        const invalidOpcode = error.message.search('invalid opcode') > 0;
        const outOfGas = error.message.search('out of gas') >= 0;
        assert(
            invalidJump || outOfGas || revert || invalidOpcode,
            'Expected throw, got \'' + error + '\' instead',
        );
        return;
    }
    assert.fail('Expected throw not received');
};

// the promiseFunction should be a function
module.exports.tryCatchRevert = async (promise, message) => {
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

module.exports.toInterestRate = (interest) => {
    const secondsInYear = 360 * 86400;
    const rawInterest = Math.floor(10000000 / interest);
    return rawInterest * secondsInYear;
};

module.exports.buyTokens = async (token, amount, account) => {
    const prevAmount = await token.balanceOf(account);
    await token.buyTokens(account, { from: account, value: amount / 4000 });
    const newAmount = await token.balanceOf(account);
    assert.equal(newAmount.sub(prevAmount), amount.toString(), 'Should have minted tokens');
};

module.exports.searchEvent = (tx, eventName) => {
    const event = tx.logs.filter(x => x.event === eventName).map(x => x.args);
    assert.equal(event.length, 1, 'Should have only one ' + eventName);
    return event[0];
};

module.exports.toEvents = async (promise, ...events) => {
    const logs = (await promise).logs;

    let eventObjs = [].concat.apply(
        [], events.map(
            event => logs.filter(
                log => log.event === event
            )
        )
    );

    if (eventObjs.length === 0 || eventObjs.some(x => x === undefined)) {
        console.warn('\t\u001b[91m\u001b[2m\u001b[1mError: The event dont find');
        assert.fail();
    }
    eventObjs = eventObjs.map(x => x.args);
    return (eventObjs.length === 1) ? eventObjs[0] : eventObjs;
};

module.exports.eventNotEmitted = async (receipt, eventName) => {
    const logsCount = receipt.logs.length;
    assert.equal(logsCount, 0, 'Should have not emitted the event ' + eventName);
};

module.exports.almostEqual = async (p1, p2, reason, margin = 3) => {
    assert.isBelow(
        Math.abs((await p1).toNumber() - (await p2)),
        margin,
        reason
    );
};

module.exports.checkState = async (stateEth, stateApi) => {
    assert.equal(stateEth.status, stateApi.status, 'state.status eq');
    assert.equal(stateEth.clock, stateApi.clock, 'state.clock eq');
    assert.equal(stateEth.lastPayment, stateApi.last_payment, 'state.last_payment eq');
    assert.equal(stateEth.paid, stateApi.paid, 'state.paid eq');
    assert.equal(stateEth.paidBase, stateApi.paid_base, 'state.paid_base eq');
    assert.equal(stateEth.interest, stateApi.interest, 'state.interest eq');
};

module.exports.checkConfig = async (configEth, configApi) => {
    assert.equal(configEth.installments, configApi.data.installments, 'config.installments eq');
    assert.equal(configEth.timeUnit, configApi.data.time_unit, 'config.time_unit eq');
    assert.equal(configEth.duration, configApi.data.duration, 'config.duration eq');
    assert.equal(configEth.lentTime, configApi.data.lent_time, 'config.lent_time eq');
    assert.equal(configEth.cuota, configApi.data.cuota, 'config.cuota eq');
    assert.equal(configEth.interestRate, configApi.data.interest_rate, 'config.interest_rate eq');
};

module.exports.checkDebt = async (debtEth, debtApi) => {
    assert.equal(debtEth.error, debtApi.error, 'debt.error eq');
    assert.equal(debtEth.balance, debtApi.balance, 'debt.balance eq');
    assert.equal(debtEth.model, debtApi.model, 'debt.model eq');
    assert.equal(debtEth.creator, debtApi.creator, 'debt.creator eq');
    assert.equal(debtEth.oracle, debtApi.oracle, 'debt.oracle eq');
};

module.exports.checkLoan = async (loanEth, loanApi, checkKeys) => {
    if (checkKeys.includes('open')) {
        assert.equal(loanEth.open, loanApi.open, 'loan.open');
    }
    if (checkKeys.includes('approved')) {
        assert.equal(loanEth.approved, loanApi.approved, 'loan.approved');
    }
    if (checkKeys.includes('position')) {
        assert.equal(loanEth.position, loanApi.position, 'loan.position');
    }
    if (checkKeys.includes('expiration')) {
        assert.equal(loanEth.expiration, loanApi.expiration, 'loan.expiration');
    }
    if (checkKeys.includes('amount')) {
        assert.equal(loanEth.amount, loanApi.amount, 'loan.amount');
    }
    if (checkKeys.includes('cosigner')) {
        assert.equal(loanEth.cosigner, loanApi.cosigner, 'loan.cosigner');
    }
    if (checkKeys.includes('model')) {
        assert.equal(loanEth.model, loanApi.model, 'loan.model');
    }
    if (checkKeys.includes('creator')) {
        assert.equal(loanEth.creator, loanApi.creator, 'loan.creator');
    }
    if (checkKeys.includes('oracle')) {
        assert.equal(loanEth.oracle, loanApi.oracle, 'loan.oracle');
    }
    if (checkKeys.includes('borrower')) {
        assert.equal(loanEth.borrower, loanApi.borrower, 'loan.borrower');
    }
    if (checkKeys.includes('callback')) {
        assert.equal(loanEth.callback, loanApi.callback, 'loan.callback');
    }
    if (checkKeys.includes('salt')) {
        assert.equal(loanEth.salt, loanApi.salt, 'loan.salt');
    }
    if (checkKeys.includes('loanData')) {
        assert.equal(loanEth.loanData, loanApi.loanData, 'loan.loanData');
    }
};
