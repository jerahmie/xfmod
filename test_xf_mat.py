#!/usr/bin/env python2

#from __future__ import(absolute_import, division, generators,
#                       print_function, unicode_literals)
#
import os
import scipy.io as spio

XF_TEST_MAT_FILE1 = os.path.normpath(os.path.join('/Data/CMRR/rf_coil_scripts/python/Test_Data/Test_Coil.xf/Export/Raw/total_B_field_data_raw_000001.mat'))

os.path.exists(XF_TEST_MAT_FILE1)

spio.loadmat(XF_TEST_MAT_FILE1)
