from abstract import AbstractLock

class DummyLock(AbstractLock):
    """
    A simple in-memory lock suitable for testing.
    """
    def init(self, config):
        self.locked = False
    def acquire(self):
        if self.locked:
            return False
        else:
            self.locked = True
            return True
    def release(self):
        self.locked = False
