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

module.exports.increaseTime = function increaseTime(duration) {
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


module.exports.check_state = async (state_eth, state_api) => {

    assert.equal(state_eth.status, state_api.status, "state.status eq");
    assert.equal(state_eth.clock, state_api.clock, "state.clock eq");
    assert.equal(state_eth.lastPayment, state_api.last_payment, "state.last_payment eq");
    assert.equal(state_eth.paid, state_api.paid, "state.paid eq");
    assert.equal(state_eth.paidBase, state_api.paid_base, "state.paid_base eq");
    assert.equal(state_eth.interest, state_api.interest, "state.interest eq");

    return;
}

module.exports.check_config = async (config_eth, config_api) => {

    assert.equal(config_eth.installments, config_api.data.installments, "config.installments eq")
    assert.equal(config_eth.timeUnit, config_api.data.time_unit, "config.time_unit eq")
    assert.equal(config_eth.duration, config_api.data.duration, "config.duration eq")
    assert.equal(config_eth.lentTime, config_api.data.lent_time, "config.lent_time eq")
    assert.equal(config_eth.cuota, config_api.data.cuota, "config.cuota eq")
    assert.equal(config_eth.interestRate, config_api.data.interest_rate, "config.interest_rate eq")

    return
}

module.exports.check_debt = async (debt_eth, debt_api) => {

    assert.equal(debt_eth.error, debt_api.error, "debt.error eq");
    assert.equal(debt_eth.balance, debt_api.balance, "debt.balance eq");
    assert.equal(debt_eth.model, debt_api.model, "debt.model eq");
    assert.equal(debt_eth.creator, debt_api.creator, "debt.creator eq");
    assert.equal(debt_eth.oracle, debt_api.oracle, "debt.oracle eq");

    return
}

module.exports.check_loan = async (loan_eth, loan_api, check_keys) => {

    if (check_keys.includes("open")) {
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