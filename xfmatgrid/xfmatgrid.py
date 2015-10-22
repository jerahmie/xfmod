"""
Post-process XFdtd-generated MAT-Files, regrid, and save results to disk.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os, re
from glob import glob
import struct
import numpy as np
from xfmatgrid.xfmultipoint import (XFMultiPointInfo, XFMultiPointFrequencies,
                                    XFMultiPointGeometry, XFMultiPointSSField)
from xfmatgrid.xfutils import xf_sim_id_to_str, xf_run_id_to_str
from xfgeomod import XFGeometry

MP_SS_RE = r'([0-9A-Za-z/_.]*)(MultiPoint_Solid_Sensor[0-9]*_[0-9]*)'

class XFFieldNonUniformGrid(object):
    """Holds XF field data on non-uniform grid."""
    def __init__(self, project_dir, sim_id, run_id):
        xf_geometry_dir = os.path.join(project_dir, r'Simulations',
                                       xf_sim_id_to_str(sim_id),
                                       xf_run_id_to_str(run_id))
        self._project_dir = project_dir
        self._sim_id = int(sim_id)
        self._run_id = int(run_id)
        self._set_mp_info()
        self._set_data_dirs()
        self._mp_field_types = []
        self._xdim = np.zeros(1)
        self._ydim = np.zeros(1)
        self._zdim = np.zeros(1)
        self._ss_field_data = np.zeros(1)
        self._get_mp_field_types()
        self._load_geom()
        self._xf_grid = XFGeometry(xf_geometry_dir)
        self._load_mp_ss_grid()

    def _load_mp_ss_grid(self):
        """Loads subregion of grid encompassing the multipoint solid sensor."""
        # get multipoint solid sensor x-values 
        temp_dim = np.array(self._xf_grid.grid_data.x_coods())
        self._xdim = temp_dim[self._mp_geom.x_domain]

        # get multipoint solid sensor y-values
        temp_dim = np.array(self._xf_grid.grid_data.y_coods())
        self._ydim = temp_dim[self._mp_geom.y_domain]

        # get multipoint solid sensor z-values
        temp_dim = np.array(self._xf_grid.grid_data.z_coods())
        self._zdim = temp_dim[self._mp_geom.z_domain]

    def _set_mp_info(self):
        """Load multipoint sensor info."""
        if os.path.exists(self._project_dir):
            mp_info_file = os.path.join(self._project_dir,
                                        r'Simulations',
                                        xf_sim_id_to_str(self._sim_id),
                                        xf_run_id_to_str(self._run_id),
                                        r'output', r'*_info.bin')
            self._mp_ss_info_file = glob(mp_info_file)
            self._mp_ss_info = XFMultiPointInfo(self._mp_ss_info_file[0])

        else:
            print(r"Could not find project: " + self._project_dir)

    def _set_data_dirs(self):
        """Set the project directory and set sensor file location."""
        mp_sensor_dir = re.match(MP_SS_RE, self._mp_ss_info_file[0])
        self._mp_frequencies_file = os.path.join(mp_sensor_dir.group(1),
                                                  mp_sensor_dir.group(2),
                                                  r'frequencies.bin')
        self._mp_freq = XFMultiPointFrequencies(self._mp_frequencies_file)
        self._mp_geom_file = os.path.join(mp_sensor_dir.group(1),
                                          mp_sensor_dir.group(2),
                                          r'geom.bin')
    def _get_mp_field_types(self):
        """
        Determine which data directories should be present from info flags.
        """
        time_domain_Scattered_E = 1<<31
        time_domain_Total_E = 1<<30
        time_domain_Scattered_H = 1<<29
        time_domain_Total_H = 1<<28
        time_domain_Scattered_B = 1<<27
        time_domain_Total_B = 1<<26
        time_domain_J = 1<<25
        discrete_frequency_Total_E = 1<<24
        discrete_frequency_Total_H = 1<<23
        discrete_frequency_J = 1<<22
        discrete_frequency_Total_B = 1<<21
        discrete_frequency_Dissipated_Power_Density = 1<<20

        mask = self._mp_ss_info.fields_mask

        if mask & time_domain_Scattered_E:
            self._mp_field_types.append(r'tr_Exs')
            self._mp_field_types.append(r'tr_Eys')
            self._mp_field_types.append(r'tr_Ezs')
        if mask & time_domain_Total_E:
            self._mp_field_types.append(r'tr_Ext')
            self._mp_field_types.append(r'tr_Eyt')
            self._mp_field_types.append(r'tr_Ezt')
        if mask & time_domain_Scattered_H:
            self._mp_field_types.append(r'tr_Hxs')
            self._mp_field_types.append(r'tr_Hys')
            self._mp_field_types.append(r'tr_Hzs')
        if mask & time_domain_Total_H:
            self._mp_field_types.append(r'tr_Hxt')
            self._mp_field_types.append(r'tr_Hyt')
            self._mp_field_types.append(r'tr_Hzt')
        if mask & time_domain_Scattered_B:
            self._mp_field_types.append(r'tr_Bxs')
            self._mp_field_types.append(r'tr_Bys')
            self._mp_field_types.append(r'tr_Bzs')
        if mask & time_domain_Total_B:
            self._mp_field_types.append(r'tr_Bxt')
            self._mp_field_types.append(r'tr_Byt')
            self._mp_field_types.append(r'tr_Bzt')
        if mask & time_domain_J:
            self._mp_field_types.append(r'tr_Jx')
            self._mp_field_types.append(r'tr_Jy')
            self._mp_field_types.append(r'tr_Jz')
        if mask & discrete_frequency_Total_E:
            self._mp_field_types.append(r'ss_Exit')
            self._mp_field_types.append(r'ss_Exrt')
            self._mp_field_types.append(r'ss_Eyit')
            self._mp_field_types.append(r'ss_Eyrt')
            self._mp_field_types.append(r'ss_Ezit')
            self._mp_field_types.append(r'ss_Ezrt')
        if mask & discrete_frequency_Total_H:
            self._mp_field_types.append(r'ss_Hxit')
            self._mp_field_types.append(r'ss_Hxrt')
            self._mp_field_types.append(r'ss_Hyit')
            self._mp_field_types.append(r'ss_Hyrt')
            self._mp_field_types.append(r'ss_Hzit')
            self._mp_field_types.append(r'ss_Hzrt')
        if mask & discrete_frequency_J:
            self._mp_field_types.append(r'ss_Jxi')
            self._mp_field_types.append(r'ss_Jxr')
            self._mp_field_types.append(r'ss_Jyi')
            self._mp_field_types.append(r'ss_Jyr')
            self._mp_field_types.append(r'ss_Jzi')
            self._mp_field_types.append(r'ss_Jzr')
        if mask & discrete_frequency_Total_B:
            self._mp_field_types.append(r'ss_Bxit')
            self._mp_field_types.append(r'ss_Bxrt')
            self._mp_field_types.append(r'ss_Byit')
            self._mp_field_types.append(r'ss_Byrt')
            self._mp_field_types.append(r'ss_Bzit')
            self._mp_field_types.append(r'ss_Bzrt')
        if mask & discrete_frequency_Dissipated_Power_Density:
            self._mp_field_types.append(r'ss_PddEx')
            self._mp_field_types.append(r'ss_PddEy')
            self._mp_field_types.append(r'ss_PddEz')
            self._mp_field_types.append(r'ss_PddHx')
            self._mp_field_types.append(r'ss_PddHy')
            self._mp_field_types.append(r'ss_PddHz')

    def _load_geom(self):
        """Load the data in geom.bin"""
        print(r"Loading geom.bin")
        if os.path.exists(self._mp_geom_file):
            self._mp_geom = XFMultiPointGeometry(self._mp_geom_file, 
                                                 self._mp_ss_info.num_points)
        else:
            print(r"Could not find geometry file: " + self._mp_geom_file )

#    def export_ss_mat(self, field_types):
#        """Export ss sensor field data to Mat files."""
#        export_dict = dict()
        

    @property
    def xdim(self):
        """Return the X dimension values."""
        return self._xdim

    @property
    def ydim(self):
        """Return the Y dimension values."""
        return self._ydim

    @property
    def zdim(self):
        """Return the Z dimension values."""
        return self._zdim

    def ss_field_data(self, field_name):
        """Return the real components of the field values."""
        if field_name in self._mp_field_types:
            (path_head, path_tail) = os.path.split(self._mp_ss_info_file[0])
            path_tail = ''.join(path_tail.split('_info.bin'))
            mp_ss_dir = os.path.join(path_head, path_tail)
            file_name = os.path.join( mp_ss_dir, field_name, r'0.bin')
            print("Loading field data from: ", file_name)
            mp_ss_field = XFMultiPointSSField(file_name, self._mp_ss_info, self._mp_geom)
            self._ss_field_data = mp_ss_field.ss_field

        return self._ss_field_data

    @property
    def project_dir(self):
        """Return the grid units."""
        return self._project_dir

    @property
    def sim_id(self):
        """Return the current simulation id."""
        return self._sim_id

    @sim_id.setter
    def sim_id(self, sim_id):
        """Set the Simulation ID."""
        self._sim_id = int(sim_id)

    @property
    def run_id(self, run_id):
        """Return the current run ID."""
        return self._run_id

    @run_id.setter
    def run_id(self, run_id):
        """Set the Run ID."""
        self._run_id = int(run_id)

    @property
    def mp_field_types(self):
        """Return the multipoint field directories."""
        return self._mp_field_types
