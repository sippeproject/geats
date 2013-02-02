from abstractstoragevolume import AbstractStorageVolume

class DummyStorageVolume(AbstractStorageVolume):
    def __init__(self, name, definition, vm, config):
        self.name = name
        self.definition = definition
        self.vm = vm
    def get_name(self):
        return self.name
    def define(self):
        return None
    def activate(self):
        return None
    def deactivate(self):
        return None
    def undefine(self):
        return None
    def format(self):
        return None
    def get_blockdevice(self):
        return self.definition.get("blockdevice", None)
    def get_directory(self):
        return self.definition.get("directory", None)
    def get_filename(self):
        return self.definition.get("filename", None)
    def is_local(self):
        return True
    def is_online(self):
        return True
