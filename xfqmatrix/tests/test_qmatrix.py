#!/usr/bin/env python
"""
Test xfqmatrix.py
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
import unittest
import xfqmatrix

class myTest(unittest.TestCase):
    def setUp(self):
        self.qm = xfqmatrix.XFQMatrix()
        self.file_name = os.path.join('/Data','CMRR',
                                      'XFdtd_Results','Test_Coil.xf')
        self.qm.file_name = self.file_name

    def test_setters(self):
        self.assertEqual(self.qm.file_name, self.file_name)

    def test_sim_run_path(self):
        self.assertEqual(self.qm._sim_run_number_to_path(1,1),
                         ['000000','Run0000'])

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()


    
