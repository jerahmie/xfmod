#!/usr/bin/env python
"""
Test XFMUltipointGeom class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

TEST_MP_INFO = '/Data/CMRR/rf_coil_scripts/python/Test_Data/Test_Coil.xf/Simulations/000001/Run0001/output/MultiPoint_Solid_Sensor1_0_info.bin'
TEST_MP_DIR = '/Data/CMRR/rf_coil_scripts/python/Test_Data/Test_Coil.xf/Simulations/000001/Run0001/output/MultiPoint_Solid_Sensor1_0'

import os
from xfmatgrid import *

class TestXFMultiPointGeometry(unittest.TestCase):
    """Tests for Multipoint sensor info."""
    def setUp(self):
        self.mp_info = XFMultiPointInfo(TEST_MP_INFO)
        self.mp_geom = XFMultiPointGeometry(os.path.join(TEST_MP_DIR,
                                                         'geom.bin'))

    def test_multipoint_geometry(self):
        """Test multipoint geometry file."""
        self.assertEqual(self.mp_info.num_points, 
                         self.mp_geom._num_points)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

