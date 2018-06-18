from datetime import datetime as dt
from handler import Handler



class FakeCreatedLoanHandler(Handler):
    def _parse_event(self, event):
        loan = {
            "amount": "200000000000000000000",
            "borrower": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "cancelable_at": "1970-01-03 00:00:00",
            "cosigner": "0x0000000000000000000000000000000000000000",
            "created": "2016-11-20 11:48:50",
            "creator": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "currency": "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00",
            "due_time": "2018-05-21 20:42:59",
            "dues_in": "1970-01-13 00:00:00",
            "expiration_requests": "2018-06-05 19:40:58",
            "index": event.get('args').get('_index'),
            "interest": "1533334812242862439",
            "interest_rate": "13523478260869",
            "interest_rate_punitory": "12441600000000",
            "interest_timestamp": "2018-06-04 20:57:31",
            "lender": "0x35d803F11E900fb6300946b525f0d08D1Ffd4bed",
            "lender_balance": "0",
            "oracle": "0x0000000000000000000000000000000000000000",
            "paid": "122000000000000000000",
            "punitory_interest": "1423141359661568706",
            "status": "1"
        }

        return loan

class CreatedLoanHandler(Handler):
    def _parse_event(self, event):
        loan = dict()
        index = event.get('args').get('_index')
        block_number = event.get('blockNumber')
        loan['index'] = index
        loan['created'] = dt.utcfromtimestamp(self._w3.eth.getBlock(block_number).timestamp)
        loan['status'] = str(self._contract.functions.getStatus(index).call())
        loan['oracle'] = self._contract.functions.getOracle(index).call()
        loan['borrower'] = self._contract.functions.getBorrower(index).call()
        loan['lender'] = self._contract.functions.ownerOf(index).call()
        loan['creator'] = self._contract.functions.getCreator(index).call()
        loan['cosigner'] = self._contract.functions.getCosigner(index).call()
        loan['amount'] = self._contract.functions.getAmount(index).call()
        loan['interest'] = self._contract.functions.getInterest(index).call()
        loan['punitory_interest'] = self._contract.functions.getPunitoryInterest(index).call()
        loan['interest_timestamp'] = self._contract.functions.getInterestTimestamp(index).call()
        loan['paid'] = self._contract.functions.getPaid(index).call()
        loan['interest_rate'] = self._contract.functions.getInterestRate(index).call()
        loan['interest_rate_punitory'] = self._contract.functions.getInterestRatePunitory(index).call()
        loan['due_time'] = dt.utcfromtimestamp(self._contract.functions.getDueTime(index).call())
        loan['dues_in'] = self._contract.functions.getDuesIn(index).call()
        loan['currency'] = self._contract.functions.getCurrency(index).call()
        loan['cancelable_at'] = self._contract.functions.getCancelableAt(index).call()
        loan['lender_balance'] = self._contract.functions.getLenderBalance(index).call()
        loan['expiration_requests'] = self._contract.functions.getExpirationRequest(index).call()

        for key, value in loan.items():
            loan[key] = str(value)

        return loan
