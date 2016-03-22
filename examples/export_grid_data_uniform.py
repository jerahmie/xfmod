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
import xfgeomod
from xfutils import xf_regrid_3d_nearest

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
        self._ex_sigma = None; self._ey_sigma = None; self._ez_sigma = None
        self._hx_sigma = None; self._hy_sigma = None; self._hz_sigma = None
        self._ex_density = None; self._ey_density = None; self._ez_density = None
        self._hx_density = None; self._hy_density = None; self._hz_density = None
        self._ex_epsilon_r = None
        self._ey_epsilon_r = None
        self._ez_epsilon_r = None
        self._hx_epsilon_r = None
        self._hy_epsilon_r = None
        self._hz_epsilon_r = None
        self._geom = xfgeomod.XFGeometry(run_path)
        self._mesh = xfgeomod.XFMesh(run_path)
        self._grid_exporter = xfgeomod.XFGridExporter(self._geom, self._mesh)

    def set_origin(self, x0, y0, z0):
        """Set origin of export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def set_len(self, xlen, ylen, zlen):
        """Set dimension of export region."""
        self._xlen = xlen
        self._ylen = ylen
        self._zlen = zlen

    def set_grid_resolution(self, dx, dy, dz):
        """Set the resolution of the export region."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def _regrid(self):
        """Regrid the mesh and grid data."""
        print("_regrid orign: ", self._x0, ",", self._y0, ",", self._z0)
        print("_regrid lengths: ", self._xlen, ",", self._ylen, ",", self._zlen)
        print("_regrid deltas: ", self._dx, ",", self._dy, ",", self._dz)
  
        self._xdim = np.arange(self._x0 - self._xlen/2.0,
                               self._x0 + self._xlen/2.0,
                               self._dx)
        self._ydim = np.arange(self._y0 - self._ylen/2.0,
                               self._y0 + self._ylen/2.0,
                               self._dy)
        self._zdim = np.arange(self._z0 - self._zlen/2.0,
                               self._z0 + self._zlen/2.0,
                               self._dz)
        print("_regrid: _xdim: ", np.shape(self._xdim))
        print("_regrid: _ydim: ", np.shape(self._ydim))
        print("_regrid: _zdim: ", np.shape(self._zdim))
        print("Interpolating data.")
        self._ex_sigma = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim,
                                               self._ydim,
                                               self._zdim),
                                              self._grid_exporter.ex_sigma)
        self._ey_sigma = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim,
                                               self._ydim,
                                               self._zdim),
                                              self._grid_exporter.ey_sigma)
        self._ez_sigma = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                               self._grid_exporter.grid_y,
                                               self._grid_exporter.grid_z),
                                              (self._xdim,
                                               self._ydim,
                                               self._zdim),
                                              self._grid_exporter.ez_sigma)
        self._ex_epsilon_r = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim,
                                                   self._ydim,
                                                   self._zdim),
                                                  self._grid_exporter.ex_epsilon_r)
        self._ey_epsilon_r = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim,
                                                   self._ydim,
                                                   self._zdim),
                                                  self._grid_exporter.ey_epsilon_r)
        self._ez_epsilon_r = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                   self._grid_exporter.grid_y,
                                                   self._grid_exporter.grid_z),
                                                  (self._xdim,
                                                   self._ydim,
                                                   self._zdim),
                                                  self._grid_exporter.ez_epsilon_r)
        self._ex_density = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim,
                                                 self._ydim,
                                                 self._zdim),
                                                self._grid_exporter.ex_density)
        self._ey_density = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim,
                                                 self._ydim,
                                                 self._zdim),
                                                self._grid_exporter.ey_density)
        self._ez_density = xf_regrid_3d_nearest((self._grid_exporter.grid_x,
                                                 self._grid_exporter.grid_y,
                                                 self._grid_exporter.grid_z),
                                                (self._xdim,
                                                 self._ydim,
                                                 self._zdim),
                                                self._grid_exporter.ez_density)
        
    def export_matfile(self, file_name):
        """Export mesh/grid data to matlab file."""
        self._regrid()
        export_dict = dict()
        if self._ex_density is not None:
            print('Adding MeshExDensity to export mat file.')
            print(np.shape(self._ex_density))
            export_dict['MeshExDensity'] = self._ex_density
        if self._ex_sigma is not None:
            print('Adding MeshExSigma to export mat file.')
            print(np.shape(self._ex_sigma))
            export_dict['MeshExSigma'] = self._ex_sigma
        if self._ex_epsilon_r is not None:
            print('Adding MeshExEpsilon_r to export mat file.')
            print(np.shape(self._ex_epsilon_r))
            export_dict['MeshExEpsilon_r'] = self._ex_epsilon_r
        if self._ey_density is not None:
            print('Adding MeshEyDensity to export mat file.')
            print(np.shape(self._ey_density))
            export_dict['MeshEyDensity'] = self._ey_density
        if self._ey_sigma is not None:
            print('Adding MeshEySigma to export mat file.')
            print(np.shape(self._ey_sigma))
            export_dict['MeshEySigma'] = self._ey_sigma
        if self._ey_epsilon_r is not None:
            print('Adding MeshEyEpsilon_r to export mat file.')
            print(np.shape(self._ey_epsilon_r))
            export_dict['MeshEyEpsilon_r'] = self._ey_epsilon_r
        if self._ez_density is not None:
            print('Adding MeshEzDensity to export mat file.')
            print(np.shape(self._ez_density))
            export_dict['MeshEzDensity'] = self._ez_density
        if self._ez_sigma is not None:
            print('Adding MeshEzSigma to export mat file.')
            print(np.shape(self._ez_sigma))
            export_dict['MeshEzSigma'] = self._ez_sigma
        if self._ez_epsilon_r is not None:
            print('Adding MeshEzEpsilon_r to export mat file.')
            print(np.shape(self._ez_epsilon_r))
            export_dict['MeshEzEpsilon_r'] = self._ez_epsilon_r
        if self._hx_density is not None:
            print('Adding MeshHxDensity to export mat file.')
            print(np.shape(self._hx_density))
            export_dict['MeshHxDensity'] = self._hx_density
        if self._hx_sigma is not None:
            print('Adding MeshHxSigma to export mat file.')
            print(np.shape(self._hx_sigma))
            export_dict['MeshHxSigma'] = self._hx_sigma
        if self._hy_density is not None:
            print('Adding MeshHyDensity to export mat file.')
            print(np.shape(self._hy_density))
            export_dict['MeshHyDensity'] = self._hy_density
        if self._hy_sigma is not None:
            print('Adding MeshHySigma to export mat file.')
            print(np.shape(self._hy_sigma))
            export_dict['MeshHySigma'] = self._hy_sigma
        if self._hz_density is not None:
            print('Adding MeshHzDensity to export mat file.')
            print(np.shape(self._hz_density))
            export_dict['MeshHzDensity'] = self._hz_density
        if self._hz_sigma is not None:
            print('Adding MeshHzSigma to export mat file.')
            print(np.shape(self._hz_sigma))
            export_dict['MeshHzSigma'] = self._hz_sigma
        if self._xdim is not None:
            print('Adding grid_X to export mat file.')
            export_dict['grid_X'] = [x*self._grid_exporter.units_scale_factor for x in self._xdim]
        if self._ydim is not None:
            print('Adding grid_Y to export mat file.')
            export_dict['grid_Y'] = [x*self._grid_exporter.units_scale_factor for x in self._ydim]
        if self._zdim is not None:
            print('Adding grid_Z to export mat file.')
            export_dict['grid_Z'] = [x*self._grid_exporter.units_scale_factor for x in self._zdim]
            export_dict['units'] = self._grid_exporter.units
        # writing data to mat file (file_name)
        print("Saving mesh data to Mat file.")
        spio.savemat(file_name, export_dict)
    
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
    print(arg_dict)
    print("[main] lengths: ", arg_dict['lengths'][0], ",", arg_dict['lengths'][1], ",", arg_dict['lengths'][2])
    xf_grid_writer.set_len(arg_dict['lengths'][0],
                           arg_dict['lengths'][1],
                           arg_dict['lengths'][2])
    print("[main] _lengths: ", xf_grid_writer._xlen, ",", xf_grid_writer._ylen, ",", xf_grid_writer._zlen)
    xf_grid_writer.set_grid_resolution(arg_dict['deltas'][0],
                                       arg_dict['deltas'][1],
                                       arg_dict['deltas'][2])
    xf_grid_writer.export_matfile(arg_dict['export_file'])

if __name__ == '__main__':
    main(sys.argv[1:])
    

