"""
Vopgen property map exporter.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from xfutils import xf_regrid_3d_nearest as regrid3d
from xfgeomod import XFMesh, XFGeometry, XFGridExporter
from xfwriter import XFMatWriterUniform, XFGridDataWriterUniform
from xfwriter.vopgen.sarmask import VopgenSarMask

class VopgenPropertyMap(XFMatWriterUniform):
    """Matlab writer for 4-D conductivity and mass density maps."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._xf_project_dir = xf_project_dir
        self._sim_id = sim_id
        self._run_id = run_id
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
        self._mass_density_map = None
        self._conductivity_map = None
        geom = XFGeometry(xf_project_dir, sim_id, run_id)
        mesh = XFMesh(xf_project_dir, sim_id, run_id)
        self._grid_exporter = XFGridExporter(geom, mesh)
        self._mask = None
        
    def _make_mask(self):
        """Create mask to return only tissue values."""
        vopgen_sar_mask = VopgenSarMask(self._xf_project_dir,
                                        self._sim_id, self._run_id)
        vopgen_sar_mask.set_grid_origin(self._x0, self._y0, self._z0)
        vopgen_sar_mask.set_grid_len(self._xlen, self._ylen, self._zlen)
        vopgen_sar_mask.set_grid_resolution(self._dx, self._dy, self._dz)
        self._mask = vopgen_sar_mask.make_sar_mask()
        
        
    def make_mass_density_map(self):
        """
        Construct the mass density map with dimensions [xdim, ydim, zdim, 3]
        """
        self._update_export_grid()
        self._mass_density_map = np.empty([len(self._xdim_uniform), 
                                           len(self._ydim_uniform),
                                           len(self._zdim_uniform), 3],
                                          dtype = np.dtype(np.double))

        # Mass density components on Ex grid locations,
        # resampled on uniform grid
        self._mass_density_map[:,:,:,0] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ex_density)
        
        # Mass density components on Ey grid locations,
        # resampled on uniform grid
        self._mass_density_map[:,:,:,1] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ey_density)

        # Mass density components on Ez grid locations,
        # resampled on uniform grid
        self._mass_density_map[:,:,:,2] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ez_density)

        # apply mask
        if self._mask is None:
            self._make_mask()        
        self._mass_density_map[:,:,:,0] = np.multiply(self._mass_density_map[:,:,:,0], self._mask)
        self._mass_density_map[:,:,:,1] = np.multiply(self._mass_density_map[:,:,:,1], self._mask)
        self._mass_density_map[:,:,:,2] = np.multiply(self._mass_density_map[:,:,:,2], self._mask)
        
        return self._mass_density_map

    def make_conductivity_map(self):
        """Construct the conductivity map."""
        self._update_export_grid()

        if self._mask is None:
            self._make_mask()

        self._conductivity_map = np.empty([len(self._xdim_uniform),
                                           len(self._ydim_uniform),
                                           len(self._zdim_uniform), 3],
                                          dtype = np.dtype(np.double))

        # Conductivity component on Ex grid locations,
        # resampled on uniform grid
        self._conductivity_map[:,:,:,0] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ex_sigma)

        # Conductivity component on Ex grid locations,
        # resampled on uniform grid
        self._conductivity_map[:,:,:,1] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ey_sigma)
        
        # Conductivity component on Ex grid locations,
        # resampled on uniform grid
        self._conductivity_map[:,:,:,2] = regrid3d((self._grid_exporter.grid_x,
                                                    self._grid_exporter.grid_y,
                                                    self._grid_exporter.grid_z),
                                                   (self._xdim_uniform,
                                                    self._ydim_uniform,
                                                    self._zdim_uniform),
                                                   self._grid_exporter.ez_sigma)
        if self._mask is None:
            self._make_mask()
        self._conductivity_map[:,:,:,0] = np.multiply(self._conductivity_map[:,:,:,0], self._mask)
        self._conductivity_map[:,:,:,1] = np.multiply(self._conductivity_map[:,:,:,1], self._mask)
        self._conductivity_map[:,:,:,2] = np.multiply(self._conductivity_map[:,:,:,2], self._mask)

        return self._conductivity_map

    def savemat(self, file_name):
        """Save the property map data to matlab file."""
        self._update_export_grid()
        self.make_mass_density_map()
        self.make_conductivity_map()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['condMap'] = self._conductivity_map
        export_dict['mdenMap'] = self._mass_density_map
        spio.savemat(file_name, export_dict, oned_as = 'column')
