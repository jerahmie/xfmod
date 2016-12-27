#!/usr/bin/env python
"""
Test citi module using unittest framework.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
from os.path import (normpath, join)
import unittest
import citi

FILE_PATH = os.path.realpath(__file__)
TEST_CITI_FILE = normpath(join(FILE_PATH, '..', '..', '..',
                               'Test_Data', 'project-s11.cti'))

class TestCiti(unittest.TestCase):
    """Tests for citi module."""
    @classmethod
    def setUpClass(cls):
        pass

    def setup(self):
        pass

    def test_test_case(self):
        """
        Ensure unittest.TestCase is set up properly.
        """
        self.assertTrue(True)

    def test_citi_object(self):
        """
        Ensure inheritance chain.
        """
        tc = citi.Citi()
        self.assertIsInstance(tc, object)
        self.assertIsInstance(tc, citi.Citi)
        
    def test_citi_bad(self):
        """
        Missing file should raise appropriate error.
        """
        with self.assertRaises(FileNotFoundError) as err:
            tc = citi.Citi('nociti.cti')
            
    def test_citi_parse(self):
        """
        Ensure valid Citi file parses properly.
        """
        tc = citi.Citi(TEST_CITI_FILE)
        self.assertEqual('A.01.00', tc.version) 
        self.assertEqual('DATA', tc.name)
        self.assertEqual('FREQ', tc.var)
        self.assertEqual('MAG', tc.var_type)
        self.assertEqual(121, tc.var_num)
        self.assertEqual('S[1,1]', tc.data_name)
        self.assertEqual('RI', tc._data_type)
        self.assertEqual(121, len(tc.var_list))
        self.assertEqual(121, len(tc.data))
    
    def test_citi_set_file(self):
        """
        Create an empty Citi object and specify file later.
        """
        tc = citi.Citi()
        self.assertEqual(None, tc.version)
        self.assertEqual(None, tc.name)
        self.assertEqual(None, tc.var)
        self.assertEqual(None, tc.var_type)
        self.assertEqual(None, tc.var_num)
        self.assertEqual(None, tc.data_name)
        self.assertEqual(None, tc._data_type)
        tc.file(TEST_CITI_FILE)
        self.assertEqual('A.01.00', tc.version) 
        self.assertEqual('DATA', tc.name)
        self.assertEqual('FREQ', tc.var)
        self.assertEqual('MAG', tc.var_type)
        self.assertEqual(121, tc.var_num)
        self.assertEqual('S[1,1]', tc.data_name)
        self.assertEqual('RI', tc._data_type)
        self.assertEqual(121, len(tc.var_list))
        self.assertEqual(121, len(tc.data))
    
    def test_citi_data_at_var(self):
        """
        Test data_at_var interpolation 
        """
        
        tc = citi.Citi(TEST_CITI_FILE)
        self.assertAlmostEqual(-0.5490502-0.4400053j, tc.data_at_var(447.0e6), 
                               places=5)
        self.assertAlmostEqual(-0.5709536-0.4329997j, tc.data_at_var(460.0e6), 
                               places=5)
    def teardown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
