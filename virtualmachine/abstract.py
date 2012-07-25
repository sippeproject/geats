from ..exceptions import VMException

class AbstractVirtualMachine(object):
    def __init__(self, manager, vm_definition, config):
        assert manager is not None
        assert type(vm_definition) == dict
        self.manager = manager
        self.name = vm_definition["name"]
        self.definition = vm_definition
        self.storage_volumes = []
        self.config = config
        #
        if vm_definition.get("vm_type", None) is None:
            raise VMException("VM type not defined")
        #
        if "storage" in self.definition:
            for storage in self.definition["storage"]:
                if "type" not in storage:
                    raise VMException("Every storage entry must have a type.")
                valid_storage_types = self.config.get("valid_storage_types", None)
                if valid_storage_types is not None and storage["type"] not in valid_storage_types:
                    raise VMException("Unsupported storage type for this VM. Must be one of: %s" % (
                        ", ".join(valid_storage_types)))
                vol = self.manager._make_storage_volume(
                    storage["type"], storage, self)
                self.storage_volumes.append(vol)
        self.lock = self.manager.get_lock("vm-"+self.name)


    def get_name(self):
        return self.name

    def get_description(self):
        return self.definition.get("description", self.name)

    def get_state(self):
        raise NotImplementedError

    def define(self):
        with self.lock:
            self._define()
            try:
                self.define_storage()
            except:
                try: self.undefine_storage()
                except: pass
                raise

    # stop VM if running, deactivate storage, undefine VM
    def undefine(self):
        self.stop()
        with self.lock:
            self.deactivate_storage()
            self._undefine()
            ### XXX can I find a nicer way?
            self.manager.database.undefine_vm(self.name)

    # deprovision can be called instead of undefine to
    # do additional cleanup actions, like wiping the
    # storage volumes.
    def deprovision(self):
        self.undefine()

    # if not started activate storage, start VM
    def start(self):
        with self.lock:
            state, substate = self.get_state()
            # 1. Return without exception if already running.
            if state == "running" and substate != "paused":
                return
            # 2. Activate each storage volume.
            # 3. Raise a Storage exception if failed.
            self.activate_storage()
            # 4. Start the VM by calling adapter.vm_start(self)
            # 5. Raise an Exception if it failed.
            self._start()

    # stop VM if not running
    def stop(self):
        with self.lock:
            state, substate = self.get_state()
            # 1. Return without error if VM is already stopped.
            if state == "stopped":
                return
            # 2. Stop the VM by calling adapter.vm_stop(self)
            # 3. Raise an Exception if it failed.
            self._stop()

    # politely ask the VM to shut down
    def shutdown(self):
        with self.lock:
            state, substate = self.get_state()
            if state == "stopped":
                return
            self._shutdown()

    def migrate(self, destination):
        raise NotImplementedError

    # return a list of IStorageVolume objects
    def get_storage_volumes(self):
        return self.storage_volumes

    def define_storage(self):
        for storage in self.storage_volumes:
            storage.define()

    def activate_storage(self):
        for storage in self.storage_volumes:
            storage.activate()

    def deactivate_storage(self):
        for storage in self.storage_volumes:
            storage.deactivate()

    def undefine_storage(self):
        for storage in self.storage_volumes:
            storage.undefine()

    def get_definition(self):
        return self.definition

    def get_info(self):
        """
        Return an arbitrary dictionary of key->value pairs for this VM.
        """
        return {}

    def get_cpu_usage(self):
        return 0

    def get_memory_usage(self):
        return 0
