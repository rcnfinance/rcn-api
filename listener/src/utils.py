
def event_id(event):
    return str(event.get('transactionHash')) + str(event.get('logIndex'))