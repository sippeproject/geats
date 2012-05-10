class IStorageVolume:
    def get_name():
        """Return the name of this block device"""
    def activate():
        """Make the volume available"""
    def deactivate():
        """If required, de-activate the volume"""
    def format():
        """Format the device. At a minimum, clear bootsector and partitions"""
    def get_blockdevice():
        """Return the block device, or None"""
    def get_directory():
        """Return a directory, or None"""
    def get_filename():
        """Return a filename, or None"""
    def is_local():
        """Is this volume local to the machine or on a SAN/NAS/DRDB etc?"""
