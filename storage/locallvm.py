from os.path import exists

class LocalLVMVolume:
    def __init__(self, name, definition, vm, config):
        self.name = name
        self.definition = definition
        self.vm = vm
    def get_name(self):
        return self.name
    def define(self):
        """lvcreate"""
        os.system("tar -C '%s' -xzpsSf '%s'" % (rootfs, targz))
        return None
    def activate(self):
        """mount it"""
        return None
    def deactivate(self):
        """unmount it"""
        return None
    def undefine(self):
        """lvremove it"""
        return None
    def format(self):
        return None
    def get_blockdevice(self):
        return self.definition.get("blockdevice", "/dev/null")
    def is_local(self):
        return True
    def is_online(self):
        return os.path.exists(self.get_blockdevice())
