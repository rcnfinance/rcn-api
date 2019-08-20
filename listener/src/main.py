import os
import logging
import time
from requests.exceptions import ConnectionError
from block_service.block_logs_service import GraphQLService
# from block_service.mock_block_service import MockNewBlocksService
from block_service.mock_block_service import MockForkBlocksService
from processor import Processor
from chain_window import ChainWindow
from chain_window import InvalidChain
from contract_manager import ContractManager
from contracts.debtEngine.debt_engine import debt_engine
from contracts.installmentsModel.installments import installments
from contracts.loanManager.loan_manager import loan_manager

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

ORIGIN_BLOCK = os.environ.get("START_SYNC")
contract_list = [debt_engine, installments, loan_manager]
contract_manager = ContractManager(contract_list)
processor = Processor(contract_manager)
blocklogs_service = GraphQLService()
# blocklogs_service = MockForkBlocksService()
chain_window = ChainWindow(ORIGIN_BLOCK, blocklogs_service)

while 1:
    try:
        chain_window.sync()
        fork_blocks = chain_window.check_fork()
        new_blocks = chain_window.check_new_blocks()
        processor.on_fork(fork_blocks)
        processor.on_new_blocks(new_blocks)

    except ConnectionError:
        print("Connection Error ethlogs, retry...")
        time.sleep(5)
        continue
    except InvalidChain:
        print("CADENA INVALIDA")
        continue
