#!/usr/bin/env python
"""
Test XFMultiPointInfo class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import struct
import unittest
from xfmod import xfmatgrid

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..', '..', '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))

RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
TEST_MP_FILE = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0_info.bin')

MP_HEADER = 'Rmpt'
MP_VERSION = 2
MP_FIELDS_MASK = struct.unpack('>I', struct.pack('<I', 0x0000f001))[0]
MP_NUM_POINTS = struct.unpack('>Q', struct.pack('<Q', 0x581eb10000000000))[0]

class TestXFMultiPointInfo(unittest.TestCase):
    """Tests for XF Multipoint sensor info."""
    def setUp(self):
        print('Executing tests in ' + __file__)
        self.mp_info = xfmatgrid.XFMultiPointInfo(TEST_MP_FILE)

    def test_header_info(self):
        """Test the multipoint header info."""
        print(self.id())
        self.assertEqual(MP_HEADER, self.mp_info.header)
        self.assertEqual(MP_VERSION, self.mp_info.version)
        self.assertEqual(MP_FIELDS_MASK, self.mp_info.fields_mask)
        self.assertEqual(MP_NUM_POINTS, self.mp_info.num_points)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
