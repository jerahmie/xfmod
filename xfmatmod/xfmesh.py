"""
Class XFMesh processes XFDtd mesh.input file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators, 
                        print_function, unicode_literals)

from pathlib import Path
import struct

class XFMesh:

    def __init__(self):
        self._fh = None
        self._file_path = ''
        
    @property
    def file_path(self):
        """Return full file path name for mesh.input"""
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """Set the file path for mesh.input"""
        test_path = Path(value)
        if test_path.exists():
            self._file_path = test_path
        else:
            print("File not found: ", value)

    @file_path.deleter
    def file_path(self):
        """Delete the file path"""
        self._file_path = ''

    def read_mesh_header(self):
        """Read the mesh header."""
        self._fh = open(self._file_path)
        if self._fh:
            # check remcom 11-byte header
            if self._fh.read(11) != r'!remcomfdtd':
                print("Mesh input header appears malformed.")
                return
            if self._fh.read(1) != r'L':
                print("Expected little endian file format.")
                return
            if struct.unpack('H', self._fh.read(2)) != 0:
                print("Mesh input head is not mesh data type.")
                return
        else:
            print("Could not open Mesh file.")
            return
        fh.close()

#    fh = open('/Data/CMRR/mesh.input', 'rb')
#    print(fh.read(11)) # remcom 11-byte header
#    print(fh.read(1))  # Endian: 'L' for little endian
#    print(struct.unpack('H',fh.read(2))[0])  # 0 for mesh data
    

