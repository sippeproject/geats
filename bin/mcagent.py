#!/usr/bin/python
"""
mcagent is called by mcollective to run commands.

It reads the request in JSON format from a file, and it
writes the response to another file in JSON format.
"""
import sys
import json
import os.path
import traceback
from geats.manager import Manager
from geats.sysstat import SysStat

# exit codes
STATUS_OK = 0
STATUS_ABORTED = 1
STATUS_UNKNOWN_ACTION = 2
STATUS_MISSING_DATA = 3
STATUS_INVALID_DATA = 4
STATUS_OTHER_ERROR = 5

def report_exception():
    traceback.print_exc()
    sys.exit(STATUS_OTHER_ERROR)

def die(msg, status=STATUS_ABORTED):
    print >>sys.stderr, msg
    sys.exit(status)

def write_response(response, response_file):
    try:
        with open(response_file, "w") as fd:
            json.dump(response, fd)
    except:
        report_exception()

def load_request(request_file):
    try:
        with open(request_file) as fd:
            return json.load(fd)
    except:
        report_exception()

def get_system_stats():
    """Return some stats about the system"""
    sysstat = SysStat()
    return {
        "swap_total" : sysstat.swaptotal,
        "swap_used"  : sysstat.swapused,
        "swap_free"  : sysstat.swapfree,
        "mem_total"  : sysstat.memtotal,
        "mem_used"   : sysstat.memused,
        "mem_free"   : sysstat.memfree,
        "mem_buffers": sysstat.membuffers,
        "mem_cached" : sysstat.memcached,
        #"cpu_user"   : cputimes.user,
        #"cpu_system" : cputimes.system,
        #"cpu_idle"   : cputimes.idle,
        #"cpu_iowait" : cputimes.iowait,
        "load_avg"   : os.getloadavg(),
    }


def cmd_status():
    manager = Manager()
    vms = {}
    for vm_name in manager.list_vms():
        vm = manager.get_vm(vm_name)
        vm_hash = {
            "definition" : vm.get_definition(),
            "state" : vm.get_state()
        }
        vms[vm_name] = vm_hash
    return {
        "vms" : vms,
        "status" : get_system_stats(),
    }

def cmd_info(vm_name):
    manager = Manager()
    vm = manager.get_vm(vm_name)
    vm_hash = {
        "definition" : vm.get_definition(),
        "state" : vm.get_state()
    }
    return vm_hash

def cmd_define(vm_name, vm_definition):
    manager = Manager()
    vm = manager.define_vm(vm_name, vm_definition)
    vm_hash = {
        "definition": vm.get_definition(),
        "state": vm.get_state()
    }

def process_request(request):
    action = request['action']
    data = request['data']
    if action == 'status':
        return cmd_status()
    vm_name = request['data'].get('vm_name', None)
    if vm_name is None:
        die("Missing vm_name parameter", STATUS_MISSING_DATA)

    if action == 'define':
        vm_definition = request['data'].get('definition', None)
        if vm_definition is None:
            die("Missing definition parameter", STATUS_MISSING_DATA)
        return cmd_define(vm_name, vm_definition)

    if action == 'migrate':
        vm_destination = request['data'].get('vm_destination', None)
        if vm_destination is None:
            die("Missing vm_destination parameter", STATUS_MISSING_DATA)
        return cmd_migrate(vm_name, vm_destination)

    if action == 'info':
        return cmd_info(vm_name)

    # all the rest are no-argument actions on existing VMs
    manager = Manager()
    try:
        vm = manager.get_vm(vm_name)
    except KeyError:
        if action in ('undefine', 'deprovision',):
            return
        raise

    if action == 'start':
        vm.start()
    elif action == 'stop':
        vm.stop()
    elif action == 'shutdown':
        vm.shutdown()
    elif action == 'undefine':
        vm.undefine()
    elif action == 'deprovision':
        vm.deprovision()

if __name__ == "__main__":
    try:
        request_file = sys.argv[1]
        response_file = sys.argv[2]
    except IndexError:
        print >>sys.stderr, "Syntax: %s <json input file> <json output file>" % (sys.argv[0],)
        sys.exit(STATUS_OTHER_ERROR)
    request = load_request(request_file)
    try:
        response = process_request(request)
        write_response(response, response_file)
    except:
        report_exception()

