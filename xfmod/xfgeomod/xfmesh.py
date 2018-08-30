"""
Class XFMesh to contain XFDtd mesh.input file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import absolute_import, division, generators, print_function

import os
import struct
from xfmod.xfutils import xf_run_id_to_str, xf_sim_id_to_str
from math import floor

class XFMeshEdgeRun(object):
    """
    XFMeshEdgeRun: class to hold edge run data.
    """
    def __init__(self,run_type='', x_ind=None, y_ind=None, z_ind=None, stop_ind=None, mat=None):
        if run_type.upper() == 'X' or run_type.upper() == 'Y' or run_type.upper() == 'Z':
            self._run_type = run_type
        else:
            self._run_type = ''
        self._x_ind = x_ind
        self._y_ind = y_ind
        self._z_ind = z_ind
        self._stop_ind = stop_ind
        self._mat = mat

    @property
    def run_type(self):
        """Returns run type: 'X', 'Y', or 'Z'."""
        return self._run_type

    @run_type.setter
    def run_type(self, value):
        """Sets run_type.  Valid values are 'X', 'Y', or 'Z'."""
        if value.upper() == 'X':
            self._run_type = 'X'
        elif value.upper() == 'Y':
            self._run_type = 'Y'
        elif value.uppper() == 'Z':
            self._run_type = 'Z'
        else:
            print("Invalid run_type specified.  Valid values are " + \
                  "'X', 'Y', or 'Z'")

    @run_type.deleter
    def run_type(self):
        """Delete the run type value."""
        self._run_type = ''

    @property
    def x_ind(self):
        """Returns X index or run start index if run_type is 'X'."""
        return self._x_ind

    @x_ind.setter
    def x_ind(self, value):
        """Set the X index value."""
        if isinstance(value, int):
            self._x_ind = value
        else:
            print('X index must be of type integer.')

    @x_ind.deleter
    def x_ind(self):
        """Delete the X index value."""
        self._x_ind = None

    @property
    def y_ind(self):
        """Returns Y index or run start index if run_type is 'Y'."""
        return self._y_ind

    @y_ind.setter
    def y_ind(self, value):
        """Sets the Y index value."""
        if isinstance(value, int):
            self._y_ind = value
        else:
            print('Y index must be of type integer.')

    @y_ind.deleter
    def y_ind(self):
        """Deletes the Y index value."""
        self._y_ind = None

    @property
    def z_ind(self):
        """Returns Z index or run start index if run_type is 'Z'."""
        return self._z_ind

    @z_ind.setter
    def z_ind(self, value):
        """Set the Z index value."""
        if isinstance(value, int):
            self._z_ind = value
        else:
            print('Z index must be of type integer.')

    @z_ind.deleter
    def z_ind(self):
        """Delete the Z index value."""
        self._z_ind = None

    @property
    def stop_ind(self):
        """Returns run stop index for run_type."""
        return self._stop_ind

    @stop_ind.setter
    def stop_ind(self, value):
        """Set the run stop index."""
        if isinstance(value, int):
            self._stop_ind = value
        else:
            print('Stop index must be of type integer.')

    @stop_ind.deleter
    def stop_ind(self):
        """Delete the stop index value."""
        self._stop_ind = None

    @property
    def mat(self):
        """Return material in edge run."""
        return self._mat

    @mat.setter
    def mat(self, value):
        """Set the edge run material."""
        if isinstance(value, int):
            if value >= 0 and value <= 256:
                self._mat = value
        else:
            print('Material value must be an integer between 0 and 256.')

    @mat.deleter
    def mat(self):
        """Delete the edge run material."""
        self._mat = None

def read_edge_run_data(file_handle, nedge_runs):
    """
    read_edge_run_data: Helper function for XFMesh that reads edge run
    data version 0,1 and returns an instance of XFMeshEdgeRun.
    file_handle: handle to open mesh.input file
    nedge_runs: number of edge runs to read
    """
    edge_runs = []
    for run_index in range(nedge_runs):
        cur_run = XFMeshEdgeRun()
        cur_run.x_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.y_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.z_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.stop_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.mat = struct.unpack('B', file_handle.read(1))[0]
        edge_runs.append(cur_run)

    return edge_runs

def dijk_from_flat_index(flat_index, nx_cells, ny_cells, nz_cells):
    """
    dijk_from_flat_index: Helper function for XFMesh to calculate D, i, j, k
    from flat index and grid dimensions, as discribed in the XFdtd 7.8.0
    reference manual.
    flat_index: index from mesh.input version 2 data cell
    nx_cells: number of cells in grid, x-dimension
    ny_cells: number of cells in grid, y-dimension
    nz_cells: number of cells in grid, z-dimension
    """
    edge_d = floor(flat_index/(nx_cells*ny_cells*nz_cells))
    edge_i = floor((flat_index -
                    edge_d*nx_cells*ny_cells*nz_cells)/
                   (ny_cells*nz_cells))
    edge_j = floor((flat_index -
                    edge_d*nx_cells*ny_cells*nz_cells -
                    edge_i*ny_cells*nz_cells) / nz_cells)

    edge_k = flat_index - \
             edge_d*nx_cells*ny_cells*nz_cells - \
             edge_i*ny_cells*nz_cells - \
             edge_j*nz_cells


    return edge_d, edge_i, edge_j, edge_k

def read_edge_run_data_flat(file_handle, num_edge_runs, nx_cells, ny_cells, nz_cells):
    """
    read_edge_run_data_flat: Helper function for XFMesh that reads edge run data
    data in flat file format for version 2 of mesh.input.  Returns an instance
    of XFMeshEdgeRun.
    file_handle: handle to open mesh.input file
    nedge_runs: number of edge runs to read
    n{x,y,z}_cells: number of {x,y,z} cells in grid from the mesh.input header.
    """
    edge_runs = []
    for run_index in range(num_edge_runs):

        flat_edge_index = struct.unpack('Q', file_handle.read(8))[0]
        grid_stop = struct.unpack('I', file_handle.read(4))[0]
        run_mat = struct.unpack('B', file_handle.read(1))[0]
        edge_d,edge_i,edge_j,edge_k = dijk_from_flat_index(flat_edge_index,
                                                           nx_cells,
                                                           ny_cells,
                                                           nz_cells)
        if edge_d == 0:
            run_type = 'X'
        elif edge_d == 1:
            run_type = 'Y'
        elif edge_d == 2:
            run_type = 'Z'

        cur_run = XFMeshEdgeRun(run_type, edge_i, edge_j, edge_k, grid_stop, run_mat)
        edge_runs.append(cur_run)

    return edge_runs

class XFMesh(object):
    """
    Process mesh.input file
    """
    def __init__(self, xf_project_dir, sim_id, run_id):
        self._mesh_input_file_path = os.path.join(xf_project_dir,
                                                  r'Simulations',
                                                  xf_sim_id_to_str(sim_id),
                                                  xf_run_id_to_str(run_id),
                                                  r'mesh.input')
        self._mesh_version = None
        self._edge_run_bytes = 0
        self._edge_run_fmt = None
        self._num_ex_edge_runs = 0
        self._num_ey_edge_runs = 0
        self._num_ez_edge_runs = 0
        self._ex_edge_runs = []
        self._ey_edge_runs = []
        self._ez_edge_runs = []
        self._num_hx_edge_runs = 0
        self._num_hy_edge_runs = 0
        self._num_hz_edge_runs = 0
        self._hx_edge_runs = []
        self._hy_edge_runs = []
        self._hz_edge_runs = []
        self._num_e_avg_mats = 0
        self._num_h_avg_mats = 0
        self._num_e_mesh_edges_e_avg = 0
        self._num_h_mesh_edges_h_avg = 0
        self._start_ex_edge_run = 0
        self._start_ey_edge_run = 0
        self._start_ez_edge_run = 0
        self._num_x_cells = None
        self._num_y_cells = None
        self._num_z_cells = None
        self._read_mesh_header()
        print("Edge Runs: ")
        print("X: ", self._num_ex_edge_runs)
        print("Y: ", self._num_ey_edge_runs)
        print("Z: ", self._num_ez_edge_runs)
        self._read_edge_run_data()


    def _read_mesh_header(self):
        """Read the mesh header."""
        file_handle = open(self._mesh_input_file_path, 'rb')
        if file_handle:
            # check remcom 11-byte header
            if file_handle.read(11) != b'!remcomfdtd':
                print("Mesh input header appears malformed: ")
                return
            if file_handle.read(1) != b'L':
                print("Expected little endian file format.")
                return
            if struct.unpack('H', file_handle.read(2))[0] != 0:
                print("Mesh input header: mesh.input not 'mesh data' type.")
                return
            self._mesh_version = struct.unpack('H', file_handle.read(2))[0]
            if self._mesh_version == 0:
                self._edge_run_bytes = 4
                self._edge_run_fmt = 'I'
            elif self._mesh_version == 1 or self._mesh_version ==2:
                self._edge_run_bytes = 8
                self._edge_run_fmt = 'Q'
            else:
                print("Mesh input header: mesh.input version not recognized: ", self._mesh_version)
                return
            if struct.unpack('B', file_handle.read(1))[0] != 0:
                print("Mesh input header: mesh.input format " + \
                      "indicator not zeros")
                return
            # Number of Ex edge runs
            self._num_ex_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of Ey edge runs
            self._num_ey_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of Ez edge runs
            self._num_ez_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of Hx edge runs
            self._num_hx_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of Hy edge runs
            self._num_hy_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of Hz edge runs
            self._num_hz_edge_runs = struct.unpack(self._edge_run_fmt, \
                                                   file_handle.read(self._edge_run_bytes))[0]
            # Number of electric averaged materials
            self._num_e_avg_mats = struct.unpack('I', file_handle.read(4))[0]
            # Number of magnetic averaged materials
            self._num_h_avg_mats = struct.unpack('I', file_handle.read(4))[0]
            # Number of electric mesh edges using electric averaged materials
            self._num_e_mesh_edges_e_avg = struct.unpack('Q', \
                                                         file_handle.read(8))[0]
            # Number of magnetic mesh edges using magnetic averaged materials
            self._num_h_mesh_edges_h_avg = struct.unpack('Q', \
                                                         file_handle.read(8))[0]
            if self._mesh_version == 2:
                self._num_x_cells = struct.unpack('I', file_handle.read(4))[0]
                self._num_y_cells = struct.unpack('I', file_handle.read(4))[0]
                self._num_z_cells = struct.unpack('I', file_handle.read(4))[0]

            self._start_ex_edge_run = file_handle.tell()

        else:
            print("Could not open Mesh file.")
            return
        file_handle.close()

    def _read_edge_run_data(self):
        """Read Edge run data"""
        file_handle = open(self._mesh_input_file_path, 'rb')
        file_handle.seek(self._start_ex_edge_run)
        if self._mesh_version < 2:
            # read Ex edges
            if self._num_ex_edge_runs > 0:
                self._ex_edge_runs = read_edge_run_data(file_handle,
                                                        self._num_ex_edge_runs)
            # read Ey edges
            if self._num_ey_edge_runs > 0:
                self._ey_edge_runs = read_edge_run_data(file_handle,
                                                    self._num_ey_edge_runs)
            # read Ez edges
            if self._num_ez_edge_runs > 0:
                self._ez_edge_runs = read_edge_run_data(file_handle,
                                                        self._num_ez_edge_runs)
            # read Hx edges
            if self._num_hx_edge_runs > 0:
                self._hx_edge_runs = read_edge_run_data(file_handle,
                                                        self._num_hx_edge_runs)
            # read Hy edges
            if self._num_hy_edge_runs > 0:
                self._hy_edge_runs = read_edge_run_data(file_handle,
                                                        self._num_hy_edge_runs)
            # read Hz edges
            if self._num_hz_edge_runs > 0:
                self._hz_edge_runs = read_edge_run_data(file_handle,
                                                        self._num_hz_edge_runs)

        # read runs from mesh.input version 2 and higher
        else:

            num_e_runs = self._num_ex_edge_runs + \
                         self._num_ey_edge_runs + \
                         self._num_ez_edge_runs
            num_h_runs = self._num_hx_edge_runs + \
                         self._num_hy_edge_runs + \
                         self._num_hz_edge_runs

            # read E field edge runs first, then H field runs
            edge_e_runs = read_edge_run_data_flat(file_handle,
                                                  num_e_runs,
                                                  self._num_x_cells,
                                                  self._num_y_cells,
                                                  self._num_z_cells)
            edge_h_runs = read_edge_run_data_flat(file_handle,
                                                  num_h_runs,
                                                  self._num_x_cells,
                                                  self._num_y_cells,
                                                  self._num_z_cells)

            for edge_run in edge_e_runs:
                if edge_run.run_type == 'X':
                    self._ex_edge_runs.append(edge_run)
                elif edge_run.run_type == 'Y':
                    self._ey_edge_runs.append(edge_run)
                elif edge_run.run_type == 'Z':
                    self._ez_edge_runs.append(edge_run)

            for edge_run in edge_h_runs:
                if edge_run.run_type == 'X':
                    self._hx_edge_runs.append(edge_run)
                elif edge_run.run_type == 'Y':
                    self._hy_edge_runs.append(edge_run)
                elif edge_run.run_type == 'Z':
                    self._hz_edge_runs.append(edge_run)

        # TODO: Averaged material definitions
        # this is not implemented yet.
        file_handle.close()

    @property
    def ex_edge_runs(self):
        """Retrun Ex edge runs."""
        return self._ex_edge_runs

    @property
    def ey_edge_runs(self):
        """Retrun Ey edge runs."""
        return self._ey_edge_runs

    @property
    def ez_edge_runs(self):
        """Retrun Ez edge runs."""
        return self._ez_edge_runs

    @property
    def hx_edge_runs(self):
        """Retrun Hx edge runs."""
        return self._hx_edge_runs

    @property
    def hy_edge_runs(self):
        """Retrun Hy edge runs."""
        return self._hy_edge_runs

    @property
    def hz_edge_runs(self):
        """Return Hz edge runs."""
        return self._hz_edge_runs
