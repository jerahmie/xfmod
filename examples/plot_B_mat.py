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


if __name__ == '__main__':
    B = spio.loadmat('testB.mat')
    BU = spio.loadmat('test_B_uniform.mat')
    XDim = B['XDim']; YDim = B['YDim']; ZDim = B['ZDim']
    XDimU = BU['XDim']; YDimU = BU['YDim']; ZDimU = BU['ZDim']
    BModNonUniform = np.sqrt(np.real(B['Bx'] * np.conjugate(B['Bx'])) + 
                             np.real(B['By'] * np.conjugate(B['By'])) +
                             np.real(B['Bz'] * np.conjugate(B['Bz'])))
    BModUniform = np.sqrt(np.real(BU['Bx'] * np.conjugate(BU['Bx'])) + 
                          np.real(BU['By'] * np.conjugate(BU['By'])) +
                          np.real(BU['Bz'] * np.conjugate(BU['Bz'])))
    # plot the results: non-uniform
    zIndex=10
    zUIndex=75
    plt.figure(1)
    X1, Y1 = np.meshgrid(XDim, YDim)
    print("Len ZDim: ", len(ZDim))
    print("Len ZDimU: ", len(ZDimU))
    CS = plt.pcolor(X1, Y1, BModNonUniform[:,:,zIndex].T)
    plt.axis('equal')
    plt.axis('tight')
    plt.title('|B| (non-uniform grid, z=%f)' % ZDim[zIndex])
    plt.colorbar()

    # plot the results: uniform
    plt.figure(2)
    XU, YU = np.meshgrid(XDimU, XDimU)
    plt.pcolor(XU, YU, BModUniform[:,:,zUIndex].T)
    plt.axis('equal')
    plt.axis('tight')
    plt.title('|B| (uniform grid, z=%f)' % ZDimU[zUIndex])
    plt.colorbar()

    # show the plot figures.
    plt.show()
