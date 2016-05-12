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
        geom = XFGeometry(xf_project_dir, sim_id, run_id)
        mesh = XFMesh(xf_project_dir, sim_id, run_id)
        self._grid_exporter = XFGridExporter(geom, mesh)
        
    def _make_sar_mask(self):
        """Construct the sar mask on uniformly spaced grid."""
        pass

    def savemat(self, file_name):
        self._update_export_grid()
        self._make_sar_mask()
        export_dict = dict()
        export_dict['XDim'] = self._xdim_uniform
        export_dict['YDim'] = self._ydim_uniform
        export_dict['ZDim'] = self._zdim_uniform
        export_dict['sarmask_new'] = self._sar_mask
        spio.savemat(file_name, export_dict, oned_as = 'column')
