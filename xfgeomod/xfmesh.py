"""
Class XFMesh processes XFDtd mesh.input file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import absolute_import, division, generators, print_function

import os, struct

class XFMeshEdgeRun(object):
    """
    XFMeshEdgeRun: class to hold edge run data.
    """
    def __init__(self):
        self._run_type = ''
        self._x_ind = None
        self._y_ind = None
        self._z_ind = None
        self._stop_ind = None
        self._mat = None

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

def read_edge_run_data(file_handle, num_edge_runs):
    """
    read_edge_run_data: Helper function for XFMesh that reads edge run
    data and returns an instance of XFMeshEdgeRun.
    """
    edge_runs = []
    for run_index in range(num_edge_runs):
        cur_run = XFMeshEdgeRun()
        cur_run.x_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.y_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.z_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.stop_ind = struct.unpack('I', file_handle.read(4))[0]
        cur_run.mat = struct.unpack('B', file_handle.read(1))[0]
        edge_runs.append(cur_run)

    return edge_runs


class XFMesh(object):
    """
    Process mesh.input file
    """
    def __init__(self, sim_run_path):
        self._file_path = sim_run_path
        self._file_name = os.path.join(sim_run_path, 'mesh.input')
        self._mesh_version = None
        self._edge_run_bytes = 0
        self._edge_run_fmt = None
        self._num_ex_edge_runs = 0
        self._num_ey_edge_runs = 0
        self._num_ez_edge_runs = 0
        self._ex_edge_runs = None
        self._ey_edge_runs = None
        self._ez_edge_runs = None
        self._num_hx_edge_runs = None
        self._num_hy_edge_runs = None
        self._num_hz_edge_runs = None
        self._hx_edge_runs = None
        self._hy_edge_runs = None
        self._hz_edge_runs = None
        self._num_e_avg_mats = None
        self._num_h_avg_mats = None
        self._num_e_mesh_edges_e_avg = None
        self._num_h_mesh_edges_h_avg = None
        self._start_ex_edge_run = 0
        self._start_ey_edge_run = 0
        self._start_ez_edge_run = 0
        self._read_mesh_header()
        self._read_edge_run_data()

    @property
    def file_path(self):
        """Return full file path name for mesh.input"""
        return self._file_path

    def _read_mesh_header(self):
        """Read the mesh header."""
        file_handle = open(self._file_name, 'rb')
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
            elif self._mesh_version == 1:
                self._edge_run_bytes = 8
                self._edge_run_fmt = 'Q'
            else:
                print("Mesh input header: mesh.input not version 0 or 1.")
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
            self._start_ex_edge_run = file_handle.tell()

        else:
            print("Could not open Mesh file.")
            return
        file_handle.close()

    def dump_header_info(self):
        """Dumpp header info."""
        print("        Filename: ", self._file_name)
        print("    Mesh version: ", self._mesh_version)
        print("  Edge run bytes: ", self._edge_run_bytes)
        print(" Edge run format: ", self._edge_run_fmt)
        print("Number of Ex edge runs: ", self._num_ex_edge_runs)
        print("Number of Ey edge runs: ", self._num_ey_edge_runs)
        print("Number of Ez edge runs: ", self._num_ez_edge_runs)
        print("Number of Hx edge runs: ", self._num_hx_edge_runs)
        print("Number of Hy edge runs: ", self._num_hy_edge_runs)
        print("Number of Hz edge runs: ", self._num_hz_edge_runs)
        print("Number of electric averaged materials: ", self._num_e_avg_mats)
        print("Number of magnetic averaged materials: ", self._num_h_avg_mats)
        print("Number of electric mesh edges using electric " + \
              "averaged materials: ", self._num_e_mesh_edges_e_avg)
        print("Number of magnetic mesh edges using electric " + \
              "averaged materials: ", self._num_h_mesh_edges_h_avg)

    def _read_edge_run_data(self):
        """Read Edge run data"""
        file_handle = open(self._file_name, 'rb')
        file_handle.seek(self._start_ex_edge_run)
        # read Ex edges
        if self._num_ex_edge_runs > 0:
            self._ex_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_ex_edge_runs)
        # read Ey edges
        if self._num_ey_edge_runs > 0:
            self._ey_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_ey_edge_runs)
        # read Ez edges
        if self._num_ez_edge_runs > 0:
            self._ez_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_ez_edge_runs)
        # read Hx edges
        if self._num_hx_edge_runs > 0:
            self._hx_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_hx_edge_runs)
        # read Hy edges
        if self._num_hy_edge_runs > 0:
            self._hy_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_hy_edge_runs)
        # read Hz edges
        if self._num_hz_edge_runs > 0:
            self._hz_edge_runs = read_edge_run_data(file_handle, \
                                                    self._num_hz_edge_runs)
        # Averaged material definitions
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
