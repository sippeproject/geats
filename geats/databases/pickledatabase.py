#
# A pickled database
#

import cPickle as pickle
import os.path
import fcntl
from .. import exceptions

class PickleDatabase:
    def __init__(self, config):
        self.datastore = {}
        #CONFVAR# database.$pickle.filename: location of pickle file
        self.savefile = config["filename"]
        self._load()

    def _save(self):
        fd = open(self.savefile, 'w')
        fcntl.lockf(fd.fileno(), fcntl.LOCK_EX)
        try:
            pickle.dump(self.datastore, fd)
        finally:
            fd.close()

    def _upgrade(self):
        if self.datastore.get("__version__", 1) == 2:
            return
        for name, data in self.datastore.items():
            if "definition" not in data:
                self.datastore[name] = {
                    "definition": data,
                }
            self.datastore["__version__"] = 2
        self._save()

    def _load(self):
        # XXX - use a lockfile
        if not os.path.exists(self.savefile):
            self.datastore = {}
            return
        fd = open(self.savefile, 'r')
        fcntl.lockf(fd.fileno(), fcntl.LOCK_SH)
        try:
            self.datastore = pickle.load(fd)
            self._upgrade() # change format..
            return
        finally:
            fd.close()

    def create(self, name, definition, **extras):
        assert not name.startswith("__")
        if name in self.datastore:
            raise exceptions.AlreadyExistsException("%s already exists in datastore" % (name,))
        assert type(definition) == dict
        for k, v in extras.items():
            assert isinstance(k, basestring)
            assert type(v) == dict
        self.datastore[name] = extras
        extras["definition"] = definition
        self._save()

    def update(self, name, definition=None, **extras):
        assert not name.startswith("__")
        if name not in self.datastore:
            raise KeyError("Key '%s' not found in datastore" % (name,))
        if definition is not None:
            assert type(definition) == dict
            self.datastore[name]["definition"] = definition
        for key, valdict in extras.items():
            assert isinstance(key, basestring)
            assert type(valdict) == dict
            extras[key] = valdict
        self._save()

    def delete(self, name):
        """Delete the given key from the datastore"""
        assert not name.startswith("__")
        if name in self.datastore:
            del self.datastore[name]
            self._save()

    def list(self):
        """List all keys in the datastore"""
        return [x for x in self.datastore.keys() if not x.startswith("__")]

    def get_definition(self, name):
        """Shortcut to return the definition for the given $name"""
        assert not name.startswith("__")
        res = self.datastore.get(name, None)
        if res:
            return res["definition"]

    def get(self, name, key=None):
        """
        Returns None if $name isn't found in datastore.
        If key is in the dict of $name, return the value of it.
        If key isn't in the dict of $name, return an empty dict.
        """
        assert not name.startswith("__")
        data = self.datastore.get(name, None)
        if key is None:
            return data
        elif data is not None:
            return data.get(key, {})
        else:
            return None
