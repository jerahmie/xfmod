"""
Tissue material density map, and tissue material map with SAR mask applied.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from  xfutils import xf_regrid_3d_nearest
from xfgeomod import XFMesh, XFGeometry, XFGridExporter
from xfwriter import XFMatWriterUniform
from xfwriter.vopgen import VopgenSarMask, VopgenPropertyMap
from xfwriter.vopgen.removeNaNs import removeNaNs

class VopgenMassDensityMap3D(XFMatWriterUniform):
    """Matlab writer for 3D mass density maps."""
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
        self._mass_density_3d = None
        self._mass_density_3d_mask = None
        self._mass_density_3d_tissue_mask = None
        self._prop_map = VopgenPropertyMap(xf_project_dir, sim_id, run_id)
        self._sar_mask = VopgenSarMask(xf_project_dir, sim_id, run_id)
        

    def _make_mass_density_map_3d(self):
        """
        Construct mass density map and masked mass density map on 3d grid.
        """
        self._update_export_grid()
        self._prop_map.set_grid_origin(self._x0, self._y0, self._z0)
        self._prop_map.set_grid_len(self._xlen, self._ylen, self._zlen)
        self._prop_map.set_grid_resolution(self._dx, self._dy, self._dz)
        self._sar_mask.set_grid_origin(self._x0, self._y0, self._z0)
        self._sar_mask.set_grid_len(self._xlen, self._ylen, self._zlen)
        self._sar_mask.set_grid_resolution(self._dx, self._dy, self._dz)
        sar_mask_3d = self._sar_mask.make_sar_mask()
        sar_tissue_mask_3d = self._sar_mask.make_tissue_mask()
        mass_density_map = removeNaNs(self._prop_map.make_mass_density_map())
        self._mass_density_3d = (mass_density_map[:, :, :, 0] + \
                                 mass_density_map[:, :, :, 1] + \
                                 mass_density_map[:, :, :, 2]) / 3.0
        self._mass_density_3d_mask = np.multiply(self._mass_density_3d,
                                                 sar_mask_3d.astype(np.float))
        self._mass_density_3d_tissue_mask  = np.multiply(self._mass_density_3d,
                                                         sar_tissue_mask_3d.astype(np.float))

    def savemat(self, file_name):
        """Save the mass density map data to a matlab file."""
        self._make_mass_density_map_3d()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['mden3D'] = self._mass_density_3d
        export_dict['mden3Dm'] = self._mass_density_3d_mask
        export_dict['mden3Dm_tissue'] = self._mass_density_3d_tissue_mask
        spio.savemat(file_name, export_dict, oned_as = 'column')
