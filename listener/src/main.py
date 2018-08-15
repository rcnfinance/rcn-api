from event_buffer import EventBuffer
from listener import Listener
from processor import Processor


def run():
    buffer = EventBuffer()
    processor = Processor(buffer)
    listener = Listener(buffer)
    listener.run()


if __name__ == '__main__':
    run()
