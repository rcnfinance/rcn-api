import logging

logger = logging.getLogger(__name__)


class Event:
    def __init__(self, event):
        self.data = event
        self.position = event['blockNumber'] * 1000000000 + event['transactionIndex'] * 1000000 + event['logIndex']

    def __eq__(self, other):
        return other.position == self.position


class EventBuffer:
    synced_block = 0
    last_event = 0
    last_timestamp = 0

    registry = []
    integrity_callbacks = []
    entries_callbacks = []

    # It should receive events, ignore duplicated ones and
    # register new ones. If an event between to already registered events
    # is dettected we should raise the alarm to the listeners.
    def feed(self, lastblock, timestamp, events):
        state_changed = False

        for event in events:
            if event is not Event:
                event = Event(event)

            if event not in self.registry:
                self.registry.append(event)
                state_changed = True

                # Check if we have events already ahead
                if event.position < self.last_event:
                    logger.info('Rogue event dettected {}'.format(event.position))
                    self.integrity_broken()
                else:
                    self.last_event = event.position

        if self.synced_block < lastblock:
            self.synced_block = lastblock
            state_changed = True

        if timestamp > self.last_timestamp:
            self.last_timestamp = timestamp

        if state_changed:
            self.new_entries()

    def subscribe_integrity(self, callback):
        if callback not in self.integrity_callbacks:
            self.integrity_callbacks.append(callback)

    def subscribe_changes(self, callback):
        if callback not in self.entries_callbacks:
            self.entries_callbacks.append(callback)

    def integrity_broken(self):
        self.registry.sort(key=lambda x: x.position)
        logger.info(
            'Integrity error dettected current block {} last event {}'.format(self.synced_block, self.last_event))
        logger.debug('Current database:')
        for l in self.registry:
            logger.debug(l.data)
        for callback in self.integrity_callbacks:
            callback()

    def new_entries(self):
        for callback in self.entries_callbacks:
            callback(self.last_timestamp)
