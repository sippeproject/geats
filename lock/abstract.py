from ..exceptions import FailedToAcquireLockException

class AbstractLock(object):
    """
    A named lock class, using lockmanager primitives.

    Usage:
        with manager.get_lock(key):
            do something
    """
    def __init__(self, key, config):
        self.key = key
        self.config = config
        self.init()

    def init(self):
        pass

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    def __enter__(self):
        if not self.acquire():
            raise FailedToAcquireLockException("Failed to acquire lock for %s" % (self.key,))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type != FailedToAcquireLockException:
            self.release()
