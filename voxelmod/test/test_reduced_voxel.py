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
from reduced_voxel import ReducedVoxelMap, VoxelWriter

class TestReducedVoxelData(unittest.TestCase):
    """Tests for voxel material reductions."""
    @classmethod
    def setUpClass(cls):
        voxel_map_file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + sep + 'material_map_4.txt')
        print('voxel_map_file: ', voxel_map_file)
        cls.vmap = ReducedVoxelMap(voxel_map_file)

    def testVoxelMap(self):
        """Test the VoxelMap class."""
        self.assertEqual(r'Muscle', self.vmap.voxel_map['Tongue'])
        self.assertEqual(r'Fat', self.vmap.voxel_map['Fat'])
        self.assertEqual(r'Bone', self.vmap.voxel_map['Mandible'])

    def testVoxelWriter(self):
        """Write a simple voxel file."""
        vw_info = voxelinfo.VoxelInfo()
        vw_info.nx = 10; vw_info.ny = 10; vw_info.nz = 10
        vw_info.dx = 0.005; vw_info.dy = 0.005; vw_info.dz = 0.005
        
        test_voxel_txt = VoxelWriter()
        self.assertEqual('text_voxel', test_voxel_txt.voxel_name)
        


if __name__ == '__main__':
    unittest.main()
