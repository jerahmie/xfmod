#!/usr/bin/env python3
"""
Test the xfsar module.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
import unittest
import numpy as np
import scipy.io as spio
import numpy.testing as npt
import xfsar

# Relative xf project path is assumed to be ../../../Test_Data/Test_Coil.xf
TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..','..','..',
                                              'Test_Data','Test_Coil.xf'))

class TestXFSar(unittest.TestCase):
    """Tests for xfsar module."""
    @classmethod
    def setUpClass(cls):
        cls.test_sar = xfsar.XFSar(TEST_COIL_DIR,1,1)

    def setUp(self):
        pass

    def test_trivial(self):
        """This should pass"""
        self.assertEqual(1,1)

    def test_xf_sar_class(self):
        """Create a XFSar class."""
        self.assertIsInstance(self.test_sar,xfsar.XFSar)

    def test_grid_mesh(self):
        """This should not throw exceptions"""
        self.test_sar._test_grid()
        
    def testDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
