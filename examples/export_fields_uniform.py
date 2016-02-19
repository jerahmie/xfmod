#!/usr/bin/env python3
"""
Re-grid steady-state XFdtd field data and export in matfile format.
"""

# Ensure python 2 and 3 compatibility.
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
import xfmatgrid

class XFFieldWriterUniform(object):
    """Writes XFdtd field data to mat file on uniform grid. """
    def __init__(self, xfProjectDir, simID, runID):
        self.fieldNonUniformGrid = xfmatgrid.XFFieldNonUniformGrid(xfProjectDir,
                                                                   simID, 
                                                                   runID)
        self.fieldUniformGrid = None
        self._fx = None; self._fy = None; self._fz = None;
        self._xDim = None; self._yDim = None; self._zDim = None;
        self._x0 = 0.0; self._y0 = 0.0; self._z0 = 0.0;
        self._xLen = 0.0; self._yLen = 0.0; self._zLen = 0.0;
        self._dx = 0.0; self._dy = 0.0; self._dz = 0.0;
        
    def setOrigin(self, x0, y0, z0):
        """Set origin of export region."""
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0

    def setLen(self, xLen, yLen, zLen):
        """Set the dimension of the export region."""
        self._xLen = xLen
        self._yLen = yLen
        self._zLen = zLen

    def setGridSize(self, dx, dy, dz):
        """Sets the grid step size of the uniformly interpolated grid size."""
        self._dx = dx
        self._dy = dy
        self._dz = dz

    def _regridField(self, fieldType):
        """
        Resample field data on uniform grid.

        Args :
        X0 (list): The lower corner [x0, y0, z0] (mm) of the region to regrid.
        XLen (list): Dimensions of regrid region [xLen, yLen, zLen] (mm).
        dX (list): Grid spacing [dx, dy, dz] (mm).

        """

        XIndex1 = np.argmin(np.absolute(self.fieldNonUniformGrid.xdim +
                                        self._xLen/2.0 - self._x0))
        XIndex2 = np.argmin(np.absolute(self.fieldNonUniformGrid.xdim -
                                        self._xLen/2.0 - self._x0))
        YIndex1 = np.argmin(np.absolute(self.fieldNonUniformGrid.ydim +
                                        self._yLen/2.0 - self._y0))
        YIndex2 = np.argmin(np.absolute(self.fieldNonUniformGrid.ydim -
                                        self._yLen/2.0 - self._y0))
        ZIndex1 = np.argmin(np.absolute(self.fieldNonUniformGrid.zdim +
                                        self._zLen/2.0 - self._z0))
        ZIndex2 = np.argmin(np.absolute(self.fieldNonUniformGrid.zdim -
                                        self._zLen/2.0 - self._z0))

        XDimReduced = self.fieldNonUniformGrid.xdim[XIndex1:XIndex2]
        YDimReduced = self.fieldNonUniformGrid.ydim[YIndex1:YIndex2]
        ZDimReduced = self.fieldNonUniformGrid.zdim[ZIndex1:ZIndex2]

        fxReduced = np.transpose(self.fieldNonUniformGrid.ss_field_data(fieldType, 'x'), (2,1,0))
        fyReduced = np.transpose(self.fieldNonUniformGrid.ss_field_data(fieldType, 'y'), (2,1,0))
        fzReduced = np.transpose(self.fieldNonUniformGrid.ss_field_data(fieldType, 'z'), (2,1,0))
        
        print("Interpolating Data.")
        self._xDim = np.linspace(-(self._xLen/2.0 + self._x0),
                                 self._xLen/2.0 + self._x0,
                                 num=len(XDimReduced))
        self._yDim = np.linspace(-(self._yLen/2.0 + self._y0),
                                 self._yLen/2.0 + self._y0,
                                 num=len(YDimReduced))
        self._zDim = np.linspace(-(self._zLen/2.0 + self._z0),
                                 self._zLen/2.0 + self._z0,
                                 num=len(ZDimReduced))

        # Caculate Z indices
        ZIndices = []
        for i in range(len(self._zDim)):
            ZIndices.append(np.argmin(np.absolute(ZDimReduced-ZDim[i])))
        
        # regridded field data
        self._fx = np.zeros((len(self._xDim), len(self._yDim), len(self._zDim)))
        self._fy = np.zeros((len(self._xDim), len(self._yDim), len(self._zDim)))
        self._fz = np.zeros((len(self._xDim), len(self._yDim), len(self._zDim)))
        
        ZInterpIndex = 0
        for zRawIndex in ZIndices:
            print("zRawIndex: ", zRawIndex)
            self._fx[:,:,ZInterpIndex] = griddata((self._xDim, self._yDim), 
                                                  fxReduced[:,:,zRawIndex],
                                                  (XDimReduced, YDimReduced),
                                                  method='nearest')
            self._fy[:,:,ZInterpIndex] = griddata((self._xDim, self._yDim), 
                                                  fyReduced[:,:,zRawIndex],
                                                  (XDimReduced, YDimReduced),
                                                  method='nearest')
            self._fz[:,:,ZInterpIndex] = griddata((self._xDim, self._yDim ), 
                                                  fzReduced[:,:,zRawIndex],
                                                  (XDimReduced, YDimReduced), 
                                                  method='nearest')
        
    def exportMatFile(self, fieldType, fileName):
        self._regridField(fieldType)
        print("Exporting field data to mat file.")
        export_dict = dict()
        export_dict['XDim'] = self._xDim
        export_dict['YDim'] = self._yDim
        export_dict['ZDim'] = self._zDim
        export_dict[fieldType + 'x'] = self._fx
        export_dict[fieldType + 'y'] = self._fy
        export_dict[fieldType + 'z'] = self._fz
        spio.savemat(fileName, export_dict, oned_as='column')

if __name__ == "__main__":
    X0 = [0.0, -0.0257, -0.102]
    XLen = [0.050, 0.050, 0.050]
    dX = [0.002, 0.002, 0.002]

    print("Exporting XFdtd field data on UNIFORM grid.")

    xfFieldW = XFFieldWriterUniform('../Test_Data/Test_Coil.xf',1,1)
    xfFieldW.setOrigin(X0[0], X0[1], X0[2])
    xfFieldW.setLen(XLen[0], XLen[1], XLen[2])
    xfFieldW.setGridSize(dX[0], dX[1], dX[2])
    xfFieldW.exportMatFile('B','test_B_uniform.mat')
    
    print("Done.")
