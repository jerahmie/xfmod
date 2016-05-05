#!/usr/bin/env python
"""
Test xfproject routines.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
from os.path import normpath, realpath, join
from shutil import rmtree
import unittest
from xfutils import xf_sim_id_to_str, xf_run_id_to_str
from xfutils.xfproject import XFProjectInfo

MOCK_XF_PROJECT = 'mock.xf'

class TestXFProject(unittest.TestCase):
    """Unit tests for xfproject module."""
    @classmethod
    def setUpClass(cls):
        # Create a mock project directory structure.
        simulations = [1, 2, 3] + list(range(8,10))
        cls._sim_run_list = [[]] * simulations[-1]
        print('simulations: ', simulations)
        for sim_id in simulations:
            run_list = []
            for run_id in range(sim_id % 3 + 1):
                sim_run_dir = join(MOCK_XF_PROJECT,
                                   r'Simulations',
                                   xf_sim_id_to_str(sim_id),
                                   xf_run_id_to_str(run_id + 1))
                run_list.append(run_id + 1)
                os.makedirs(sim_run_dir)
            cls._sim_run_list[sim_id - 1] = run_list

    def setUp(self):
        pass

    def test_xfproject_mock_xf(self):
        """"Run tests on mocked xf project."""
        mock_info = XFProjectInfo(MOCK_XF_PROJECT)
        self.assertEqual(self._sim_run_list, mock_info.xf_sim_run_list)
        
    def test_coil_xf(self):
        """Test XFProject info run list against Test_Coil.xf"""
        xf_test_coil_path = normpath(join(realpath(__file__),
                                          '..', '..', '..',
                                          'Test_Data',
                                          'Test_Coil.xf'))
        print(xf_test_coil_path)
        xf_test_coil_info = XFProjectInfo(xf_test_coil_path)
        self.assertEqual([[1],[1],[1]], xf_test_coil_info.xf_sim_run_list)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # remove mock directory structure
        print("Removing ", MOCK_XF_PROJECT)
        rmtree(MOCK_XF_PROJECT)

if __name__ == "__main__":
    unittest.main()
