# Semantic Analysis Tool

Check some conditions:

* Commits are sorted by timestamp
* First commit is request_loan
* Loan approved after loan_request
* Loan loan_expired after loan_request
* Loan lent after approved_loan
* Loan total_payment after partial_payment
* Loan loan_in_debt after lent

# Requirements

pip3 install -r requirements.txt

# Usage

python3 loans_check_all.py URL_LOAN_ENDPOINT

example: python3 loans_check_all.py https://testnet.rnode.rcn.loans/v1/loans/
