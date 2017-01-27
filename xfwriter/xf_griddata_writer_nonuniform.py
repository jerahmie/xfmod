"""
Grid data exporter on simulation grid.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import xfgeomod
from xfwriter import XFMatWriter

class XFGridDataWriterNonUniform(XFMatWriter):
    """Write XFdtd grid data to mat file on native simulation grid."""
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._geom = xfgeomod.XFGeometry(xf_project_dir, sim_id, run_id)
        self._mesh = xfgeomod.XFMesh(xf_project_dir, sim_id, run_id)
        self._grid_exporter = xfgeomod.XFGridExporter(self._geom, self._mesh)
        self._xdim = self._grid_exporter.grid_x
        self._ydim = self._grid_exporter.grid_y
        self._zdim = self._grid_exporter.grid_z
        self._ex_density = self._grid_exporter.ex_density
        self._ey_density = self._grid_exporter.ey_density
        self._ez_density = self._grid_exporter.ez_density
        self._ex_sigma = self._grid_exporter.ex_sigma
        self._ey_sigma = self._grid_exporter.ey_sigma
        self._ez_sigma = self._grid_exporter.ez_sigma
        self._ex_epsilon_r = self._grid_exporter.ex_epsilon_r
        self._ey_epsilon_r = self._grid_exporter.ey_epsilon_r
        self._ez_epsilon_r = self._grid_exporter.ez_epsilon_r
        self._hx_density = None
        self._hy_density = None
        self._hz_density = None
        self._hx_sigma = None
        self._hy_sigma = None
        self._hz_sigma = None
        self._hx_epsilon_r = None
        self._hy_epsilon_r = None
        self._hz_epsilon_r = None

    def savemat(self, file_name):
        """Export mesh/grid data to matlab file."""
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
