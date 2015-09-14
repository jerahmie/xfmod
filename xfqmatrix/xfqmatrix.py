"""
xfqmatrix.py creates Q matrix data from electric field data and grid data.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
from scipy.io import loadmat, savemat
import xfgeomod

class XFQMatrix(object):
    """Calculate Q Matrix from XFdtd E field and mesh data."""
    def __init__(self):
        self._project_name = ""
        self._mesh = None
        self._sim_number = 1

    @property
    def project_name(self):
        """Returns XF project file name string"""
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Setter for XF project name."""
        self._project_name = project_name
        
    @project_name.deleter
    def project_name(self):
        """Deleter for XF project name."""
        self._project_name = ""
    
    @private
    def _sim_run_number_to_path(self, sim_number, run_number):
        """Converts simulation and run number to directory names."""
        # Simulation directory name is a fixed-length string with pre-pended
        # zeros
        sim_str_len = 6  
        run_str_zero_len = 4
        sim_digits = len(str(sim_number))
        run_digits = len(str(run_number))
        sim_str = ""
        run_str = "Run"
        # Simulation directory string
        for i in range(sim_str_len - sim_digits):
            sim_str += "0"
        sim_str += str(sim_number)
        # Run directory string
        for i in range(run_str_zero_len - run_digits):
            run_str += "0"
        run_str += str(run_number)

        return [sim_str, run_str]
