#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import struct
import unittest
import numpy as np
import xfmatgrid

TEST_COIL_DIR = os.path.join('/Data', 'CMRR', 'rf_coil_scripts', 'python',
                             'Test_Data', 'Test_Coil.xf')
TEST_PROJECT_DIR = os.path.realpath(os.path.relpath(TEST_COIL_DIR))
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
MULTIPOINT_SENSOR_FILE = os.path.realpath(os.path.join(RUN_OUT_DIR,
                                                       'MultiPoint_Solid_Sensor1_0_info.bin'))
FREQUENCIES_BIN = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0',
                                'frequencies.bin')
TEST_FREQUENCY = 296500000.0  # 296.5 MHz

TEST_MULTIPOINT_DIRS = ['ss_Exit', 'ss_Exrt', 'ss_Eyit', 'ss_Eyrt', 'ss_Ezit', 'ss_Ezrt', 'ss_Hxit', 'ss_Hxrt', 'ss_Hyit', 'ss_Hyrt', 'ss_Hzit', 'ss_Hzrt', 'ss_Jxi', 'ss_Jxr', 'ss_Jyi', 'ss_Jyr', 'ss_Jzi', 'ss_Jzr', 'ss_Bxit', 'ss_Bxrt', 'ss_Byit', 'ss_Byrt', 'ss_Bzit', 'ss_Bzrt', 'ss_PddEx', 'ss_PddEy', 'ss_PddEz', 'ss_PddHx', 'ss_PddHy', 'ss_PddHz']

class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    @classmethod
    def setUpClass(cls):
        cls.field_nugrid = xfmatgrid.XFFieldNonUniformGrid(TEST_PROJECT_DIR, 
                                                           1, 1)

    def setUp(self):
        pass
 
    def test_xf_run_id_to_str(self):
        """Verify XFdtd valid run string composition."""
        self.assertTrue(xfmatgrid.xfutils.is_valid_run_id(1))
        self.assertTrue(xfmatgrid.xfutils.is_valid_run_id(9999))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(-1))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(0))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(10000.0))
        self.assertEqual('Run0001', xfmatgrid.xfutils.xf_run_id_to_str(1))
        self.assertEqual('Run9999', xfmatgrid.xfutils.xf_run_id_to_str(9999))

    def test_xf_sim_id_to_str(self):
        """Verify XFdtd valid simulation string composition."""
        self.assertTrue(xfmatgrid.xfutils.is_valid_sim_id(1))
        self.assertTrue(xfmatgrid.xfutils.is_valid_sim_id(999999))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(-1.1))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(0))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(1000000))
        self.assertEqual('000001', xfmatgrid.xfutils.xf_sim_id_to_str(1))
        self.assertEqual('999999', xfmatgrid.xfutils.xf_sim_id_to_str(999999))

    def test_project_file(self):
        self.assertEqual(TEST_PROJECT_DIR, self.field_nugrid.project_dir)
        self.assertEqual(MULTIPOINT_SENSOR_FILE,
                         self.field_nugrid._mp_ss_info_file[0])
        self.assertEqual('Rmpt', self.field_nugrid._mp_ss_info.header)

    def test_frequencies_bin(self):
        self.assertEqual(TEST_FREQUENCY, 
                         self.field_nugrid._mp_freq._frequencies[0])

    def test_field_data(self):
        self.assertEqual(TEST_MULTIPOINT_DIRS, 
                         self.field_nugrid._mp_field_types)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
