#!/usr/bin/env python
"""
Test XFMultiPointSSField class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import os
import re
import unittest
import numpy as np
from xfmod import xfmatgrid

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))

RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
TEST_MP_INFO_FILE = os.path.join(RUN_OUT_DIR,
                                 'MultiPoint_Solid_Sensor1_0_info.bin')
TEST_MP_DIR = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0')
TEST_SS_BXIT = os.path.join(TEST_MP_DIR, 'ss_Bxit', '0.bin')
TEST_SS_BXRT = os.path.join(TEST_MP_DIR, 'ss_Bxrt', '0.bin')
TEST_SS_EXIT = os.path.join(TEST_MP_DIR, 'ss_Exit', '0.bin')
TEST_SS_EXRT = os.path.join(TEST_MP_DIR, 'ss_Exrt', '0.bin')
TEST_SS_PDDEY = os.path.join(TEST_MP_DIR, 'ss_Pddey', '0.bin')
TEST_SS_JPDDHZ = os.path.join(TEST_MP_DIR, 'ss_JPddHz', '0.bin')
MP_SS_RE = r'([0-9A-Za-z/_.]*)(MultiPoint_Solid_Sensor[0-9]*_[0-9]*)'

class TestXFMultiPointFrequencies(unittest.TestCase):
    """Tests for Multipoint solid state field."""
    def setUp(self):
        print('Executing tests in ' + __file__)
        self.mp_info = xfmatgrid.XFMultiPointInfo(TEST_MP_INFO_FILE)
        mp_sensor_dir = re.match(MP_SS_RE, TEST_MP_INFO_FILE)
        mp_geom_file = os.path.join(mp_sensor_dir.group(1),
                                    mp_sensor_dir.group(2),
                                    r'geom.bin')
        self.mp_geom = xfmatgrid.XFMultiPointGeometry(mp_geom_file,
                                                      self.mp_info.num_points)
        self.mp_ss_field = xfmatgrid.XFMultiPointSSField(TEST_SS_BXIT,
                                                         self.mp_info,
                                                         self.mp_geom)

    def test_ss_bxit(self):
        """Read steady-state field data from test project."""
        print(self.id())
        self.assertEqual(self.mp_info.num_points,
                         np.size(self.mp_ss_field.ss_field))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
