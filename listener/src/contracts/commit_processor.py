import logging


class CommitProcessor():
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, commit, *args, **kwargs):
        raise NotImplementedError()
