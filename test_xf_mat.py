#!/usr/bin/env python3

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import scipy.io as spio

#XF_TEST_MAT_FILE1 = os.path.normpath(os.path.join('/Data/CMRR/xfmod/Test_Data/Test_Coil.xf/Export/Raw/tE_mod.mat'))
XF_TEST_MAT_FILE1 = os.path.normpath(os.path.join('/Data/CMRR/xfmod/Test_Data/Test_Coil.xf/Export/Raw/total_B_field_data_raw_000001.mat'))
#XF_TEST_MAT_FILE1 = os.path.normpath(os.path.join('/Data/CMRR/xfmod/xfmatgrid/test/test.mat'))
print(XF_TEST_MAT_FILE1)

os.path.exists(XF_TEST_MAT_FILE1)

a = spio.loadmat(XF_TEST_MAT_FILE1)
print(a)
