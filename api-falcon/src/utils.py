import logging
import requests
from oracle_interface import OracleInterface
from datetime import datetime as dt

from models import Debt
from models import State
from models import Config
from models import Loan
from models import Collateral

U_128_OVERFLOW = 2**128
ORACLE_URL = "https://oracle.ripio.com/rate"

logger = logging.getLogger(__name__)

def get_data(id_loan):
    debt = Debt.objects.get(id=id_loan)
    now = int(dt.utcnow().timestamp())

    paid = get_paid(id_loan)
    due_time = get_due_time(id_loan)
    estimated_obligation = get_estimate_obligation(id_loan)
    next_obligation = get_obligation(id_loan, due_time)[0]
    current_obligation = get_obligation(id_loan, now)[0]
    debt_balance = int(debt.balance)
    owner = get_owner(id_loan)

    data = {
        "paid": paid,
        "due_time": due_time,
        "estimated_obligation": estimated_obligation,
        "next_obligation": next_obligation,
        "current_obligation": current_obligation,
        "debt_balance": debt_balance,
        "owner": owner
    }
    return data


def get_owner(id_loan):
    loan = Loan.objects.get(id=id_loan)
    owner = loan.lender

    return owner


def base_debt(clock, duration, installments, cuota):
    logger = logging.getLogger("test.base_debt")
    logger.info("base_debt function")
    logger.debug("clock: {}, duration: {}, installments: {}, cuota: {}".format(
        clock, duration, installments, cuota)
    )
    installment = clock // duration
    if installment < installments:
        base = installment * cuota
    else:
        base = installments * cuota

    logger.info("Output value: {}".format(base))
    return base


