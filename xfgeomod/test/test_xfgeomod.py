#!/usr/bin/env python
"""
Test xfgeomod using unittest
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os
import unittest
from xfutils import xf_run_id_to_str, xf_sim_id_to_str
import numpy as np
import xfgeomod

# Location of Test_Coil.xf XFdtd project relative to this file.
test_project_dir = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                 '..', '..', '..',
                                                  'Test_Data', 'Test_Coil.xf'))
test_sim_number = 1
test_run_number = 1


# Test_Data values
# Grid Data
grid_origin = [-0.134075642, -0.154854313, -0.0397661068]
grid_num_x_cells = 254
grid_num_y_cells = 263
grid_num_z_cells = 196

# Mesh Data
mesh_version = 1
mesh_edge_run_bytes = 8
mesh_run_edge_format = 'Q'
mesh_num_ex_edge_runs = 162199
mesh_num_ey_edge_runs = 152099
mesh_num_ez_edge_runs = 52152
mesh_num_hx_edge_runs = 0
mesh_num_hy_edge_runs = 0
mesh_num_hz_edge_runs = 0
mesh_num_electric_averaged_materials = 0
mesh_num_magnetic_averaged_materials = 0
mesh_num_electric_mesh_edges_eam = 0
mesh_num_magnetic_mesh_edges_eam = 0
mesh_materials = ['PTFE (Teflon)', 'Copper', 'phantom_material']
mesh_units = 'mm'

class TestXFGeoMod(unittest.TestCase):
    """Tests for xfgeomod."""

    @classmethod
    def setUpClass(cls):
        # Load XFdtd Geometry info
        cls.xf_geom = xfgeomod.XFGeometry(test_project_dir, test_sim_number, test_run_number)

        # Load XFdtd Mesh data file
        cls.xf_mesh = xfgeomod.XFMesh(test_project_dir, test_sim_number, test_run_number)

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
        self.assertAlmostEqual(grid_origin,
                               self.xf_geom.grid_data.origin,
                               delta=0.0000001)
        self.assertEqual(grid_num_x_cells,
                         self.xf_geom.grid_data.num_x_cells)
        self.assertEqual(grid_num_y_cells,
                         self.xf_geom.grid_data.num_y_cells)
        self.assertEqual(grid_num_z_cells,
                         self.xf_geom.grid_data.num_z_cells)

    def test_mesh_header(self):
        """
        Test data from mesh info.
        """
        grid_dim = (grid_num_x_cells, grid_num_y_cells, grid_num_z_cells)
        self.assertEqual(mesh_version, self.xf_mesh._mesh_version)
        self.assertEqual(mesh_edge_run_bytes, self.xf_mesh._edge_run_bytes)
        self.assertEqual(mesh_run_edge_format, self.xf_mesh._edge_run_fmt)
        self.assertEqual(mesh_num_ex_edge_runs, self.xf_mesh._num_ex_edge_runs)
        self.assertEqual(mesh_num_ey_edge_runs, self.xf_mesh._num_ey_edge_runs)
        self.assertEqual(mesh_num_ez_edge_runs, self.xf_mesh._num_ez_edge_runs)
        self.assertEqual(mesh_num_hx_edge_runs, self.xf_mesh._num_hx_edge_runs)
        self.assertEqual(mesh_num_hy_edge_runs, self.xf_mesh._num_hy_edge_runs)
        self.assertEqual(mesh_num_hz_edge_runs, self.xf_mesh._num_hz_edge_runs)
        self.assertEqual(mesh_num_electric_averaged_materials,
                         self.xf_mesh._num_e_avg_mats)
        self.assertEqual(mesh_num_magnetic_averaged_materials,
                         self.xf_mesh._num_h_avg_mats)
        self.assertEqual(mesh_num_electric_mesh_edges_eam,
                         self.xf_mesh._num_e_mesh_edges_e_avg)
        self.assertEqual(mesh_num_magnetic_mesh_edges_eam,
                         self.xf_mesh._num_h_mesh_edges_h_avg)
        self.assertEqual(grid_dim, np.shape(self.xf_export.ex_sigma))
        self.assertEqual(grid_dim, np.shape(self.xf_export.ey_sigma))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ez_sigma))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ex_epsilon_r))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ey_epsilon_r))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ez_epsilon_r))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ex_density))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ey_density))
        self.assertEqual((grid_num_x_cells,
                          grid_num_y_cells,
                          grid_num_z_cells),
                         np.shape(self.xf_export.ez_density))
        self.assertEqual(grid_dim, np.shape(self.xf_export.ex_tissue))
        self.assertEqual(grid_dim, np.shape(self.xf_export.ey_tissue))
        self.assertEqual(grid_dim, np.shape(self.xf_export.ez_tissue))

    def test_xfgeomod_materials(self):
        """Test the xfgeomod materials to match list."""
        # verify the material names
        self.assertEqual(mesh_materials,
                         [mat.name for mat in self.xf_export._materials_list[2:]])

        # verify the tissue properties of the materials
        self.assertEqual([0, 0, 1], [mat.tissue for mat in self.xf_export._materials_list[2:]])

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
