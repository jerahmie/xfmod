"""
XFdtd multipoint field file info and geometry.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)
import struct
import numpy as np
import line_profiler

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
        self._num_points = num_points
        self._load_vertices(file_name)

    def _load_vertices(self, file_name):
        """Load vertices from geom.bin"""
        with open(file_name, 'rb') as file_handle:
            chunk = file_handle.read(MP_VERTEX_LEN * self._num_points)
            temp = struct.unpack('I'*3*self._num_points, chunk)
            x_val = np.transpose(np.array([temp[0::3]]))
            y_val = np.transpose(np.array([temp[1::3]]))
            z_val = np.transpose(np.array([temp[2::3]]))
            self._vertices = np.hstack((x_val, y_val, z_val))
            self._x_domain = np.unique(x_val)
            self._y_domain = np.unique(y_val)
            self._z_domain = np.unique(z_val)
        file_handle.close()

    @property
    def x_domain(self):
        """Return the unique x domain index values."""
        return self._x_domain

    @property
    def y_domain(self):
        """Return the unique y domain index values."""
        return self._y_domain

    @property
    def z_domain(self):
        """Return the unique z domain index values."""
        return self._z_domain

    @property
    def vertices(self):
        """Return the vertex index array."""
        return self._vertices

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
    def __init__(self, file_name, mp_info, mp_geometry):
        self._num_points = mp_info.num_points
        self._mp_geom = mp_geometry
        self._load_field_data(file_name)

#    @profile
    def _load_field_data(self, file_name ):
        """Load field data from given binary file."""
        with open(file_name, 'rb') as file_handle:
            chunk = file_handle.read(MP_FLOAT_LEN*self._num_points)
            temp_field_data = struct.unpack('f'*self._num_points,
                                             chunk)
        file_handle.close()
        self._ss_field = np.empty([len(self._mp_geom.x_domain),
                                  len(self._mp_geom.y_domain),
                                  len(self._mp_geom.z_domain)])

        min_i_domain = np.amin(self._mp_geom.x_domain)
        min_j_domain = np.amin(self._mp_geom.y_domain)
        min_k_domain = np.amin(self._mp_geom.z_domain)

        ind_i = self._mp_geom.vertices[:,0] - min_i_domain
        ind_j = self._mp_geom.vertices[:,1] - min_j_domain
        ind_k = self._mp_geom.vertices[:,2] - min_k_domain
        
#        self._ss_field[ind_i[:]][ind_j[:]][ind_k[:]] = temp_field_data[:]
#        for index in range(len(temp_field_data)):
#            self._ss_field[ind_i[index]][ind_j[index]][ind_k[index]] = \
#                temp_field_data[index]
#        for index in range(len(temp_field_data)):
#            self._ss_field[ind_i[index],ind_j[index],ind_k[index]] = temp_field_data[index]
        self._ss_field[ind_i,ind_j,ind_k] = temp_field_data

    @property
    def ss_field(self):
        """Return field data."""
        return self._ss_field
