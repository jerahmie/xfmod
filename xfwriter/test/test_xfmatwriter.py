#!/usr/bin/env python
"""
Test xfmatwriter using unittest framework.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import unittest
import scipy.io as spio
import numpy as np
import xfwriter


TEST_PROJECT_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                 '..', '..', '..',
                                                 'Test_Data', 'Test_Coil.xf'))
TEST_SIM_NUMBER = 1
TEST_RUN_NUMBER = 1
XF_RAW_MAT_FILE = os.path.normpath(os.path.join(TEST_PROJECT_DIR,
                                                'Export', 'Raw',
                                                'total_E_field_data_raw_000001.mat'))
SAVE_MAT_FILE_NONUNIFORM = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                         '..', 'test_E_field_nonuniform.mat'))
SAVE_MAT_FILE_UNIFORM = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                      '..', 'test_E_field_uniform.mat'))

class TestXFMatWriter(unittest.TestCase):
    """Tests for xfmatwriter."""
    @classmethod
    def setUpClass(cls):
        print("loading xfmatwriter...")
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
                print("Error while removing file: " + SAVE_MAT_FILE_UNIFORM)
                raise

        if(os.path.exists(SAVE_MAT_FILE_NONUNIFORM)):
            try:
                os.remove(SAVE_MAT_FILE_NONUNIFORM)
            except:
                print("Error while removing file: " + SAVE_MAT_FILE_NONUNIFORM)
                raise

    def setUp(self):
        pass

    def test_class_xfmatwriter(self):
        """Test abstract base class XFMatWriter."""
        print(self.id())
        self.assertIsInstance(self.xfmw, xfwriter.XFMatWriter)

    def test_xf_field_writer_uniform_hierarchy(self):
        """Test abstract class for uniformly interpolated data."""
        print(self.id())
        self.assertIsInstance(self.xfmw_uniform, xfwriter.XFMatWriter)
        self.assertIsInstance(self.xfmw_uniform, xfwriter.XFFieldWriterUniform)
        

    def test_xf_write_uniform_matfile(self):
        """
        Write mat file and verify the file exists and data is reasonable.
        """
        print(self.id())
        with self.assertRaises(ZeroDivisionError):
            xf_e_mat_u = self.xfmw_uniform.savemat('E', SAVE_MAT_FILE_UNIFORM)

        self.xfmw_uniform.set_grid_origin(0,0,0.044)
        self.xfmw_uniform.set_grid_len(0.256, 0.256, 0.256)
        self.xfmw_uniform.set_grid_resolution(0.002, 0.002, 0.002)
        self.xfmw_uniform.net_input_power = 1.0
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
        Note: XFdtd 7.5 and earlier exported mat files must have array value types of 
              0x06 changed to 0x09 (double) with hex editor or equivalent according to 
              Mat-file format spec.
        """
        print(self.id())
        self.xfmw_nu.savemat('E', SAVE_MAT_FILE_NONUNIFORM)
        self.assertTrue(os.path.exists(SAVE_MAT_FILE_NONUNIFORM))
        xf_e_mat = spio.loadmat(XF_RAW_MAT_FILE)
        xfmatgrid_e_mat = spio.loadmat(os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                                     SAVE_MAT_FILE_NONUNIFORM)))
        self.assertTrue(np.allclose(xf_e_mat['X_Dimension_3\x00  ']/1000.0,
                                    xfmatgrid_e_mat['XDim']))
        self.assertTrue(np.allclose(xf_e_mat['Y_Dimension_2\x00  ']/1000.0,
                                    xfmatgrid_e_mat['YDim']))
        self.assertTrue(np.allclose(xf_e_mat['Z_Dimension_1\x00  ']/1000.0,
                                    xfmatgrid_e_mat['ZDim']))
        xfdtd_ex = xf_e_mat['TotalField_E_X\x00 '][:,:,:,0]
        self.assertTrue(np.shape(xfdtd_ex), xfmatgrid_e_mat['Ex'])
        self.assertTrue(np.allclose(np.transpose(xfdtd_ex, (2,1,0)), xfmatgrid_e_mat['Ex']))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
