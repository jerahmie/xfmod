"""
Vopgen property map exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from xfutils import xf_regrid_3d_nearest
from xfgeomod import XFMesh, XFGeometry, XFGridExporter
from xfwriter import XFMatWriter, XFGridDataWriterUniform

class VopgenPropertyMap(XFMatWriter):
    """Matlab writer for 4-D conductivity and mass density maps."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._xdim_uniform = None
        self._ydim_uniform = None
        self._zdim_uniform = None
        self._dx = 0.0
        self._dy = 0.0
        self._dz = 0.0
        self._x0 = 0.0
        self._y0 = 0.0
        self._z0 = 0.0
        self._xlen = 0.0
        self._ylen = 0.0
        self._zlen = 0.0
        self._sigma_map = None
        self._rho_map = None
        geom = XFGeometry(xf_project_dir, sim_id, run_id)
        mesh = XFMesh(xf_project_dir, sim_id, run_id)
        self._grid_exporter = XFGridExporter(geom, mesh)
        
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
    def _mass_density_map(self):
        """Construct the mass density map: [xdim, ydim, zdim, 3]"""
        self._rho_map = np.empty([len(self._xdim_uniform), 
                                  len(self._ydim_uniform),
                                  len(self._zdim_uniform), 3],
                                 dtype = np.dtype(np.double))

        # Mass density components on Ex grid locations, resampled on uniform grid
        self._rho_map[:,:,:,0] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim_uniform,
                                                       self._ydim_uniform,
                                                       self._zdim_uniform),
                                                      self._grid_exporter.ex_density)

        # Mass density components on Ey grid locations, resampled on uniform grid
        self._rho_map[:,:,:,1] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim_uniform,
                                                       self._ydim_uniform,
                                                       self._zdim_uniform),
                                                      self._grid_exporter.ey_density)

        # Mass density components on Ez grid locations, resampled on uniform grid
        self._rho_map[:,:,:,2] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim_uniform,
                                                       self._ydim_uniform,
                                                       self._zdim_uniform),
                                                      self._grid_exporter.ez_density)
        

    def _conductivity_map(self):
        """Construct the conductivity map."""
        self._sigma_map = np.empty([len(self._xdim_uniform),
                                    len(self._ydim_uniform),
                                    len(self._zdim_uniform), 3],
                                   dtype = np.dtype(np.double))

        # Conductivity component on Ex grid locations, resampled on uniform grid
        self._sigma_map[:,:,:,0] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim_uniform,
                                                         self._ydim_uniform,
                                                         self._zdim_uniform),
                                                        self._grid_exporter.ex_sigma)

        # Conductivity component on Ex grid locations, resampled on uniform grid
        self._sigma_map[:,:,:,1] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim_uniform,
                                                         self._ydim_uniform,
                                                         self._zdim_uniform),
                                                        self._grid_exporter.ey_sigma)
        
        # Conductivity component on Ex grid locations, resampled on uniform grid
        self._sigma_map[:,:,:,2] = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim_uniform,
                                                         self._ydim_uniform,
                                                         self._zdim_uniform),
                                                        self._grid_exporter.ez_sigma)

    def savemat(self, file_name):
        """Save the property map data to matlab file."""
        self._update_export_grid()
        self._mass_density_map()
        self._conductivity_map()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['condMap'] = self._sigma_map
        export_dict['mdenMap'] = self._rho_map
        spio.savemat(file_name, export_dict, oned_as='column')
