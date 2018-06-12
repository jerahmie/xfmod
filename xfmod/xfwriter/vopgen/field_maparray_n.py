"""
Vopgen data exporter class for 5-D E-Field data.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from xfsystem import XFSystem
from xfwriter import XFFieldWriterUniform

class VopgenFieldMapArrayN(XFFieldWriterUniform):
    """Matlab writer base class for 5-D Field data."""

    def _get_net_input_power_per_coil(self):
        """Return array of net input powers, one per coil in simulation."""
        self._net_input_power_per_coil = np.empty(self._num_coils,
                                                  dtype=np.dtype(np.float64))
        for idx, coil_index in enumerate(self._sim_ids):
            sim_system = XFSystem(self._xf_project_dir, coil_index, 1)
            self._net_input_power_per_coil[idx] = sim_system.net_input_power


    def _update_export_grid(self):
        """Updates xdim, ydim, zdim dimensions."""
        self._xdim_uniform = np.arange(self._x0 - self._xlen/2.0,
                                       self._x0 + self._xlen/2.0,
                                       self._dx)
        self._ydim_uniform = np.arange(self._y0 - self._ylen/2.0,
                                       self._y0 + self._ylen/2.0,
                                       self._dy)
        self._zdim_uniform = np.arange(self._z0 - self._zlen/2.0,
                                       self._z0 + self._zlen/2.0,
                                       self._dz)

    def _field_map_array_n(self):
        """Populate field map array for N channels."""
        self._update_export_grid()
        self._f_map_array_n = np.empty([len(self._xdim_uniform),
                                            len(self._ydim_uniform),
                                            len(self._zdim_uniform),
                                            3, self._num_coils],
                                           dtype=np.dtype(np.complex_))
        for coil_index, sim_id in enumerate(self._sim_ids):
            print("SimID: ", sim_id, "/", self._sim_ids)
            field_uniform_wr = XFFieldWriterUniform(self._xf_project_dir,
                                                    sim_id, 1)
            field_uniform_wr.set_grid_origin(self._x0, self._y0, self._z0)
            field_uniform_wr.set_grid_len(self._xlen, self._ylen, self._zlen)
            field_uniform_wr.set_grid_resolution(self._dx, self._dy, self._dz)
            field_uniform_wr.net_input_power = 1.0
            self._field_norm_n.append(field_uniform_wr.field_norm)
            [field_x, field_y, field_z] = field_uniform_wr._regrid_fields(self._field_type_str)
            self._f_map_array_n[:,:,:,0,coil_index] = field_x
            self._f_map_array_n[:,:,:,1,coil_index] = field_y
            self._f_map_array_n[:,:,:,2,coil_index] = field_z

class VopgenEFMapArrayN(VopgenFieldMapArrayN):
    """Matlab writer for 5-D E-Field data."""
    def __init__(self, xf_project_dir, sim_ids):
        self._xf_project_dir = xf_project_dir
        self._sim_ids = sim_ids
        self._num_coils = len(sim_ids)
        self._f_map_array_n = None
        self._field_type_str = 'E'
        self._xdim_uniform = None
        self._ydim_uniform = None
        self._zdim_uniform = None
        self._net_input_power_per_coil = None
        self._dx = 0.0
        self._dy = 0.0
        self._dz = 0.0
        self._x0 = 0.0
        self._y0 = 0.0
        self._z0 = 0.0
        self._xlen = 0.0
        self._ylen = 0.0
        self._zlen = 0.0
        self._get_net_input_power_per_coil()
        self._field_norm_n = []

    def savemat(self, file_name):
        """Save the E-field data in format expected by vopgen."""
        self._field_map_array_n()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['efMapArrayN'] = self._f_map_array_n
        spio.savemat(file_name, export_dict, oned_as='column')
        print("Saved efield map array with field normalizations: " + \
              str(self._field_norm_n))


class VopgenBFMapArrayN(VopgenFieldMapArrayN):
    """Matlab writer for 5-D E-Field data."""
    def __init__(self, xf_project_dir, sim_ids):
        self._xf_project_dir = xf_project_dir
        self._sim_ids = sim_ids
        self._num_coils = len(sim_ids)
        self._f_map_array_n = None
        self._field_type_str = 'B'
        self._xdim_uniform = None
        self._ydim_uniform = None
        self._zdim_uniform = None
        self._net_input_power_per_coil = None
        self._dx = 0.0
        self._dy = 0.0
        self._dz = 0.0
        self._x0 = 0.0
        self._y0 = 0.0
        self._z0 = 0.0
        self._xlen = 0.0
        self._ylen = 0.0
        self._zlen = 0.0
        self._get_net_input_power_per_coil()
        self._field_norm_n = []

    def _rotating_field_map_array_n(self):
        """Populate B1 rotating field map array for N channels."""
        self._update_export_grid()
        self._f_map_array_n = np.empty([len(self._xdim_uniform),
                                        len(self._ydim_uniform),
                                        len(self._zdim_uniform),
                                        2, self._num_coils],
                                       dtype=np.dtype(np.complex_))
        for coil_index, sim_id in enumerate(self._sim_ids):
            print("SimID: ", sim_id, "/", self._sim_ids)
            field_uniform_wr = XFFieldWriterUniform(self._xf_project_dir,
                                                    sim_id, 1)
            field_uniform_wr.set_grid_origin(self._x0, self._y0, self._z0)
            field_uniform_wr.set_grid_len(self._xlen, self._ylen, self._zlen)
            field_uniform_wr.set_grid_resolution(self._dx, self._dy, self._dz)
            field_uniform_wr.net_input_power = 1.0
            self._field_norm_n.append(field_uniform_wr.field_norm)
            [field_x, field_y, field_z] = field_uniform_wr._regrid_fields(self._field_type_str)
            self._f_map_array_n[:,:,:,0,coil_index] = 0.5*(field_x + 1j*field_y)
            self._f_map_array_n[:,:,:,1,coil_index] = 0.5*(np.conj(field_x) 
                                                           + 1j*np.conj(field_y))

    def savemat(self, file_name):
        """Save the B-field data in format expected by vopgen."""
        self._rotating_field_map_array_n()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['bfMapArrayN'] = self._f_map_array_n
        spio.savemat(file_name, export_dict, oned_as='column')
        print("Saved efield map array with field normalizations: " + \
              str(self._field_norm_n))
