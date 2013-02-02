class INamedLock:
    """
    Implements a machine-local named lock on the given key
    """

    def __init__(key, config):
        """
        :param key: name of the lock
        :param config: dictionary of config from the [lock] config file section
        """

    def acquire():
        """
        Acquire a lock on the named key.

        :returns: True on success, False on failure.
        """

    def release():
        """
        Release the lock (if any) on the named key.

        :param key: name of the lock
        :type key: string
        """

    def __enter__():
        """
        Acquire a lock or throw FailedToAcquireLockException
        """

    def __exit__(exc_type, exc_value, exc_traceback):
        """
        Release the lock
        """

