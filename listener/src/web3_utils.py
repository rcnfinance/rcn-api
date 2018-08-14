class SafeWeb3:
    def __init__(self, web3):
        self.web3 = web3
        self.eth = SafeEth(web3)


class SafeEth:
    def __init__(self, web3):
        self.web3 = web3

    def getBlock(self, target):
        block = self.web3.eth.getBlock(target)
        assert target == 'latest' or block.number == target, 'ETH Node responded with wrong block'
        return block

    def getLogs(self, props):
        # TODO Validate response
        return self.web3.eth.getLogs(props)
