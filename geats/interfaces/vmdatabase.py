class IVMDatabase:
    """
    Store and retrieve VM information.  It's important that it does this
    without losing any information (eg. from a full disk)
    """
    def list():
        """
        Return a list of entries by name
        """
    def create(name, definition, **extras):
        """
        Create the entry in the database.
        @param name: VM name (primary key)
        @param definition: dict of the VM definition
        @param extras: dict of dicts to be used by plugins, etc.
        """
    def update(vm_name, definition=None, **extras):
        """
        Update the definition or the extras dictionary
        """
    def delete(name):
        """
        Remove the name from the database.
        """
    def get_definition(name):
        """
        Return the definition dict for the given name.
        """
    def get(name, key=None):
        """
        Return the given key (or all if key is None) for the given name.
        If the key is not found in the store for $name,
        returns an empty dict.
        """
