#!/usr/bin/env python3
"""
Test Voxel python classes.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
from os.path import pardir, sep
import unittest
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir))
from virtual_population import *

class TestReducedVoxelData(unittest.TestCase):
    """Tests for Voxel Info and Data."""
    @classmethod
    def setUpClass(cls):
        """Class-wide files"""
        cls.voxel_info_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.txt')
        cls.voxel_data_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.raw')
        print('Voxel metadata file: ', cls.voxel_info_file)
        print('Voxel data file: ', cls.voxel_data_file)

    def testVoxelEnvironment(self):
        """Test Voxel Info (meta-data) class."""
        self.assertTrue(os.path.isfile(self.voxel_info_file))
        self.assertTrue(os.path.isfile(self.voxel_data_file))

    def testCreateVirtPopVoxel(self):
        """Create a virtual population object."""
        testVoxel = VirtualPopulation()
        self.assertIsInstance(testVoxel, VirtualPopulation)
        testVoxel.name = 'myVoxel'
        self.assertEqual('myVoxel',testVoxel.name)
        testVoxel.nx = 100; testVoxel.ny = 200; testVoxel.nz = 300
        testVoxel.dx = 0.005; testVoxel.dy = 0.005; testVoxel.dz = 0.005;
        self.assertEqual(100, testVoxel.nx)
        self.assertEqual(200, testVoxel.ny)
        self.assertEqual(300, testVoxel.nz)
        self.assertEqual(0.005, testVoxel.dx)
        self.assertEqual(0.005, testVoxel.dy)
        self.assertEqual(0.005, testVoxel.dz)
        testVoxel.appendMaterial('Bone', 1.0, 1.0, 1.0)
        self.assertEqual([1, 'Bone', 1.0, 1.0, 1.0], testVoxel.material(1))
        testVoxel.appendMaterial('Fat')
        testVoxel.appendMaterial('Muscle')
        testVoxel.appendMaterial('Air')
        self.assertEqual(5, testVoxel.numMaterials)
        testVoxel.removeMaterial('Bone')
        self.assertEqual(4, testVoxel.numMaterials)
        

    def testCreateVirtPopVoxelFromFile(self):
        """Create a virtual population object from a raw and info files."""
        testVoxelReader = VirtualPopulationReader()
        self.assertIsInstance(testVoxelReader, VirtualPopulationReader)
        self.assertIsInstance(testVoxelReader.voxelModel, VirtualPopulation)
        testVoxelReader.loadVoxelInfo('full_materials.txt')
        self.assertEqual('full_materials', testVoxelReader.voxelModel.name)
        

if __name__ == '__main__':
    unittest.main()

