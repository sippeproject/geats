def get_config(config_searchpaths):
    from configobj import ConfigObj
    import os.path

    for path in config_searchpaths:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return ConfigObj(path)
    return ConfigObj()

def dynamic_lookup(moduleColonName):
    modulestr, name = moduleColonName.split(":")
    module = __import__(modulestr, fromlist=[name])
    return getattr(module, name)

_static_config = None

class Config(object):
    def __init__(self, config_searchpaths=None):
        global _static_config
        if _static_config != None:
            self.config = _static_config
        else:
            searchpath = config_searchpaths or ["~/.config/sippe/geats.conf", "/etc/sippe/geats.conf"]
            _static_config = self.config = get_config(searchpath)
    def get_vm_config(self, vm_type):
        vms = self.config.get('vms', {})
        return vms.get(vm_type, {})
    def get_vm_factory(self, vm_type):
        vm_config = self.get_vm_config(vm_type)
        if "factory" in vm_config:
            return dynamic_lookup(vm_config["factory"])
    def get_storage_config(self, storage_type):
        storages = self.config.get('storage', {})
        return storages.get(storage_type, {})
    def get_storage_factory(self, storage_type):
        storage = self.get_storage_config(storage_type)
        if "factory" in storage:
            return dynamic_lookup(storage["factory"])
    def get_storage_adapters(self, storage_type):
        storage = self.get_storage_config(storage_type)
        if "adapter_factory" in storage:
            adapters = storage["adapter_factory"]
            if not type(adapters) in (tuple, list):
                adapters = [adapters]
            return map(dynamic_lookup, adapters)
    def get_database_config(self):
        db_config = self.config.get("database", {})
        #CONFVAR# database.current: name of the database plugin to use
        current = db_config.get("current", None)
        return db_config.get(current)
    def get_database_factory(self):
        db_config = self.get_database_config()
        if "factory" in db_config:
            return dynamic_lookup(db_config["factory"])
    def get_lock_config(self):
        return self.config.get("lock", {})
    def get_lock_factory(self):
        lock_config = self.get_lock_config()
        if "factory" in lock_config:
            return dynamic_lookup(lock_config["factory"])
