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
#import matplotlib.pyplot as plt
import xfwriter


TEST_PROJECT_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                 '..', '..', '..',
                                                 'Test_Data', 'Test_Coil.xf'))
TEST_SIM_NUMBER = 1
TEST_RUN_NUMBER = 1
XF_RAW_MAT_FILE = os.path.normpath(os.path.join(TEST_PROJECT_DIR,
                                                'Export', 'Raw',
                                                'total_E_field_data_raw_000001.mat'))
SAVE_MAT_FILE = 'test_E_field_nonuniform.mat'

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
            #cls.xfmw_nu.net_input_power = 1.0

        except NameError as err:
            print("Unable to create instance of XFMatWriter.")
            raise err

    def setUp(self):
        pass

    def test_class_xfmatwriter(self):
        """Test abstract clas XFMatWriter."""
        self.assertIsInstance(self.xfmw, xfwriter.XFMatWriter)

    def test_xf_field_writer_nonuniform_hierarchy(self):
        """Test the fieldwriter on nonuniform grid."""
        self.assertIsInstance(self.xfmw_nu, xfwriter.XFMatWriter)
        self.assertIsInstance(self.xfmw_nu, xfwriter.XFFieldWriterNonUniform)

    def test_xf_write_nonuniform_matfile(self):
        """
        Write mat file and verify we get the same data as XFdtd matlab exporter.
        Note: XFdtd 7.5 and earlier exported mat files must have array value types of 
              0x06 changed to 0x09 (double) with hex editor or equivalent according to 
              Mat-file format spec.
        """
        self.xfmw_nu.savemat('E', SAVE_MAT_FILE)
        self.assertTrue(os.path.exists(SAVE_MAT_FILE))
        xf_e_mat = spio.loadmat(XF_RAW_MAT_FILE)
        xfmatgrid_e_mat = spio.loadmat(os.path.normpath(os.path.join(os.getcwd(),
                                                                     SAVE_MAT_FILE)))
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
        """Remove exported mat file."""
        try:
            os.remove(SAVE_MAT_FILE)
        except FileNotFoundError as err:
            print("Exported mat file, ", SAVE_MAT_FILE, ", not found.")

if __name__ == "__main__":
    unittest.main()
