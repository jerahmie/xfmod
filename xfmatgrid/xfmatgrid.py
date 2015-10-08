"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
from glob import glob
import struct
from xfmatgrid.xfmultipoint import XFMultiPointInfo
from xfmatgrid.xfutils import xf_sim_id_to_str

class XFFieldNonUniformGrid(object):
    """Holds XF field data on non-uniform grid."""
    def __init__(self):
        self._project_dir = ''
        self._multipoint_sensor_info_file = []
        self._multipoint_sensor_info = []
        self._run_id = 0
        self._sim_id = 0
        self._frequencies = []

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
                                      xf_sim_id_to_str(self._sim_id),
                                      'Run0001',
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

