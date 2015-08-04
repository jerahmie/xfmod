"""
Class XFMesh processes XFDtd mesh.input file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators, 
                        print_function, unicode_literals)

from pathlib import Path
import sys, os
import struct

class XFMesh:
    """
    Process mesh.input file
    """
    def __init__(self):
        self._file_path = ''
        self._file_name = ''
        self._mesh_version = None
        self._edge_run_bytes = 0
        self._edge_run_fmt = None
        self._num_ex_edge_runs = None
        self._num_ey_edge_runs = None
        self._num_ez_edge_runs = None
        self._num_hx_edge_runs = None
        self._num_hy_edge_runs = None
        self._num_hz_edge_runs = None
        self._num_e_avg_mats = None
        self._num_h_avg_mats = None
        self._num_e_mesh_edges_e_avg = None
        self._num_h_mesh_edges_h_avg = None
        self._start_ex_edge_run = 0
        self._start_ey_edge_run = 0
        self._start_ez_edge_run = 0
        
        
    @property
    def file_path(self):
        """Return full file path name for mesh.input"""
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """Set the file path for mesh.input"""
        test_file_name = os.path.join(value, 'mesh.input')
        if os.path.exists(test_file_name):
            self._file_path = test_file_name
        else:
            print("File not found: ", test_file_name)

    @file_path.deleter
    def file_path(self):
        """Delete the file path"""
        self._file_path = ''

    def read_mesh_header(self):
        """Read the mesh header."""
        fh = open(self._file_path, 'rb')
        if fh:
            # check remcom 11-byte header
            if fh.read(11) != b'!remcomfdtd':
                print("Mesh input header appears malformed: ")
                return
            if fh.read(1) != b'L':
                print("Expected little endian file format.")
                return
            if struct.unpack('H', fh.read(2))[0] != 0:
                print("Mesh input header: mesh.input not 'mesh data' type.")
                return
            self._mesh_version = struct.unpack('H', fh.read(2))[0] 
            if self._mesh_version == 0: 
                self._edge_run_bytes = 4
                self._edge_run_fmt = 'I'
            elif self._mesh_version == 1: 
                self._edge_run_bytes = 8
                self._edge_run_fmt = 'Q'
            else:
                print("Mesh input header: mesh.input not version 0 or 1.")
                return
            if struct.unpack('B', fh.read(1))[0] != 0:
                print("Mesh input header: mesh.input format " + \
                      "indicator not zeros")
                return
            # Number of Ex edge runs 
            print(self._edge_run_fmt, self._edge_run_bytes)
            self._num_ex_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of Ey edge runs
            self._num_ey_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of Ez edge runs
            self._num_ez_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of Hx edge runs
            self._num_hx_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of Hy edge runs
            self._num_hy_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of Hz edge runs
            self._num_hz_edge_runs = struct.unpack(self._edge_run_fmt, \
                                     fh.read(self._edge_run_bytes))[0]
            # Number of electric averaged materials 
            self._num_e_avg_mats = struct.unpack('I', fh.read(4))[0]
            # Number of magnetic averaged materials
            self._num_h_avg_mats = struct.unpack('I', fh.read(4))[0]
            # Number of electric mesh edges using electric averaged materials
            self._num_e_mesh_edges_e_avg = struct.unpack('Q', fh.read(8))[0]
            # Number of magnetic mesh edges using magnetic averaged materials
            self._num_h_mesh_edges_h_avg = struct.unpack('Q', fh.read(8))[0]
            self._start_ex_edge_run = fh.tell()

        else:
            print("Could not open Mesh file.")
            return
        fh.close()
        
        
    def dump_header_info(self):
        """Dump header info."""
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
        
    def read_edge_run_data(self):
        """Read Edge run data"""
        fh = open(self._file_path, 'rb')
        fh.seek(self._start_ex_edge_run)
        print(fh.tell())
        # read Ex edges
        if self._num_ex_edge_runs > 0:
            for runIndex in range(self._num_ex_edge_runs):
                xStart = struct.unpack('I', fh.read(4))[0]
                yInd = struct.unpack('I', fh.read(4))[0] 
                zInd = struct.unpack('I', fh.read(4))[0]
                xStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                if mat == 1:
                    print(runIndex, mat)
                # Assign Ex material data
                # Ex Sigma data
                # Ey Density data
        print(fh.tell())
        # read Ey edges
        if self._num_ey_edge_runs > 0:
            for runIndex in range(self._num_ey_edge_runs):
                xInd = struct.unpack('I', fh.read(4))[0]
                yStart = struct.unpack('I', fh.read(4))[0]
                zInd = struct.unpack('I', fh.read(4))[0]
                yStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                if mat == 1:
                    print(runIndex, mat)
                # Assign Ey material data
                # Ey Sigma data
                # Ey Density data
        print(fh.tell())
        # read Ez edges
        if self._num_ez_edge_runs > 0:
            for runIndex in range(self._num_ez_edge_runs):
                xInd = struct.unpack('I', fh.read(4))[0]
                yInd = struct.unpack('I', fh.read(4))[0]
                zStart = struct.unpack('I', fh.read(4))[0]
                zStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                if mat == 1:
                    print(runIndex, mat)
                # Assign Ez material data
                # Ez Sigma data
                # Ez Density data
        print(fh.tell())

        # read Hx edges
        if self._num_hx_edge_runs > 0:
            for runIndex in range(self._num_hx_edge_runs):
                xStart = struct.unpack('I', fh.read(4))[0]
                yInd = struct.unpack('I', fh.read(4))[0]
                zInd = struct.unpack('I', fh.read(4))[0]
                xStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                # Assign Hx material data
                
        # read Hy edges
        if self._num_hy_edge_runs > 0:
            for runIndex in range(self._num_hy_edge_runs):
                xInd = struct.unpack('I', fh.read(4))[0]
                yStart = struct.unpack('I', fh.read(4))[0]
                zInd = struct.unpack('I', fh.read(4))[0]
                yStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                # Assign Hy material data
                
        # read Hz edges
        if self._num_hz_edge_runs > 0:
            for runIndex in range(self._num_hz_edge_runs):
                xInd = struct.unpack('I', fh.read(4))[0]
                yInd = struct.unpack('I', fh.read(4))[0]
                zStart = struct.unpack('I', fh.read(4))[0]
                zStop = struct.unpack('I', fh.read(4))[0]
                mat = struct.unpack('B', fh.read(1))[0]
                # Assign Hz material data

        # Averaged material definitions
        # this is not implemented yet.
            
        fh.close()
