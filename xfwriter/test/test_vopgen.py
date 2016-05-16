#!/usr/bin/env python
"""
Test for vopgen exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from os import getcwd, remove
from os.path import normpath, dirname, realpath, join, isfile
import unittest
from numpy import allclose, arange, shape
import scipy.io as spio
from xfutils.xfproject import XFProjectInfo
import xfwriter.vopgen

coil_xf_path = normpath(join(realpath(__file__),
                             '..', '..', '..',
                             'Test_Data',
                             'Test_Coil.xf'))

xf_test_coil_powers = [5.78071000e-05, 1.27783000e-04, 1.57568000e-04]
ef_map_array_file = normpath(join(dirname(realpath(__file__)),
                                  'efMapArrayN.mat'))
property_map_file = normpath(join(dirname(realpath(__file__)),
                                  'propmap.mat'))
sar_mask_file = normpath(join(dirname(realpath(__file__)),
                              'sarmask_aligned.mat'))
mass_density_map_3d_file = normpath(join(dirname(realpath(__file__)),
                                         'massdensityMap3D.mat'))
sim_id = 1
run_id = 1

# Uniform grid resolution
dx = 0.002 # m
dy = 0.002 # m
dz = 0.002 # m

# roi dimensions
x_roi_len = 0.256 # m
y_roi_len = 0.256 # m
z_roi_len = 0.256 # m

# roi center
x0 = 0.0
y0 = 0.0
z0 = 0.044

# roi grid dimensions
x_roi_dim = int(x_roi_len/dx)
y_roi_dim = int(y_roi_len/dy)
z_roi_dim = int(z_roi_len/dz)

class TestVopgenWriter(unittest.TestCase):
    """Tests for vopgen matfile writers."""
    @classmethod
    def setUpClass(cls):
        if isfile(ef_map_array_file):
            remove(ef_map_array_file)
        cls.sim_ids = []
        cls._xf_project_info = XFProjectInfo(coil_xf_path)
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
        tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(coil_xf_path, self.sim_ids)
        self.assertEqual(3, len(tvopgen._net_input_power_per_coil))
        self.assertTrue(allclose(xf_test_coil_powers,
                                 tvopgen._net_input_power_per_coil))

    def test_ef_map_array_n_mat(self):
        """
        Test the shape of data structures within the saved mat file and generate
        png images of the electric field regions for efMapArrayN.mat
        """
        tvopgen = xfwriter.vopgen.VopgenEFMapArrayN(coil_xf_path, self.sim_ids)
        tvopgen.set_grid_origin(x0, y0, z0)
        self.assertEqual(x0, tvopgen._x0)
        self.assertEqual(y0, tvopgen._y0)
        self.assertEqual(z0, tvopgen._z0)
        tvopgen.set_grid_len(x_roi_len, y_roi_len, z_roi_len)
        self.assertEqual(x_roi_len, tvopgen._xlen)
        self.assertEqual(y_roi_len, tvopgen._ylen)
        self.assertEqual(z_roi_len, tvopgen._zlen)
        tvopgen.set_grid_resolution(0.002, 0.002, 0.002)
        self.assertEqual(dx, tvopgen._dx)
        self.assertEqual(dy, tvopgen._dy)
        self.assertEqual(dz, tvopgen._dz)
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
        tvopgen.savemat(ef_map_array_file)
        self.assertTrue(isfile(ef_map_array_file))
        ef_map = spio.loadmat(ef_map_array_file)
        self.assertTrue((x_roi_dim, y_roi_dim, z_roi_dim, 3, 3),
                        ef_map['efMapArrayN'])

    def test_propmap_mat(self):
        """
        Tests to create/read propmat.mat
        """
        tpropmap = xfwriter.vopgen.VopgenPropertyMap(coil_xf_path,
                                                     sim_id, run_id)
        tpropmap.set_grid_origin(x0, y0, z0)
        self.assertEqual(x0, tpropmap._x0)
        self.assertEqual(y0, tpropmap._y0)
        self.assertEqual(z0, tpropmap._z0)
        tpropmap.set_grid_len(x_roi_len, y_roi_len, z_roi_len)
        self.assertEqual(x_roi_len, tpropmap._xlen)
        self.assertEqual(y_roi_len, tpropmap._ylen)
        self.assertEqual(z_roi_len, tpropmap._zlen)
        tpropmap.set_grid_resolution(dx, dy, dz)
        self.assertEqual(dx, tpropmap._dx)
        self.assertEqual(dy, tpropmap._dy)
        self.assertEqual(dz, tpropmap._dz)
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
        tpropmap.savemat(property_map_file)
        self.assertTrue(isfile(property_map_file))
        prop_map = spio.loadmat(property_map_file)
        self.assertEqual(x_roi_dim, len(prop_map['XDim']))
        self.assertEqual(y_roi_dim, len(prop_map['YDim']))
        self.assertEqual(z_roi_dim, len(prop_map['ZDim']))
        self.assertEqual((x_roi_dim, y_roi_dim, z_roi_dim, 3),
                         shape(prop_map['condMap']))
        self.assertEqual((x_roi_dim, y_roi_dim, z_roi_dim, 3),
                         shape(prop_map['mdenMap']))

    def test_sarmask_aligned_mat(self):
        """
        Tests to create/read sarmask_aligned.mat.
        """
        print("sar_mask_file: ", sar_mask_file)
        tsarmask = xfwriter.vopgen.VopgenSarMask(coil_xf_path, sim_id, run_id)
        tsarmask.set_grid_origin(x0, y0, z0)
        tsarmask.set_grid_len(x_roi_len, y_roi_len, z_roi_len)
        tsarmask.set_grid_resolution(dx, dy, dz)
        tsarmask.savemat(sar_mask_file)
        self.assertTrue(isfile(sar_mask_file))
        sar_mask_mat = spio.loadmat(sar_mask_file)
        self.assertEqual(x_roi_dim, len(sar_mask_mat['XDim']))
        self.assertEqual(y_roi_dim, len(sar_mask_mat['YDim']))
        self.assertEqual(z_roi_dim, len(sar_mask_mat['ZDim']))
        self.assertEqual((x_roi_dim, y_roi_dim, z_roi_dim),
                         shape(sar_mask_mat['sarmask_new']))

    def test_massdensity_map_3d_mat(self):
        """
        Tests to create/read massdensityMat3D.mat.
        """
        tmdenmap3d = xfwriter.vopgen.VopgenMassDensityMap3D(coil_xf_path,
                                                        sim_id, run_id)
        tmdenmap3d.set_grid_origin(x0, y0, z0)
        tmdenmap3d.set_grid_len(x_roi_len, y_roi_len, z_roi_len)
        tmdenmap3d.set_grid_resolution(dx, dy, dz)
        tmdenmap3d.savemat(mass_density_map_3d_file)
        self.assertTrue(isfile(mass_density_map_3d_file))
        mdenmap3d_mat = spio.loadmat(mass_density_map_3d_file)
        self.assertEqual(x_roi_dim, len(mdenmap3d_mat['XDim']))
        self.assertEqual(y_roi_dim, len(mdenmap3d_mat['YDim']))
        self.assertEqual(z_roi_dim, len(mdenmap3d_mat['ZDim']))
        self.assertEqual((x_roi_dim, y_roi_dim, z_roi_dim),
                         shape(mdenmap3d_mat['mden3D']))
        self.assertEqual((x_roi_dim, y_roi_dim, z_roi_dim),
                         shape(mdenmap3d_mat['mden3Dm']))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
