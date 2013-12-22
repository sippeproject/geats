#
# An in-memory database, suitable for testing.
#
class DummyDatabase:
    def __init__(self, config):
        self.datastore = {}

    def create(self, name, definition, **extras):
        self.datastore[name] = extras
        extras['definition'] = definition

    def update(self, name, definition=None, **extras):
        d = self.datastore[name]
        if definition:
            d['definition'] = d
        d.update(extras)

    def delete(self, name):
        if name in self.datastore:
            del self.datastore[name]

    def list(self):
        return self.datastore.keys()

    def get_definition(self, name):
        d = self.datastore.get(name, None)
        if d:
            return d["definition"]
        else:
            return None

    def get(self, name, key=None):
        if name not in self.datastore:
            return None
        if key is None:
            return self.datastore[name]
        else:
            return self.datastore[name].get(key, {})

