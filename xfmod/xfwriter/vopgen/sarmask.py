"""
Matrix bitmap that masks SAR calculation region.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from xfutils import xf_regrid_3d_nearest
from xfgeomod import XFMesh, XFGeometry, XFGridExporter
from xfwriter import XFMatWriterUniform
from xfwriter.vopgen.removeNaNs import removeNaNs

# threshold for scaling/rounding to ensure tissue only if ex, ey, and ez grid
# values are tissue.
#TISSUE_THRESHOLD = 0.2  

class VopgenSarMask(XFMatWriterUniform):
    """Matlab writer for 3-D SAR bitmap mask."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._xdim_uniform = None
        self._ydim_uniform = None
        self._zdim_uniform = None
        self._dx = 0.0
        self._dy = 0.0
        self._dz = 0.0
        self._xlen = 0.0
        self._ylen = 0.0
        self._zlen = 0.0
        self._x0 = 0.0
        self._y0 = 0.0
        self._z0 = 0.0
        self._sar_mask = None
        self._tissue_mask = None
        geom = XFGeometry(xf_project_dir, sim_id, run_id)
        mesh = XFMesh(xf_project_dir, sim_id, run_id)
        self._grid_exporter = XFGridExporter(geom, mesh)
        
    def make_tissue_mask(self):
        """Construct a mask from tissue properties on uniformly spaced grid."""
        self._update_export_grid()
        self._tissue_mask = np.empty((len(self._xdim_uniform),
                                      len(self._ydim_uniform),
                                      len(self._zdim_uniform)),
                                     dtype = np.dtype(int))
        tissue_mask_ex = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim_uniform,
                                               self._ydim_uniform,
                                               self._zdim_uniform),
                                              self._grid_exporter.ex_tissue)
        tissue_mask_ey = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim_uniform,
                                               self._ydim_uniform,
                                               self._zdim_uniform),
                                              self._grid_exporter.ey_tissue)
        tissue_mask_ez = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim_uniform,
                                               self._ydim_uniform,
                                               self._zdim_uniform),
                                           self._grid_exporter.ez_tissue)
        self._tissue_mask = np.zeros((len(self._xdim_uniform),
                                      len(self._ydim_uniform),
                                      len(self._zdim_uniform)),
                                     dtype = np.int )
        self._tissue_mask[np.where((tissue_mask_ex + tissue_mask_ey + tissue_mask_ez) > 0.0)] = 1
        
        return self._tissue_mask

    def make_sar_mask(self):
        """Construct a SAR mask using the vopgen method."""
        self._update_export_grid()

        # Material Conducivity on resampled Ex, Ey, Ez grid
        sigma_ex_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim_uniform,
                                                 self._ydim_uniform,
                                                 self._zdim_uniform),
                                                self._grid_exporter.ex_sigma)
        sigma_ey_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim_uniform,
                                                 self._ydim_uniform,
                                                 self._zdim_uniform),
                                                self._grid_exporter.ey_sigma)
        sigma_ez_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim_uniform,
                                                 self._ydim_uniform,
                                                 self._zdim_uniform),
                                                self._grid_exporter.ez_sigma)

        # Material Density on resampled Ex, Ey, Ez grid
        density_ex_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim_uniform,
                                                   self._ydim_uniform,
                                                   self._zdim_uniform),
                                                  self._grid_exporter.ex_density)
        density_ey_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim_uniform,
                                                   self._ydim_uniform,
                                                   self._zdim_uniform),
                                                  self._grid_exporter.ey_density)
        density_ez_uniform = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim_uniform,
                                                   self._ydim_uniform,
                                                   self._zdim_uniform),
                                                  self._grid_exporter.ez_density)
        cod_x = np.greater(removeNaNs(0.5 * np.divide(sigma_ex_uniform, density_ex_uniform)), 0.0)
        
        cod_y = np.greater(removeNaNs(0.5 * np.divide(sigma_ey_uniform, density_ey_uniform)), 0.0)
        cod_z = np.greater(removeNaNs(0.5 * np.divide(sigma_ez_uniform, density_ez_uniform)), 0.0)
        self._sar_mask = np.logical_or(cod_x, cod_y, cod_z)
        self._sar_mask = 1 * np.logical_or(self._sar_mask, cod_z)  # cast to int array

        return self._sar_mask
    
    def savemat(self, file_name):
        """Save the SAR mask to a matlab file."""
        self.make_sar_mask()
        self.make_tissue_mask()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['sarmask_new'] = self._sar_mask
        export_dict['sar_tissue_mask'] = self._tissue_mask
        spio.savemat(file_name, export_dict, oned_as = 'column')

