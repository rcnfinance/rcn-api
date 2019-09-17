import os
from event_buffer import EventBuffer
from listener import Listener
from processor import Processor
from contract_manager import ContractManager
from contracts.debtEngine.debt_engine import debt_engine
from contracts.installmentsModel.installments import installments
from contracts.loanManager.loan_manager import loan_manager
from contracts.collateral.collateral import Collateral

all_contracts = [debt_engine, installments, loan_manager, Collateral]

contract_manager = ContractManager(all_contracts)

sleep_in_sync = int(os.environ.get("SLEEP_IN_SYNC", 5))


def run():
    buffer = EventBuffer()
    processor = Processor(buffer, contract_manager)
    listener = Listener(buffer, contract_manager)
    listener.run(sleep_in_sync)


if __name__ == '__main__':
    run()
