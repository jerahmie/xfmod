#!/usr/bin/env python3
"""
Test reduce_itis_voxel.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
from os.path import pardir, sep
import unittest
sys.path.append(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) +
                                 sep + pardir ))
from virtual_population import *
from reduced_voxel import ReduceVoxel

class TestReducedVoxelData(unittest.TestCase):
    """Tests for voxel material reductions."""
    @classmethod
    def setUpClass(cls):
        cls.voxelMapFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                        sep + 'material_map_4.txt')
        fullMaterialInfoFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                                sep + 'full_materials.txt')
        fullMaterialDataFile = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + \
                                                sep + 'full_materials.raw')
        
        print('voxelMapFile: ', cls.voxelMapFile)
        print('dukeVoxelInfoFile: ', fullMaterialInfoFile)
        print('dukeVoxelDatafile: ', fullMaterialDataFile)
        
        voxelReader = VirtualPopulationReader()
        voxelReader.loadInfo(fullMaterialInfoFile)
        voxelReader.loadData(fullMaterialDataFile)
        cls.fullMaterialVoxel =  voxelReader.voxelModel

    def testEnvironment(self):
        """Verify the test class is set up properly."""
        self.assertIsInstance(self.fullMaterialVoxel, VirtualPopulation)
        

    def testReduceVoxel(self):
        """Test the ReduceVoxel class."""
        fourMatVoxelWriter = VirtualPopulationWriter()
        fourMatVoxelWriter.voxelModel = ReduceVoxel(self.voxelMapFile, self.fullMaterialVoxel).voxelModel
        self.assertIsInstance(fourMatVoxelWriter.voxelModel, VirtualPopulation)
        fourMatVoxelWriter.voxelModel.name = 'Duke_4_Mat_Head_5mm'
        fourMatVoxelWriter.writeVoxelToFile()

if __name__ == '__main__':
    unittest.main()
