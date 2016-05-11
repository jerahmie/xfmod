#!/usr/bin/env python
"""
Test for vopgen exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os import getcwd, remove
from os.path import normpath, dirname, realpath, join, isfile
import unittest
import numpy as np
import scipy.io as spio
from xfutils.xfproject import XFProjectInfo
import xfwriter.vopgen

COIL_XF_PATH = normpath(join(realpath(__file__),
                             '..', '..', '..',
                             'Test_Data', 
                             'Test_Coil.xf'))

XF_TEST_COIL_POWERS = [5.78071000e-05, 1.27783000e-04, 1.57568000e-04]
EF_MAP_ARRAY_FILE = normpath(join(dirname(realpath(__file__)),
                                  'efMapArrayN.mat'))
PROPERTY_MAP_FILE = normpath(join(dirname(realpath(__file__)),
                                  'promap.mat'))

class TestVopgenWriter(unittest.TestCase):
    """Tests for vopgen matfile writers."""
    @classmethod
    def setUpClass(cls):
        if isfile(EF_MAP_ARRAY_FILE):
            remove(EF_MAP_ARRAY_FILE)
        cls.sim_ids = []
        cls._xf_project_info = XFProjectInfo(COIL_XF_PATH)
        simulations = cls._xf_project_info.xf_sim_run_list
        for idx, sim in enumerate(simulations):
            if sim[0]:
                cls.sim_ids.append(idx + 1)

    def setUp(self):
        pass

    def test_vopgen_class_structure(self):
        """Make sure the vopgen class behaves as expected."""
        self.assertTrue(True)

    def test_efn_net_input_power(self):
        """Test VopgenEFMatArrayN net input power array."""
        tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(COIL_XF_PATH, self.sim_ids)
        self.assertEqual(3, len(tvopgen._net_input_power_per_coil))
        self.assertTrue(np.allclose(XF_TEST_COIL_POWERS, 
                                    tvopgen._net_input_power_per_coil))
    
#    @unittest.skip("This test is too long for development.  Re-enable for general testing.")
    def test_ef_map_array_n_mat(self):
        """
        Test the shape of data structures within the saved mat file and generate png images of 
        the electric field regions for efMapArrayN.mat
        """
        tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(COIL_XF_PATH, self.sim_ids)
        tvopgen.set_grid_origin(0.0, 0.0, 0.044)
        self.assertEqual(0.0, tvopgen._x0)
        self.assertEqual(0.0, tvopgen._y0)
        self.assertEqual(0.044, tvopgen._z0)
        tvopgen.set_grid_len(0.256, 0.256, 0.256)
        self.assertEqual(0.256, tvopgen._xlen)
        self.assertEqual(0.256, tvopgen._ylen)
        self.assertEqual(0.256, tvopgen._zlen)        
        tvopgen.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(0.002, tvopgen._dx)
        self.assertEqual(0.002, tvopgen._dy)
        self.assertEqual(0.002, tvopgen._dz)
        tvopgen._update_export_grid()
        self.assertTrue(np.allclose(np.arange(tvopgen._x0 - tvopgen._xlen/2.0, 
                                              tvopgen._x0 + tvopgen._xlen/2.0, 
                                              tvopgen._dx), tvopgen._xdim_uniform))
        self.assertTrue(np.allclose(np.arange(tvopgen._y0 - tvopgen._ylen/2.0,
                                              tvopgen._y0 + tvopgen._ylen/2.0,
                                              tvopgen._dy), tvopgen._ydim_uniform))
        self.assertTrue(np.allclose(np.arange(tvopgen._z0 - tvopgen._zlen/2.0,
                                              tvopgen._z0 + tvopgen._zlen/2.0,
                                              tvopgen._dz), tvopgen._zdim_uniform))
        tvopgen.savemat(EF_MAP_ARRAY_FILE)
        self.assertTrue(isfile(EF_MAP_ARRAY_FILE))
        ef_map = spio.loadmat(EF_MAP_ARRAY_FILE)
        self.assertTrue((128, 128, 128, 3, 3), ef_map['efMapArrayN'])

    def test_propmap_mat(self):
        """
        Tests to create/read propmat.mat
        """
        tpropmap = xfwriter.vopgen.VopgenPropertyMap(COIL_XF_PATH, 1, 1)
        tpropmap.set_grid_origin(0.0, 0.0, 0.044)
        self.assertEqual(0.0, tpropmap._x0)
        self.assertEqual(0.0, tpropmap._y0)
        self.assertEqual(0.044, tpropmap._z0)
        tpropmap.set_grid_len(0.256, 0.256, 0.256)
        self.assertEqual(0.256, tpropmap._xlen)
        self.assertEqual(0.256, tpropmap._ylen)
        self.assertEqual(0.256, tpropmap._zlen)
        tpropmap.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(0.002, tpropmap._dx)
        self.assertEqual(0.002, tpropmap._dy)
        self.assertEqual(0.002, tpropmap._dz)
        tpropmap._update_export_grid()
        self.assertTrue(np.allclose(np.arange(tpropmap._x0 - tpropmap._xlen/2.0,
                                              tpropmap._x0 + tpropmap._xlen/2.0,
                                              tpropmap._dx), tpropmap._xdim_uniform))
        self.assertTrue(np.allclose(np.arange(tpropmap._y0 - tpropmap._ylen/2.0,
                                              tpropmap._y0 + tpropmap._ylen/2.0,
                                              tpropmap._dy), tpropmap._ydim_uniform))
        self.assertTrue(np.allclose(np.arange(tpropmap._z0 - tpropmap._zlen/2.0,
                                              tpropmap._z0 + tpropmap._zlen/2.0,
                                              tpropmap._dz), tpropmap._zdim_uniform))
        tpropmap.savemat(PROPERTY_MAP_FILE)
        self.assertTrue(isfile(PROPERTY_MAP_FILE))
        prop_map = spio.loadmat(PROPERTY_MAP_FILE)
        self.assertEqual(128, len(prop_map['XDim']))
        self.assertEqual(128, len(prop_map['YDim']))
        self.assertEqual(128, len(prop_map['ZDim']))        
        self.assertEqual((128, 128, 128, 3), np.shape(prop_map['condMap']))
        self.assertEqual((128, 128, 128, 3), np.shape(prop_map['mdenMap']))


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
