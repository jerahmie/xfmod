#!/usr/bin/env python
"""
Test XFMUltipointGeom class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import unittest
import numpy as np
from xfmod import xfmatgrid

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..', '..', '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))

RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
TEST_MP_INFO = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0_info.bin')
TEST_MP_DIR = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0')
TEST_MP_GEOM = os.path.join(TEST_MP_DIR, 'geom.bin')

class TestXFMultiPointGeometry(unittest.TestCase):
    """Tests for Multipoint sensor info."""
    @classmethod
    def setUpClass(cls):
        print('Executing tests in ' + __file__)
        cls.mp_info = xfmatgrid.XFMultiPointInfo(TEST_MP_INFO)
        cls.mp_geom = xfmatgrid.XFMultiPointGeometry(TEST_MP_GEOM,
                                                     cls.mp_info.num_points)
    def setUp(self):
        pass

    def test_multipoint_geometry(self):
        """Test multipoint geometry file."""
        print(self.id())
        self.assertEqual((self.mp_info.num_points, 3),
                         np.shape(self.mp_geom._vertices))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
