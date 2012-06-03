Hypervisor-local provisioning of VMs
------------------------------------

NOTE: VM is used to refer to real "Virtual Machines", "Containers"
like OpenVZ/LXC, or any other service that implements the API.  For
example, you might create a customised LXC VM type that installs,
configures and runs specific services within containers, and
adds/removes them to/from a load balancer.

This handles the lifecycle of a local VM, including:
  * Defining VM
  * Locating/Provisioning the storage volume(s)
  * Provisioning OS template (if not PXE install)
  * Starting VM
  * Nice shutdown of VM
  * Poweroff of VM
  * Undefining VM
  * Disabling/Deprovisioning storage volumes
  * Deprovisioning VM

When a VM is first defined, a specific structure is passed in,
containing configuration for compute, storage, and network.  Depending
on the virtualisation type, this may not all be relevant.

It supports a pluggable framework to support different types of
virtualisation (eg. KVM, OpenVZ, Xen, LXC), and to support different
storage plugins.

Storage is pluggable, which may or may not make sense for any given
type of VM.  Storage plugins may also wrap other storage plugins, such
that you could have a storage plugin implementing get_directory(),
which uses an underlying storage device which implemented
get_blockdevice() (ie. format and mount an arbitrary block device,
which may actually be iSCSI or similar).  If the provided storage
plugins don't make sense for your use-case, you're free to create
new plugins, or adapt (via an adaption framework) existing plugins.

Additionally, you are free to not follow the storage API at all,
and have the storage plugins incompatible with other VM types, and
only useful to your VM type(s).
