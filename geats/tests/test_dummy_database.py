# test the DummyDatabase

import unittest

from ..databases.dummydatabase import DummyDatabase

class DummyDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = DummyDatabase({})
        self.vmdef = {
            "vm_type": "dummy",
            "name": "vm001",
            "description": "vm001 / appserver 001",
        }

    def test_create_vm(self):
        self.db.create('vm001', self.vmdef)

    def test_list(self):
        self.db.create('vm001', self.vmdef)
        vms = self.db.list()
        self.assertEqual(vms, ["vm001"]) 

    def test_get_definition(self):
        self.db.create('vm001', self.vmdef)
        vmdef = self.db.get_definition('vm001')
        self.assertEqual(vmdef, self.vmdef)
