#!/usr/bin/env python
"""
Test XFMultiPointInfo class.
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

TEST_MP_FILE = '/Data/CMRR/rf_coil_scripts/python/Test_Data/Test_Coil.xf/Simulations/000001/Run0001/output/MultiPoint_Solid_Sensor1_0_info.bin'

import os
from xfmatgrid import *

class TestXFMultiPointInfo(unittest.TestCase):
    """Tests for XF Multipoint sensor info."""
    def setUp(self):
        self.mp_info = XFMultiPointInfo(TEST_MP_FILE)
        
    def test_header_info(self):
        MP_HEADER = 'Rmpt'
        MP_VERSION = 2
        MP_FIELDS_MASK = struct.unpack('>I',struct.pack('<I',0x0000f001))[0]
        MP_NUM_POINTS = struct.unpack('>Q',struct.pack('<Q',0x581eb10000000000))[0]
        self.assertEqual(MP_HEADER, self.mp_info.header)
        self.assertEqual(MP_VERSION, self.mp_info.version)
        self.assertEqual(MP_FIELDS_MASK, self.mp_info.fields_mask)
        self.assertEqual(MP_NUM_POINTS, self.mp_info.num_points)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
