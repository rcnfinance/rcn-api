"""
Dependencias python:
pip3 install faker
pip3 install mongoengine

Dependencias Componentes:
docker-compose up mongo

Run:
python3 populate_db model count

Help:
python3 populate_db -h

"""
import argparse

from mongoengine import connect
from faker import Faker

from models import Loan
from models import Descriptor
from models import Debt
from models import Config
from models import Commit
from models import OracleHistory


MONGO_HOST = "localhost"
MONGO_DB = "rcn"

connect(db=MONGO_DB, host=MONGO_HOST)


def random_oracle_history(faker):
    oracle = {
        "id": faker.uuid4(),
        "tokens": str(faker.random_int()),
        "equivalent": str(faker.random_int()),
        "timestamp": str(faker.date_time().timestamp())
    }
    return OracleHistory(**oracle)


def random_debt(faker):
    debt = {
        "id": faker.uuid4(),
        "error": faker.boolean(),
        "currency": faker.uuid4(),
        "balance": str(faker.random_int()),
        "model": faker.uuid4(),
        "creator": faker.uui4(),
        "oracle": faker.uui4(),
        "created": str(faker.date_time().timestamp())
    }

    commits = [random_commit(faker)]

    debt["commits"] = commits

    return Debt(**debt)

def random_loan(faker):
    loan = {
        "id" : faker.uuid4(),
        "open" : faker.boolean(),
        "approved" : faker.boolean(),
        "position" : str(faker.pyint()),
        "expiration" : str(faker.pyint()),
        "amount" : str(faker.pyint()),
        "cosigner" : str(faker.pyint()),
        "model" : str(faker.pyint()),
        "creator" : str(faker.pyint()),
        "oracle" : str(faker.pyint()),
        "borrower" : str(faker.pyint()),
        "salt" : str(faker.pyint()),
        "loanData" : str(faker.pyint()),
        "created" : str(faker.pyint()),
        "descriptor" : random_descriptor(faker),
        "currency" : str(faker.pyint()),
        "status" : str(faker.pyint()),
    }

    return Loan(**loan)

def random_descriptor(faker):
    descriptor = {
        "first_obligation": str(faker.pyint()),
        "total_obligation": str(faker.pyint()),
        "duration": str(faker.pyint()),
        "interest_rate": str(faker.pyint()),
        "punitive_interest_rate": str(faker.pyint()),
        "frequency": str(faker.pyint()),
        "installments": str(faker.pyint()),
    }

    return Descriptor(**descriptor)

def random_config(faker):
    config = {
        "id": faker.uuid4(),
        "data": {}
    }

    commits = [random_commit(faker)]

    config["commits"] = commits

    return Config(**config)

def random_commit(faker):
    commit = {
        "opcode": faker.word(),
        "timestamp": faker.date_time().timestamp(),
        "order": faker.random_digit(),
        "proof": faker.uuid4(),
        "data": {"name": "pepito"}
    }

    return Commit(**commit)

def insert_n_oracles(n):
    faker = Faker()
    for i in range(n):
        oracle = random_oracle_history(faker)
        oracle.save()

def insert_n_configs(n):
    faker = Faker()
    for i in range(n):
        config = random_config(faker)
        config.save()

def insert_n_debts(n):
    faker = Faker()
    for i in range(n):
        debt = random_debt(faker)
        debt.save()

def insert_n_loans(n):
    faker = Faker()
    for i in range(n):
        request = random_loan(faker)
        request.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model", choices=["loan", "debt", "config"])
    parser.add_argument("count", type=int, help="count elem to insert")
    args = parser.parse_args()
    print(args)

    map_model_fn = {
        "loan": insert_n_loans,
        "debt": insert_n_debts,
        "config": insert_n_configs
    }

    map_model_fn[args.model](args.count)
