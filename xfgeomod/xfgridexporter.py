"""
XFGridExporter: class to export grid and mesh information.
This class constructs the numpy matrices and writes them to a mat file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

from scipy.io import savemat
import numpy as np

class XFGridExporter(object):
    """Export grid and mesh info."""
    def __init__(self, grid, mesh):
        self._mesh = mesh
        self._grid = grid
        self._grid_x = self._grid.grid_data.x_coods()
        self._x_dim = len(self._grid_x)
        self._grid_y = self._grid.grid_data.y_coods()
        self._y_dim = len(self._grid_y)
        self._grid_z = self._grid.grid_data.z_coods()
        self._z_dim = len(self._grid_z)
        self._export_units = 'm'          # grid/mesh units (default = meters)
        self._export_units_scale = 1.0    # scale factor (meters = 1.0)
        self._materials_list = grid.load_materials()
        self._ex_edge_runs = self._mesh.ex_edge_runs
        self._ey_edge_runs = self._mesh.ey_edge_runs
        self._ez_edge_runs = self._mesh.ez_edge_runs
        self._hx_edge_runs = self._mesh.hx_edge_runs
        self._hy_edge_runs = self._mesh.hy_edge_runs
        self._hz_edge_runs = self._mesh.hz_edge_runs
        self._mesh_ex_density = None; self._mesh_ey_density = None; self._mesh_ez_density = None
        self._mesh_ex_sigma = None; self._mesh_ey_sigma = None; self._mesh_ez_sigma = None
        self._mesh_ex_epsilon_r = None
        self._mesh_ey_epsilon_r = None
        self._mesh_ez_epsilon_r = None
        self._mesh_hx_density = None; self._mesh_hy_density = None; self._mesh_hz_density = None
        self._mesh_hx_sigma = None; self._mesh_hy_sigma = None; self._mesh_hz_sigma = None
        self._mesh_hx_epsilon_r = None
        self._mesh_hy_epsilon_r = None
        self._mesh_hz_epsilon_r = None
        self._set_mesh_data()
#        self._reorder_mesh_data()

    @property
    def grid_x(self):
        return self._grid_x

    @property
    def grid_y(self):
        return self._grid_y

    @property
    def grid_z(self):
        return self._grid_z

    @property
    def units(self):
        """Return export grid/mesh units."""
        return self._export_units

    @property
    def ex_sigma(self):
        """Return conductivity on Ex grid locations."""
        return self._mesh_ex_sigma

    @property
    def ey_sigma(self):
        """Return conductivity on Ey grid locations."""
        return self._mesh_ey_sigma

    @property
    def ez_sigma(self):
        """Return conductivity on Ez grid locations."""
        return self._mesh_ez_sigma

    @property
    def ex_epsilon_r(self):
        """Return relative permittivity on Ex grid locations."""
        return self._mesh_ex_epsilon_r

    @property
    def ey_epsilon_r(self):
        """Return relative permittivity on Ey grid locations."""
        return self._mesh_ey_epsilon_r
    
    @property
    def ez_epsilon_r(self):
        """Return relative permittivity on Ez grid locations."""
        return self._mesh_ez_epsilon_r

    @property
    def ex_density(self):
        """Return density on Ex grid locations."""
        return self._mesh_ex_density

    @property
    def ey_density(self):
        """Return density on Ey grid locations."""
        return self._mesh_ey_density

    @property
    def ez_density(self):
        """Return density on Ez grid locaitons."""
        return self._mesh_ez_density

    @units.setter
    def units(self,value):
        """Set the export grid/mesh units."""
        if value == 'm':
            self._export_units = 'm'
            self._export_units_scale = 1.0
        elif value == 'mm':
            self._export_units = 'mm'
            self._export_units_scale = 1000.0
        elif value == 'cm':
            self._export_units = 'cm'
            self._export_units_scale = 100.0
        elif value == 'um':
            self._export_units = 'um'
            self._export_units_scale = 1.0e6
        elif value == 'nm':
            self._export_units = 'nm'
            self._export_units_scale = 1.0e9
        elif (value == 'inches') or (value == 'in'):
            self._export_units = 'inches'
            self._export_units_scale = 39.2701
        else:
            print('Invalid unit type: ', value)

    @property
    def units_scale_factor(self):
        """Return the grid and meshing scale factor."""
        return self._export_units_scale

    def _set_mesh_data(self):
        """Set mesh data from edge run data."""
        print('Setting mesh/grid data.')
        print('Mesh Units: ', self._export_units)
        # set Ex material properties
        if self._ex_edge_runs is not None:
            print('Calculating Ex mesh values.')
            self._mesh_ex_density = np.empty((self._x_dim, self._y_dim, self._z_dim))

            self._mesh_ex_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_ex_epsilon_r = np.empty((self._x_dim, self._y_dim, self._z_dim))
            # initialize to freespace
            self._mesh_ex_density[:] = np.NAN
            self._mesh_ex_sigma[:] = self._materials_list[0].conductivity
            # relative permittivity is set to zero for PEC values (mat type 1)
            # free space (mat type 0) or material permittivity for all others.
            self._mesh_ex_epsilon_r[:] = self._materials_list[0].epsilon_r
            for edge_run in self._ex_edge_runs:
                for index in range(edge_run.x_ind, edge_run.stop_ind):
                    if edge_run.mat == 1:
                        self._mesh_ex_epsilon_r[index,edge_run.y_ind, edge_run.z_ind] = 0.0
                    else:
                        self._mesh_ex_density[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_ex_sigma[index, edge_run.y_ind, edge_run.z_ind,] = self._materials_list[edge_run.mat].conductivity
                        self._mesh_ex_epsilon_r[index, edge_run.y_ind, edge_run.z_ind,] = self._materials_list[edge_run.mat].epsilon_r

        # set Ey material properties
        if self._ey_edge_runs is not None:
            print('Calculating Ey mesh values.')
            self._mesh_ey_density = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_ey_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_ey_epsilon_r = np.empty((self._x_dim, self._y_dim, self._z_dim))
            # initialize to freespace
            self._mesh_ey_density[:] = np.NAN
            self._mesh_ey_sigma[:] = self._materials_list[0].conductivity
            # relative permittivity is set to zero for PEC values (mat type 1)
            # free space (mat type 0) or material permittivity for all others.
            self._mesh_ey_epsilon_r[:] = self._materials_list[0].epsilon_r
            for edge_run in self._ey_edge_runs:
                for index in range(edge_run.y_ind, edge_run.stop_ind):
                    if edge_run.mat == 1:
                        self._mesh_ey_epsilon_r[edge_run.x_ind, index, edge_run.z_ind] = 0.0
                    else:
                        self._mesh_ey_density[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_ey_sigma[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].conductivity
                        self._mesh_ey_epsilon_r[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].epsilon_r

        # set Ez material properties
        if self._ez_edge_runs is not None:
            print('Calculating Ez mesh values.')
            self._mesh_ez_density = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_ez_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_ez_epsilon_r = np.empty((self._x_dim, self._y_dim, self._z_dim))

            # initialize to freespace
            self._mesh_ez_density[:] = np.NAN
            self._mesh_ez_sigma[:] = self._materials_list[0].conductivity
            # relative permittivity is set to zero for PEC values (mat type 1)
            # free space (mat type 0) or material permittivity for all others.
            self._mesh_ez_epsilon_r[:] = self._materials_list[0].epsilon_r
            for edge_run in self._ez_edge_runs:
                for index in range(edge_run.z_ind, edge_run.stop_ind):
                    if edge_run.mat == 1:
                        self._mesh_ez_epsilon_r[edge_run.x_ind, edge_run.y_ind, index] = 0.0
                    else:
                        self._mesh_ez_density[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].density
                        self._mesh_ez_sigma[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].conductivity
                        self._mesh_ez_epsilon_r[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].epsilon_r

        # set Hx material properties
        if self._hx_edge_runs is not None:
            print('Calculating Hx mesh values.')
            self._mesh_hx_density = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hx_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hx_density[:] = np.NAN
            self._mesh_hx_sigma[:] = np.NAN
            for edge_run in self._hx_edge_runs:
                for index in range(edge_run.x_ind, edge_run.stop_ind):
                    if edge_run.mat > 1:
                        self._mesh_hx_density[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_hx_sigma[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].conductivity

        # set Hy material properties
        if self._hy_edge_runs is not None:
            print('Calculating Hy mesh values.')
            self._mesh_hy_density = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hy_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hy_density[:] = np.NAN
            self._mesh_hy_sigma[:] = np.NAN

            for edge_run in self._hy_edge_runs:
                for index in range(edge_run.y_ind, edge_run.stop_ind):
                    if edge_run.mat > 1:
                        self._mesh_hy_density[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_hy_sigma[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].conducivity

        # set Hz material properties
        if self._hz_edge_runs is not None:
            print('Calculating Hz mesh values.')
            self._mesh_hz_density = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hz_sigma = np.empty((self._x_dim, self._y_dim, self._z_dim))
            self._mesh_hz_density[:] = np.NAN
            self._mesh_hz_sigma[:] = np.NAN
            for edge_run in self._hz_edge_runs:
                for index in range(edge_run.z_ind, edge_run.stop_ind):
                    if edge_run.mat > 1:
                        self._mesh_hz_density[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].density
                        self._mesh_hz_sigma[ edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].conducivity

#    def _reorder_mesh_data(self):
#        """Reorder the mesh data from (z,y,x) to (x,y,z) ordering."""
#
#        print("Reordering mesh density data.")
#        if self._mesh_ex_density is not None:
#            np.transpose(self._mesh_ex_density, (2,1,0))
#        if self._mesh_ey_density is not None:
#            np.transpose(self._mesh_ey_density, (2,1,0))
#        if self._mesh_ez_density is not None:
#            np.transpose(self._mesh_ez_density, (2,1,0))
#        if self._mesh_hx_density is not None:
#            np.transpose(self._mesh_hx_density, (2,1,0))
#        if self._mesh_hy_density is not None:
#            np.transpose(self._mesh_hy_density, (2,1,0))
#        if self._mesh_hz_density is not None:
#            np.transpose(self._mesh_hz_density, (2,1,0))
#            
#        print("Reordering mesh permittivity data.")
#        if self._mesh_ex_epsilon_r is not None:
#            np.transpose(self._mesh_ex_epsilon_r, (2,1,0))
#        if self._mesh_ey_epsilon_r is not None:
#            np.transpose(self._mesh_ey_epsilon_r, (2,1,0))
#        if self._mesh_ez_epsilon_r is not None:
#            np.transpose(self._mesh_ez_epsilon_r, (2,1,0))
#
#        print("Reordering mesh conductivity data.")
#        if self._mesh_ex_sigma is not None:
#            np.transpose(self._mesh_ex_sigma, (2,1,0))
#        if self._mesh_ey_sigma is not None:
#            np.transpose(self._mesh_ey_sigma, (2,1,0))
#        if self._mesh_ez_sigma is not None:
#            np.transpose(self._mesh_ez_sigma, (2,1,0))
        

    def export_mesh_data(self, file_name):
        """Export mesh data to matlab file."""
        export_dict = dict()
        if self._mesh_ex_density is not None:
            print('Adding MeshExDensity to export mat file.')
            export_dict['MeshExDensity'] = self._mesh_ex_density
        if self._mesh_ex_sigma is not None:
            print('Adding MeshExSigma to export mat file.')
            export_dict['MeshExSigma'] = self._mesh_ex_sigma
        if self._mesh_ex_epsilon_r is not None:
            print('Adding MeshExEpsilon_r to export mat file.')
            export_dict['MeshExEpsilon_r'] = self._mesh_ex_epsilon_r
        if self._mesh_ey_density is not None:
            print('Adding MeshEyDensity to export mat file.')
            export_dict['MeshEyDensity'] = self._mesh_ey_density
        if self._mesh_ey_sigma is not None:
            print('Adding MeshEySigma to export mat file.')
            export_dict['MeshEySigma'] = self._mesh_ey_sigma
        if self._mesh_ey_epsilon_r is not None:
            print('Adding MeshEyEpsilon_r to export mat file.')
            export_dict['MeshEyEpsilon_r'] = self._mesh_ey_epsilon_r
        if self._mesh_ez_density is not None:
            print('Adding MeshEzDensity to export mat file.')
            export_dict['MeshEzDensity'] = self._mesh_ez_density
        if self._mesh_ez_sigma is not None:
            print('Adding MeshEzSigma to export mat file.')
            export_dict['MeshEzSigma'] = self._mesh_ez_sigma
        if self._mesh_ez_epsilon_r is not None:
            print('Adding MeshEzEpsilon_r to export mat file.')
            export_dict['MeshEzEpsilon_r'] = self._mesh_ez_epsilon_r
        if self._mesh_hx_density is not None:
            print('Adding MeshHxDensity to export mat file.')
            export_dict['MeshHxDensity'] = self._mesh_hx_density
        if self._mesh_hx_sigma is not None:
            print('Adding MeshHxSigma to export mat file.')
            export_dict['MeshHxSigma'] = self._mesh_hx_sigma
        if self._mesh_hy_density is not None:
            print('Adding MeshHyDensity to export mat file.')
            export_dict['MeshHyDensity'] = self._mesh_hy_density
        if self._mesh_hy_sigma is not None:
            print('Adding MeshHySigma to export mat file.')
            export_dict['MeshHySigma'] = self._mesh_hy_sigma
        if self._mesh_hz_density is not None:
            print('Adding MeshHzDensity to export mat file.')
            export_dict['MeshHzDensity'] = self._mesh_hz_density
        if self._mesh_hz_sigma is not None:
            print('Adding MeshHzSigma to export mat file.')
            export_dict['MeshHzSigma'] = self._mesh_hz_sigma
        if self._grid_x is not None:
            print('Adding grid_X to export mat file.')
            export_dict['grid_X'] = [x*self._export_units_scale for x in self._grid_x]
        if self._grid_y is not None:
            print('Adding grid_Y to export mat file.')
            export_dict['grid_Y'] = [x*self._export_units_scale for x in self._grid_y]
        if self._grid_z is not None:
            print('Adding grid_Z to export mat file.')
            export_dict['grid_Z'] = [x*self._export_units_scale for x in self._grid_z]
            export_dict['units'] = self._export_units

        # writing data to mat file (file_name)
        print("Saving mesh data to Mat file.")
        savemat(file_name, export_dict)
