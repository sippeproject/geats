from ..exceptions import VMException, VMLockedException

class AbstractVirtualMachine(object):
    """
    AbstractVirtualMachine provides the basic methods and workflow
    of a virtual machine from its creation time through to its
    destruction.  It expects to be sub-classed and for the following
    methods to be defined on the subclass:
      * _define()
      * _start()
      * _stop()
      * _shutdown()
      * _undefine()

    The sub-class may optionally want to override the following two
    methods:
      * provision() - by default calls self.define()
      * deprovision() - by default calls self.undefine()
    """
    def __init__(self, manager, config, vm_name, vm_definition):
        assert manager is not None
        assert type(vm_definition) == dict
        self.manager = manager
        self.name = vm_name
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
        self._lock = self.manager.get_lock("vm-"+self.name)


    def get_name(self):
        """Return the name of this VM"""
        return self.name


    def get_description(self):
        return self.definition.get("description", self.name)


    def get_state(self):
        """
        Return a tuple for the VM state
        """
        raise NotImplementedError


    def define(self):
        """
        define() is called when a VM is first defined on this host.
        """
        with self._lock:
            self._define()
            try:
                self.define_storage()
            except:
                try: self.undefine_storage()
                except: pass
                raise


    def provision(self):
        """
        provision by default just calls define(), but it is separate
        to allow for additional steps which may make sense for
        different scenarios.  For example, it might wipe storage
        volumes first or generate some new access keys.
        """
        return self.define()


    def undefine(self):
        """
        Deactivate storage and undefine the VM.
        It will also tell the database to delete it.
        If a VM is running, it will first be stopped.
        """
        if self.is_locked():
            raise VMLockedException("VM cannot be undefined while it's locked. Unlock it first.")
        self.stop()
        with self._lock:
            self.deactivate_storage()
            self._undefine()
            ### XXX can I find a nicer way?
            self.manager.database.delete(self.name)


    def deprovision(self):
        """
        deprovision can be called instead of undefine to
        do additional cleanup actions, like wiping the
        storage volumes.
        """
        return self.undefine()


    def start(self):
        """
        If a VM isn't already running, activate storage, then start it.
        """
        with self._lock:
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


    def stop(self):
        """
        Stop the VM if it's not already stopped
        """
        with self._lock:
            state, substate = self.get_state()
            # 1. Return without error if VM is already stopped.
            if state == "stopped":
                return
            # 2. Stop the VM by calling adapter.vm_stop(self)
            # 3. Raise an Exception if it failed.
            self._stop()


    def reboot(self):
        """
        Perform a reboot.  By default, it calls the stop and start methods.
        """
        self.stop()
        self.start()


    def reinit(self):
        """
        Deprovision and Reprovision the VM
        """
        self.deprovision()
        self.manager.provision_vm(self.name, self.definition)


    def shutdown(self):
        """
        politely ask the VM to shut down
        """
        with self._lock:
            state, substate = self.get_state()
            if state == "stopped":
                return
            self._shutdown()


    def migrate(self, destination):
        """
        If applicable, migrate should perform a live-migration
        to the destination host.
        """
        raise NotImplementedError

    def lock(self):
        """
        lock(), if implemented, should stop a VM from being undefined.
        """
        raise NotImplementedError

    def unlock(self):
        """
        unlock(), if implemented, should allow a locked VM to be undefined.
        """
        raise NotImplementedError

    def is_locked(self):
        """
        Return True if this VM is currently locked.
        """
        return False

    def get_storage_volumes(self):
        """Return a list of this VM's storage volumes"""
        return self.storage_volumes


    def define_storage(self):
        """Iterate storage volumes calling volume.define()"""
        for storage in self.storage_volumes:
            storage.define()


    def activate_storage(self):
        """Iterate storage volumes calling volume.activate()"""
        for storage in self.storage_volumes:
            storage.activate()


    def deactivate_storage(self):
        """Iterate storage volumes calling volume.deactivate()"""
        for storage in self.storage_volumes:
            storage.deactivate()


    def undefine_storage(self):
        """Iterate storage volumes calling volume.undefine()"""
        for storage in self.storage_volumes:
            storage.undefine()


    def get_definition(self):
        """
        Return a copy of the VM's definition
        """
        return dict(self.definition)


    def get_info(self):
        """
        Return an arbitrary dictionary of key->value pairs for this VM.
        """
        return {}


    def get_cpu_usage(self):
        """Return a measure of CPU usage"""
        return 0


    def get_memory_usage(self):
        """Return a measure of memory usage"""
        return 0


    def get_primary_ip(self):
        """
        If relevant, return the primary IP of this VM, otherwise None.
        """
        return None


    def get_console_command(self):
        """
        If relevant, return a command that could be used to access the
        console of this VM from the host.
        """
        return None
