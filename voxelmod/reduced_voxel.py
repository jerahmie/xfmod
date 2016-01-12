#!/usr/bin/env python3

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os, re
from random import random
from voxelinfo import VoxelInfo

material_pattern = re.compile('^([a-zA-Z_]*)[\s]*([a-zA-Z_]*)$')
#fh = open('full_materials.raw','rb');
#rawBytes = bytearray(fh.read());
#
#fh.close()

class ReducedVoxelMap(object):
    """ Voxel map for reduced set of biological materials."""
    def __init__(self, voxel_map_file):
        self._voxel_map_file = voxel_map_file
        self._voxel_map = {}
        self._load_map_from_file()

    def _load_map_from_file(self):
        """Loads the map file and create a python dictionary."""
        if not os.path.isfile(self._voxel_map_file):
            print("Could not find file: ", self._voxel_map_file)
        else:
            print("Found: ", self._voxel_map_file)
            with open(self._voxel_map_file,'r') as fh:
                map_content = fh.readlines()
            fh.close()
            for map_string in map_content:
                material_match = material_pattern.match(map_string)
                if material_match:
                    self._voxel_map[material_match.group(1)] = material_match.group(2)

    @property
    def voxel_map(self):
        return self._voxel_map

class VoxelWriter(object):
    """Writes a voxel material file for given material set and dimensions."""
    def __init__(self):
        self._voxel_info = None
        self._voxel_data = None
        self._voxel_name = ''
        self._voxel_path = ''
        self._material_color = []

    def _add_material_colors(self):
        """Fill material colors."""
        for index in range(len(self._material_color),
                           self._voxel_info.numMaterials):
            self._material_color.append([random(), random(), random()])
        
    def write_voxel_files(self):
        """Writes voxel data and description file."""
        if len(self._material_colors) < self._voxel_info.numMaterials:
            print("[INFO] VoxelWriter: appending random material colors.")
            self._add_material_colors()
            
        fh_txt = open(self._voxel_name + '.txt', 'w')
            for index in range(len(self._voxel_info.numMaterials)):
                fh_text.write(index, '\t',
                              "{0:.6f}".format(self._material_color[index][0]),
                              '\t',
                              "{0:.6f}".format(self._material_color[index][1]),
                              '\t',
                              "{0:.6f}".format(self._material_color[index][2]),
                              '\t', self._voxel_info.material(index), '\n')

            fh_text.write('\nGrid extent (number of cells)\n')
            fh_text.write('nx\t',str(self._nx),'\n')
            fh_text.write('ny\t',str(self._ny),'\n')
            fh_text_write('nz\t',str(self._nz),'\n')
            fh_text.write('\nSpatial stems [m]\n')
            fh_text.write('dx\t',str(self._dx),'\n')
            fh_text.write('dy\t',str(self._dy),'\n')
            fh_text.write('dz\t',str(self._dz),'\n')
            fh_txt.close()

        @property
        def voxel_name(self):
            return self._voxel_name
        @property
        def voxel_path(self):
            return self._voxel_path
        @property
        def material_color(self):
            return self._material_color
            
#        if not self._voxel_data:
#            print('[ERROR] VoxelWriter: Voxel data is empty.')
#        else:
#            fh_raw = open(self._voxel_name + '.raw', 'wb')
#
#            fh_raw.close()
    
