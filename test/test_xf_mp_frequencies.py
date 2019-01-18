#!/usr/bin/env python
"""
Test XFMultiPointFrequencies class.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import os
import unittest
from xfmod import xfmatgrid

TEST_FREQUENCY = 296500000.0  # 296.5 MHz

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))

RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
TEST_MP_DIR = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0')
FREQUENCIES_BIN = os.path.join(TEST_MP_DIR, 'frequencies.bin')

class TestXFMultiPointFrequencies(unittest.TestCase):
    """Tests for Multipoint sensor frequencies."""
    def setUp(self):
        print('Executing tests in ' + __file__)
        self.mp_frequencies = xfmatgrid.XFMultiPointFrequencies(FREQUENCIES_BIN)

    def test_single_frequency(self):
        """Read frequencies.bin from test data."""
        print(self.id())
        self.assertEqual(TEST_FREQUENCY, self.mp_frequencies.frequencies[0])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
