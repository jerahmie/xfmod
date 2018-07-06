#!/usr/bin/env python
"""
Test the xfsystem module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import unittest
from xfmod import xfsystem

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__), 
                                              '..', '..', '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))
SYSTEM_SSOUT = os.path.normpath(os.path.join(TEST_COIL_DIR, 'Simulations', 
                                             '000001','Run0001','output',
                                             'SteadyStateOutput','f0',
                                             'system.ssout'))
class testXFSystemFile(unittest.TestCase):
    """Test for xfsystem module."""
    @classmethod
    def setUpClass(cls):
        cls.xfSystem = xfsystem.XFSystem(TEST_COIL_DIR,1,1)

    def test_unittest(self):
        """Test set of steady state system info file."""
        print(self.id())
        self.assertEqual(SYSTEM_SSOUT,self.xfSystem._system_ssout)

    def test_system_frequency(self):
        """Test steady state system frequency."""
        print(self.id())
        self.assertAlmostEqual(296500000.0, self.xfSystem.frequency)

    def test_system_computed_power(self):
        """Test computed power values."""
        print(self.id())
        self.assertAlmostEqual(5.78071e-5, self.xfSystem.net_input_power)
        

if __name__ == '__main__':
    unittest.main()
