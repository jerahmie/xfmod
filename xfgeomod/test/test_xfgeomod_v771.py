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
                                                  'Test_Data', 'Test_Coil_v771.xf'))
test_sim_number = 1
test_run_number = 1


# Test_Data values
# Grid Data
grid_origin = [-0.4247180681335669, -0.31771806813356684, -0.3631170688583829]
grid_num_x_cells = 292
grid_num_y_cells = 212
grid_num_z_cells = 230

# Mesh Data
mesh_version = 2
mesh_edge_run_bytes = 8
mesh_run_edge_format = 'Q'
mesh_num_ex_edge_runs = 419494
mesh_num_ey_edge_runs = 420347
mesh_num_ez_edge_runs = 450712
mesh_num_hx_edge_runs = 0
mesh_num_hy_edge_runs = 0
mesh_num_hz_edge_runs = 0
mesh_num_electric_averaged_materials = 2032
mesh_num_magnetic_averaged_materials = 0
mesh_num_electric_mesh_edges_eam = 0
mesh_num_magnetic_mesh_edges_eam = 0
mesh_materials = ['Adrenal_gland','Air_internal','Artery','Bladder',
                  'Blood_vessel','Bone', 'Brain_grey_matter',
                  'Brain_white_matter','Bronchi','Bronchi_lumen','Cartilage',
                  'Cerebellum','Cerebrospinal_fluid','Commissura_anterior',
                  'Commissura_posterior','Connective_tissue','Cornea','Diaphragm',
                  'Ear_cartilage','Ear_skin','Epididymis','Esophagus',
                  'Esophagus_lumen','Eye_lens','Eye_Sclera',
                  'Eye_vitreous_humor','Fat','Gallbladder','Heart_lumen',
                  'Heart_muscle','Hippocampus','Hypophysis','Hypothalamus',
                  'Intervertebral_disc','Kidney_cortex','Kidney_medulla',
                  'Large_intestine','Large_intestine_lumen','Larynx',
                  'Liver','Lung','Mandible','Marrow_red','Medulla_oblongata',
                  'Meniscus','Midbrain','Mucosa','Muscle','Nerve','Pancreas',
                  'Patella','Penis','Pharynx','Pinealbody','Pons','Prostate',
                  'SAT','Skin','Skull','Small_intestine',
                  'Small_intestine_lumen','Spinal_cord','Spleen','Stomach',
                  'Stomach_lumen','Teeth','Tendon_Ligament','Testis','Thalamus',
                  'Thymus','Thyroid_gland','Tongue','Trachea','Trachea_lumen',
                  'Ureter_Urethra','Vein','Vertebrae','Copper (Pure) [ND]',
                  'PETE','Polytetrafluorethylene (Generalized) [ND]']
material_mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

mesh_units = 'mm'

class TestXFGeoMod(unittest.TestCase):
    """Tests for xfgeomod."""

    @classmethod
    def setUpClass(cls):
        # Load XFdtd Geometry info
        print('Executing tests in ' + __file__)
        cls.xf_geom = xfgeomod.XFGeometry(test_project_dir, test_sim_number, test_run_number)

        # Load XFdtd Mesh data file
        cls.xf_mesh = xfgeomod.XFMesh(test_project_dir, test_sim_number, test_run_number)

        # Create XFdtd data exporter
        cls.xf_export = xfgeomod.XFGridExporter(cls.xf_geom, cls.xf_mesh)
        cls.xf_export.units = 'mm'
        cls.xf_export.export_mesh_data('test_v771.mat')

    def setUp(self):
        pass

    def test_grid_data(self):
        """
        Test grid data has proper dimensions.
        """
        print(self.id())
        print("--> Origin from file: ", self.xf_geom.grid_data.origin)
        print("--> Origin expected:  ", grid_origin)
        self.assertAlmostEqual(grid_origin[0],
                               self.xf_geom.grid_data.origin[0],
                               delta=0.0000001)
        self.assertAlmostEqual(grid_origin[1],
                               self.xf_geom.grid_data.origin[1],
                               delta=0.0000001)
        self.assertAlmostEqual(grid_origin[2],
                               self.xf_geom.grid_data.origin[2],
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
        print(self.id())
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
        print(self.id())
        # verify the material names
        self.assertEqual(mesh_materials,
                         [mat.name for mat in self.xf_export._materials_list[2:]])

        # verify the tissue properties of the materials
        self.assertEqual(material_mask, [mat.tissue for mat in self.xf_export._materials_list[2:]])

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
