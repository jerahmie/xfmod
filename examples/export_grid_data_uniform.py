#!/usr/bin/env python3
"""
Example grid data exporter on uniform grid.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os, sys, ast, getopt
import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
import xfutils, xfgeomod

class XFGridDataWriterUniform(object):
    """Write XFdtd field data to mat file on uniform grid."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        run_path = os.path.join(xf_project_dir,
                                'Simulations',
                                xfutils.xf_sim_id_to_str(sim_id),
                                xfutils.xf_run_id_to_str(run_id))
        self._x0 = 0.0; self._y0 = 0.0; self._z0 = 0.0
        self._dx = 0.0; self._dy = 0.0; self._dz = 0.0
        self._xlen = 0.0; self._ylen = 0.0; self._zlen = 0.0
        self._ex_sigma = None; self.ey_sigma = None; self._ez_sigma = None
        self._ex_epsilon_r = None
        self._ey_epsilon_r = None
        self._ez_epsilon_r = None
        self._ex_density = None
        self._ey_density = None
        self._ez_density = None
        self._geom = xfgeomod.XFGeometry(run_path)
        self._mesh = xfgeomod.XFMesh(run_path)
        self._grid_exporter = xfgeomod.XFGridExporter(self._geom, self._mesh)

    def set_origin(self, x0, y0, z0):
        """Set origin of export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def set_len(self, x_len, y_len, z_len):
        """Set dimension of export region."""
        self._x_len = x_len
        self._y_len = y_len
        self._z_len = z_len

    def set_grid_resolution(self, dx, dy, dz):
        """Set the resolution of the export region."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def _regrid(self):
        """Regrid the mesh and grid data."""
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
        self._ex_sigma = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim, self._ydim, self._zdim),
                                                      np.transpose(self._grid_exporter.ex_sigma,(2,1,0)))
        self._ey_sigma = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim, self._ydim, self._zdim),
                                                      np.transpose(self._grid_exporter.ey_sigma,(2,1,0)))
        self._ez_sigma = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                       self._grid_exporter.grid_y,
                                                       self._grid_exporter.grid_z),
                                                      (self._xdim, self._ydim, self._zdim),
                                                      np.transpose(self._grid_exporter.ez_sigma,(2,1,0)))
        self._ex_epsilon_r = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                           self._grid_exporter.grid_y,
                                                           self._grid_exporter.grid_z),
                                                          (self._xdim, self._ydim, self._zdim),
                                                          np.transpose(self._grid_exporter.ex_epsilon_r,(2,1,0)))
        self._ey_epsilon_r = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                           self._grid_exporter.grid_y,
                                                           self._grid_exporter.grid_z),
                                                          (self._xdim, self._ydim, self._zdim),
                                                          np.transpose(self._grid_exporter.ey_epsilon_r,(2,1,0)))
        self._ez_epsilon_r = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                           self._grid_exporter.grid_y,
                                                           self._grid_exporter.grid_z),
                                                          (self._xdim, self._ydim, self._zdim),
                                                          np.transpose(self._grid_exporter.ez_epsilon_r,(2,1,0)))
        self._ex_density = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim, self._ydim, self._zdim),
                                                        np.transpose(self._grid_exporter.ex_density,(2,1,0)))
        self._ey_density = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim, self._ydim, self._zdim),
                                                        np.transpose(self._grid_exporter.ey_density,(2,1,0)))
        self._ez_density = xfutils.xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                         self._grid_exporter.grid_y,
                                                         self._grid_exporter.grid_z),
                                                        (self._xdim, self._ydim, self._zdim),
                                                        np.transpose(self._grid_exporter.ez_density,(2,1,0)))
        
    def export_matfile(self, file_name):
        """Export mesh/grid data to matlab file."""
        self._regrid()
    
def usage(exit_status=None):
    """Print the usage statement and exit with given status."""
    print("")
    print("Usage: export_fields_uniform.py project [--origin='[x0,y0,z0]'] \\")
    print("                                [--lengths='[x,y,z]'] \\")
    print("                                [--deltas='[dx, dy, dz]']")
    print("  --origin: the origin coordinates, " + \
          "string representing a Python list.")
    print("  --lengths: dimensions of the ROI, centered at the origin, " + \
          "string prepresenting a Python list.")
    print("  --deltas: grid resolution, string representing a Python list.")
    print("")
    print("Example: ")
    print("  $ export_fields_uniform.py / --origin='[0.0,0.0,0.0]' \\" + \
          "--lengths='[0.01,0.01,0.02]' --deltas='[0.02, 0.02, 0.02]'")
    print("")
    if(exit_status):
        sys.exit(exit_status)
    else:
        sys.exit()

def main(argv):
    """Parse command line arguments and make call to exporter."""
    arg_dict = {}
    switches = { 'origin':list, 'lengths':list, 'deltas':list,
                 'xf_project':str, 'run':str, 'sim':str,
                 'export_file':str }

    singles = ''
    long_form = [x+'=' for x in switches]
    d = {x[0]+':':'--'+x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, long_form)

    except getopt.GetoptError as e:
        print("Bad argument Getopt: ", e.msg)
        usage(2)

    for opt, arg in opts:
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o=''
        if o and arg:
            if (switches[o].__name__ == 'list'):
                arg_dict[o]=ast.literal_eval(arg)
            else:
                arg_dict[o]=arg
    
        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)
        
    # Get project directory
    if(not os.path.exists(arg_dict['xf_project'])):
       print("XFdtd project (", arg_dict['xf_project'], ") not found.")
       usage(2)
    if len(arg_dict['origin']) != 3:
       print("Bad regrid region origin.")
       usage(2)
    if len(arg_dict['lengths']) != 3:
       print("Bad region dimensions.")
       usage(2)
    if len(arg_dict['deltas']) != 3:
       print("Bad regrid resolution.")
       usage(2)

    print("Exporting grid for project: ", arg_dict['xf_project'])

    xf_grid_writer = XFGridDataWriterUniform(arg_dict['xf_project'],
                                             int(arg_dict['sim']),
                                             int(arg_dict['run']))
    xf_grid_writer.set_origin(arg_dict['origin'][0],
                              arg_dict['origin'][1],
                              arg_dict['origin'][2])
    xf_grid_writer.set_len(arg_dict['lengths'][0],
                           arg_dict['lengths'][1],
                           arg_dict['lengths'][2])
    xf_grid_writer.set_grid_resolution(arg_dict['deltas'][0],
                                       arg_dict['deltas'][1],
                                       arg_dict['deltas'][2])
    xf_grid_writer.export_matfile(arg_dict['export_file'])

if __name__ == '__main__':
    main(sys.argv[1:])
    

