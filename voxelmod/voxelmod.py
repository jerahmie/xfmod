"""
A python class to manipulate voxel representations.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os.path, ntpath
import re
import numpy
import vtk


class VoxelInfo(object):
    """A class to set and retrieve voxel metadata."""

    # Class variables regular expression patterns
    _VOXEL_MODEL_NAME_RE = "([a-zA-Z0-9_]*).txt$"
    _MAT_RE_PATTERN = "(^[0-9]+)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s[a-zA-Z0-9_]*/([a-zA-Z0-9_]*)"
    _NXYZ_RE_PATTERN = "^n([xyz])\s([0-9]*)"
    _DXYZ_RE_PATTERN = "^d([xyz])\s([0-9.]*)"

    def __init__(self, fileName):
        """
        Initialize instance variables and compile regular expressions.
        """
        if os.path.isfile(fileName):
            self._fileName = fileName
        else:
            raise Exception("File name: ", fileName, " does not exist." )
        print("fileName: ", self._fileName)
        self._fileHandle = None
        self._material = []
        self._nx = 0; self._ny = 0; self._nz = 0
        self._dx = 0; self._dy = 0; self._dz = 0
        self._prog_mat = re.compile(self._MAT_RE_PATTERN)
        self._prog_nxyz = re.compile(self._NXYZ_RE_PATTERN)
        self._prog_dxyz = re.compile(self._DXYZ_RE_PATTERN)

        filePath, fileTail = ntpath.split(fileName)
        m = re.match(self._VOXEL_MODEL_NAME_RE, fileTail)        
        self._modelName = m.group(1)

    @property
    def nx(self):
        return self._nx

    @property
    def ny(self):
        return self._ny

    @property
    def nz(self):
        return self._nz

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy

    @property
    def dz(self):
        return self._dz

    def material(self, matNum):
        if (0 <= matNum) and (matNum < len(self._material)):
            return self._material[matNum]
        else:
            print("Material index, ", matNum ,
                  " is out of range.  Valid range is [0,",
                  len(matNum)-1, ")")
    
    def loadVoxelInfo(self):
        """
        Load voxel metadata from .txt file
        """
        try:
            self._fileHandle = open(self._fileName, 'r')
            for line in self._fileHandle:
                m_mat = re.match(self._prog_mat, line)
                m_nxyz = re.match(self._prog_nxyz, line)
                m_dxyz = re.match(self._prog_dxyz, line)
                if m_mat:
                    # material list item has format:
                    # ['material number', 'name', RGB_Red, RGB_Green, RGB_Blue]
                    self._material.append([ m_mat.group(1),
                                            m_mat.group(5),
                                            m_mat.group(2),
                                            m_mat.group(3),
                                            m_mat.group(4) ])
                elif m_nxyz:
                    if m_nxyz.group(1) == "x":
                        self._nx = int(m_nxyz.group(2))
                    elif m_nxyz.group(1) == "y":
                        self._ny = int(m_nxyz.group(2))
                    elif m_nxyz.group(1) == "z":
                        self._nz = int(m_nxyz.group(2))
                    else:
                        print(m_nxyz.group(1), m_nxyz.group(2))
                elif m_dxyz:
                    if m_dxyz.group(1) == "x":
                        self._dx = float(m_dxyz.group(2))
                    elif m_dxyz.group(1) == "y":
                        self._dy = float(m_dxyz.group(2))
                    elif m_dxyz.group(1) == "z":
                        self._dz = float(m_dxyz.group(2))
                    else:
                        print(m_dxyz.group(1), m_dxyz.group(2))

            self._fileHandle.close()
            
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("Unexpected Error.")

    def printVoxelInfo(self):
        """Displays Voxel geometry and composition information."""
        print( "\n\n--------------------------------------------------")        
        print( "Voxel Info Summary for ", self._modelName )
        print( "--------------------------------------------------")
        print( "\nNumber of Voxel Materials: ", len(self._material))
        print( "\nGrid Extend (number of cells): " )
        print( "\tnx = ", self.nx )
        print( "\tny = ", self.ny )
        print( "\tnz = ", self.nz )
        print( "\nSpatial Steps [m]:" )
        print( "\tdx = ", self.dx )
        print( "\tdy = ", self.dy )
        print( "\tdz = ", self.dz )

class VoxelData(object):
    """A class to store voxel data"""
    def __init__(self, voxelInfo):
        self._voxelData = numpy.empty([voxelInfo.nx,
                                       voxelInfo.ny,
                                       voxelInfo.nz],
                                      dtype=byte,order='C')
    def plotVoxelData(self):
        print("plot voxel data")
#class VoxelMod(object):
#    """A class to modify voxel data."""
#    def __init__(self, voxelInfo):


