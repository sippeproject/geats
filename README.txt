Geats
=====

Geats is a pluggable Local Resource Manager to manage resources such
as VMs and containers on a single server.  It manages the entire
lifecycle of resources on a single server, from initial provisioning
to the final deprovisioning of them.

It comes with built-in support for managing LXC containers using the
standard lxc tools, but makes it easy to extend it to use other
virtualisation or container technologies such as KVM, Xen, or OpenVZ.

Geats can be thought of as filling a similar role to libvirt, in that
it comes with an easy-to-use python API, and a simple command line
tool.

Geats can be used in conjunction with the `Vagoth
<https://github.com/sippeproject/vagoth>`_ a Cluster Controller to
manage VMs across multiple servers.

Lifecycle management
--------------------

A typical lifecycle of a VM or container is as follows:
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

Virtual Machine Plugins
-----------------------

Geats supports a pluggable framework to support different types of
virtualisation, containers, or other resources (eg. KVM, OpenVZ, Xen,
LXC).  Your implementation should match the IVirtualMachine interface
to work nicely with the existing CLI tool.  This is made easy by
inheriting from the AbstractVirtualMachine class and overloading the
methods to manage the given VM/container/resource.

Storage Plugins
---------------

Storage is pluggable, which may or may not make sense for any given
type of VM or resource.  Storage plugins may also wrap other storage
plugins, such that you could have a storage plugin implementing
get_directory(), which uses an underlying storage device which
implemented get_blockdevice() (ie. format and mount an arbitrary block
device, which may actually be iSCSI or similar).  If the provided
storage plugins don't make sense for your use-case, you're free to
create new plugins or adapt existing plugins via the adaption
framework.

Additionally, you are free to not follow the storage API at all, and
have the storage plugins incompatible with other VM types, and only
useful to your VM type(s).


Database Plugins
----------------

It's possible to implement a different database than the default
pickle-based database.

Given the nature of Geats only managing local resources, it probably
doesn't make sense to use a remotely-hosted data store.

