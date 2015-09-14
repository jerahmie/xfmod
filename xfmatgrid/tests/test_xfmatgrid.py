#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(division, print_function, unicode_literals)

import sys, os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), 
                                            os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from xfmatgrid import XFFieldNonUniformGrid

TEST_PROJECT_DIR = os.path.realpath(os.path.relpath(os.path.join('..','..','Test_Data','Test_Coil.xf')))

class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    def setUp(self):
        self.grid = XFFieldNonUniformGrid()
    
    def test_project_file(self):
        self.grid.project_dir = TEST_PROJECT_DIR
        self.assertEqual(TEST_PROJECT_DIR, self.grid.units)

    def tearDown(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
