class IVMDatabase:
    """
    Store and retrieve VM information.  It's important that it does this
    without losing any information (eg. from a full disk)
    """
    def list_vms():
        """
        Return a list of defined VMs by name
        """
    def define_vm(vm_name, vm_definition):
        """
        Create the VM in the database.
        """
    def undefine_vm(vm_name):
        """
        Remove the VM from the database.
        """
    def get_vm_definition(vm_name):
        """
        Return the VM definition for the given VM.
        """
