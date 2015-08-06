"""XFGridExporter: class to export grid and mesh information."""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

from scipy.io import savemat
import numpy as np

class XFGridExporter:
    """Export grid and mesh info."""
    def __init__(self):
        self._x_dim = 0
        self._y_dim = 0
        self._z_dim = 0
        self._materials_list = None
        self._grid_x = None
        self._grid_y = None
        self._grid_z = None
        self._ex_edge_runs = None
        self._ey_edge_runs = None
        self._ez_edge_runs = None
        self._hx_edge_runs = None
        self._hy_edge_runs = None
        self._hz_edge_runs = None
        self._mesh_ex_density = None
        self._mesh_ey_density = None
        self._mesh_ez_density = None
        self._mesh_ex_sigma = None
        self._mesh_ey_sigma = None
        self._mesh_ez_sigma = None
        self._mesh_hx_density = None
        self._mesh_hy_density = None
        self._mesh_hz_density = None
        self._mesh_hx_sigma = None
        self._mesh_hy_sigma = None
        self._mesh_hz_sigma = None

    @property
    def grid_x(self):
        """Return X grid values."""
        return self._grid_x

    @grid_x.setter
    def grid_x(self, value):
        """Set X grid values."""
        self._grid_x = value
        self._x_dim = len(self._grid_x)

    @grid_x.deleter
    def grid_x(self):
        """Delete x grid values."""
        del self._grid_x
        self._grid_x = None
        self._x_dim = 0

    @property
    def grid_y(self):
        """Return Y grid values."""
        return self._grid_y

    @grid_y.setter
    def grid_y(self, value):
        """Set Y grid values."""
        self._grid_y = value
        self._y_dim = len(self._grid_y)

    @grid_y.deleter
    def grid_y(self):
        """Delete Y grid values."""
        del self._grid_y
        self.grid_y = None
        self._y_dim = 0

    @property
    def grid_z(self):
        """Return Z grid values."""
        return self._grid_z

    @grid_z.setter
    def grid_z(self, value):
        """Set Z grid values."""
        self._grid_z = value
        self._z_dim = len(self._grid_z)

    @grid_z.deleter
    def grid_z(self):
        """Delete Z grid values."""
        del self._grid_z
        self.grid_z = None
        self._z_dim = 0

    @property
    def materials_list(self):
        """Return the XF materials list."""
        return self._materials_list

    @materials_list.setter
    def materials_list(self, value):
        """Set the XF materials list."""
        self._materials_list = value

    @materials_list.deleter
    def materials_list(self):
        """Delete the XF materials list."""
        self._materials_list = None

    # Ex edge runs
    @property
    def ex_edge_runs(self):
        """Return the Ex edge runs."""
        return self._ex_edge_runs

    @ex_edge_runs.setter
    def ex_edge_runs(self, value):
        """Set the Ex edge runs."""
        self._ex_edge_runs = value

    @ex_edge_runs.deleter
    def ex_edge_runs(self):
        """Delete the Ex edge runs."""
        self._ex_edge_runs = None

    # Ey edge runs
    @property
    def ey_edge_runs(self):
        """Return the Ey edge runs."""
        return self._ey_edge_runs

    @ey_edge_runs.setter
    def ey_edge_runs(self, value):
        """Set the Ey edge runs."""
        self._ey_edge_runs = value

    @ey_edge_runs.deleter
    def ey_edge_runs(self):
        """Delete the Ey edge runs."""
        self._ey_edge_runs = None

    # Ez edge runs
    @property
    def ez_edge_runs(self):
        """Return the Ez edge runs."""
        return self._ez_edge_runs

    @ez_edge_runs.setter
    def ez_edge_runs(self, value):
        """Set the Ez edge runs."""
        self._ez_edge_runs = value

    @ez_edge_runs.deleter
    def ez_edge_runs(self):
        """Delete the Ez edge runs."""
        self._ez_edge_runs = None

    # Hx edge runs
    @property
    def hx_edge_runs(self):
        """Return the Hx edge runs."""
        return self._hx_edge_runs

    @hx_edge_runs.setter
    def hx_edge_runs(self, value):
        """Set the Hx edge runs."""
        self._hx_edge_runs = value

    @hx_edge_runs.deleter
    def hx_edge_runs(self):
        """Delete the Hx edge runs."""
        self._hx_edge_runs = None

    # Hy edge runs
    @property
    def hy_edge_runs(self):
        """Return the Hy edge runs."""
        return self._hy_edge_runs

    @hy_edge_runs.setter
    def hy_edge_runs(self, value):
        """Set the Hy edge runs."""
        self._hy_edge_runs = value

    @hy_edge_runs.deleter
    def hy_edge_runs(self):
        """Delete the Hy edge runs."""
        self._hy_edge_runs = None

    # Hz edge runs
    @property
    def hz_edge_runs(self):
        """Return the Hz edge runs."""
        return self._hz_edge_runs

    @hz_edge_runs.setter
    def hz_edge_runs(self, value):
        """Set the Hz edge runs."""
        self._hz_edge_runs = value

    @hz_edge_runs.deleter
    def hz_edge_runs(self):
        """Delete the Hz edge runs."""
        self._hz_edge_runs = None

    def set_mesh_data(self):
        """Set mesh data from edge run data."""
        if self._ex_edge_runs is not None:
            print('Calculating Ex mesh values.')
            self._mesh_ex_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))

            self._mesh_ex_sigma = np.empty(shape=(self._x_dim, \
                                                  self._y_dim, \
                                                  self._z_dim))
            self._mesh_ex_density[:] = np.NAN
            self._mesh_ex_sigma[:] = np.NAN

            # set Ex material properties
            for edge_run in self._ex_edge_runs:
                for index in range(edge_run.x_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_ex_density[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_ex_sigma[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].conductivity

        if self._ey_edge_runs is not None:
            print('Calculating Ey mesh values.')
            self._mesh_ey_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))
            self._mesh_ey_sigma = np.empty((self._x_dim, \
                                            self._y_dim, \
                                            self._z_dim))
            self._mesh_ey_density[:] = np.NAN
            self._mesh_ey_sigma[:] = np.NAN

            for edge_run in self._ey_edge_runs:
                for index in range(edge_run.y_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_ey_density[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_ey_sigma[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].conductivity


        if self._ez_edge_runs is not None:
            print('Calculating Ez mesh values.')
            self._mesh_ez_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))
            self._mesh_ez_sigma = np.empty((self._x_dim, \
                                            self._y_dim, \
                                            self._z_dim))
            self._mesh_ez_density[:] = np.NAN
            self._mesh_ez_sigma[:] = np.NAN
            # set Ez material properties
            for edge_run in self._ez_edge_runs:
                for index in range(edge_run.z_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_ez_density[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].density
                        self._mesh_ez_sigma[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].conductivity

        if self._hx_edge_runs is not None:
            print('Calculating Hx mesh values.')
            self._mesh_hx_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))
            self._mesh_hx_sigma = np.empty((self._x_dim, \
                                            self._y_dim, \
                                            self._z_dim))
            self._mesh_hx_density[:] = np.NAN
            self._mesh_hx_sigma[:] = np.NAN
            # set Hx material properties
            for edge_run in self._hx_edge_runs:
                for index in range(edge_run.x_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_hx_density[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_hx_sigma[index, edge_run.y_ind, edge_run.z_ind] = self._materials_list[edge_run.mat].conductivity

        if self._hy_edge_runs is not None:
            print('Calculating Hy mesh values.')
            self._mesh_hy_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))
            self._mesh_hy_sigma = np.empty((self._x_dim, \
                                            self._y_dim, \
                                            self._z_dim))
            self._mesh_hy_density[:] = np.NAN
            self._mesh_hy_sigma[:] = np.NAN
            # set Hy material properties
            for edge_run in self._hy_edge_runs:
                for index in range(edge_run.y_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_hy_density[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].density
                        self._mesh_hy_sigma[edge_run.x_ind, index, edge_run.z_ind] = self._materials_list[edge_run.mat].conducivity

        if self._hz_edge_runs is not None:
            print('Calculating Hz mesh values.')
            self._mesh_hz_density = np.empty((self._x_dim, \
                                              self._y_dim, \
                                              self._z_dim))
            self._mesh_hz_sigma = np.empty((self._x_dim, \
                                            self._y_dim, \
                                            self._z_dim))
            self._mesh_hz_density[:] = np.NAN
            self._mesh_hz_sigma[:] = np.NAN
            # set Hz material properties
            for edge_run in self._hz_edge_runs:
                for index in range(edge_run.z_ind, edge_run.stop_ind):
                    if edge_run.mat >= 2:
                        self._mesh_hz_density[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].density
                        self._mesh_hz_sigma[edge_run.x_ind, edge_run.y_ind, index] = self._materials_list[edge_run.mat].conducivity

    def export_mesh_data(self, file_name):
        """Export mesh data to matlab file."""
        export_dict = dict()
        if self._mesh_ex_density is not None:
            print('Adding MeshExDensity to export mat file.')

        if self._mesh_ex_sigma is not None:
            print('Adding MeshExSigma to export mat file.')

        if self._mesh_ey_density is not None:
            print('Adding MeshEyDensity to export mat file.')

        if self._mesh_ey_sigma is not None:
            print('Adding MeshEySigma to export mat file.')

        if self._mesh_ez_density is not None:
            print('Adding MeshEzDensity to export mat file.')

        if self._mesh_ey_sigma is not None:
            print('Adding MeshEzSigma to export mat file.')

        if self._mesh_hx_density is not None:
            print('Adding MeshHxDensity to export mat file.')

        if self._mesh_hx_sigma is not None:
            print('Adding MeshHxSigma to export mat file.')

        if self._mesh_hy_density is not None:
            print('Adding MeshHyDensity to export mat file.')

        if self._mesh_hy_sigma is not None:
            print('Adding MeshHySigma to export mat file.')

        if self._mesh_hz_density is not None:
            print('Adding MeshHzDensity to export mat file.')

        if self._mesh_hz_sigma is not None:
            print('Adding MeshHzSigma to export mat file.')
