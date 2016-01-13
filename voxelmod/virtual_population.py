"""
A python class to represent Virtual Population voxel model info and data.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os.path, ntpath
from random import random
import re

class VirtualPopulation(object):
    """Holds Virtual Population """
    def __init__(self):
        self._name = ''
        self._nx = 0; self._ny = 0; self._nz = 0
        self._dx = 0; self._dy = 0; self._dz = 0
        self._materials = [[int('0'),
                           'Free Space',
                           float('0'), float('0'), float('0')]]

    @property
    def name(self):
        """Returns name of Voxel Model."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the Voxel Model name."""
        self._name = value

    @property
    def nx(self):
        """Returns x-dimension of voxel object."""
        return self._nx

    @nx.setter
    def nx(self, value):
        """Sets x-dimension of voxel object."""
        self._nx = value

    @property
    def ny(self):
        """Returns y-dimension of voxel object."""
        return self._ny

    @ny.setter
    def ny(self, value):
        """Sets y-dimension of voxel object."""
        self._ny = value

    @property
    def nz(self):
        """Returns z-dimension of voxel object."""
        return self._nz

    @nz.setter
    def nz(self, value):
        """Sets z-dimension of voxel object."""
        self._nz = value

    @property
    def dx(self):
        """Returns delta-x of voxel object."""
        return self._dx

    @dx.setter
    def dx(self, value):
        """Sets delta-x of voxel object."""
        self._dx = value

    @property
    def dy(self):
        """Returns delta-y of voxel object."""
        return self._dy

    @dy.setter
    def dy(self, value):
        """Sets delta-y of voxel object."""
        self._dy = value

    @property
    def dz(self):
        """Returns delta-z of voxel object."""
        return self._dz

    @dz.setter
    def dz(self, value):
        """Sets delta-z of voxel object."""
        self._dz = value

    @property
    def numMaterials(self):
        """Returns the number of materials in voxel object."""
        return len(self._materials)

    def material(self, matNum):
        """Returns the material at specified location."""
        if (0 <= matNum) and (matNum < len(self._materials)):
            return self._materials[matNum]
        else:
            print("Material index, ", matNum ,
                  " is out of range.  Valid range is [0,",
                  len(matNum)-1, ")")

    def appendMaterial(self, materialName, RGB_Red = random(),
                       RGB_Green=random(), RGB_Blue = random()):
        """
        Add a material to the end of the list with optional RGB color.
        If no color is provided, a random rgb value is assigned.
        """
        self._materials.append([self.numMaterials, materialName, 
                                RGB_Red, RGB_Green, RGB_Blue])

    def removeMaterial(self, materialName ):
        """Remove material with given name."""
        matRemove = []
        for matIndex in range(len(self._materials)):
            if self._materials[matIndex][1] == materialName:
                matRemove.append(matIndex)
        for matIndex in matRemove:
            del(self._materials[matIndex])
        self._renumberMaterials()

    def _renumberMaterials(self):
        """Fix material numbering after removal."""
        index = 0
        for mat in self._materials:
            mat[0] = index
            index+=1
                

class VirtualPopulationReader(object):
    """A class to population Virtual Population voxel data from file."""

    # Class variables regular expression patterns
    _VOXEL_MODEL_NAME_RE = "([a-zA-Z0-9_.]*).txt$"
    _MAT_RE_PATTERN = "(^[0-9]+)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([a-zA-Z0-9_/]*)"
    _NXYZ_RE_PATTERN = "^n([xyz])\s([0-9]*)"
    _DXYZ_RE_PATTERN = "^d([xyz])\s([0-9.]*)"

    def __init__(self):
        """
        Initialize instance variables and compile regular expressions.
        """
        self._fileName = ''
        self._fileHandle = None
        self._prog_mat = re.compile(self._MAT_RE_PATTERN)
        self._prog_nxyz = re.compile(self._NXYZ_RE_PATTERN)
        self._prog_dxyz = re.compile(self._DXYZ_RE_PATTERN)
        self._voxelModel = VirtualPopulation()

    @property
    def voxelModel(self):
        """Returns Virtual Population model instance."""
        return self._voxelModel

    def loadVoxelInfo(self, fileName):
        """
        Load voxel metadata from .txt file
        """
        if os.path.isfile(fileName):
            self._fileName = fileName
        else:
            raise Exception("File name: ", fileName, " does not exist.")
        print("fileName: ", self._fileName)
        
        filePath, fileTail = ntpath.split(fileName)
        m = re.match(self._VOXEL_MODEL_NAME_RE, fileTail)        
        self._voxelModel.name = m.group(1)        

#        try:
#            self._fileHandle = open(self._fileName, 'r')
#            for line in self._fileHandle:
#                m_mat = re.match(self._prog_mat, line)
#                m_nxyz = re.match(self._prog_nxyz, line)
#                m_dxyz = re.match(self._prog_dxyz, line)
#                if m_mat:
#                   # material list item has format:
#                    # ['material number', 'name', RGB_Red, RGB_Green, RGB_Blue]
#                    self._material.append([ int(m_mat.group(1)),
#                                            m_mat.group(5),
#                                            float(m_mat.group(2)),
#                                            float(m_mat.group(3)),
#                                            float(m_mat.group(4)) ])
#                elif m_nxyz:
#                    if m_nxyz.group(1) == "x":
#                        self._nx = int(m_nxyz.group(2))
#                    elif m_nxyz.group(1) == "y":
#                        self._ny = int(m_nxyz.group(2))
#                    elif m_nxyz.group(1) == "z":
#                        self._nz = int(m_nxyz.group(2))
#                    else:
#                        print(m_nxyz.group(1), m_nxyz.group(2))
#                elif m_dxyz:
#                    if m_dxyz.group(1) == "x":
#                        self._dx = float(m_dxyz.group(2))
#                    elif m_dxyz.group(1) == "y":
#                        self._dy = float(m_dxyz.group(2))
#                    elif m_dxyz.group(1) == "z":
#                        self._dz = float(m_dxyz.group(2))
#                    else:
#                        print(m_dxyz.group(1), m_dxyz.group(2))
#
#            self._fileHandle.close()
#            
#        except IOError as e:
#            print("I/O error({0}): {1}".format(e.errno, e.strerror))
#        except:
#            print("Unexpected error:", sys.exc_info()[0])
#            raise Exception("Unexpected Error.")
#
#    def printVoxelInfo(self):
#        """Displays Voxel geometry and composition information."""
#        print( "\n\n--------------------------------------------------")        
#        print( "Voxel Info Summary for ", self._modelName )
#        print( "--------------------------------------------------")
#        print( "\nNumber of Voxel Materials: ", len(self._material))
#        print( "\nGrid Extend (number of cells): " )
#        print( "\tnx = ", self.nx )
#        print( "\tny = ", self.ny )
#        print( "\tnz = ", self.nz )
#        print( "\nSpatial Steps [m]:" )
#        print( "\tdx = ", self.dx )
#        print( "\tdy = ", self.dy )
#        print( "\tdz = ", self.dz )

