# test the DummyDatabase

import unittest

from ..storage.dummystoragevolume import DummyStorageVolume

class DummyStorageTest(unittest.TestCase):
    def setUp(self):
        self.volume = DummyStorageVolume("vda", {
            "name": "vda",
            "blockdevice": "/dev/DOES_NOT_EXIST",
        }, vm=None, config={})

    def test_get_name(self):
        self.assertEqual(self.volume.get_name(), "vda")

    def test_activate_volume(self):
        self.volume.activate()

    def test_deactivate_volume(self):
        self.volume.deactivate()

    def test_format_volume(self):
        self.volume.format()

    def test_get_blockdevice(self):
        self.assertEqual("/dev/DOES_NOT_EXIST", self.volume.get_blockdevice())

    def test_is_local(self):
        self.assertTrue(self.volume.is_local())
