# test the DummyDatabase

import unittest

from ..databases import DummyDatabase

class DummyDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = DummyDatabase({})
        self.vmdef = {
            "vm_type": "dummy",
            "name": "vm001",
            "description": "vm001 / appserver 001",
        }
    def test_define_vm(self):
        self.db.define_vm('vm001', self.vmdef)

    def test_list_vms(self):
        self.db.define_vm('vm001', self.vmdef)
        vms = self.db.list_vms()
        self.assertEqual(vms, ["vm001"]) 

    def test_get_vm_definition(self):
        self.db.define_vm('vm001', self.vmdef)
        vmdef = self.db.get_vm_definition('vm001')
        self.assertEqual(vmdef, self.vmdef)
