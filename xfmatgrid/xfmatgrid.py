"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
from glob import glob
from scipy.io import loadmat, savemat
import scipy.interpolate as interp

class XFFieldNonUniformGrid(object):
    """A class to hold XF field data on non-uniform grid."""
    def __init__(self):
        self._project_dir = ''
        self._multipoint_sensor_files = []
        self._run_id = 0
        self._sim_id = 0
        self._field_type = ''

    @property
    def project_dir(self):
        """Return the grid units."""
        return self._project_dir
    
    @project_dir.setter
    def project_dir(self, project_dir):
        """Set the project directory and set sensor file location."""
        self._project_dir = project_dir
        if os.path.exists(self._project_dir):
            self._multipoint_sensor_files = \
                    glob(os.path.join(self._project_dir,
                        'Simulations', 
                        xf_sim_id_to_str(self._sim_id), 'Run0001', 
                        'output', '*_info.bin'))
    @property
    def sim_id(self):
        """Return the current simulation id."""
        return self._sim_id
    
    @sim_id.setter
    def sim_id(self, sim_id):
        """Set the Simulation ID."""
        self._sim_id = sim_id

    
    

# TODO: Helper functions - refactor to xf_utils/ or similar
def is_valid_run_id(run_id):
    """Check whether run_id is valid XFdtd run id."""
    MIN_RUN_ID = 1
    MAX_RUN_ID = 9999
    if isinstance(run_id, int):
        if (run_id >= MIN_RUN_ID) and (run_id <= MAX_RUN_ID):
            return True
    return False

def is_valid_sim_id(sim_id):
    """Check whether sim_id is valid XFdtd simulatin id."""
    MIN_SIM_ID = 1
    MAX_SIM_ID = 999999
    if isinstance(sim_id, int):
        if (sim_id >= MIN_SIM_ID) and (sim_id <= MAX_SIM_ID):
            return True
    return False

def xf_run_id_to_str(run_id):
    """Converts a integer to XFdtd RunID string."""
    padded_string_length = 4
    run_id_string = 'Run'
    if is_valid_run_id(run_id):
        run_id_string_length = len(str(run_id))
        for i in range(padded_string_length - run_id_string_length):
            run_id_string += '0'
        run_id_string += str(run_id)
        return run_id_string
    else:
        print("Invalid Run ID: ", run_id)
        return None

def xf_sim_id_to_str(sim_id):
    """Converts an integer to a valid XFdtd SimID string."""
    padded_string_length = 6
    sim_id_string = ''
    if is_valid_sim_id(sim_id):
        sim_id_string_length = len(str(sim_id))
        for i in range(padded_string_length - sim_id_string_length):
            sim_id_string += '0'
        sim_id_string += str(sim_id)
        return sim_id_string
    else:
        print("Invalid Simulation ID: ", sim_id)
        return None
