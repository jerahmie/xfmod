#!/usr/bin/env python
"""
Helper class to store data for individual XF simulation.
"""
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import unittest
from xfmod.xfutils import XFSimulationInfo

class TestXFSimulation(unittest.TestCase):
    """Unit tests for xfsimulation module.
    """
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)
        

    def setUp(self):
        pass

    def test_environment(self):
        """Test the environmental setup.
        """
        self.assertEqual(-1,-1)

    def test_simulation_setup(self):
        """Create an empty simulation class.
        """
        
        ts = XFSimulationInfo()
        self.assertIsInstance(ts,object)
        

    def test_bad_simulation_path(self):
        """Create a XFSimulationInfo object and test for FileNotFoundErr
        Exception if bad path provided.
        """
        
        with self.assertRaises(FileNotFoundError):
            
            

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
