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
import xfgeomod, xfmatgrid, xfsar
from xfutils import xf_sim_id_to_str, xf_run_id_to_str

# Relative xf project path is assumed to be three levels up in Test_Data/Test_Coil.xf
TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..','..','..',
                                              'Test_Data','Test_Coil.xf'))

class TestXFSar(unittest.TestCase):
    """Tests for xfsar module."""
    @classmethod
    def setUpClass(cls):
        _run_path = os.path.join(TEST_COIL_DIR, r'Simulations',
                                 xf_sim_id_to_str(1),
                                 xf_run_id_to_str(1))
        _geom = xfgeomod.XFGeometry(_run_path)
        _mesh = xfgeomod.XFMesh(_run_path)
        cls._grid_exporter = xfgeomod.XFGridExporter(_geom, _mesh)

    def setUp(self):
        pass

    def test_trivial(self):
        """This should pass"""
        self.assertEqual(1,1)

    def disabled_test_xf_sar_class(self):
        """Create a XFSar class."""
        cls.test_sar = xfsar.XFSar()
        self.assertIsInstance(self.test_sar,xfsar.XFSar)

    def testDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
