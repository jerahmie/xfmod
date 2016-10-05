#!/usr/bin/env python3
"""
Use matplotlib to plot XFdtd B field data from mat file.
"""

# Ensure python 2 and 3 compatibility
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

class Field2D(object):
    """Regrid B fields on uniform grid"""
    def __init__(self, xDim0, yDim0, field0):
        self._xdim0 = xDim0 # original dimension and field data
        self._ydim0 = yDim0
        self._field0 = field0
        self._field_regrid = None

    def regridField(self, xDim1, yDim1):
        """regrid the field"""
        X0, Y0 = np.meshgrid(self._xdim0, self._ydim0, indexing='ij')
        X1, Y1 = np.meshgrid(xDim1, yDim1, indexing='ij')
        
        self._field_regrid = griddata((X0.ravel(),
                                       Y0.ravel()),
                                      self._field0.ravel(),
                                      (X1, Y1),
                                      method='cubic')
        return self._field_regrid
        

if __name__ == '__main__':
    B = spio.loadmat('testB.mat')
    XDim = B['XDim']
    YDim = B['YDim']
    ZDim = B['ZDim']
    BNonUniform = np.sqrt(np.real(B['Bx'] * np.conjugate(B['Bx'])) + 
                             np.real(B['By'] * np.conjugate(B['By'])) +
                             np.real(B['Bz'] * np.conjugate(B['Bz'])))
    xDimUniform = np.arange(XDim[0], XDim[-1], 0.002)
    yDimUniform = np.arange(YDim[0], YDim[-1], 0.002)
    BUniform = Field2D(XDim, YDim, BNonUniform[:,:,10]).regridField(xDimUniform, yDimUniform)

    # plot the results: non-uniform
    plt.figure(1)
    X1, Y1 = np.meshgrid(XDim, YDim)
    CS = plt.pcolor(X1, Y1, BNonUniform[:,:,10].T)
    plt.axis('equal')
    plt.axis('tight')
    plt.title('|B| (non-uniform grid)')
    plt.colorbar()

    # plot the results: uniform
    plt.figure(2)
    XU, YU = np.meshgrid(xDimUniform, yDimUniform)
    plt.pcolor(XU, YU, BUniform.T)
    plt.axis('equal')
    plt.axis('tight')
    plt.title('|B| (uniform grid)')
    plt.colorbar()

    # plot the dimensions
    plt.figure(3)
    plt.subplot(2,2,1)
    plt.plot(XDim)
    plt.title('X-Dimension (non-uniform)')
    plt.subplot(2,2,2)
    plt.plot(YDim)
    plt.title('Y-Dimension (non-uniform)')
    plt.subplot(2,2,3)
    plt.plot(xDimUniform)
    plt.title('X-Dimension (uniform)')
    plt.subplot(2,2,4)
    plt.plot(yDimUniform)
    plt.title('Y-Dimension (uniform)')
    plt.show()
