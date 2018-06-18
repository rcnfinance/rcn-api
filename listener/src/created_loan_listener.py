from created_loan_filter import FakeCreatedLoanFilter, CreatedLoanFilter
from api_preserver import APIPreserver, EchoPreserver
from created_loan_handler import FakeCreatedLoanHandler, CreatedLoanHandler
from event_listener import EventListener


def main():
    CONFIG_PATH = "config_created_loan.json"
    created_loan_filter = FakeCreatedLoanFilter()
    # created_loan_filter = CreatedLoanFilter.create(CONFIG_PATH)
    api_preserver = APIPreserver()
    echo_preserver = EchoPreserver()
    created_loan_handler = FakeCreatedLoanHandler(CONFIG_PATH, [api_preserver, echo_preserver])
    listener = EventListener(
        CONFIG_PATH,
        created_loan_filter,
        created_loan_handler
    )

    listener.main_loop(5)

if __name__ == '__main__':
    main()