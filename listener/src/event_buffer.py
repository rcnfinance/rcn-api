import logging

logger = logging.getLogger(__name__)


class Event:
    def __init__(self, event):
        self.data = event
        self.position = event['blockNumber'] * 1000000000 + event['transactionIndex'] * 1000000 + event['logIndex']

    def __eq__(self, other):
        return other.position == self.position


def make_event_position(event):
    position = event['blockNumber'] * 1000000000 + event['transactionIndex'] * 1000000 + event['logIndex']

    return position


class IntegrityBroken(Exception):
    pass


class Registry:
    def __init__(self):
        self.registry = []
        self.last_event_position = 0

    def add_event(self, event):
        event_position = make_event_position(event)

        if event_position < self.last_event_position:
            raise IntegrityBroken("integrity broken")

        elif event_position == self.last_event_position:
            return None
        
        else:
            self.registry.append(event)
            self.last_event_position = event_position

            return True

    def clean_events(self):
        self.registry = []


class EventBuffer:
    def __init__(self):
        self.synced_block = 0
        self.last_event = 0
        self.last_timestamp = 0

        self.registry = Registry()
        self.integrity_callbacks = []
        self.entries_callbacks = []

    # It should receive events, ignore duplicated ones and
    # register new ones. If an event between to already registered events
    # is dettected we should raise the alarm to the listeners.
    def feed(self, lastblock, timestamp, events):
        new_events = []

        for event in events:
            try:
                added = self.registry.add_event(event)
                if added:
                    new_events.append(event)

            except IntegrityBroken as e:
                self.integrity_broken()
                #sys.exit(1)
            except Exception as e:
                pass
                #sys.exit(1)

        if self.synced_block < lastblock:
            self.synced_block = lastblock

        if timestamp > self.last_timestamp:
            self.last_timestamp = timestamp

        if new_events:
            self.new_entries(new_events, self.last_timestamp)

        self.registry.clean_events()

        #     event = Event(event)

        #     if event not in self.registry:
        #         self.registry.append(event)
        #         state_changed = True

        #         # Check if we have events already ahead
        #         if event.position < self.last_event:
        #             logger.info('Rogue event dettected {}'.format(event.position))
        #             self.integrity_broken()
        #         else:
        #             self.last_event = event.position

        # if self.synced_block < lastblock:
        #     self.synced_block = lastblock
        #     state_changed = True

        # if timestamp > self.last_timestamp:
        #     self.last_timestamp = timestamp

        # if state_changed:
        #     self.new_entries()

    def subscribe_integrity(self, callback):
        if callback not in self.integrity_callbacks:
            self.integrity_callbacks.append(callback)

    def subscribe_changes(self, callback):
        if callback not in self.entries_callbacks:
            self.entries_callbacks.append(callback)

    def integrity_broken(self):
        logger.info('Integrity error dettected current block {}'.format(self.synced_block))
        for callback in self.integrity_callbacks:
            callback()

    def new_entries(self, events, timestamp):
        for callback in self.entries_callbacks:
            callback(events, timestamp)
