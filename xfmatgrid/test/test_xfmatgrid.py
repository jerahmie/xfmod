#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import struct
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),
                                            os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from xfmatgrid import *

TEST_PROJECT_DIR = os.path.realpath(os.path.relpath(os.path.join('..', '..',
                                                            'Test_Data',
                                                            'Test_Coil.xf')))
MULTIPOINT_SENSOR_FILE = os.path.realpath(os.path.join(TEST_PROJECT_DIR,
                                'Simulations', '000001', 'Run0001', 'output',
                                'MultiPoint_Solid_Sensor1_0_info.bin'))

class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    def setUp(self):
        self.field_nugrid = XFFieldNonUniformGrid()
        self.field_nugrid.sim_id = 1

    def test_xf_run_id_to_str(self):
        """Verify XFdtd valid run string composition."""
        self.assertTrue(is_valid_run_id(1))
        self.assertTrue(is_valid_run_id(9999))
        self.assertFalse(is_valid_run_id(-1))
        self.assertFalse(is_valid_run_id(0))
        self.assertFalse(is_valid_run_id(10000.0))
        self.assertEqual('Run0001',xf_run_id_to_str(1))
        self.assertEqual('Run9999',xf_run_id_to_str(9999))

    def test_xf_sim_id_to_str(self):
        """Verify XFdtd valid simulation string composition."""
        self.assertTrue(is_valid_sim_id(1))
        self.assertTrue(is_valid_sim_id(999999))
        self.assertFalse(is_valid_sim_id(-1.1))
        self.assertFalse(is_valid_sim_id(0))
        self.assertFalse(is_valid_sim_id(1000000))
        self.assertEqual('000001',xf_sim_id_to_str(1))
        self.assertEqual('999999',xf_sim_id_to_str(999999))

    def test_project_file(self):
        self.field_nugrid.project_dir = TEST_PROJECT_DIR
        self.assertEqual(TEST_PROJECT_DIR, self.field_nugrid.project_dir)
        self.assertEqual(MULTIPOINT_SENSOR_FILE,
                         self.field_nugrid._multipoint_sensor_info_files[0])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
