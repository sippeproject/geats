from os.path import exists

class AbstractStorageAdapter:
    """
    A Storage Adapter should inherit from this class, and override the
    following methods (at the very least):

       * define()
       * undefine()
       * activate()
       * deactivate()
       * format()
       * is_online()

    and it should override one of the following:

       * get_blockdevice()
       * get_directory()
       * get_filename()

    self.wrapped_volume is available, referring to the volume that this
    class is wrapping.
    """
    def __init__(self, wrapped_volume, definition, vm, config):
        self.wrapped_volume = wrapped_volume
        self.name = wrapped_volume.name
        self.definition = definition
        self.vm = vm
    def get_name(self):
        return self.name
    def define(self):
        """
        Called when a VM is defined. It should check the validity of the
        storage volume, obtain locks if necessary, but probably not do much
        else.
        """
        raise NotImplementedError
    def activate(self):
        """
        Called to activate the storage volume.  This should be an idempotent
        operation.
        """
        raise NotImplementedError
    def deactivate(self):
        """
        Called to deactivate the storage volume.  For a mounted directory,
        it should probably unmount it.  Storage volumes will only be
        de-activate'd after the VM has successfully shut down.
        """
        raise NotImplementedError
    def undefine(self):
        """
        Called just before a VM is undefine'd on the server.  Cleanup
        actions should go here (like releasing locks on shared storage)
        If this is a transient storage type, you might remove it
        altogether.
        """
        raise NotImplementedError
    def format(self):
        """
        Format the volume.  Make it pristine again.  This might mean
        removing a file, zero'ing the boot sector & partition table,
        or rm -rf'ing all files in a directory.
        """
        raise NotImplementedError
    def get_blockdevice(self):
        """
        If this storage plugin provides a block device, then return the full
        path to the block device.  If not, return None.
        """
        return None
    def get_directory(self):
        """
        If this storage plugin provides a directory, then return the full
        path to the directory.  If not, return None.
        """
        return None
    def get_filename(self):
        """
        If this storage volume is a single file (eg. qcow2, sparsefile) then
        return the full filename.  If not, return None.
        """
        return None
    def is_local(self):
        """
        Is the storage volume local to this server, or is it on a shared
        medium (eg. NFS, DRBD, iSCSI)
        """
        return self.wrapped_volume.is_local()
    def is_online(self):
        """
        Is the storage volume currently available for use?
        """
        raise NotImplementedError
