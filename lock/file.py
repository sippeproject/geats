import os.path
import hashlib
import fcntl
from abstract import AbstractLock
import warnings
import time

class FileLock(AbstractLock):
    """
    A simple file-based lock.  It uses an fcntl-lock to control
    access to the lock directory.
    """

    def init(self):
        lock_dir = self.config.get("lock_directory", "/var/lock/geats")
        if not os.path.exists(lock_dir):
            os.mkdir(lock_dir)
        self.dirlockfile = os.path.join(lock_dir, "LOCK")
        filename = hashlib.md5(self.key).hexdigest()+".lock"
        self.lockfile = os.path.join(lock_dir, filename)
        self.locked = None # for the warning only

    def acquire(self):
        # obtain directory lock
        lockfd = open(self.dirlockfile, "w")
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX)
        except IOError:
            lockfd.close()
            return False
        # create named lockfile
        try:
            if os.path.exists(self.lockfile):
                return False
            else:
                fd = open(self.lockfile, "w")
                fd.write("%s\n" % (self.key,))
                fd.close()
                self.locked = True
                return True
        # release directory lock
        finally:
            fcntl.flock(lockfd, fcntl.LOCK_UN)
            lockfd.close()
        return False

    def release(self):
        # obtain directory lock
        lockfd = open(self.dirlockfile, "w")
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX)
        except IOError:
            lockfd.close()
            return False
        # remove named lockfile
        try:
            if os.path.exists(self.lockfile):
                os.unlink(self.lockfile)
            self.locked = False
        # release directory lock
        finally:
            fcntl.flock(lockfd, fcntl.LOCK_UN)
            lockfd.close()

    def __del__(self):
        if self.locked:
            warnings.warn("Unreleased lock: %s" % (self.key))
            self.release()
