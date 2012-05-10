"""
Support for KVM virtual machines using LibVirt
"""

from abstract import AbstractVirtualMachine
import os.path
import shutil
import ipaddr
import libvirt
import mako

def convert_ip_netmask_to_cidr(ip, netmask):
    return str(ipaddr.IPv4Network("%s/%s" % (ip, netmask)))

def create_kvm_config(directory, name, ip, netmask, hwaddr, bridge='br0'):
    

def create_firstboot_config(directory, name, ip, netmask, gateway, metadata=None):
    firstboot = os.path.join(directory, "rootfs/etc/firstboot.config")
    fd = open(firstboot, 'w')
    try:
        fd.write('NAME="%s"\n' % (name,))
        fd.write('IPADDRESS="%s"\n' % (ip,))
        fd.write('NETMASK="%s"\n' % (netmask,))
        fd.write('GATEWAY="%s"\n' % (gateway,))
        if metadata:
            for k,v in metadata.items():
                fd.write('%s="%s"\n' % (k,v))
    finally:
        fd.close()

class KVMVirtualMachine(AbstractVirtualMachine):
    def _define(self):
        # FIXME
        name = self.get_name()
        directory = os.path.join("/var/lib/lxc/", name)
        template = self.definition['template']
        targz = os.path.join("/scratch/templates/lxc/%s.tar.gz" % (template,))
        network = self.definition.get('network')
        eth0 = network.get('eth0')
        ip = eth0['ipaddress']
        netmask = eth0['netmask']
        gateway = eth0['gateway']
	hwaddr = eth0['hwaddr']
        create_lxc_config(directory, name, ip, netmask, hwaddr)
        hostnamefile = os.path.join(directory, "rootfs/etc/hostname")
        if not os.path.exists(hostnamefile):
            unpack_lxc_rootfs(directory, name, targz)
            create_firstboot_config(
                directory,
                name,
                ip,
                "255.255.255.0",
                "192.168.1.1",
                metadata=self.definition.get('metadata', None))
        # update hostname file
        fd = open(hostnamefile, 'w')
        try:
            fd.write(name+"\n")
        finally:
            fd.close()
    def _start(self):
        os.system("/opt/lxc/bin/lxc-start -d -n %s" % (self.name,))
    def _stop(self):
        os.system("/opt/lxc/bin/lxc-stop -n %s" % (self.name,))
    def _shutdown(self):
        os.system("/opt/lxc/bin/lxc-stop -n %s" % (self.name,))
    def _undefine(self):
        name = self.get_name()
        directory = os.path.join("/var/lib/lxc/", name)
        shutil.rmtree(directory)
    def get_state(self):
        if os.path.isdir(os.path.join("/cgroup", self.name)):
            return "running", "running"
        else:
            return "stopped", "stopped"
    def get_cpu_usage(self):
        return 1
    def get_memory_usage(self):
        return 1024
