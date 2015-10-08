#!/usr/bin/env python
"""
Test XFMultiPointSSField class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import os
import unittest
import xfmatgrid

TEST_COIL_DIR = os.path.join('/Data', 'CMRR', 'rf_coil_scripts', 'python',
                             'Test_Data', 'Test_Coil.xf')
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
TEST_MP_INFO_FILE = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0_info.bin')
TEST_MP_DIR = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0')
TEST_SS_BXIT = os.path.join(TEST_MP_DIR, 'ss_Bxit', '0.bin')
TEST_SS_BXRT = os.path.join(TEST_MP_DIR, 'ss_Bxrt', '0.bin')
TEST_SS_EXIT = os.path.join(TEST_MP_DIR, 'ss_Exit', '0.bin')
TEST_SS_EXRT = os.path.join(TEST_MP_DIR, 'ss_Exrt', '0.bin')
TEST_SS_PDDEY = os.path.join(TEST_MP_DIR, 'ss_Pddey', '0.bin')
TEST_SS_JPDDHZ = os.path.join(TEST_MP_DIR, 'ss_JPddHz', '0.bin')

class TestXFMultiPointFrequencies(unittest.TestCase):
    """Tests for Multipoint solid state field."""
    def setUp(self):
        self.mp_info = xfmatgrid.XFMultiPointInfo(TEST_MP_INFO_FILE)
        self.mp_ssField = xfmatgrid.XFMultiPointSSField(TEST_SS_BXIT, 
                                                        self.mp_info.num_points)

    def test_ssBxit(self):
        """Read steady-state field data from test project."""
        self.assertEqual(self.mp_info.num_points,
                         len(self.mp_ssField.ss_field))
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
