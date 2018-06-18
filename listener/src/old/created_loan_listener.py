from datetime import datetime as dt
import requests
from event_listener import EventListener


def insert_loan(loan_data):
    url = "http://api:8000/v1/loan/"
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.post(url, json=loan_data, headers=headers)
    return response.status_code, response.text


class CreatedLoanListener(EventListener):

    def __init__(self, config_filename):
        super().__init__(config_filename)

    def _create_filter(self, argument_filters=None, fromBlock=0, toBlock='latest'):
        event = self._contract.events.CreatedLoan.createFilter(argument_filters=argument_filters, fromBlock=fromBlock, toBlock=toBlock)
        return event.filter_id

    def handle_event(self, event):
        print(event)
        loan = self.fill_loan(event)
        print(insert_loan(loan))
        print(loan)
        assert len(loan.keys()) == 21

    def fill_index(self, index, d):
        d['index'] = index
    def fill_created(self, block_number, d):
        d['created'] = dt.utcfromtimestamp(self._w3.eth.getBlock(block_number).timestamp)
    def fill_status(self, index, d):
        d['status'] = str(self._contract.functions.getStatus(index).call())
    def fill_oracle(self, index, d):
        d['oracle'] = self._contract.functions.getOracle(index).call()
    def fill_borrower(self, index, d):
        d['borrower'] = self._contract.functions.getBorrower(index).call()
    def fill_lender(self, index, d):
        d['lender'] = self._contract.functions.ownerOf(index).call()
    def fill_creator(self, index, d):
        d['creator'] = self._contract.functions.getCreator(index).call()
    def fill_cosigner(self, index, d):
        d['cosigner'] = self._contract.functions.getCosigner(index).call()
    def fill_amount(self, index, d):
        d['amount'] = self._contract.functions.getAmount(index).call()
    def fill_interest(self, index, d):
        d['interest'] = self._contract.functions.getInterest(index).call()
    def fill_punitory_interest(self, index, d):
        d['punitory_interest'] = self._contract.functions.getPunitoryInterest(index).call()
    def fill_interest_timestamp(self, index, d):
        d['interest_timestamp'] = self._contract.functions.getInterestTimestamp(index).call()
    def fill_paid(self, index, d):
        d['paid'] = self._contract.functions.getPaid(index).call()
    def fill_interest_rate(self, index, d):
        d['interest_rate'] = self._contract.functions.getInterestRate(index).call()
    def fill_interest_rate_punitory(self, index, d):
        d['interest_rate_punitory'] = self._contract.functions.getInterestRatePunitory(index).call()
    def fill_due_time(self, index, d):
        d['due_time'] = dt.utcfromtimestamp(self._contract.functions.getDueTime(index).call())
    def fill_dues_in(self, index, d):
        d['dues_in'] = self._contract.functions.getDuesIn(index).call()
    def fill_currency(self, index, d):
        d['currency'] = self._contract.functions.getCurrency(index).call()
    def fill_cancelable_at(self, index, d):
        d['cancelable_at'] = self._contract.functions.getCancelableAt(index).call()
    def fill_lender_balance(self, index, d):
        d['lender_balance'] = self._contract.functions.getLenderBalance(index).call()
    def fill_expiration_requests(self, index, d):
        d['expiration_requests'] = self._contract.functions.getExpirationRequest(index).call()

    def fill_loan(self, event):
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

    def insert_all_loans(self):
        event_filter = self._contract.events.CreatedLoan.createFilter(fromBlock=0)
        all_events = event_filter.get_all_entries()
        print('Event length = {}'.format(len(all_events)))
        for event in all_events:
            print(type(event))
            print(event)
            print('getting information')
            loan = self.fill_loan(event)
            print(loan)
            print('insert to db')
            print(insert_loan(loan))
        print(self._w3.eth.uninstallFilter(event_filter.filter_id))



if __name__ == '__main__':
    listener = CreatedLoanListener('config_created_loan.json')
    listener.main_loop()