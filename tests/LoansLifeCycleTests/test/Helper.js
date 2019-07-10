module.exports.address0x = '0x0000000000000000000000000000000000000000';
module.exports.bytes320x = '0x0000000000000000000000000000000000000000000000000000000000000000';

// mnemonic used to create accounts
// "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"
// command: ganache-cli -m "delay practice wall dismiss amount tackle energy annual wrap digital arrive since"

// Accounts
// const creatorPrivateKey = '0xaf080fd098ca962cc4778758dab7b88b4692afa18a613e7a93b77f8667207dd1';
module.exports.creator = '0x1B274E25A1B02D77f8de7550daFf58C07A0D12c8';
// const borrowerPrivateKey = '0x9cd9fa19cb2d594f41aa1e89bc6ca3ee8998d405b4f7d096e366fcb59743c277';
module.exports.borrower = '0x3FaD5afc06e263Ad2E73E82C98377739E746eF15';
// const lenderPrivateKey = '0xda06412214b4901dc170f99a3b51cc36b485bb92d688a449de94638117978c56';
module.exports.lender = '0xa4D49A5e03c6cEEa80eCC48fBF92835AFd4C37e1';
// const newLenderPrivateKey = '0x1ac6294ae9975943a1917d49d967db683a5755237c626658530a52f2f61209e1';
module.exports.newLender = '0x060a109b32d70e58e39376516b2f97E9346939a9';

// Debt Status
module.exports.STATUS_REQUEST = '0';
module.exports.STATUS_ONGOING = '1';
module.exports.STATUS_PAID = '2';
module.exports.STATUS_ERROR = '4';

module.exports.sleep = (millis) => {
  return new Promise(resolve => setTimeout(resolve, millis));
};

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
  const block = await web3.eth.getBlock(await web3.eth.getBlockNumber());
  return block.timestamp;
};

module.exports.getTxTime = async (tx) => {
  if (tx instanceof Promise) { tx = await tx; }
  const blockNumber = tx.receipt.blockNumber;
  const block = await web3.eth.getBlock(blockNumber);
  return block.timestamp;
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
module.exports.tryCatchRevert = async (promise, message, headMsg = 'revert ') => {
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
      'Expected a revert \'' + headMsg + message + '\', got \'' + error.message + '\' instead'
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

module.exports.toEvents = async (tx, ...events) => {
  if (tx instanceof Promise) { tx = await tx; }

  const logs = tx.logs;

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
