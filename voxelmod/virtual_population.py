"""
A python class to represent Virtual Population voxel model info and data.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os, ntpath
from os.path import sep
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
        self._data = None

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
    def data(self):
        """Return the Raw Voxel Data"""
        return self._data

    @data.setter
    def data(self, value):
        """Set the raw voxel data."""
        self._data = value

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

    def appendMaterial(self, materialName, RGB_Red, RGB_Green, RGB_Blue):
        """
        Add a material to the end of the list with optional RGB color.
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
    """Class to populate Virtual Population voxel object with data from file."""

    # Class variables regular expression patterns
    _VOXEL_MODEL_NAME_RE = "([a-zA-Z0-9_.]*).txt$"
    _MAT_RE_PATTERN = "(^[0-9]+)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([a-zA-Z0-9_/]*)"
    _NXYZ_RE_PATTERN = "^n([xyz])\s([0-9]*)"
    _DXYZ_RE_PATTERN = "^d([xyz])\s([0-9.]*)"

    def __init__(self):
        """
        Initialize instance variables and compile regular expressions.
        """
        self._prog_mat = re.compile(self._MAT_RE_PATTERN)
        self._prog_nxyz = re.compile(self._NXYZ_RE_PATTERN)
        self._prog_dxyz = re.compile(self._DXYZ_RE_PATTERN)
        self._voxelModel = VirtualPopulation()

    @property
    def voxelModel(self):
        """Returns Virtual Population model instance."""
        return self._voxelModel

    def loadData(self, fileName):
        """Load raw voxel data from file."""
        if not os.path.isfile(fileName):
            raise Exception("File name: ", fileName, " does not exist.")
        try:
            fileHandle = open(fileName, 'rb')
            self._voxelModel.data = bytearray(fileHandle.read())
            fileHandle.close()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys_exc_info()[0])
            raise Exception("Unexpected Error.")

    def loadInfo(self, fileName):
        """Load voxel metadata from .txt file."""
        if not os.path.isfile(fileName):
            raise Exception("File name: ", fileName, " does not exist.")

        filePath, fileTail = ntpath.split(fileName)
        m = re.match(self._VOXEL_MODEL_NAME_RE, fileTail)
        self._voxelModel.name = m.group(1)

        try:
            fileHandle = open(fileName, 'r')
            for line in fileHandle:
                m_mat = re.match(self._prog_mat, line)
                m_nxyz = re.match(self._prog_nxyz, line)
                m_dxyz = re.match(self._prog_dxyz, line)
                if m_mat:
                    self._voxelModel.appendMaterial(m_mat.group(5),
                                                    float(m_mat.group(2)),
                                                    float(m_mat.group(3)),
                                                    float(m_mat.group(4)))
                elif m_nxyz:
                    if m_nxyz.group(1) == "x":
                        self._voxelModel.nx = int(m_nxyz.group(2))
                    elif m_nxyz.group(1) == "y":
                        self._voxelModel.ny = int(m_nxyz.group(2))
                    elif m_nxyz.group(1) == "z":
                        self._voxelModel.nz = int(m_nxyz.group(2))
                    else:
                        print(m_nxyz.group(1), m_nxyz.group(2))
                elif m_dxyz:
                    if m_dxyz.group(1) == "x":
                        self._voxelModel.dx = float(m_dxyz.group(2))
                    elif m_dxyz.group(1) == "y":
                        self._voxelModel.dy = float(m_dxyz.group(2))
                    elif m_dxyz.group(1) == "z":
                        self._voxelModel.dz = float(m_dxyz.group(2))
                    else:
                        print(m_dxyz.group(1), m_dxyz.group(2))
            fileHandle.close()

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("Unexpected Error.")

class VirtualPopulationWriter(object):
    """Class to write Virtual Population data to file."""
    def __init__(self):
        self._fileNameInfo = ''
        self._fileNameData = ''
        self._filePath = os.getcwd()
        self._voxelModel = None

    @property
    def voxelModel(self):
        """Return the current Voxel Model."""
        return self._voxelModel

    @voxelModel.setter
    def voxelModel(self, value):
        """Set the current voxel model."""
        self._voxelModel = value

    @property
    def filePath(self):
        """Return the current path where voxel data is to be saved."""
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        """Set the path where voxel data is to be saved."""
        if os.path.isdir(value):
            self._filePath = value
        else:
            print("Directory (", value, ") not found.")
            return -1

    def writeVoxelToFile(self):
        """
        Save Voxel object data to text file formatted using the itis Virtual
        Family metadata format.
        """
        if not self._voxelModel:
            print("Voxel object not defined.")
        else:
            self._fileNameInfo = os.path.realpath(self._filePath + sep + \
                                                  self._voxelModel.name + '.txt')
            self._fileNameData = os.path.realpath(self._filePath + sep + \
                                                  self._voxelModel.name + '.raw')
            # Write metadata file
            try:
                fileHandle = open(self._fileNameInfo, 'w')
                # write materials
                for index in range(1,self._voxelModel.numMaterials):
                    material = self._voxelModel.material(index)
                    fileHandle.write(str(material[0]) + '\t' + \
                                     "{0:.6f}".format(material[2]) + '\t' + \
                                     "{0:.6f}".format(material[3]) + '\t' + \
                                     "{0:.6f}".format(material[4]) + '\t' + \
                                     material[1] + '\n')
                # write grid extents
                fileHandle.write('\nGrid extent (number of cells)\n')
                fileHandle.write('nx\t' + str(self._voxelModel.nx) + '\n')
                fileHandle.write('ny\t' + str(self._voxelModel.ny) + '\n')
                fileHandle.write('nz\t' + str(self._voxelModel.nz) + '\n')

                # write spatial steps (resolution)
                fileHandle.write('\nSpatial steps [m]\n')
                fileHandle.write('dx\t' + str(self._voxelModel.dx) + '\n')
                fileHandle.write('dy\t' + str(self._voxelModel.dy) + '\n')
                fileHandle.write('dz\t' + str(self._voxelModel.dz) + '\n')

                fileHandle.close()
            except IOError as e:
                print("I/O Error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise Exception("Unexpected Error.")

            # Write binary data file

            try:
                fileHandle = open(self._fileNameData, 'wb')
                fileHandle.write(self._voxelModel.data)
                fileHandle.close()
            except IOError as e:
                print("I/O Error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise Exception("Unexpected Error.")
