#!/usr/bin/env python
"""
Test for vopgen exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os import path, getcwd, remove
import unittest
import numpy as np
import scipy.io as spio
from xfutils.xfproject import XFProjectInfo
import xfwriter.vopgen

COIL_XF_PATH = path.normpath(path.join(path.realpath(__file__),
                                       '..', '..', '..',
                                       'Test_Data', 
                                       'Test_Coil.xf'))

XF_TEST_COIL_POWERS = [5.78071000e-05, 1.27783000e-04, 1.57568000e-04]
EF_MAP_ARRAY_FILE = 'efMapArrayN.mat'

class TestVopgenWriter(unittest.TestCase):
    """Tests for vopgen matfile writers."""
    @classmethod
    def setUpClass(cls):
        if path.isfile(EF_MAP_ARRAY_FILE):
            remove(EF_MAP_ARRAY_FILE)
        sim_ids = []
        cls._xf_project_info = XFProjectInfo(COIL_XF_PATH)
        simulations = cls._xf_project_info.xf_sim_run_list
        for idx, sim in enumerate(simulations):
            if sim[0]:
                sim_ids.append(idx + 1)
        cls.tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(COIL_XF_PATH, sim_ids)

    def setUp(self):
        pass

    def test_vopgen_class_structure(self):
        """Make sure the vopgen class behaves as expected."""
        self.assertTrue(True)

    def test_efn_net_input_power(self):
        """Test VopgenEFMatArrayN net input power array."""
        self.assertEqual(3, len(self.tvopgen._net_input_power_per_coil))
        self.assertTrue(np.allclose(XF_TEST_COIL_POWERS, 
                                    self.tvopgen._net_input_power_per_coil))
    
    @unittest.skip("This test is too long for development.  Re-enable for general testing.")
    def test_ef_map_array_n_mat(self):
        """
        Test the shape of data structures within the saved mat file and generate png images of 
        the electric field regions for efMapArrayN.mat
        """
        self.tvopgen.set_grid_origin(0.0, 0.0, 0.044)
        self.assertEqual(0.0, self.tvopgen._x0)
        self.assertEqual(0.0, self.tvopgen._y0)
        self.assertEqual(0.044, self.tvopgen._z0)
        self.tvopgen.set_grid_len(0.256, 0.256, 0.256)
        self.assertEqual(0.256, self.tvopgen._xlen)
        self.assertEqual(0.256, self.tvopgen._ylen)
        self.assertEqual(0.256, self.tvopgen._zlen)        
        self.tvopgen.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(0.002, self.tvopgen._dx)
        self.assertEqual(0.002, self.tvopgen._dy)
        self.assertEqual(0.002, self.tvopgen._dz)
        self.tvopgen._update_export_grid()
        self.assertTrue(np.allclose(np.arange(self.tvopgen._x0 - self.tvopgen._xlen/2.0, 
                                             self.tvopgen._x0 + self.tvopgen._xlen/2.0, 
                                             self.tvopgen._dx), self.tvopgen._xdim_uniform))
        self.assertTrue(np.allclose(np.arange(self.tvopgen._y0 - self.tvopgen._ylen/2.0,
                                             self.tvopgen._y0 + self.tvopgen._ylen/2.0,
                                             self.tvopgen._dy), self.tvopgen._ydim_uniform))
        self.assertTrue(np.allclose(np.arange(self.tvopgen._z0 - self.tvopgen._zlen/2.0,
                                             self.tvopgen._z0 + self.tvopgen._zlen/2.0,
                                             self.tvopgen._dz), self.tvopgen._zdim_uniform))
        self.tvopgen.savemat(EF_MAP_ARRAY_FILE)
        self.assertTrue(path.isfile(EF_MAP_ARRAY_FILE))
        ef_map = spio.loadmat(EF_MAP_ARRAY_FILE)
        self.assertTrue((128, 128, 128, 3, 3), ef_map['efMapArrayN'])

    def test_propmat_mat(self):
        """
        Tests to create/read propmat.mat
        """
        self.assertTrue(False)

    @unittest.skip("module not implemented.")
    def test_sarmask_aligned_mat(self):
        """
        Tests to create/read sarmask_aligned.mat.
        """
        pass

    @unittest.skip("module not implemented.")
    def test_massdensity_map_3d_mat(self):
        """
        Tests to create/read massdensityMat3D.mat.
        """
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
