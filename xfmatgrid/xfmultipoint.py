"""
XFdtd multipoint field file info and geometry.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)
import struct

MP_VERTEX_LEN = 12   # (X,Y,Z) = 4-byte uint * 3
MP_FLOAT_LEN = 4      # 4-byte float

class XFMultiPointInfo(object):
    """Hold  MultiPoint file info."""
    def __init__(self, file_name):
        self._header = ''
        self._version = 0
        self._fields_mask = 0
        self._num_points = 0
        self._load_multipoint_info(file_name)

    @property
    def header(self):
        """Return multipoint sensor file header."""
        return self._header

    @property
    def version(self):
        """Return the multipoint sensor file version."""
        return self._version

    @property
    def fields_mask(self):
        """Returns the fields mask."""
        return self._fields_mask

    @property
    def num_points(self):
        """Returns the number of points in the sensor field."""
        return self._num_points

    def _load_multipoint_info(self, file_name):
        """Load multipoint sensor info from file."""
        file_handle = open(file_name, 'rb')
        self._header = file_handle.read(4).decode("utf-8")
        self._version = struct.unpack('B', file_handle.read(1))[0]
        self._fields_mask = struct.unpack('I', file_handle.read(4))[0]
        if self._version == 0:
            self._num_points = struct.unpack('I', file_handle.read(4))[0]
        else:
            self._num_points = struct.unpack('Q', file_handle.read(8))[0]
        file_handle.close()

class XFMultiPointGeometry(object):
    """Multi Point Geometry Info"""
    def __init__(self, file_name, num_points):
        self._vertices = []
        self._num_points = num_points
        self._load_vertices(file_name)

    def _load_vertices(self, file_name):
        """Load vertices from geom.bin"""
        with open(file_name, 'rb') as file_handle:
            chunk = file_handle.read(MP_VERTEX_LEN * self._num_points)
            temp = struct.unpack('I'*3*self._num_points, chunk)
            x_val = temp[0::3]
            y_val = temp[1::3]
            z_val = temp[2::3]
            self._vertices = [[x_val[i], y_val[i], z_val[i]] 
                              for i in range(self._num_points)]
#            for ind in range(self._num_points):
#                self._vertices.append([x_val[ind], y_val[ind], z_val[ind]])
            
        file_handle.close()

class XFMultiPointFrequencies(object):
    """Extract and store steady state frequency data from frequencies.bin"""
    def __init__(self, file_name):
        self._frequencies = []
        self._load_frequencies(file_name)
        
    def _load_frequencies(self,file_name):
        """Load frequencies from frequencies.bin"""
        with open(file_name, 'rb') as file_handle:
            while True:
                chunk = file_handle.read(MP_FLOAT_LEN)
                if len(chunk) < MP_FLOAT_LEN:
                    break
                else:
                    self._frequencies.append(struct.unpack('f', chunk)[0])
        file_handle.close()
    
    @property
    def frequencies(self):
        """Return list of frequencies read from frequencies.bin"""
        return self._frequencies

class XFMultiPointSSField(object):
    """Extract steady state field values from file."""
    def __init__(self, file_name, n_points):
        self._field_data = []
        self._n_points = n_points
        self._load_field_data(file_name)

    def _load_field_data(self, file_name ):
        """Load field data from given binary file."""
        with open(file_name, 'rb') as file_handle:
            chunk = file_handle.read(MP_FLOAT_LEN*self._n_points)
            self._field_data = struct.unpack('f'*self._n_points, 
                                             chunk)
        file_handle.close()

    @property
    def ss_field(self):
        """Return field data."""
        return self._field_data
    
        

