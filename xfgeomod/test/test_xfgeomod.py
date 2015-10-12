#!/usr/bin/env python
"""
Test xfgeomod using unittest 
"""

from __future__ import (absolute_import, division, 
                        print_function, unicode_literals)
import sys, os
import unittest
from xfmatgrid.xfutils import xf_run_id_to_str, xf_sim_id_to_str 
import xfgeomod

TEST_PROJECT_DIR = os.path.join('/Data', 'CMRR', 'rf_coil_scripts', 
                                'python', 'Test_Data', 'Test_Coil.xf')
TEST_SIM_NUMBER = 1
TEST_RUN_NUMBER = 1

TEST_RUN_PATH = os.path.join(TEST_PROJECT_DIR, 'Simulations',
                             xf_sim_id_to_str(TEST_SIM_NUMBER),
                             xf_run_id_to_str(TEST_RUN_NUMBER))

class TestXFGeoMod(unittest.TestCase):
    """Tests for xfgeomod."""
    def setUp(self):
        # Load XFdtd Geometry info
        xf_geom = xfgeomod.XFGeometry(TEST_RUN_PATH)
        xf_geom.print_materials()
        #xf_geom.print_grid_data()
    
        # Load XFdtd Mesh data file
        xf_mesh = xfgeomod.XFMesh(TEST_RUN_PATH)

        # Create XFdtd data exporter
        xf_export = xfgeomod.XFGridExporter(xf_geom, xf_mesh)
        xf_export.units = 'mm'
        xf_export.export_mesh_data('test.mat')

    def test_a_test(self):
        """ 
        This is a fake test to help migrate to TDD.  Delete it when real 
        testing begins.
        """
        self.assertEqual(1,1)
        
        def tearDown(self):
            pass

if __name__ == "__main__":
    unittest.main()

