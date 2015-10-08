#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import struct
import unittest

#PACKAGE_PARENT = '..'
#SCRIPT_RP = os.path.realpath(os.path.join(os.getcwd(),
#                                          os.path.expanduser(__file__)))
#SCRIPT_DIR = os.path.dirname(SCRIPT_RP)
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import xfmatgrid

TEST_COIL_DIR = os.path.join('/Data', 'CMRR', 'rf_coil_scripts', 'python',
                             'Test_Data', 'Test_Coil.xf')
TEST_PROJECT_DIR = os.path.realpath(os.path.relpath(TEST_COIL_DIR))
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
MULTIPOINT_SENSOR_FILE = os.path.realpath(os.path.join(RUN_OUT_DIR,
                                                       'MultiPoint_Solid_Sensor1_0_info.bin'))

class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    def setUp(self):
        self.field_nugrid = xfmatgrid.XFFieldNonUniformGrid()
        self.field_nugrid.sim_id = 1

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
        self.field_nugrid.project_dir = TEST_PROJECT_DIR
        self.assertEqual(TEST_PROJECT_DIR, self.field_nugrid.project_dir)
        self.assertEqual(MULTIPOINT_SENSOR_FILE,
                         self.field_nugrid._multipoint_sensor_info_file[0])
        self.assertEqual(1, len(self.field_nugrid._multipoint_sensor_info))
        self.assertEqual('Rmpt', self.field_nugrid._multipoint_sensor_info[0].header)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()