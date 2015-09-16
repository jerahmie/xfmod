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

from xfmatgrid import *

class TestXFMultiPointInfo(unittest.TestCase):
    """Tests for XF Multipoint sensor info."""
    def setUp(self):
        self.mp_info = XFMultiPointInfo()
        
    def test_header_info(self):
        MP_HEADER = 'Rmpt'
        MP_VERSION = 2
        MP_FIELDS_MASK = struct.unpack('>I',struct.pack('<I',0x0000f001))[0]
        MP_NUM_POINTS = struct.unpack('>Q',struct.pack('<Q',0x581eb10000000000))[0]
        self.assertEqual(MP_HEADER, self.mp_info.header)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
