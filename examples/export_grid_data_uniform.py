#!/usr/bin/env python3
"""
Example grid data exporter on uniform grid.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os, sys
import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
from xfmatgrid.xfutils import xf_run_id_to_str, xf_sim_id_to_str
import xfgeomod


class XFGridDataWriterUniform(object):
    """Write XFdtd field data to mat file on uniform grid."""
    def __init__(self, xfProjectDir, simId, runId):
        

def quick_regrid(gridExporter):
    """quick exporter with regrid"""
    dx=0.002; dy=0.002; dz=0.002
    x0=0.0; y0=0.0; z0=0.05;
    xLen=0.256; yLen=0.256; zLen=0.350
    
    print("regridding mesh data.")
    nu_grid_x = np.array(gridExporter.grid_x)
    nu_grid_y = np.array(gridExporter.grid_y)
    nu_grid_z = np.array(gridExporter.grid_z)
    XIndex1 = np.argmin(np.absolute(nu_grid_x + xLen/2.0 - x0))
    XIndex2 = np.argmin(np.absolute(nu_grid_x - xLen/2.0 - x0))
    YIndex1 = np.argmin(np.absolute(nu_grid_y + yLen/2.0 - y0))
    YIndex2 = np.argmin(np.absolute(nu_grid_y - yLen/2.0 - y0))
    ZIndex1 = np.argmin(np.absolute(nu_grid_z + zLen/2.0 - z0))
    ZIndex2 = np.argmin(np.absolute(nu_grid_z - zLen/2.0 - z0))
    XDimReduced = nu_grid_x[XIndex1:XIndex2]
    YDimReduced = nu_grid_y[YIndex1:YIndex2]
    ZDimReduced = nu_grid_z[ZIndex1:ZIndex2]
    
    ExSigma = np.transpose(gridExporter._mesh_ex_sigma,(2,1,0))    
    EySigma = np.transpose(gridExporter._mesh_ey_sigma,(2,1,0))
    EzSigma = np.transpose(gridExporter._mesh_ez_sigma,(2,1,0))
    print("After transpose: ", np.shape(EzSigma))

    ExSigmaReduced = ExSigma[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]
    EySigmaReduced = EySigma[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]
    EzSigmaReduced = EzSigma[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]

    print("Interpolating data.")
    xDimUniform = np.arange(-xLen/2.0 + x0, xLen/2.0 + x0, dx)
    yDimUniform = np.arange(-yLen/2.0 + y0, yLen/2.0 + y0, dy)
    zDimUniform = np.arange(-zLen/2.0 + z0, zLen/2.0 + z0, dz)

    # calculate z indices
    ZIndices = []
    for i in range(len(zDimUniform)):
        ZIndices.append(np.argmin(np.absolute(ZDimReduced-zDimUniform[i])))

    ExSigmaUniform = np.zeros((len(xDimUniform), len(yDimUniform), len(zDimUniform)))
    EySigmaUniform = np.zeros((len(xDimUniform), len(yDimUniform), len(zDimUniform)))
    EzSigmaUniform = np.zeros((len(xDimUniform), len(yDimUniform), len(zDimUniform)))
    ZInterpIndex = 0
    X1, Y1 = np.meshgrid(XDimReduced, YDimReduced, indexing='ij')
    X2, Y2 = np.meshgrid(xDimUniform, yDimUniform, indexing='ij')

    for zRawIndex in ZIndices:
        sys.stdout.write("zRawIndex: %d \r" % zRawIndex)
        sys.stdout.flush()
        ExSigmaUniform[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                    ExSigmaReduced[:,:,zRawIndex].ravel(),
                                                    (X2, Y2), method='nearest')
        EySigmaUniform[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                    EySigmaReduced[:,:,zRawIndex].ravel(),
                                                    (X2, Y2), method='nearest')
        EzSigmaUniform[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                    EzSigmaReduced[:,:,zRawIndex].ravel(),
                                                    (X2, Y2), method='nearest')
        ZInterpIndex += 1

    exportDict={}
    exportDict['XDim'] = xDimUniform
    exportDict['YDim'] = yDimUniform
    exportDict['ZDim'] = zDimUniform
    exportDict['ExSigma'] = ExSigmaUniform
    exportDict['EySigma'] = EySigmaUniform
    exportDict['EzSigma'] = EzSigmaUniform
    spio.savemat('conductivity_mask.mat', exportDict, oned_as='column')
    

def main(xfProjectDir, simId, runId):
    if os.path.isdir(xfProjectDir):
        print("found: ", xfProjectDir)
    runDir=os.path.join(xfProjectDir, 'Simulations',
                        xf_sim_id_to_str(simId),
                        xf_run_id_to_str(runId))
    if os.path.isdir(runDir):
        print("found: ", runDir)

    xfGeometry = xfgeomod.XFGeometry(os.path.join(xfProjectDir,
                                                  'Simulations',
                                                  xf_sim_id_to_str(simId),
                                                  xf_run_id_to_str(runId)))
    xfMesh = xfgeomod.XFMesh(os.path.join(xfProjectDir,
                                          'Simulations',
                                          xf_sim_id_to_str(simId),
                                          xf_run_id_to_str(runId)))
    gridExporter = xfgeomod.XFGridExporter(xfGeometry, xfMesh)

    print(np.shape(gridExporter._grid_x))
    print(np.shape(gridExporter._grid_y))
    print(np.shape(gridExporter._grid_z))
    print(np.shape(gridExporter._mesh_ey_sigma))
    quick_regrid(gridExporter)
    

if __name__ == '__main__':
    main('/mnt/DATA/XFdtd_Results/Dipole_Coil_10p5T_Phantom.xf', 1, 1)

