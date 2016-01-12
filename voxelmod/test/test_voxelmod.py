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
from voxelinfo import VoxelInfo
from voxeldata import VoxelData

class TestReducedVoxelData(unittest.TestCase):
    """Tests for Voxel Info and Data."""
    @classmethod
    def setUpClass(cls):
        """Class-wide files"""
        cls.voxel_info_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.txt')
        cls.voxel_data_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'full_materials.raw')
        print('Voxel metadata file: ', cls.voxel_data_file)
        print('Voxel data file: ', cls.voxel_data_file)

    def testVoxelInfo(self):
        """Test Voxel Info (meta-data) class."""
        self.assertTrue(os.path.isfile(self.voxel_info_file))
        self.assertTrue(os.path.isfile(self.voxel_data_file))
        
