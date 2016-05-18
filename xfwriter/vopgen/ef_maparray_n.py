"""
Vopgen data exporter class for 5-D E-Field data.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from xfsystem import XFSystem
from xfwriter import XFMatWriter, XFFieldWriterUniform

class VopgenEFMapArrayN(XFMatWriter):
    """Matlab writer for 5-D E-Field data."""
    def __init__(self, xf_project_dir, sim_ids):
        self._xf_project_dir = xf_project_dir
        self._sim_ids = sim_ids
        self._num_coils = len(sim_ids)
        self._ef_map_array_n = None
        self._ex = None
        self._ey = None
        self._ez = None
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

    def _efield_map_array_n(self):
        """Populate E field map array for N coils."""
        self._update_export_grid()
        self._ef_map_array_n = np.empty([len(self._xdim_uniform),
                                         len(self._ydim_uniform),
                                         len(self._zdim_uniform),
                                         3, self._num_coils],
                                        dtype=np.dtype(np.complex_))
        for coil_index, sim_id in enumerate(self._sim_ids):
            print("SimID: ", sim_id, "/", self._sim_ids)
            efield_uniform_wr = XFFieldWriterUniform(self._xf_project_dir,
                                                     sim_id, 1)
            efield_uniform_wr.set_origin(self._x0, self._y0, self._z0)
            efield_uniform_wr.set_len(self._xlen, self._ylen, self._zlen)
            efield_uniform_wr.set_grid_resolution(self._dx, self._dy, self._dz)
            [Ex, Ey, Ez] = efield_uniform_wr.regrid_fields('E')
            self._ef_map_array_n[:, :, :, 0, coil_index] = Ex
            self._ef_map_array_n[:, :, :, 1, coil_index] = Ey
            self._ef_map_array_n[:, :, :, 2, coil_index] = Ez

    def set_grid_origin(self, x0, y0, z0):
        """Set the origin of the export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def set_grid_len(self, xlen, ylen, zlen):
        """Set the dimension of the export region."""
        self._xlen = xlen
        self._ylen = ylen
        self._zlen = zlen

    def set_grid_resolution(self, dx, dy, dz):
        """Set the grid step size of the uniformly interpolated grid."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def savemat(self, file_name):
        """Save the field data in format expected by vopgen."""
        self._efield_map_array_n()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['efMapArrayN'] = self._ef_map_array_n
        spio.savemat(file_name, export_dict, oned_as='column')
