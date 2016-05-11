#!/usr/bin/env python3
"""
Re-grid steady-state XFdtd field data and export in matfile format.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import os
import sys
import ast
import getopt
from math import sqrt
import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
import xfsystem
from xfmatgrid import XFFieldNonUniformGrid
from xfutils import xf_regrid_3d_nearest

class XFFieldWriterUniform(object):
    """Writes XFdtd field data to mat file on uniform grid. """
    def __init__(self, xf_project_dir, sim_id, run_id):
        self.field_nonuniform_grid = XFFieldNonUniformGrid(xf_project_dir,
                                                           sim_id,
                                                           run_id)
        self._xf_system = xfsystem.XFSystem(xf_project_dir, sim_id, run_id)
        self.field_uniform_grid = None
        self._fx = None
        self._fy = None
        self._fz = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._x0 = 0.0
        self._y0 = 0.0
        self._z0 = 0.0
        self._xlen = 0.0
        self._ylen = 0.0
        self._zlen = 0.0
        self._dx = 0.0
        self._dy = 0.0
        self._dz = 0.0
        self._net_input_power = 1.0

    def set_origin(self, x0, y0, z0):
        """Set origin of export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def set_len(self, xlen, ylen, zlen):
        """Set the dimension of the export region."""
        self._xlen = xlen
        self._ylen = ylen
        self._zlen = zlen

    def set_grid_resolution(self, dx, dy, dz):
        """Sets the grid step size of the uniformly interpolated grid size."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def regrid_fields(self, field_type):
        """
        Resample field data on uniform grid.

        Args :
        X0 (list): The lower corner [x0, y0, z0] (mm) of the region to regrid.
        XLen (list): Dimensions of regrid region [xLen, yLen, zLen] (mm).
        dX (list): Grid spacing [dx, dy, dz] (mm).
        """
        self._xdim = np.arange(self._x0 - self._xlen/2.0,
                               self._x0 + self._xlen/2.0,
                               self._dx)
        self._ydim = np.arange(self._y0 - self._ylen/2.0,
                               self._y0 + self._ylen/2.0,
                               self._dy)
        self._zdim = np.arange(self._z0 - self._zlen/2.0,
                               self._z0 + self._zlen/2.0,
                               self._dz)

        print("Interpolating data.")
        self._fx = xf_regrid_3d_nearest((self.field_nonuniform_grid.xdim,
                                         self.field_nonuniform_grid.ydim,
                                         self.field_nonuniform_grid.zdim),
                                        (self._xdim,
                                         self._ydim,
                                         self._zdim),
                                        self.field_nonuniform_grid.ss_field_data(field_type, 'x'))
        self._fy = xf_regrid_3d_nearest((self.field_nonuniform_grid.xdim,
                                         self.field_nonuniform_grid.ydim,
                                         self.field_nonuniform_grid.zdim),
                                        (self._xdim,
                                         self._ydim,
                                         self._zdim),
                                        self.field_nonuniform_grid.ss_field_data(field_type, 'y'))
        self._fz = xf_regrid_3d_nearest((self.field_nonuniform_grid.xdim,
                                         self.field_nonuniform_grid.ydim,
                                         self.field_nonuniform_grid.zdim),
                                        (self._xdim,
                                         self._ydim,
                                         self._zdim),
                                        self.field_nonuniform_grid.ss_field_data(field_type, 'z'))
        return self._fx, self._fy, self._fz

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

    @property
    def net_input_power(self):
        """Desired net input power."""
        return self._net_input_power

    @net_input_power.setter
    def net_input_power(self, power):
        """Set the desired net input power for simulation."""
        self._net_input_power = power

    def scale_fields(self):
        """Normalize the field value to be net input power."""
        field_norm = self._net_input_power / sqrt(self._xf_system.net_input_power)
        self._fx = self._fx * field_norm
        self._fy = self._fy * field_norm
        self._fz = self._fz * field_norm

    def export_matfile(self, field_type, file_name):
        """Export field data in mat file."""
        self.regrid_fields(field_type)
        self.scale_fields()
        print("Exporting field data to mat file.")
        export_dict = dict()
        export_dict['XDim'] = self._xdim
        export_dict['YDim'] = self._ydim
        export_dict['ZDim'] = self._zdim
        export_dict[field_type + 'x'] = self._fx
        export_dict[field_type + 'y'] = self._fy
        export_dict[field_type + 'z'] = self._fz
        spio.savemat(file_name, export_dict, oned_as='column')

def usage(exit_status=None):
    """Print the usage statement and exit with given status."""
    print("")
    print("Usage: export_fields_uniform.py project [--origin='[x0,y0,z0]'] \\")
    print("                                [--lengths='[x,y,z]'] \\")
    print("                                [--deltas='[dx, dy, dz]']")
    print("  --origin: the origin coordinates, string representing a " +
          "Python list.")
    print("  --lengths: dimensions of the ROI, centered at the origin, " +
          "string prepresenting a Python list.")
    print("  --deltas: grid resolution, string representing a Python list.")
    print("")
    print("Example: ")
    print("  $ export_fields_uniform.py / --origin='[0.0,0.0,0.0]' " +
          "--lengths='[0.01,0.01,0.02]' --deltas='[0.02, 0.02, 0.02]'")
    print("")
    if exit_status:
        sys.exit(exit_status)
    else:
        sys.exit()

def main(argv):
    """Parse command line arguments and make call to exporter."""
    arg_dict = {}
    switches = {'origin':list, 'lengths':list, 'deltas':list,
                'xf_project':str, 'run':str, 'sim':str,
                'export_file':str, 'field':str}
    singles = ''
    long_form = [x + '=' for x in switches]
    d = {x[0] + ':' : '--' + x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError as e:
        print("Bad argument Getopt: ", e.msg)
        usage(2)

    for opt, arg in opts:
        if opt[1] + ':' in d: o = d[opt[1]+':'][2:]
        elif opt in d.values(): o = opt[2:]
        else: o = ''
        if o and arg:
            if switches[o].__name__ == 'list':
                arg_dict[o] = ast.literal_eval(arg)
            else:
                arg_dict[o] = arg

        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    # Get project directory
    if not os.path.exists(arg_dict['xf_project']):
        print("XFdtd project (", arg_dict['xf_project'], ") not found.")
        usage(2)
    if len(arg_dict['origin']) != 3:
        print("Bad regrid region origin.")
        usage(2)
    if len(arg_dict['lengths']) != 3:
        print("Bad regrid region dimensions.")
        usage(2)
    if len(arg_dict['deltas']) != 3:
        print("Bad regrid resolution.")
        usage(2)

    xf_field_writer = XFFieldWriterUniform(arg_dict['xf_project'],
                                           int(arg_dict['sim']),
                                           int(arg_dict['run']))
    xf_field_writer.set_origin(arg_dict['origin'][0],
                               arg_dict['origin'][1],
                               arg_dict['origin'][2])
    xf_field_writer.set_len(arg_dict['lengths'][0],
                            arg_dict['lengths'][1],
                            arg_dict['lengths'][2])
    xf_field_writer.set_grid_resolution(arg_dict['deltas'][0],
                                        arg_dict['deltas'][1],
                                        arg_dict['deltas'][2])

    xf_field_writer.export_matfile(arg_dict['field'], arg_dict['export_file'])

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done.")
