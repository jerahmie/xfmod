#!/usr/bin/env python
"""
Test xfproject routines.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

from os import path, makedirs
from shutil import rmtree
import unittest
from xfutils import (xf_sim_id_to_str, xf_run_id_to_str, 
                     XFProjectInfo, XFProjectError)

_MOCK_XF_PROJECT = 'mock.xf'

class TestXFProject(unittest.TestCase):
    """Unit tests for xfproject module."""
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)
        # Create a mock project directory structure.
        simulations = [1, 2, 3] + list(range(8,10))
        cls._sim_run_list = [[]] * simulations[-1]
        for sim_id in simulations:
            run_list = []
            for run_id in range(sim_id % 3 + 1):
                sim_run_dir = path.join(_MOCK_XF_PROJECT,
                                        r'Simulations',
                                        xf_sim_id_to_str(sim_id),
                                        xf_run_id_to_str(run_id + 1))
                run_list.append(run_id + 1)
                makedirs(sim_run_dir)
            cls._sim_run_list[sim_id - 1] = run_list

    def setUp(self):
        pass

    def test_empty_constructor(self):
        """
        What happens when XFProjectInfo constructor is called without 
        valid project.
        """
        xfmt = XFProjectInfo()
        xfmt.xf_project_dir(_MOCK_XF_PROJECT)
        self.assertEqual(self._sim_run_list, xfmt.xf_sim_run_list)
        with self.assertRaises(FileNotFoundError) as err:
            xfmt.xf_project_dir('/my/bad/project.xf')

    def test_xf_project_error_exception(self):
        """
        Test raise XFProjectError exception.
        """
        with self.assertRaises(XFProjectError) as err:
            raise XFProjectError("Project has error.")
        
    def test_xfproject_mock_xf(self):
        """"Run tests on mocked xf project."""
        print(self.id())
        mock_info = XFProjectInfo(_MOCK_XF_PROJECT)
        self.assertEqual(self._sim_run_list, mock_info.xf_sim_run_list)
        
    def test_coil_xf(self):
        """Test XFProject info run list against Test_Coil.xf"""
        print(self.id())
        xf_test_coil_path = path.normpath(path.join(path.realpath(__file__),
                                                    '..', '..', '..',
                                                    'Test_Data',
                                                    'Test_Coil.xf'))
        xf_test_coil_info = XFProjectInfo(xf_test_coil_path)
        self.assertEqual([[1],[1],[1]], xf_test_coil_info.xf_sim_run_list)

    def test_bad_project(self):
        """
        Ensure proper exception is raised during attempt to extract info 
        from bad or missing project.
        """
        with self.assertRaises(FileNotFoundError) as err:
            XFProjectInfo('/my/bad/project')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # remove mock directory structure
        print("Removing ", _MOCK_XF_PROJECT)
        rmtree(_MOCK_XF_PROJECT)

if __name__ == "__main__":
    unittest.main()
