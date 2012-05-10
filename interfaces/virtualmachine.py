class IVirtualMachine:
    def get_name():
        """Return the name/identifier of this virtual machine"""
    def get_description():
        """Return the description of this virtual machine"""
    def get_state():
        """
        Return the state as a tuple of state & substate:
            (running, substate)
            (paused, substate)
            (stopped, substate)
            (unknown, substate)
        
        The substates may be used in the event that there are additional
        steps involved in the lifecycle of a particular type of VM.
        An example might be "paused/migrating".  By default, substate is
        the same as state.
        """
    def lock():
        """
        Lock the VM - do not allow state changes until it is unlocked
        """
    def unlock():
        """
        Unlock the VM
        """
    def is_locked():
        """
        Is the VM currently locked?
        """
    def define():
        """
        Do any actions to define this VM in the hypervisor.
        eg. Create libvirt XML, LXC config file, etc.
        
        The VM definition will probably have been passed in with the
        constructor.  It's OK for define() to modify the vm definition.
        Modifications after this point will be ignored.
        """
    def start():
        """
        Start this VM:
          1. Return without exception if already running.
          2. Activate each storage volume.
          3. Raise a Storage exception if failed.
          4. Start the VM by calling self._vm_start(self)
          5. Raise an Exception if it failed.
        """
    def migrate(destination):
        """
        Migrate this VM to the given destination.  If not supported for this VM
        type, it will raise a NotImplementedError.
        """
    def stop():
        """
        Stop this VM:
          1. Return without error if VM is already stopped.
          2. Stop the VM
          3. Raise an Exception if it failed.

        Storage Volumes remain active.
        """
    def shutdown():
        """
        Politely shutdown this VM:
          1. Return without error if VM is already stopped.
          2. Shutdown the VM, falling back to stop() if appropriate.
          3. Raise an Exception if it failed.

        Shutdown can return immediately, without confirming that it succeeded.
        
        Indeed, it may not succeed (eg. ACPI shutdown was ignored)
        
        Storage Volumes may remain active (if appropriate)
        """
    def undefine():
        """
        Undefine this VM, stopping it first if necessary.
        """
    def get_storage_volumes():
        """
        Return an array of IStorageVolume's (if applicable).

        The first entry in the array should store the boot sector and/or
        operating system.  On re-install, storage_array[0].format()
        may be called to wipe the boot sector/partition tables.
        """
    def activate_storage():
        """
        If state is stopped, iterate through storage devices
        and activate them.

        This will typically occur right before a VM is started.
        """
    def deactivate_storage():
        """
        If state is stopped, iterate through storage devices
        and deactivate them.

        This will typically occur right before a VM is undefined.
        """
    def get_definition():
        """
        Return the VM definition.  This is the definition that will
        be saved in the VM database.
        """
    def get_info():
        """
        Return an arbitrary dictionary of key->value information about this
        VM.  Keys are as follows:
            hypervisor => dictionary returned by adapter.vm_info(self)
            definition => initial dictionary used to define this VM
        """
    def get_cpu_usage():
        """
        Return the number of CPUs allocated to this VM.
        """
    def get_memory_usage():
        """
        Return the amount of memory, in MB, allocated to this VM.
        """
