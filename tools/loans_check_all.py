import sys
from abc import ABC, abstractmethod
import datetime
import requests
from termcolor import colored, cprint


def get_loan(url):
    response = requests.get(url)
    return response

def load_loan(response):
    loan_data = response.json().get("content")
    commits = loan_data.get("commits")
    loan_data["commits"] = parse_commits(commits)
    loan = Loan(**loan_data)

    return loan

def loan_url_generator(url):
    index_loan = 1
    while True:
        yield requests.compat.urljoin(url, str(index_loan))
        index_loan += 1

def get_class_commit_by_opcode(opcode):
    table_definition = {
        "loan_request": RequestLoanCommit,
        "approved_loan": ApprovedLoanCommit,
        "lent": LentCommit,
        "loan_expired": ExpiredLoanCommit,
        "loan_in_debt": InDebtCommit,
        "transfer": TransferCommit,
        "destroyed_loan": DestroyedLoanCommit,
        "partial_payment": PartialPaymentCommit,
        "total_payment": TotalPaymentCommit
    }
    return table_definition.get(opcode)

def parse_commits(commits):
    parsed_commits = []
    for commit in commits:
        class_ = get_class_commit_by_opcode(commit.get("opcode"))
        parsed_commits.append(class_(**commit))
    return parsed_commits

class Commit(ABC):
    def __init__(self, **commit_data):
        for k, v in commit_data.items():
            setattr(self, k, v)
        self.date = datetime.datetime.utcfromtimestamp(self.timestamp)
    

class RequestLoanCommit(Commit):
    pass

class ApprovedLoanCommit(Commit):
    pass

class LentCommit(Commit):
    pass

class ExpiredLoanCommit(Commit):
    pass

class InDebtCommit(Commit):
    pass

class TransferCommit(Commit):
    pass

class DestroyedLoanCommit(Commit):
    pass

class PartialPaymentCommit(Commit):
    pass

class TotalPaymentCommit(Commit):
    pass

class Loan():
    def __init__(self, **loan_data):
        for key, value in loan_data.items():
            setattr(self, key, value)

def contains(list_, filter_):
    for x in list_:
        if filter_(x):
            return True
    return False


def commits_are_sorted(loan):
    return is_sorted(loan.commits, fn=lambda commit: getattr(commit, "timestamp"))

def is_sorted(list_, fn=lambda x: x):
    return all([fn(list_[i]) <= fn(list_[i + 1]) for i in range(len(list_) - 1)])

def first_commits_is_request(loan):
    return loan.commits[0].opcode == "loan_request"


def find_event(commit_list, opcode_event):
    for index, event in enumerate(commit_list):
        if event.opcode == opcode_event:
            return index
    return -1


def check_event_after_other(loan, event_opcode1, event_opcode2):
    index_event = find_event(loan.commits, event_opcode1)
    if index_event >= 0:
        return contains(loan.commits[:index_event], lambda commit: commit.opcode == event_opcode2)
    return True

def print_function_result(boolean_fn, params, message):
    boolean_result = boolean_fn(**params)
    color = "green" if boolean_result else "red"
    wrapped_msg = "|✔| " if boolean_result else "|✘| "
    wrapped_msg += message
    print(colored(wrapped_msg, color))
    return 1 if boolean_result else 0
    

def analize_loans(url_endpoint):
    loan_url_gen = loan_url_generator(url_endpoint)
    
    while True:
        status_codes = []
        current_url = next(loan_url_gen)
        loan_request = get_loan(current_url)
        if loan_request.ok:
            print(current_url)
            loan = load_loan(loan_request)
            
            params = {"loan": loan}
            message = "Commits are sorted by timestamp"
            status_code = print_function_result(commits_are_sorted, params, message)
            status_codes.append(status_code)

            params = {"loan": loan}
            message = "First commit is request_loan"
            status_code = print_function_result(first_commits_is_request, params, message)
            status_codes.append(status_code)

            params = {"loan": loan, "event_opcode1": "approved_loan", "event_opcode2": "loan_request"}
            message = "Loan approved after loan_request"
            status_code = print_function_result(check_event_after_other, params, message)
            status_codes.append(status_code)

            params = {"loan": loan, "event_opcode1": "loan_expired", "event_opcode2": "loan_request"}
            message = "Loan loan_expired after loan_request"
            status_code = print_function_result(check_event_after_other, params, message)
            status_codes.append(status_code)

            params = {"loan": loan, "event_opcode1": "lent", "event_opcode2": "approved_loan"}
            message = "Loan lent after approved_loan"
            status_code = print_function_result(check_event_after_other, params, message)
            status_codes.append(status_code)

            params = {"loan": loan, "event_opcode1": "total_payment", "event_opcode2": "partial_payment"}
            message = "Loan total_payment after partial_payment"
            status_code = print_function_result(check_event_after_other, params, message)
            status_codes.append(status_code)

            params = {"loan": loan, "event_opcode1": "loan_in_debt", "event_opcode2": "lent"}
            message = "Loan loan_in_debt after lent"
            status_code = print_function_result(check_event_after_other, params, message)
            status_codes.append(status_code)

        else:
            print("No more loans to check :)")
            break
    return 1 if any(status_codes) else 0

if __name__ == '__main__':
    # LOCAL_URL_BASE = "http://192.168.0.249:8000/v1/loans/"
    # REMOTE_URL_BASE = "https://testnet.rnode.rcn.loans/v1/loans/"
    if len(sys.argv) < 2:
        print("Usage: python3 {} URL_ENDPOINT".format(__file__))
        print("Example python3 {} https://testnet.rnode.rcn.loans/v1/loans/".format(__file__))
        sys.exit(1)
    else:
        url_endpoint = sys.argv[1]
        status = analize_loans(url_endpoint)
        sys.exit(status)