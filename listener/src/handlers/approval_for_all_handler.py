import web3
from .event_handler import EventHandler
from handlers import utils

class ApprovalForAllHandler(EventHandler):
    signature = 'ApprovalForAll(address,address,bool)'
    signature_hash = web3.Web3.sha3(text=signature)

    def _parse(self):
        data = self._event.get('data')[2:]
        splited_args = utils.split_every(64, data)
        # self._owner = utils.to_address(splited_args[0])
        # self._operator = utils.to_address(splited_args[1])
        # self._approved = utils.to_bool(splited_args[2])

    def do(self):
        return []
