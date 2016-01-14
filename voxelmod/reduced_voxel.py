#!/usr/bin/env python3
"""
Reduces the number of materials in a Virtual Population voxel model.
"""
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os, re
from random import random
from virtual_population import *

materialPattern = re.compile('^([a-zA-Z_]*)[\s]*([a-zA-Z_]*)$')

class ReduceVoxel(object):
    """ Voxel map for reduced set of biological materials."""
    def __init__(self, voxelMapFile, voxelObject):
        self._voxelMapFile = voxelMapFile
        self._voxelMap = {}
        self._voxelMapByte = {0:0}
        self._originalVoxelObject = voxelObject
        self._reducedVoxelObject = VirtualPopulation()
        self._loadMapFromFile()
        self._remapMaterials()

    def _loadMapFromFile(self):
        """Loads the map file and create a python dictionary."""
        if not os.path.isfile(self._voxelMapFile):
            print("Could not find file: ", self._voxelMapFile)
        else:
            print("Found: ", self._voxelMapFile)
            with open(self._voxelMapFile,'r') as fh:
                mapContent = fh.readlines()
            fh.close()
            for mapString in mapContent:
                materialMatch = materialPattern.match(mapString)
                if materialMatch:
                    self._voxelMap[materialMatch.group(1)] = materialMatch.group(2)

        # Add reduced set of materials to reduced voxel object
        reducedMatMap = {}
        mapIndex = 1
        reducedMaterials = set(self._voxelMap.values())
        for mat in reducedMaterials:
            self._reducedVoxelObject.appendMaterial(mat, random(), random(), random())
            reducedMatMap[mat]=mapIndex
            mapIndex += 1
        
        # Create raw material dictionary for mapping raw voxel data
        mapIndex = 1
        for matItem in self._voxelMap:
            self._voxelMapByte[mapIndex] = reducedMatMap[self._voxelMap[matItem]]
            mapIndex += 1
    
    def _remapMaterials(self):
        """Remap the materials according to the map file and populate voxel object."""
        self._reducedVoxelObject.name = self._originalVoxelObject.name + '_reduced'
        self._reducedVoxelObject.nx = self._originalVoxelObject.nx
        self._reducedVoxelObject.ny = self._originalVoxelObject.ny
        self._reducedVoxelObject.nz = self._originalVoxelObject.nz
        self._reducedVoxelObject.dx = self._originalVoxelObject.dx
        self._reducedVoxelObject.dy = self._originalVoxelObject.dy
        self._reducedVoxelObject.dz = self._originalVoxelObject.dz
        reducedData = self._originalVoxelObject.data
        for index in range(len(reducedData)):
            reducedData[index] = self._voxelMapByte[reducedData[index]]
        self._reducedVoxelObject.data = reducedData

        
    @property
    def voxelModel(self):
        """Return the reduced voxel model object."""
        return self._reducedVoxelObject
