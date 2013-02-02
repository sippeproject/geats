#
# A pickled database
#

import cPickle as pickle
import os.path
import fcntl

class PickleDatabase:
    def __init__(self, config):
        self.vms = {}
        #CONFVAR# database.$pickle.filename: location of pickle file
        self.savefile = config["filename"]
        self._load()

    def _save(self):
        fd = open(self.savefile, 'w')
        fcntl.lockf(fd.fileno(), fcntl.LOCK_EX)
        try:
            pickle.dump(self.vms, fd)
        finally:
            fd.close()

    def _load(self):
        # XXX - use a lockfile
        if not os.path.exists(self.savefile):
            self.vms = {}
            return
        fd = open(self.savefile, 'r')
        fcntl.lockf(fd.fileno(), fcntl.LOCK_SH)
        try:
            self.vms = pickle.load(fd)
            return
        finally:
            fd.close()

    def define_vm(self, name, vm_definition):
        self.vms[name] = vm_definition
        self._save()

    def undefine_vm(self, name):
        if name in self.vms:
            del self.vms[name]
            self._save()

    def list_vms(self):
        return self.vms.keys()

    def get_vm_definition(self, vm_name):
        return self.vms.get(vm_name, None)

