#
# An in-memory database, suitable for testing.
#
class DummyDatabase:
    def __init__(self, config):
        self.vms = {}

    def define_vm(self, name, vm_definition):
        self.vms[name] = vm_definition

    def undefine_vm(self, name):
        if name in self.vms:
            del self.vms[name]

    def list_vms(self):
        return self.vms.keys()

    def get_vm_definition(self, vm_name):
        return self.vms.get(vm_name, None)

