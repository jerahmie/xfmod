"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
from glob import glob
from functools import partial
import struct
from scipy.io import loadmat, savemat
import scipy.interpolate as interp

class XFFieldNonUniformGrid(object):
    """A class to hold XF field data on non-uniform grid."""
    def __init__(self):
        self._project_dir = ''
        self._multipoint_sensor_info_file = []
        self._multipoint_sensor_info = []
        self._run_id = 0
        self._sim_id = 0
        self._field_mask = 0
        
    @property
    def project_dir(self):
        """Return the grid units."""
        return self._project_dir

    @project_dir.setter
    def project_dir(self, project_dir):
        """Set the project directory and set sensor file location."""
        self._project_dir = project_dir
        if os.path.exists(self._project_dir):
            self._multipoint_sensor_info_file = \
                    glob(os.path.join(self._project_dir,
                        'Simulations',
                        xf_sim_id_to_str(self._sim_id), 'Run0001',
                        'output', '*_info.bin'))
            mp_info = XFMultiPointInfo(self._multipoint_sensor_info_file[0])
            self._multipoint_sensor_info.append(mp_info)

    @property
    def sim_id(self):
        """Return the current simulation id."""
        return self._sim_id

    @sim_id.setter
    def sim_id(self, sim_id):
        """Set the Simulation ID."""
        self._sim_id = sim_id

    

class XFMultiPointGeometry(object):
    """Class to hold Multi Point Geometry Info"""
    def __init__(self, file_name):
        self._MP_VERTEX_LEN=12  # (X,Y,Z) = 4-byte uint * 3
        self._vertices = []
        self._frequencies = []
        self._load_vertices(file_name)
        self._num_points = len(self._vertices)


    def _load_vertices(self, file_name):
        """Load vertices from geom.bin"""
        print("Loading vertices...")
        with open(file_name,'rb') as file_handle:
            while True:
                chunk = file_handle.read(self._MP_VERTEX_LEN)
                if len(chunk) < self._MP_VERTEX_LEN:
                    print('Last chunk length: ', len(chunk))
                    break
                else:
                    x = struct.unpack('I',chunk[0:4])[0]
                    y = struct.unpack('I',chunk[4:8])[0]
                    z = struct.unpack('I',chunk[8:12])[0]
                    self._vertices.append([x,y,z])
        print("Done.")
        file_handle.close()

class XFMultiPointInfo(object):
    """Class to hold MultiPoint file info."""
    def __init__(self, file_name):
        self._header = ''
        self._version = 0
        self._fields_mask = 0
        self._num_points = 0
        self._load_multipoint_info(file_name)

    @property
    def header(self):
        """Return multipoint sensor file header."""
        return self._header

    @property
    def version(self):
        """Return the multipoint sensor file version."""
        return self._version
    
    @property
    def fields_mask(self):
        return self._fields_mask

    @property
    def num_points(self):
        return self._num_points

    def _load_multipoint_info(self, file_name):
        """Load multipoint sensor info from file."""
        file_handle = open(file_name,'rb')
        self._header = file_handle.read(4).decode("utf-8")
        self._version = struct.unpack('B',file_handle.read(1))[0]
        self._fields_mask = struct.unpack('I', file_handle.read(4))[0]
        if self._version == 0:
            self._num_points = struct.unpack('I',file_handle.read(4))[0]
        else:
            self._num_points = struct.unpack('Q',file_handle.read(8))[0]
        file_handle.close()

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
