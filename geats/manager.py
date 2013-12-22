# vim: ft=python softtabstop=4
#
# Geats Manager for VMs and VM-like objects
#

from config import Config
from exceptions import UnsupportedVMType
from exceptions import InvalidVMDefinition
from exceptions import UnsupportedStorageType

class Manager(object):
    def __init__(self, database=None, config=None):
        # config
        if config:
            self.config = config
        else:
            self.config = config = Config()
        # database
        if database:
            self.database = database
        else:
            db_config = config.get_database_config()
            db_factory = config.get_database_factory()
            self.database = db_factory(db_config)

    def _make_virtual_machine(self, vm_name, vm_definition):
        """
        Given the vm_type and vm_definition, instantiate the
        right class to manage a VM.  Note: We MUST call
        vm.define() before everything else.
        """
        if not isinstance(vm_definition, dict):
            raise ValueError("vm_definition parameter must be of type dict")
        if not vm_definition.has_key('name'):
            vm_definition['name'] = vm_name
        elif vm_definition['name'] != vm_name:
            raise InvalidVMDefinition("Name in VM definition differs from name in call")
        if not vm_definition.has_key('description'):
            vm_definition['description'] = vm_definition['name']
        if vm_definition.has_key('vm_type'):
            vm_type = vm_definition['vm_type']
        else:
            raise InvalidVMDefinition("No type set for VM")

        vm_factory = self.config.get_vm_factory(vm_type)
        if vm_factory:
            vm_config = self.config.get_vm_config(vm_type)
            return vm_factory(self, vm_config, vm_name, vm_definition)
        else:
            raise UnsupportedVMType("Unsupported vm_type: %s" % (vm_type,))

    def _make_storage_volume(self, storage_type, storage_definition, vm):
        """
        Given a storage type, storage definition, and the VM it is
        for, return a new storage volume
        """
        name = vm.get_name()+"-"+storage_definition.get('name','storage')
        storage_factory = self.config.get_storage_factory(storage_type)
        if storage_factory:
            storage_config = self.config.get_storage_config(storage_type)
            storage_instance = storage_factory(name, storage_definition, vm,
                                   storage_config)
            # check for any adapters for this storage type
            storage_adapters = self.config.get_storage_adapters(storage_type)
            if storage_adapters:
                # if we have any adapters, wrap storage_instance with each
                for adapter in reversed(storage_adapters):
                    storage_instance = adapter(storage_instance,
                        storage_definition, vm, storage_config)
            return storage_instance
        raise UnsupportedStorageType("Unsupported storage_type: %s" % (storage_type,))

    def provision_vm(self, vm_name, vm_definition):
        # 1. Instantiate VM object
        vm = self._make_virtual_machine(vm_name, vm_definition)
        # 2. Call vm.vm_provision
        result = vm.provision()
        # 3. Save VM to VMDatabase
        self.database.create(vm_name, vm_definition)
        # 4. Return the VM object
        return vm

    def define_vm(self, vm_name, vm_definition):
        # 1. Instantiate VM object
        vm = self._make_virtual_machine(vm_name, vm_definition)
        # 2. Call vm.vm_define
        result = vm.define()
        # 3. Save VM to VMDatabase
        self.database.create(vm_name, vm_definition)
        # 4. Return the VM object
        return vm

    def get_vm(self, vm_name):
        """
        Given a VM name, return the VM instance.
        """
        vmdef = self.database.get_definition(vm_name)
        if not vmdef:
            raise KeyError("Unknown VM: %s" % (vm_name,))
        return self._make_virtual_machine(vm_name, vmdef)

    def list_vms(self):
        """
        Return a list of all VMs by name
        """
        return self.database.list()

    def get_lock(self, key):
        """
        Return a Lock instance for the given key.
        """
        lock_config = self.config.get_lock_config()
        lock_factory = self.config.get_lock_factory()
        return lock_factory(key, lock_config)
