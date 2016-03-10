#!/usr/bin/env python
"""
Test xfgeomod using unittest 
"""

from __future__ import (absolute_import, division, 
                        print_function, unicode_literals)
import sys, os
import unittest
from xfutils import xf_run_id_to_str, xf_sim_id_to_str 
import xfgeomod

# Location of Test_Coil.xf XFdtd project relative to this file.
TEST_PROJECT_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                 '..', '..', '..',
                                                  'Test_Data', 'Test_Coil.xf'))
TEST_SIM_NUMBER = 1
TEST_RUN_NUMBER = 1

TEST_RUN_PATH = os.path.join(TEST_PROJECT_DIR, 'Simulations',
                             xf_sim_id_to_str(TEST_SIM_NUMBER),
                             xf_run_id_to_str(TEST_RUN_NUMBER))

# Test_Data values
# Grid Data
GRID_ORIGIN = [-0.134075642, -0.154854313, -0.0397661068]
GRID_NUM_X_CELLS = 254
GRID_NUM_Y_CELLS = 263
GRID_NUM_Z_CELLS = 196


# Mesh Data
MESH_VERSION = 1
MESH_EDGE_RUN_BYTES = 8
MESH_RUN_EDGE_FORMAT = 'Q'
MESH_NUM_EX_EDGE_RUNS = 162199
MESH_NUM_EY_EDGE_RUNS = 152099
MESH_NUM_EZ_EDGE_RUNS = 52152
MESH_NUM_HX_EDGE_RUNS = 0
MESH_NUM_HY_EDGE_RUNS = 0
MESH_NUM_HZ_EDGE_RUNS = 0
MESH_NUM_ELECTRIC_AVERAGED_MATERIALS = 0
MESH_NUM_MAGNETIC_AVERAGED_MATERIALS = 0
MESH_NUM_ELECTRIC_MESH_EDGES_EAM = 0
MESH_NUM_MAGNETIC_MESH_EDGES_EAM = 0
MESH_MATERIALS = ['PTFE (Teflon)', 'Copper', 'phantom_material']
MESH_UNITS = 'mm'

class TestXFGeoMod(unittest.TestCase):
    """Tests for xfgeomod."""
    
    @classmethod
    def setUpClass(cls):
        # Load XFdtd Geometry info
        cls.xf_geom = xfgeomod.XFGeometry(TEST_RUN_PATH)
    
        # Load XFdtd Mesh data file
        cls.xf_mesh = xfgeomod.XFMesh(TEST_RUN_PATH)

        # Create XFdtd data exporter
        cls.xf_export = xfgeomod.XFGridExporter(cls.xf_geom, cls.xf_mesh)
        cls.xf_export.units = 'mm'
        cls.xf_export.export_mesh_data('test.mat')

    def setUp(self):
        pass

    def test_grid_data(self):
        """
        Test grid data has proper dimensions.
        """
        self.assertAlmostEqual(GRID_ORIGIN,
                               self.xf_geom.grid_data.origin, 
                               delta=0.0000001)
        self.assertEqual(GRID_NUM_X_CELLS,
                         self.xf_geom.grid_data.num_x_cells)
        self.assertEqual(GRID_NUM_Y_CELLS,
                         self.xf_geom.grid_data.num_y_cells)
        self.assertEqual(GRID_NUM_Z_CELLS,
                         self.xf_geom.grid_data.num_z_cells)

    def test_mesh_header(self):
        """ 
        Test data from mesh info.
        """
        self.assertEqual(MESH_VERSION, self.xf_mesh._mesh_version)
        self.assertEqual(MESH_EDGE_RUN_BYTES, self.xf_mesh._edge_run_bytes)
        self.assertEqual(MESH_RUN_EDGE_FORMAT, self.xf_mesh._edge_run_fmt)
        self.assertEqual(MESH_NUM_EX_EDGE_RUNS, self.xf_mesh._num_ex_edge_runs)
        self.assertEqual(MESH_NUM_EY_EDGE_RUNS, self.xf_mesh._num_ey_edge_runs)
        self.assertEqual(MESH_NUM_EZ_EDGE_RUNS, self.xf_mesh._num_ez_edge_runs)
        self.assertEqual(MESH_NUM_HX_EDGE_RUNS, self.xf_mesh._num_hx_edge_runs)
        self.assertEqual(MESH_NUM_HY_EDGE_RUNS, self.xf_mesh._num_hy_edge_runs)
        self.assertEqual(MESH_NUM_HZ_EDGE_RUNS, self.xf_mesh._num_hz_edge_runs)
        self.assertEqual(MESH_NUM_ELECTRIC_AVERAGED_MATERIALS, 
                         self.xf_mesh._num_e_avg_mats)
        self.assertEqual(MESH_NUM_MAGNETIC_AVERAGED_MATERIALS,
                         self.xf_mesh._num_h_avg_mats)
        self.assertEqual(MESH_NUM_ELECTRIC_MESH_EDGES_EAM,
                         self.xf_mesh._num_e_mesh_edges_e_avg)
        self.assertEqual(MESH_NUM_MAGNETIC_MESH_EDGES_EAM,
                         self.xf_mesh._num_h_mesh_edges_h_avg)
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

