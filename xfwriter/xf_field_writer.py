"""
Write field data on XFdtd nonuniform grid to Mat file.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import abc
from math import sqrt
import numpy as np
import scipy.io as spio
from xfwriter import XFMatWriter
from xfsystem import XFSystem
from xfmatgrid import XFFieldNonUniformGrid

class XFFieldError(Exception):
    """
    XFdtd Field Error
    """
    def __init__(self, message):
        self.message = "[XFFieldError] " + str(message)

class XFFieldWriter(XFMatWriter):
    """Base class for writing xf field data to mat file."""
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self._fx = None
        self._fy = None
        self._fz = None
        self._fx_original = None
        self._fy_original = None
        self._fz_original = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._field_norm = None
        self._field_nonuniform_grid = None
        self._xf_sys = None

    @property
    def xdim(self):
        """Return x grid values."""
        return self._xdim

    @property
    def ydim(self):
        """Return y grid values."""
        return self._ydim

    @property
    def zdim(self):
        """Return z grid values."""
        return self._zdim

    def scale_b1_at_point(self, b1_mag, b1_point):
        """
        Set scale factor such b1 is normalized to b1_mag at b1_point.
        """
        if len(b1_point) != 3:
            raise XFFieldError("Scaling positions must be [x,y,z]")

        x_ind = np.argmin(abs(self._field_nonuniform_grid.xdim - b1_point[0]))
        if (x_ind == 0) or \
           (x_ind == (len(self._field_nonuniform_grid.xdim) - 1)):
            raise XFFieldError("Scaling by B1 outside of computational domain.")
        y_ind = np.argmin(abs(self._field_nonuniform_grid.ydim - b1_point[1]))
        if (y_ind == 0) or \
           (y_ind == (len(self._field_nonuniform_grid.ydim) - 1)):
            raise XFFieldError("Scaling by B1 outside of computational domain.")
        z_ind = np.argmin(abs(self._field_nonuniform_grid.zdim - b1_point[2]))
        if (z_ind == 0) or \
           (z_ind == (len(self._field_nonuniform_grid.zdim) - 1)):
            raise XFFieldError("Scaling by B1 outside of computational domain.")

        b1x = self._field_nonuniform_grid.ss_field_data('B', 'x')[x_ind,
                                                                  y_ind,
                                                                  z_ind]
        b1y = self._field_nonuniform_grid.ss_field_data('B', 'y')[x_ind,
                                                                  y_ind,
                                                                  z_ind]
        b1z = self._field_nonuniform_grid.ss_field_data('B', 'z')[x_ind,
                                                                  y_ind,
                                                                  z_ind]
        self._field_norm = b1_mag/sqrt(abs(b1x*b1x.conjugate()) +
                                       abs(b1y*b1y.conjugate()) +
                                       abs(b1z*b1z.conjugate()))
    @property
    def field_norm(self):
        """Returns the field scale factor."""
        return self._field_norm

    @property
    def net_input_power(self):
        """Desired net input power."""
        return self._field_norm**2 * self._xf_sys.net_input_power

    @net_input_power.setter
    def net_input_power(self, power):
        """Set field normalization based on coil element net input power."""
        try:
            self._field_norm = sqrt(power/self._xf_sys.net_input_power)
        except ZeroDivisionError:
            self._field_norm = 1.0
            print("Net input power is zero.  Check simulation setup.")
            raise

    def _scale_fields(self):
        """Rescale fields."""
        self._fx = self._fx_original * self._field_norm
        self._fy = self._fy_original * self._field_norm
        self._fz = self._fz_original * self._field_norm

    def _load_fields(self, field_type):
        """Extract fields from XFdtd data structures."""
        self._xdim = self._field_nonuniform_grid.xdim
        self._ydim = self._field_nonuniform_grid.ydim
        self._zdim = self._field_nonuniform_grid.zdim
        self._fx_original = self._field_nonuniform_grid.ss_field_data(field_type, 'x')
        self._fy_original = self._field_nonuniform_grid.ss_field_data(field_type, 'y')
        self._fz_original = self._field_nonuniform_grid.ss_field_data(field_type, 'z')
        self._scale_fields()

class XFFieldWriterNonUniform(XFFieldWriter):
    """Field writer for XFdtd field data on nonuniform computational grid."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._field_nonuniform_grid = XFFieldNonUniformGrid(xf_project_dir,
                                                            sim_id,
                                                            run_id)
        self._xf_sys = XFSystem(xf_project_dir, sim_id, run_id)
        self._fx_original = None
        self._fy_original = None
        self._fz_original = None
        self._fx = None
        self._fy = None
        self._fz = None
        self._field_norm = 1.0
        self._xdim = None
        self._ydim = None
        self._zdim = None

    def savemat(self, field_type, file_name):
        """Export the field data to matlab file."""
        self._load_fields(field_type)
        print("Exporting field data to mat file.")
        export_dict = dict()
        export_dict['XDim'] = self._xdim
        export_dict['YDim'] = self._ydim
        export_dict['ZDim'] = self._zdim
        export_dict[field_type + 'x'] = self._fx
        export_dict[field_type + 'y'] = self._fy
        export_dict[field_type + 'z'] = self._fz
        spio.savemat(file_name, export_dict, oned_as='column')
