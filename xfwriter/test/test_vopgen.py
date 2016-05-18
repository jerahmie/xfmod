"""
Test for vopgen exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
from os.path import normpath, dirname, realpath, join, isfile
import unittest
from numpy import allclose, arange, shape
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
        self.assertTrue(allclose(XF_TEST_COIL_POWERS,
                                 tvopgen._net_input_power_per_coil))

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
        self.assertTrue(allclose(arange(tvopgen._x0 - tvopgen._xlen/2.0,
                                        tvopgen._x0 + tvopgen._xlen/2.0,
                                        tvopgen._dx), tvopgen._xdim_uniform))
        self.assertTrue(allclose(arange(tvopgen._y0 - tvopgen._ylen/2.0,
                                        tvopgen._y0 + tvopgen._ylen/2.0,
                                        tvopgen._dy), tvopgen._ydim_uniform))
        self.assertTrue(allclose(arange(tvopgen._z0 - tvopgen._zlen/2.0,
                                        tvopgen._z0 + tvopgen._zlen/2.0,
                                        tvopgen._dz), tvopgen._zdim_uniform))
        tvopgen.savemat(EF_MAP_ARRAY_FILE)
        self.assertTrue(isfile(EF_MAP_ARRAY_FILE))
        ef_map = spio.loadmat(EF_MAP_ARRAY_FILE)
        self.assertTrue((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM, 3, 3),
                        ef_map['efMapArrayN'])

    def test_propmap_mat(self):
        """
        Tests to create/read propmat.mat
        """
        tpropmap = xfwriter.vopgen.VopgenPropertyMap(COIL_XF_PATH,
                                                     SIM_ID, RUN_ID)
        tpropmap.set_grid_origin(X0, Y0, Z0)
        self.assertEqual(X0, tpropmap._x0)
        self.assertEqual(Y0, tpropmap._y0)
        self.assertEqual(Z0, tpropmap._z0)
        tpropmap.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        self.assertEqual(X_ROI_LEN, tpropmap._xlen)
        self.assertEqual(Y_ROI_LEN, tpropmap._ylen)
        self.assertEqual(Z_ROI_LEN, tpropmap._zlen)
        tpropmap.set_grid_resolution(DX, DY, DZ)
        self.assertEqual(DX, tpropmap._dx)
        self.assertEqual(DY, tpropmap._dy)
        self.assertEqual(DZ, tpropmap._dz)
        tpropmap._update_export_grid()
        self.assertTrue(allclose(arange(tpropmap._x0 - tpropmap._xlen/2.0,
                                        tpropmap._x0 + tpropmap._xlen/2.0,
                                        tpropmap._dx), tpropmap._xdim_uniform))
        self.assertTrue(allclose(arange(tpropmap._y0 - tpropmap._ylen/2.0,
                                        tpropmap._y0 + tpropmap._ylen/2.0,
                                        tpropmap._dy), tpropmap._ydim_uniform))
        self.assertTrue(allclose(arange(tpropmap._z0 - tpropmap._zlen/2.0,
                                        tpropmap._z0 + tpropmap._zlen/2.0,
                                        tpropmap._dz), tpropmap._zdim_uniform))
        tpropmap.savemat(PROPERTY_MAP_FILE)
        self.assertTrue(isfile(PROPERTY_MAP_FILE))
        prop_map = spio.loadmat(PROPERTY_MAP_FILE)
        self.assertEqual(X_ROI_DIM, len(prop_map['XDim']))
        self.assertEqual(Y_ROI_DIM, len(prop_map['YDim']))
        self.assertEqual(Z_ROI_DIM, len(prop_map['ZDim']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM, 3),
                         shape(prop_map['condMap']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM, 3),
                         shape(prop_map['mdenMap']))

    def test_sarmask_aligned_mat(self):
        """
        Tests to create/read sarmask_aligned.mat.
        """
        print("sar_mask_file: ", SAR_MASK_FILE)
        tsarmask = xfwriter.vopgen.VopgenSarMask(COIL_XF_PATH, SIM_ID, RUN_ID)
        tsarmask.set_grid_origin(X0, Y0, Z0)
        tsarmask.set_grid_len(X_ROI_LEN, Y_ROI_LEN, Z_ROI_LEN)
        tsarmask.set_grid_resolution(DX, DY, DZ)
        tsarmask.savemat(SAR_MASK_FILE)
        self.assertTrue(isfile(SAR_MASK_FILE))
        sar_mask_mat = spio.loadmat(SAR_MASK_FILE)
        self.assertEqual(X_ROI_DIM, len(sar_mask_mat['XDim']))
        self.assertEqual(Y_ROI_DIM, len(sar_mask_mat['YDim']))
        self.assertEqual(Z_ROI_DIM, len(sar_mask_mat['ZDim']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM),
                         shape(sar_mask_mat['sarmask_new']))

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
                         shape(mdenmap3d_mat['mden3D']))
        self.assertEqual((X_ROI_DIM, Y_ROI_DIM, Z_ROI_DIM),
                         shape(mdenmap3d_mat['mden3Dm']))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
