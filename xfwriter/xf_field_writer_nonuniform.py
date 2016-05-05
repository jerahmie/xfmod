"""
Write field data on XFdtd nonuniform grid to Mat file.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import numpy as np
import scipy.io as spio
import xfwriter
from xfsystem import XFSystem
from xfmatgrid import XFFieldNonUniformGrid

class XFFieldWriterNonUniform(xfwriter.XFMatWriter):
    """Field writer for XFdtd field data on nonuniform computational grid."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._field_nonuniform_grid = XFFieldNonUniformGrid(xf_project_dir,
                                                            sim_id,
                                                            run_id)
        self._xf_sys = XFSystem(xf_project_dir, sim_id, run_id)
        self._net_input_power = self._xf_sys.net_input_power
        self._fx_original = None
        self._fy_original = None
        self._fz_original = None
        self._fx_scaled = None
        self._fy_scaled = None
        self._fz_scaled = None
        self._xdim = None
        self._ydim = None
        self._zdim = None

    def _scale_fields(self):
        """Rescale fields to match power level."""
        self._fx_scaled = self._fx_original * \
                          np.sqrt(self._net_input_power) / \
                          np.sqrt(self._xf_sys.net_input_power)
        self._fy_scaled = self._fy_original * \
                          np.sqrt(self._net_input_power)/ \
                          np.sqrt(self._xf_sys.net_input_power)
        self._fz_scaled = self._fz_original * \
                          np.sqrt(self._net_input_power) / \
                          np.sqrt(self._xf_sys.net_input_power)

    def _load_fields(self, field_type):
        """Extract fields from XFdtd data structures."""
        self._xdim = self._field_nonuniform_grid.xdim
        self._ydim = self._field_nonuniform_grid.ydim
        self._zdim = self._field_nonuniform_grid.zdim
        self._fx_original = self._field_nonuniform_grid.ss_field_data(field_type, 'x')
        self._fy_original = self._field_nonuniform_grid.ss_field_data(field_type, 'y')
        self._fz_original = self._field_nonuniform_grid.ss_field_data(field_type, 'z')
        self._scale_fields()

    def savemat(self, field_type, file_name):
        """Export the field data to matlab file."""
        self._load_fields(field_type)
        export_dict = dict()
        export_dict['XDim'] = self._xdim
        export_dict['YDim'] = self._ydim
        export_dict['ZDim'] = self._zdim
        export_dict[field_type + 'x'] = self._fx_scaled
        export_dict[field_type + 'y'] = self._fy_scaled
        export_dict[field_type + 'z'] = self._fz_scaled
        spio.savemat(file_name, export_dict, oned_as='column')
