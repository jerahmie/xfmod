"""
Test for vopgen exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
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
BF_MAP_ARRAY_FILE = normpath(join(dirname(realpath(__file__)),
                                  'bfMapArrayN.mat'))
PROPERTY_MAP_FILE = normpath(join(dirname(realpath(__file__)),
                                  'propmap.mat'))
SAR_MASK_FILE = normpath(join(dirname(realpath(__file__)),
                              'sarmask_aligned.mat'))
MASS_DENSITY_MAP_3D_FILE = normpath(join(dirname(realpath(__file__)),
                                         'massdensityMap3D.mat'))
SIM_ID = 1
RUN_ID = 1

# Uniform grid resolution
DX = 0.002 # m
DY = 0.002 # m
DZ = 0.002 # m

# roi dimensions
X_ROI_LEN = 0.256 # m
Y_ROI_LEN = 0.256 # m
Z_ROI_LEN = 0.256 # m

# roi center
X0 = 0.0
Y0 = 0.0
Z0 = 0.044

# roi grid dimensions
X_ROI_DIM = int(X_ROI_LEN/DX)
Y_ROI_DIM = int(Y_ROI_LEN/DY)
Z_ROI_DIM = int(Z_ROI_LEN/DZ)

class TestVopgenWriter(unittest.TestCase):
    """Tests for vopgen matfile writers."""
    @classmethod
    def setUpClass(cls):
        if isfile(EF_MAP_ARRAY_FILE):
            os.remove(EF_MAP_ARRAY_FILE)
        if isfile(BF_MAP_ARRAY_FILE):
            os.remove(BF_MAP_ARRAY_FILE)
        if isfile(PROPERTY_MAP_FILE):
            os.remove(PROPERTY_MAP_FILE)
        if isfile(SAR_MASK_FILE):
            os.remove(SAR_MASK_FILE)
        if isfile(MASS_DENSITY_MAP_3D_FILE):
            os.remove(MASS_DENSITY_MAP_3D_FILE)
        cls.sim_ids = []
        cls._xf_project_info = XFProjectInfo(COIL_XF_PATH)
        simulations = cls._xf_project_info.xf_sim_run_list
        for idx, sim in enumerate(simulations):
            if sim[0]:
                cls.sim_ids.append(idx + 1)

    def setUp(self):
        pass

    def test_ef_map_array_n_mat(self):
        """
        Test the shape of data structures within the saved mat file and generate
        png images of the electric field regions for efMapArrayN.mat
        """
        tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(COIL_XF_PATH, self.sim_ids)
        tvopgen.set_grid_origin(X0, Y0, Z0)
        self.assertEqual(X0, tvopgen._x0)
        self.assertEqual(Y0, tvopgen._y0)
        self.assertEqual(Z0, tvopgen._z0)
        tvopgen.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        self.assertEqual(X_ROI_LEN, tvopgen._xlen)
        self.assertEqual(Y_ROI_LEN, tvopgen._ylen)
        self.assertEqual(Z_ROI_LEN, tvopgen._zlen)
        tvopgen.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(DX, tvopgen._dx)
        self.assertEqual(DY, tvopgen._dy)
        self.assertEqual(DZ, tvopgen._dz)
        tvopgen._update_export_grid()
        self.assertTrue(np.allclose(np.arange(tvopgen._x0 - tvopgen._xlen/2.0,
                                              tvopgen._x0 + tvopgen._xlen/2.0,
                                              tvopgen._dx),
                                    tvopgen._xdim_uniform))
        self.assertTrue(np.allclose(np.arange(tvopgen._y0 - tvopgen._ylen/2.0,
                                              tvopgen._y0 + tvopgen._ylen/2.0,
                                              tvopgen._dy),
                                    tvopgen._ydim_uniform))
        self.assertTrue(np.allclose(np.arange(tvopgen._z0 - tvopgen._zlen/2.0,
                                              tvopgen._z0 + tvopgen._zlen/2.0,
                                              tvopgen._dz),
                                    tvopgen._zdim_uniform))
        tvopgen.savemat(EF_MAP_ARRAY_FILE)
        self.assertTrue(isfile(EF_MAP_ARRAY_FILE))
        ef_map = spio.loadmat(EF_MAP_ARRAY_FILE)
        self.assertTrue((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM, 3, 3),
                        ef_map['efMapArrayN'])

    def test_bf_map_array_n_mat(self):
        """
        Test the shape of data structures within the saved mat file and generate
        png images of the magnetic field regions for bfMapArrayN.mat
        """
        tvopgen = xfwriter.vopgen.VopgenBFMapArrayN(COIL_XF_PATH, self.sim_ids)
        tvopgen.set_grid_origin(X0, Y0, Z0)
        self.assertEqual(X0, tvopgen._x0)
        self.assertEqual(Y0, tvopgen._y0)
        self.assertEqual(Z0, tvopgen._z0)
        tvopgen.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        self.assertEqual(X_ROI_LEN, tvopgen._xlen)
        self.assertEqual(Y_ROI_LEN, tvopgen._ylen)
        self.assertEqual(Z_ROI_LEN, tvopgen._zlen)
        tvopgen.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(DX, tvopgen._dx)
        self.assertEqual(DY, tvopgen._dy)
        self.assertEqual(DZ, tvopgen._dz)
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
        tvopgen.savemat(BF_MAP_ARRAY_FILE)
        self.assertTrue(isfile(BF_MAP_ARRAY_FILE))
        ef_map = spio.loadmat(BF_MAP_ARRAY_FILE)
        self.assertTrue((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM, 3, 3),
                        ef_map['bfMapArrayN'])        

    def test_tissue_mask(self):
        """
        Test the tissue mask dimensions.
        """
        ttissue_mask = xfwriter.vopgen.VopgenSarMask(COIL_XF_PATH,
                                                     SIM_ID, RUN_ID)
        ttissue_mask.set_grid_origin(X0, Y0, Z0)
        ttissue_mask.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        ttissue_mask.set_grid_resolution(DX, DY, DZ)
        test_mask = ttissue_mask.make_tissue_mask()
        self.assertEqual(DX, ttissue_mask._dx)
        self.assertEqual(DY, ttissue_mask._dy)
        self.assertEqual(DZ, ttissue_mask._dz)
        self.assertEqual(X_ROI_LEN, ttissue_mask._xlen)
        self.assertEqual(Y_ROI_LEN, ttissue_mask._ylen)
        self.assertEqual(Z_ROI_LEN, ttissue_mask._zlen)
        self.assertEqual(X0, ttissue_mask._x0)
        self.assertEqual(Y0, ttissue_mask._y0)
        self.assertEqual(Z0, ttissue_mask._z0)
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM), np.shape(test_mask))

    def test_sarmask_aligned_mat(self):
        """
        Tests to create/read sarmask_aligned.mat.
        """
        print("sar_mask_file: ", SAR_MASK_FILE)
        tsar_mask = xfwriter.vopgen.VopgenSarMask(COIL_XF_PATH,
                                                  SIM_ID, RUN_ID)
        tsar_mask.set_grid_origin(X0, Y0, Z0)
        tsar_mask.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        tsar_mask.set_grid_resolution(DX, DY, DZ)
        tsar_mask.savemat(SAR_MASK_FILE)
        self.assertTrue(isfile(SAR_MASK_FILE))
        sar_mask_mat = spio.loadmat(SAR_MASK_FILE)
        self.assertEqual(X_ROI_DIM, len(sar_mask_mat['XDim']))
        self.assertEqual(Y_ROI_DIM, len(sar_mask_mat['YDim']))
        self.assertEqual(Z_ROI_DIM, len(sar_mask_mat['ZDim']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM),
                         np.shape(sar_mask_mat['sarmask_new']))
        self.assertGreater(np.sum(sar_mask_mat['sarmask_new']), 0)

    def test_massdensity_map_3d_mat(self):
        """
        Tests to create/read massdensityMat3D.mat.
        """
        tmdenmap3d = xfwriter.vopgen.VopgenMassDensityMap3D(COIL_XF_PATH,
                                                        SIM_ID, RUN_ID)
        tmdenmap3d.set_grid_origin(X0, Y0, Z0)
        tmdenmap3d.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        tmdenmap3d.set_grid_resolution(DX, DY, DZ)
        tmdenmap3d.savemat(MASS_DENSITY_MAP_3D_FILE)
        self.assertTrue(isfile(MASS_DENSITY_MAP_3D_FILE))
        mdenmap3d_mat = spio.loadmat(MASS_DENSITY_MAP_3D_FILE)
        self.assertEqual(X_ROI_DIM, len(mdenmap3d_mat['XDim']))
        self.assertEqual(Y_ROI_DIM, len(mdenmap3d_mat['YDim']))
        self.assertEqual(Z_ROI_DIM, len(mdenmap3d_mat['ZDim']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM),
                         np.shape(mdenmap3d_mat['mden3D']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM),
                         np.shape(mdenmap3d_mat['mden3Dm']))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        del cls.sim_ids
        del cls._xf_project_info

if __name__ == "__main__":
    unittest.main()
