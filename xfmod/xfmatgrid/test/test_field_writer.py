#!/usr/bin/env python3
"""
Test xffieldwriter.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys
import os
import unittest
import numpy as np
import scipy.io as spio
from xfmod import xfmatgrid

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..', '..', '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')

MP_SENSOR_NAME = r'Solid_Sensor1'

class TestXFFieldWriter(unittest.TestCase):
    """Tests for the XFFieldWriter."""
    @classmethod
    def setUpClass(cls):
        cls.field_nugrid = xfmatgrid.XFFieldNonUniformGrid(TEST_COIL_DIR,
                                                           1, 1, MP_SENSOR_NAME)

    def setUp(self):
        self.field_name = r'B'

    def test_write_field_nonuniform(self):
        """Verify non-uniform field writer creates matlab file."""
        self.field_name = r'B'

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
