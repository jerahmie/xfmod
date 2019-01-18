"""
Represent XFdtd field data on non-uniform grid.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
import re
from glob import glob
import numpy as np
from xfmod.xfmatgrid.xfmultipoint import (XFMultiPointInfo,
                                          XFMultiPointFrequencies,
                                          XFMultiPointGeometry,
                                          XFMultiPointSSField)
from xfmod.xfutils import xf_sim_id_to_str, xf_run_id_to_str
from xfmod.xfgeomod import XFGeometry


class XFFieldNonUniformGrid(object):
    """Holds XF field data on non-uniform grid."""
    def __init__(self, xf_project_dir, sim_id, run_id, mp_sensor_name):
        self._valid_types = [r'E', r'H', r'B', r'J']
        self._valid_components = [r'x', r'y', r'z']
        self._project_dir = xf_project_dir
        self._sim_id = int(sim_id)
        self._run_id = int(run_id)
        self._mp_sensor_name = mp_sensor_name
        self._mp_sensor_name_re  = r'(.*)(MultiPoint_' + mp_sensor_name \
                                   + r'_[0-9]+)'
        self._mp_ss_info_file = []
        self._mp_ss_info = None
        self._set_mp_info(r'MultiPoint_' + mp_sensor_name + '*_info.bin')
        self._set_data_dirs()
        self._mp_field_types = []
        self._xdim = np.zeros(1)
        self._ydim = np.zeros(1)
        self._zdim = np.zeros(1)
        self._ss_field_data = np.zeros(1)
        self._get_mp_field_types()
        self._load_geom()
        self._xf_grid = XFGeometry(xf_project_dir, sim_id, run_id)
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

    def _set_mp_info(self, mp_ss_info_file_name):
        """Load multipoint sensor info."""
        if os.path.exists(self._project_dir):
            mp_info_file = os.path.join(self._project_dir,
                                        r'Simulations',
                                        xf_sim_id_to_str(self._sim_id),
                                        xf_run_id_to_str(self._run_id),
                                        r'output',
                                        mp_ss_info_file_name)

            self._mp_ss_info_file = glob(mp_info_file)
            self._mp_ss_info = XFMultiPointInfo(self._mp_ss_info_file[0])

        else:
            print("Could not find project: " + self._project_dir)

    def _set_data_dirs(self):
        """Set the project directory and set sensor file location."""
        try:
            print(self._mp_ss_info_file[0])
            
        except:
            print("[Warning] Multipoint Sensor data file missing.")
            print("self._mp_ss_info_file")
            print(self._mp_ss_info_file)
            print(self._mp_ss_info_file[0])
            print(self._mp_ss_info)
            raise

        try:
            mp_sensor_dir = re.match(self._mp_sensor_name_re,
                                     self._mp_ss_info_file[0])
            self._mp_frequencies_file = os.path.join(mp_sensor_dir.group(1),
                                                     mp_sensor_dir.group(2),
                                                     r'frequencies.bin')
        except:
            print("[Warning] Mulipoint Sensor data file missing")
            print("MPSensor name: " , self._mp_sensor_name)
            raise

            self._mp_freq = XFMultiPointFrequencies(self._mp_frequencies_file)
            self._mp_geom_file = os.path.join(mp_sensor_dir.group(1),
                                              mp_sensor_dir.group(2),
                                              r'geom.bin')

            
    def _get_mp_field_types(self):
        """
        Determine which data directories should be present from info flags.
        """
        time_domain_scattered_e = 1<<31
        time_domain_total_e = 1<<30
        time_domain_scattered_h = 1<<29
        time_domain_total_h = 1<<28
        time_domain_scattered_b = 1<<27
        time_domain_total_b = 1<<26
        time_domain_j = 1<<25
        discrete_frequency_total_e = 1<<24
        discrete_frequency_total_h = 1<<23
        discrete_frequency_j = 1<<22
        discrete_frequency_total_b = 1<<21
        discrete_frequency_dissipated_power_density = 1<<20

        mask = self._mp_ss_info.fields_mask

        if mask & time_domain_scattered_e:
            self._mp_field_types.append(r'tr_Exs')
            self._mp_field_types.append(r'tr_Eys')
            self._mp_field_types.append(r'tr_Ezs')
        if mask & time_domain_total_e:
            self._mp_field_types.append(r'tr_Ext')
            self._mp_field_types.append(r'tr_Eyt')
            self._mp_field_types.append(r'tr_Ezt')
        if mask & time_domain_scattered_h:
            self._mp_field_types.append(r'tr_Hxs')
            self._mp_field_types.append(r'tr_Hys')
            self._mp_field_types.append(r'tr_Hzs')
        if mask & time_domain_total_h:
            self._mp_field_types.append(r'tr_Hxt')
            self._mp_field_types.append(r'tr_Hyt')
            self._mp_field_types.append(r'tr_Hzt')
        if mask & time_domain_scattered_b:
            self._mp_field_types.append(r'tr_Bxs')
            self._mp_field_types.append(r'tr_Bys')
            self._mp_field_types.append(r'tr_Bzs')
        if mask & time_domain_total_b:
            self._mp_field_types.append(r'tr_Bxt')
            self._mp_field_types.append(r'tr_Byt')
            self._mp_field_types.append(r'tr_Bzt')
        if mask & time_domain_j:
            self._mp_field_types.append(r'tr_Jx')
            self._mp_field_types.append(r'tr_Jy')
            self._mp_field_types.append(r'tr_Jz')
        if mask & discrete_frequency_total_e:
            self._mp_field_types.append(r'ss_Exit')
            self._mp_field_types.append(r'ss_Exrt')
            self._mp_field_types.append(r'ss_Eyit')
            self._mp_field_types.append(r'ss_Eyrt')
            self._mp_field_types.append(r'ss_Ezit')
            self._mp_field_types.append(r'ss_Ezrt')
        if mask & discrete_frequency_total_h:
            self._mp_field_types.append(r'ss_Hxit')
            self._mp_field_types.append(r'ss_Hxrt')
            self._mp_field_types.append(r'ss_Hyit')
            self._mp_field_types.append(r'ss_Hyrt')
            self._mp_field_types.append(r'ss_Hzit')
            self._mp_field_types.append(r'ss_Hzrt')
        if mask & discrete_frequency_j:
            self._mp_field_types.append(r'ss_Jxi')
            self._mp_field_types.append(r'ss_Jxr')
            self._mp_field_types.append(r'ss_Jyi')
            self._mp_field_types.append(r'ss_Jyr')
            self._mp_field_types.append(r'ss_Jzi')
            self._mp_field_types.append(r'ss_Jzr')
        if mask & discrete_frequency_total_b:
            self._mp_field_types.append(r'ss_Bxit')
            self._mp_field_types.append(r'ss_Bxrt')
            self._mp_field_types.append(r'ss_Byit')
            self._mp_field_types.append(r'ss_Byrt')
            self._mp_field_types.append(r'ss_Bzit')
            self._mp_field_types.append(r'ss_Bzrt')
        if mask & discrete_frequency_dissipated_power_density:
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
            print(r"Could not find geometry file: " + self._mp_geom_file)

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

    def _ss_pdd_dir_name(self, field_type, component):
        """
        Construct the filename for the dissipated power for
        field type, component.
        """
        return r'ss_P' + field_type + component

    def _ss_field_dir_name(self, field_type, field_component, complex_type):
        """
        Construct the filename for field value:
        field_type: 'E', 'H', 'B', 'J', 'P'
        field_component: 'x', 'y', 'z'
        complex_type:  'real' ('r') or 'imaginary' ('i')
        """
        ff_appendix = ''

        if field_type not in self._valid_types:
            print("Invalid field type: ", field_type)
        if field_component not in self._valid_components:
            print("Invalid field component: ", field_type)
        if not (complex_type == 'i' or complex_type == 'r'):
            print("Invalid field complex type: ", complex_type)

        if (field_type == 'E') or (field_type == 'H') or (field_type == 'B'):
            ff_appendix = 't'

        field_file_subdir = r'ss_' + field_type + field_component + \
                            complex_type + ff_appendix

        return field_file_subdir

    def ss_field_data(self, data_type, component):
        """Return the field or dissipated power values."""
        (path_head, path_tail) = os.path.split(self._mp_ss_info_file[0])
        path_tail = ''.join(path_tail.split('_info.bin'))
        mp_ss_dir = os.path.join(path_head, path_tail)

        # Traditional field type
        if data_type in self._valid_types:
            field_dir_real = self._ss_field_dir_name(data_type,
                                                     component, r'r')
            field_dir_imag = self._ss_field_dir_name(data_type,
                                                     component, r'i')


            file_name_real = os.path.join(mp_ss_dir, field_dir_real, r'0.bin')
            file_name_imag = os.path.join(mp_ss_dir, field_dir_imag, r'0.bin')
            print("Loading field data from: ", file_name_real)
            mp_ss_field_real = XFMultiPointSSField(file_name_real,
                                                   self._mp_ss_info,
                                                   self._mp_geom)
            print("Loading field data from: ", file_name_imag)
            mp_ss_field_imag = XFMultiPointSSField(file_name_imag,
                                                   self._mp_ss_info,
                                                   self._mp_geom)
            self._ss_field_data = mp_ss_field_real.ss_field + \
                                  1j * mp_ss_field_imag.ss_field

        # Dissipated power
        elif data_type == 'P':
            power_dir = self._ss_pdd_dir_name(data_type, component)
            file_name = os.path.join(mp_ss_dir, power_dir, r'0.bin')
            print("Loading dissipated power data from: ", file_name)
            mp_ss_dissipated_power_data = XFMultiPointSSField(file_name,
                                                              self._mp_ss_info,
                                                              self._mp_geom)
            self._ss_field_data = mp_ss_dissipated_power_data.ss_field

        else:
            print(r'Invalid data_type: ', data_type)


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
    def run_id(self):
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
