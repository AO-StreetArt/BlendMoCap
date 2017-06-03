import unittest
import bpy

#Import the addon for the purposes of the test script
import blendmocap

class TestAddon(unittest.TestCase):
    def test_addon_enabled(self):
        self.assertIsNotNone(blendmocap.bl_info)

# we have to manually invoke the test runner here
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAddon)
unittest.TextTestRunner().run(suite)
