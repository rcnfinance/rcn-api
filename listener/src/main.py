
from event_buffer import EventBuffer
from listener import Listener
from processor import Processor

class Main:
  def run(self):
    buffer = EventBuffer()
    processor = Processor(buffer)
    listener = Listener(buffer)
    listener.run()

if __name__ == '__main__':
  Main().run()