def new_interest(clock, time_unit, duration, installments, cuota, paid_base, delta, interest_rate):
    logger = logging.getLogger("test.new_interest")
    logger.info("new_interest function")
    logger.debug("clock: {}, time_unit: {}, duration: {}, installments: {}, cuota: {}, paid_base: {}, delta: {}, interest_rate: {}".format(
        clock, time_unit, duration, installments, cuota, paid_base, delta, interest_rate)
    )
    running_debt = base_debt(clock, duration, installments, cuota) - paid_base
    new_interest = (100000 * (delta // time_unit) * running_debt) // (interest_rate // time_unit)

    assert new_interest < U_128_OVERFLOW

    logger.info("Output value: {}".format(new_interest))
    return new_interest


def calc_delta(target_delta, clock, duration, installments):
    logger = logging.getLogger("test.calc_delta")
    logger.info("calc_delta function")
    logger.debug("target_delta: {}, clock: {}, duration: {}, installments: {}".format(
        target_delta, clock, duration, installments)
    )
    next_installment_delta = duration - clock % duration
    if next_installment_delta <= target_delta and clock // duration < installments:
        delta = next_installment_delta
        installment_completed = True
    else:
        delta = target_delta
        installment_completed = False

    logger.info("Output value: {},{}".format(delta, installment_completed))
    return (delta, installment_completed)


def run_advance_clock(clock, time_unit, interest, duration, cuota, installments, paid_base, interest_rate, target_clock):
    logger = logging.getLogger("test.run_advance_clock")
    logger.info("run_advance_clock function")
    logger.debug("clock: {}, time_unit: {}, interest: {}, duration: {}, cuota: {}, installments: {}, paid_base: {}, interest_rate: {}, target_clock: {}".format(
        clock, time_unit, interest, duration, cuota, installments, paid_base, interest_rate, target_clock)
    )

    do_condition = True

    while do_condition:
        delta, installment_completed = calc_delta(
            target_clock - clock,
            clock,
            duration,
            installments
        )

        _new_interest = new_interest(
            clock,
            time_unit,
            duration,
            installments,
            cuota,
            paid_base,
            delta,
            interest_rate
        )

        if installment_completed or _new_interest > 0:
            clock += delta
            interest += _new_interest
        else:
            break

        do_condition = clock < target_clock

    logger.info("Output value: {},{}".format(interest, clock))
    return (interest, clock)


def get_closing_obligation(_id, now=None):
    logger = logging.getLogger("test.get_closing_obligation")
    logger.info("get_closing_obligation function")
    logger.debug("id: {}, now: {}".format(_id, now))

    if now is None:
        now = int(dt.utcnow().timestamp())
        logger.debug("now: {}".format(now))

    state = State.objects.get(id=_id)
    config = Config.objects.get(id=_id)

    installments = int(config.data.get("installments"))
    cuota = int(config.data.get("cuota"))
    lent_time = int(config.data.get("lent_time"))

    current_clock = now - lent_time
    clock = int(state.clock)

    if clock >= current_clock:
        interest = int(state.interest)
    else:
        interest, _ = run_advance_clock(
            clock,
            int(config.data.get("time_unit")),
            int(state.interest),
            int(config.data.get("duration")),
            cuota,
            installments,
            int(state.paid_base),
            int(config.data.get("interest_rate")),
            current_clock
        )

    debt = cuota * installments + interest
    paid = int(state.paid)

    if debt > paid:
        closing_obligation = debt - paid
    else:
        closing_obligation = 0

    logger.info("Output value: {}".format(closing_obligation))
    return closing_obligation


def get_estimate_obligation(id, now=None):
    logger = logging.getLogger("test.get_estimate_obligation")
    logger.info("get_estimate_obligation function")
    logger.debug("id: {}, now: {}".format(id, now))

    clossing_obligation = get_closing_obligation(id, now)

    logger.info("Output value: {}".format(clossing_obligation))
    return clossing_obligation


def get_paid(_id):
    logger = logging.getLogger("test.get_paid")
    logger.info("get_paid function")
    logger.debug("id: {}".format(_id))

    state = State.objects.get(id=_id)
    paid = int(state.paid)

    logger.info("Output value: {}".format(paid))
    return paid


def get_due_time(_id):
    logger = logging.getLogger("test.get_due_time")
    logger.info("get_due_time function")
    logger.debug("id: {}".format(_id))

    config = Config.objects.get(id=_id)
    state = State.objects.get(id=_id)

    last_payment = int(state.last_payment)
    duration = int(config.data.get("duration"))
    lent_time = int(config.data.get("lent_time"))

    if last_payment != 0:
        last = last_payment
    else:
        last = duration

    due_time = last - (last % duration) + lent_time

    logger.info("Output value: {}".format(due_time))
    return due_time


def sim_run_clock(clock, target_clock, prev_interest, config, state):
    logger = logging.getLogger("test.sim_run_clock")
    logger.info("sim_run_clock function")
    logger.debug("clock: {}, target_clock: {}, prev_interest: {}, config: {}, state: {}".format(
        clock, target_clock, prev_interest, config.to_json(), state.to_json())
    )
    interest, clock = run_advance_clock(
        clock,
        int(config.data.get("time_unit")),
        prev_interest,
        int(config.data.get("duration")),
        int(config.data.get("cuota")),
        int(config.data.get("installments")),
        int(state.paid_base),
        int(config.data.get("interest_rate")),
        target_clock
    )

    logging.info("Output value: {},{}".format(interest, clock))
    return interest, clock


def get_obligation(_id, timestamp):
    logger = logging.getLogger("test.get_obligation")
    logger.info("get_obligation function")
    logger.debug("id: {}, timestamp: {}".format(_id, timestamp))

    state = State.objects.get(id=_id)
    config = Config.objects.get(id=_id)

    lent_time = int(config.data.get("lent_time"))
    duration = int(config.data.get("duration"))
    installments = int(config.data.get("installments"))
    cuota = int(config.data.get("cuota"))

    if timestamp < lent_time:
        logger.info("Output value: {},{}".format(0, True))
        return (0, True)

    current_clock = timestamp - lent_time

    base = base_debt(
        current_clock,
        duration,
        installments,
        cuota
    )

    prev_interest = int(state.interest)
    clock = int(state.clock)

    if clock >= current_clock:
        interest = prev_interest
        defined = True
    else:
        interest, current_clock = sim_run_clock(
            clock,
            current_clock,
            prev_interest,
            config,
            state
        )

        defined = prev_interest == interest

    debt = base + interest
    paid = int(state.paid)

    if debt > paid:
        obligation = debt - paid
    else:
        obligation = 0

    logger.info("Output value: {},{}".format(obligation, defined))
    return obligation, defined

def get_oracle_data(id):
    try:
        collateral = Collateral.objects.get(id=str(id))
        
        debtId = collateral.debt_id
        loan = Loan.objects.get(id=debtId)

        oracle = loan.oracle

        response = requests.get(url = ORACLE_URL)
        oracleData = response.json() 

        for currencyObject in oracleData:
            if currencyObject["currency"] == loan.currency:
                currencyData = currencyObject["data"]
            else:
                currencyData = None    

        if currencyData is None:
            _tokens = 0
            _equivalent = 0
        else: 
            (_tokens,_equivalent) = OracleInterface.readSample(currencyData, oracle)    

        return (_tokens,_equivalent)
    except Collateral.DoesNotExist:
        logger.warning("Collateral with id {} does not exist".format(str(id)))

def getBlock(w3, number):
    i = 0
    block = w3.eth.getBlock(number)

    if block is not None:
        return block
    else:
        while i < 3:
            block = w3.eth.getBlock(number)

            if block is not None:
                return block

            i += 1
        raise Exception("fucking nodo")