#!/usr/bin/env python3
"""
Test xfutils module.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys
import os
import unittest
import xfutils

class TestXFUtils(unittest.TestCase):
    """Unit tests for xfutils module."""
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)

    def setUp(self):
        pass

    def test_xf_sim_id_to_str(self):
        """Verify XFdtd valid simulation string composition."""
        print(self.id())
        self.assertTrue(xfutils.is_valid_sim_id(1))
        self.assertTrue(xfutils.is_valid_sim_id(999999))
        self.assertFalse(xfutils.is_valid_sim_id(-1.1))
        self.assertFalse(xfutils.is_valid_sim_id(0))
        self.assertFalse(xfutils.is_valid_sim_id(1000000))
        self.assertEqual('000001', xfutils.xf_sim_id_to_str(1))
        self.assertEqual('999999', xfutils.xf_sim_id_to_str(999999))

    def test_xf_run_id_to_str(self):
        """Verify XFdtd valid run string composition."""
        print(self.id())
        self.assertTrue(xfutils.is_valid_run_id(1))
        self.assertTrue(xfutils.is_valid_run_id(9999))
        self.assertFalse(xfutils.is_valid_run_id(-1))
        self.assertFalse(xfutils.is_valid_run_id(0))
        self.assertFalse(xfutils.is_valid_run_id(10000.0))
        self.assertEqual('Run0001', xfutils.xf_run_id_to_str(1))
        self.assertEqual('Run9999', xfutils.xf_run_id_to_str(9999))

    def test_is_valid_run_id_str(self):
        """Check if run id string is valid."""
        print(self.id())
        self.assertFalse(xfutils.is_valid_run_id_str('Run0'))
        self.assertFalse(xfutils.is_valid_run_id_str('Xxx0001'))
        self.assertTrue(xfutils.is_valid_run_id_str('Run0001'))
        self.assertFalse(xfutils.is_valid_run_id_str('Run999999'))
        self.assertTrue(xfutils.is_valid_run_id_str('Run9999'))

    def test_xf_run_str_to_int(self):
        print(self.id())
        """Verify XFdtd run int from 'RunXXXX' string."""
        self.assertEqual(1, xfutils.xf_run_str_to_int('Run0001'))
        self.assertEqual(9999, xfutils.xf_run_str_to_int('Run9999'))


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
