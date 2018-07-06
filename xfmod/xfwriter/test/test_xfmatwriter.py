#!/usr/bin/env python
"""
Test xfmatwriter using unittest framework.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
from os.path import (normpath, join)
import unittest
import scipy.io as spio
import numpy as np
from xfmod import xfwriter

FILE_PATH=os.path.realpath(__file__)

TEST_PROJECT_DIR = normpath(join(FILE_PATH,
                                 '..', '..', '..', '..',
                                 'Test_Data', 'Test_Coil.xf'))
TEST_SIM_NUMBER = 1
TEST_RUN_NUMBER = 1
XF_RAW_MAT_FILE = normpath(join(TEST_PROJECT_DIR,
                                'Export', 'Raw',
                                'total_E_field_data_raw_000001.mat'))
SAVE_MAT_FILE_NONUNIFORM = normpath(join(FILE_PATH, '..',
                                         'test_E_field_nonuniform.mat'))
SAVE_MAT_FILE_UNIFORM = normpath(join(FILE_PATH, '..',
                                      'test_E_field_uniform.mat'))
SAVE_MAT_FILE_UNIFORM_MAIN = normpath(join(FILE_PATH, '..',
                                           'test_E_field_uniform_from_main.mat'))
SAVE_MAT_FILE_B_NONUNIFORM_SCALED = normpath(join(FILE_PATH, '..',
                                                  'test_B_field_nonuniform_scaled.mat'))


class TestXFMatWriter(unittest.TestCase):
    """Tests for xfmatwriter."""
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)
        try:
            cls.xfmw = xfwriter.XFMatWriter()
            cls.xfmw_nu = xfwriter.XFFieldWriterNonUniform(TEST_PROJECT_DIR,
                                                           TEST_SIM_NUMBER,
                                                           TEST_RUN_NUMBER)
            cls.xfmw_uniform = xfwriter.XFFieldWriterUniform(TEST_PROJECT_DIR,
                                                             TEST_SIM_NUMBER,
                                                             TEST_RUN_NUMBER)
        except NameError as err:
            print("Unable to create instance of XFMatWriter.")
            raise err
        if(os.path.exists(SAVE_MAT_FILE_UNIFORM)):
            try:
                os.remove(SAVE_MAT_FILE_UNIFORM)
            except:
                print("Error while removing file: " +
                      SAVE_MAT_FILE_UNIFORM)
                raise

        if(os.path.exists(SAVE_MAT_FILE_NONUNIFORM)):
            try:
                os.remove(SAVE_MAT_FILE_NONUNIFORM)
            except:
                print("Error while removing file: " +
                      SAVE_MAT_FILE_NONUNIFORM)
                raise

        if(os.path.exists(SAVE_MAT_FILE_B_NONUNIFORM_SCALED)):
            try:
                os.remove(SAVE_MAT_FILE_B_NONUNIFORM_SCALED)
            except:
                print("Error while removing file: " +
                      SAVE_MAT_FILE_B_NONUNIFORM_SCALED)
                raise

        if(os.path.exists(SAVE_MAT_FILE_UNIFORM_MAIN)):
            try:
                os.remove(SAVE_MAT_FILE_UNIFORM_MAIN)
            except:
                print("Error while removing file: " +
                      SAVE_MAT_FILE_UNIFORM_MAIN)
                raise

    def setUp(self):
        pass

    def test_class_xfmatwriter(self):
        """
        Test abstract base class XFMatWriter.
        """
        print(self.id())
        self.assertIsInstance(self.xfmw, xfwriter.XFMatWriter)

    def test_xf_field_writer_uniform_hierarchy(self):
        """
        Test abstract class for uniformly interpolated data.
        """
        print(self.id())
        self.assertIsInstance(self.xfmw_uniform, xfwriter.XFMatWriter)
        self.assertIsInstance(self.xfmw_uniform, xfwriter.XFFieldWriterUniform)

    def test_normalization(self):
        """
        Verify the multiple field normalization methods.
        """
        print(self.id())

        # quick check for normalization by input power
        self.xfmw_nu.net_input_power = 9.0
        self.assertAlmostEqual(9.0, self.xfmw_nu.net_input_power)

        # point for B-field normalization
        x0 = 0.0
        y0 = 0.0
        z0 = 0.0

        self.xfmw_nu.scale_b1_at_point(1e-6, [x0, y0, z0])
        field_norm_save = self.xfmw_nu._field_norm
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [])
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [3,4])
        print(err.exception.message)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [5000, 0, 0])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [-5000, 0, 0])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [0, 5000, 0])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [0, -5000, 0])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [0, 0, 5000])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        with self.assertRaises(xfwriter.XFFieldError) as err:
            self.xfmw_nu.scale_b1_at_point(1e-6, [0, 0, -5000])
        print(err.exception.message)
        self.assertAlmostEqual(field_norm_save, self.xfmw_nu._field_norm)
        self.xfmw_nu.savemat('B', SAVE_MAT_FILE_B_NONUNIFORM_SCALED)

        xf_b_scaled_mat = spio.loadmat(SAVE_MAT_FILE_B_NONUNIFORM_SCALED)
        xdim = xf_b_scaled_mat['XDim']
        ydim = xf_b_scaled_mat['YDim']
        zdim = xf_b_scaled_mat['ZDim']
        x_ind = np.argmin(abs(xdim - x0))
        y_ind = np.argmin(abs(ydim - y0))
        z_ind = np.argmin(abs(zdim - z0))
        b1x = xf_b_scaled_mat['Bx'][x_ind, y_ind, z_ind]
        b1y = xf_b_scaled_mat['By'][x_ind, y_ind, z_ind]
        b1z = xf_b_scaled_mat['Bz'][x_ind, y_ind, z_ind]
        b1_mag = np.sqrt(b1x*b1x.conjugate() +
                         b1y*b1y.conjugate() +
                         b1z*b1z.conjugate())
        self.assertAlmostEqual(1.0e-6, abs(b1_mag))

    def test_xf_write_uniform_matfile(self):
        """
        Write mat file and verify the file exists and data is reasonable.
        """
        print(self.id())
        with self.assertRaises(ZeroDivisionError):
            xf_e_mat_u = self.xfmw_uniform.savemat('E', SAVE_MAT_FILE_UNIFORM)

        self.xfmw_uniform.set_grid_origin(0.001,-0.002,0.044)
        self.xfmw_uniform.set_grid_len(0.032, 0.032, 0.050)
        self.xfmw_uniform.set_grid_resolution(0.002, 0.002, 0.002)
        self.xfmw_uniform.net_input_power = 1.0e-6
        xf_e_mat_u = self.xfmw_uniform.savemat('E', SAVE_MAT_FILE_UNIFORM)
        self.assertTrue(os.path.exists(SAVE_MAT_FILE_UNIFORM))

    def test_xf_field_writer_nonuniform_hierarchy(self):
        """Test the fieldwriter on nonuniform grid."""
        print(self.id())
        self.assertIsInstance(self.xfmw_nu, xfwriter.XFMatWriter)
        self.assertIsInstance(self.xfmw_nu, xfwriter.XFFieldWriterNonUniform)

    def test_xf_write_nonuniform_matfile(self):
        """
        Write mat file and verify we get the same data as XFdtd matlab exporter.
        Note: XFdtd 7.5 and earlier exported mat files must have array value
              types of 0x06 changed to 0x09 (double) with hex editor or
              equivalent according to Mat-file format spec.
        """
        print(self.id())
        xfmw_nu = xfwriter.XFFieldWriterNonUniform(TEST_PROJECT_DIR,
                                                   TEST_SIM_NUMBER,
                                                   TEST_RUN_NUMBER)
        xfmw_nu.savemat('E', SAVE_MAT_FILE_NONUNIFORM)
        self.assertTrue(os.path.exists(SAVE_MAT_FILE_NONUNIFORM))
        xf_e_mat = spio.loadmat(XF_RAW_MAT_FILE)
        xfmatgrid_e_mat = spio.loadmat(SAVE_MAT_FILE_NONUNIFORM)
        self.assertTrue(np.allclose(xf_e_mat['X_Dimension_3\x00  ']/1000.0,
                                    xfmatgrid_e_mat['XDim']))
        self.assertTrue(np.allclose(xf_e_mat['Y_Dimension_2\x00  ']/1000.0,
                                    xfmatgrid_e_mat['YDim']))
        self.assertTrue(np.allclose(xf_e_mat['Z_Dimension_1\x00  ']/1000.0,
                                    xfmatgrid_e_mat['ZDim']))
        xfdtd_ex = xf_e_mat['TotalField_E_X\x00 '][:,:,:,0]
        self.assertTrue(np.shape(xfdtd_ex), xfmatgrid_e_mat['Ex'])
        self.assertTrue(np.allclose(np.transpose(xfdtd_ex, (2,1,0)),
                                    xfmatgrid_e_mat['Ex']))
        del xfmw_nu

    def test_xf_uniform_field_writer_main(self):
        """
        Write mat file using main routine to test call from command line.
        """
        test_argv = [r'--xf_project=' + TEST_PROJECT_DIR, 
                     r'--export_file=' + SAVE_MAT_FILE_UNIFORM_MAIN,
                     r'--sim=1', r'--run=1', r'--field=E',
                     r'--origin=[0.001, 0.002, 0.044]',
                     r'--lengths=[0.032, 0.032, 0.050]',
                     r'--deltas=[0.002, 0.002, 0.002]',
                     r'--net_input_power=1.0'
                 ]
        xfwriter.xf_field_writer_uniform.main(test_argv)
        self.assertTrue(os.path.exists(SAVE_MAT_FILE_UNIFORM_MAIN))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
