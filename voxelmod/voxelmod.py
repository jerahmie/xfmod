"""
A python class to manipulate voxel representations.
"""

import re
import numpy


class VoxelInfo(object):
    """A class to set and retrieve voxel metadata."""

    # Class variables regular expression patterns
    #MAT_RE_PATTERN = "([\number]+)\s"
    MAT_RE_PATTERN = "(^[0-9]+)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s[a-zA-Z0-9_]*/([a-zA-Z0-9_]*)"
    NXYZ_RE_PATTERN = "^n([xyz])\s([0-9]*)"
    DXYZ_RE_PATTERN = "^d([xyz])\s([0-9.]*)"


    def __init__(self, fileHandle=None):
        """
        Initialize instance variables and compile regular expressions
        """
        self.fileHandle = fileHandle
        self.rgbValues = []
        #        self.prog_mat = re.compile(r"^([0-9]+)\s(0|0.[0-9]*|1)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s[a-zA-Z0-9_]*/([a-zA-Z0-9_]*)", re.X)
        self.prog_mat = re.compile(self.MAT_RE_PATTERN)
        self.prog_nxyz = re.compile(self.NXYZ_RE_PATTERN)
        self.prog_dxyz = re.compile(self.DXYZ_RE_PATTERN)


    def loadVoxelInfo(self):
        if self.fileHandle:
            for line in self.fileHandle:
                m_mat = re.match(self.prog_mat, line)
                m_nxyz = re.match(self.prog_nxyz, line)
                m_dxyz = re.match(self.prog_dxyz, line)
                if m_mat:
                    print(m_mat.group(1), m_mat.group(2), m_mat.group(3),
                          m_mat.group(4), m_mat.group(5))
                elif m_nxyz:
                    print(m_nxyz.group(1), m_nxyz.group(2))
                elif m_dxyz:
                    print(m_dxyz.group(2), m_dxyz.group(2))
                    
class VoxelMod(object):
    """A class to modify voxel data."""
    def __init__(self, fileHandle=None):
        self._voxelFileHandle = fileHandle
        self.voxelData = None
        # self.
