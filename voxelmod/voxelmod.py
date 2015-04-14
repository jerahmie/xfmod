"""
A python class to manipulate voxel representations.
"""

import re
import numpy


class VoxelInfo(object):
    """A class to set and retrieve voxel metadata."""

    # Class variables regular expression patterns
    MAT_RE_PATTERN = "([\number]+)\s"
    # MAT_RE_PATTERN = "([\number]+)\s([0|0.|1][\number]*)\s([0|0.|1][\number]*)\s([0|0.|1][\number]*)\s[a-zA-Z0-9_]*/([a-zA-Z0-9_]*)"
    NX_RE_PATTERN = "nx\s([0-9]*)"
    NY_RE_PATTERN = "ny\s([0-9]*)"
    NZ_RE_PATTERN = "nz\s([0-9]*)"
    DX_RE_PATTERN = "dx\s([0-9.]*)"
    DY_RE_PATTERN = "dy\s([0-9.]*)"
    DZ_RE_PATTERN = "dz\s([0-9.]*)"

    def __init__(self, fileHandle=None):
        """
        Initialize instance variables and compile regular expressions
        """
        self.fileHandle = fileHandle
        self.rgbValues = []

        self.prog_mat = re.compile(r"^([0-9]+)\s(0|0.[0-9]*|1)\s([0|0.[0-9]*|1])\s([0|0.[0-9]*|1])\s[a-zA-Z0-9_]*/([a-zA-Z0-9_]*)", re.X)
        self.prog_nx = re.compile(self.NX_RE_PATTERN)
        self.prog_ny = re.compile(self.NY_RE_PATTERN)
        self.prog_nz = re.compile(self.NZ_RE_PATTERN)
        self.prog_dx = re.compile(self.DX_RE_PATTERN)
        self.prog_dy = re.compile(self.DY_RE_PATTERN)
        self.prog_dz = re.compile(self.DZ_RE_PATTERN)

    def loadVoxelInfo(self):
        if self.fileHandle:
#            try:
            for line in self.fileHandle:
#                print(line)
#                m = re.search("([0-9]+)\s",line)

                m= re.search(self.prog_mat,line)
                if m:
                    print(m.group(1), m.group(2), m.group(3),
                          m.group(4), m.group(5))
#            except AttributeError:
#                print(AttributeError)

class VoxelMod(object):
    """A class to modify voxel data."""
    def __init__(self, fileHandle=None):
        self._voxelFileHandle = fileHandle
        self.voxelData = None
        # self.
