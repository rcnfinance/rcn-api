import web3


def split_every(n, string):
    return [string[i:i + n] for i in range(0, len(string), n)]


def to_address(hex_string):
    return '0x' + hex_string[-40:]


def to_int(hex_string):
    return web3.Web3.toInt(hexstr=hex_string)


def to_bool(hex_string):
    # TODO: fix this
    return hex_string


def calculate_interest(time_delta, interest_rate, amount):
    if amount == 0:
        interest = 0
        real_delta = time_delta
    else:
        # interest = safe_mult(safe_mult(100000, amount), time_delta) / interest_rate
        interest = (100000 * amount * time_delta) // interest_rate
        # real_delta = safe_mult(interest, interest_rate) / (amount * 100000)
        real_delta = (int(interest) * interest_rate) // (amount * 100000)
        print("interest: {}, real_delta: {}".format(interest, real_delta))
    return int(real_delta), int(interest)


def get_internal_interest(timestamp, loan_interest_timestamp, loan_interest, loan_punitory_interest, loan_due_time,
                          loan_paid, loan_amount, loan_interest_rate, loan_interest_rate_punitory):
    # loan object from models.py
    # timestamp int
    # return None if timestamp < loan.interest_timestamp
    # return None if not(new_interest != int(loan.interest) or new_punitory_interest != int(loan.punitory_interest))
    if timestamp > int(loan_interest_timestamp):
        new_interest = int(loan_interest)
        new_punitory_interest = int(loan_punitory_interest)

        end_non_punitory = min(timestamp, int(loan_due_time))

        if end_non_punitory > int(loan_interest_timestamp):
            delta_time = end_non_punitory - int(loan_interest_timestamp)

            if int(loan_paid) < int(loan_amount):
                pending = int(loan_amount) - int(loan_paid)
            else:
                pending = 0

            real_delta, calculated_interest = calculate_interest(delta_time, int(loan_interest_rate), pending)
            new_interest = calculated_interest + new_interest
            new_timestamp = int(loan_interest_timestamp) + real_delta

        if timestamp > int(loan_due_time):
            start_punitory = max(int(loan_due_time), int(loan_interest_timestamp))
            delta_time = timestamp - start_punitory

            debt = int(loan_amount) + new_interest
            aux = debt + new_punitory_interest - int(loan_paid)
            pending = min(debt, aux)

            real_delta, calculated_interest = calculate_interest(delta_time, int(loan_interest_rate_punitory), pending)
            new_punitory_interest = new_punitory_interest + calculated_interest
            new_timestamp = start_punitory + real_delta

        if (new_interest != int(loan_interest) or new_punitory_interest != int(loan_punitory_interest)):
            d = {}
            d["interest_timestamp"] = str(new_timestamp)
            d["interest"] = str(new_interest)
            d["punitory_interest"] = str(new_punitory_interest)
            return d
