class AlreadyExistsException(RuntimeError):
    """
    Generated on a .create() DB call where the key already
    exists.
    """
class InvalidVMDefinition(RuntimeError):
    """
    The VM definition was deemed invalid either by the
    Manager or by the VM instance.
    """

class UnsupportedVMType(RuntimeError):
    """
    The supplied vm_type is not supported or unknown.
    """

class UnsupportedStorageType(RuntimeError):
    """
    The supplied type for a storage volume was not found
    or is not supported for this vm_type.
    """

class VMException(RuntimeError):
    """
    An arbitrary exception while performing a VM action.
    It's expected that the exception message can be returned
    directly to the user.
    """

class FailedToAcquireLockException(VMException):
    """
    Each VM has a lockfile that prevents multiple operations
    being performed on it simultaneously.
    """

class VMLockedException(VMException):
    """
    VMLockedException means that VM.is_locked() returned True
    for an operation that requires it to be false.
    Most commonly, this is to prevent a VM being accidently
    undefine'd.
    """


