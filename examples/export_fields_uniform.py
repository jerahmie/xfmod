#!/usr/bin/env python3
"""
Re-grid steady-state XFdtd field data and export in matfile format.
"""

# Ensure python 2 and 3 compatibility.
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os, sys, ast, getopt
from math import sqrt
import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
import xfsystem, xfmatgrid


class XFFieldWriterUniform(object):
    """Writes XFdtd field data to mat file on uniform grid. """
    def __init__(self, xfProjectDir, simId, runId):
        self.fieldNonUniformGrid = xfmatgrid.XFFieldNonUniformGrid(xfProjectDir,
                                                                   simId,
                                                                   runId)
        self._xfSystem = xfsystem.XFSystem(xfProjectDir, simId, runId)
        self.fieldUniformGrid = None
        self._fx = None; self._fy = None; self._fz = None;
        self._xDim = None; self._yDim = None; self._zDim = None;
        self._x0 = 0.0; self._y0 = 0.0; self._z0 = 0.0;
        self._xLen = 0.0; self._yLen = 0.0; self._zLen = 0.0;
        self._dx = 0.0; self._dy = 0.0; self._dz = 0.0;
        self.netInputPower = 1
        
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

    def _regridFields(self, fieldType):
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
        fxTemp = self.fieldNonUniformGrid.ss_field_data(fieldType, 'x')
        fxReduced = self.fieldNonUniformGrid.ss_field_data(fieldType, 'x')[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]
        fyReduced = self.fieldNonUniformGrid.ss_field_data(fieldType, 'y')[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]
        fzReduced = self.fieldNonUniformGrid.ss_field_data(fieldType, 'z')[XIndex1:XIndex2, YIndex1:YIndex2, ZIndex1:ZIndex2]

        print("Interpolating Data.")
        self._xDim = np.arange(-self._xLen/2.0 + self._x0,
                               self._xLen/2.0 + self._x0,
                               self._dx)
        self._yDim = np.arange(-self._yLen/2.0 + self._y0,
                               self._yLen/2.0 + self._y0,
                               self._dy)
        self._zDim = np.arange(-self._zLen/2.0 + self._z0,
                               self._zLen/2.0 + self._z0,
                               self._dz)

        # Caculate Z indices
        ZIndices = []
        for i in range(len(self._zDim)):
            ZIndices.append(np.argmin(np.absolute(ZDimReduced-self._zDim[i])))

        # regridded field data
        self._fx = np.zeros((len(self._xDim),
                             len(self._yDim),
                             len(self._zDim)),
                            dtype=np.complex_)
        self._fy = np.zeros((len(self._xDim),
                             len(self._yDim),
                             len(self._zDim)),
                            dtype=np.complex_)

        self._fz = np.zeros((len(self._xDim),
                             len(self._yDim),
                             len(self._zDim)),
                            dtype=np.complex_)

        ZInterpIndex = 0
        X1, Y1 = np.meshgrid(XDimReduced, YDimReduced, indexing='ij')
        X2, Y2 = np.meshgrid(self._xDim, self._yDim, indexing='ij')

        for zRawIndex in ZIndices:
            sys.stdout.write("zRawIndex: %d \r" % zRawIndex)
            sys.stdout.flush()

            self._fx[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                  fxReduced[:,:,zRawIndex].ravel(),
                                                  (X2, Y2),
                                                  method='nearest')
            self._fy[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                  fyReduced[:,:,zRawIndex].ravel(),
                                                  (X2, Y2),
                                                  method='nearest')
            self._fz[:,:,ZInterpIndex] = griddata((X1.ravel(), Y1.ravel()),
                                                  fzReduced[:,:,zRawIndex].ravel(),
                                                  (X2, Y2),
                                                  method='nearest')
            ZInterpIndex += 1
        
    @property
    def netInputPower(self):
        """Net input power for simulation."""
        return self._netInputPower

    @netInputPower.setter
    def netInputPower(self, power):
        """Sett the net input power for simulation."""
        self._netInputPower = power
    
    def _scaleFields(self):
        """Normalize the field value to be net input power."""
        fieldNorm = self._netInputPower / sqrt(self._xfSystem.net_input_power)
        self._fx = self._fx * fieldNorm
        self._fy = self._fy * fieldNorm
        self._fz = self._fz * fieldNorm


    def exportMatFile(self, fieldType, fileName):
        """Export field data in mat file."""
        self._regridFields(fieldType)
        self._scaleFields()
        print("Exporting field data to mat file.")
        export_dict = dict()
        export_dict['XDim'] = self._xDim
        export_dict['YDim'] = self._yDim
        export_dict['ZDim'] = self._zDim
        export_dict[fieldType + 'x'] = self._fx
        export_dict[fieldType + 'y'] = self._fy
        export_dict[fieldType + 'z'] = self._fz
        spio.savemat(fileName, export_dict, oned_as='column')

def usage(exitStatus=None):
    """Print the usage statement and exit with given status."""
    print("")
    print("Usage: export_fields_uniform.py project [--origin='[x0,y0,z0]'] \\")
    print("                                [--lengths='[x,y,z]'] \\")
    print("                                [--deltas='[dx, dy, dz]']")
    print("  --origin: the origin coordinates, string representing a Python list.")
    print("  --lengths: dimensions of the ROI, centered at the origin, string prepresenting a Python list.")
    print("  --deltas: grid resolution, string representing a Python list.")
    print("")
    print("Example: ")
    print("  $ export_fields_uniform.py / --origin='[0.0,0.0,0.0]' --lengths='[0.01,0.01,0.02]' --deltas='[0.02, 0.02, 0.02]'")
    print("")
    if(exitStatus):
        sys.exit(exitStatus)
    else:
        sys.exit()

def main(argv):
    """Parse command line arguments and make call to exporter."""
    argDict = {}
    switches = { 'origin':list, 'lengths':list, 'deltas':list,
                 'xf_project':str, 'run':str, 'sim':str,
                 'export_file':str, 'field':str }
    singles = ''
    longForm = [x+'=' for x in switches]
    d = {x[0]+':':'--'+x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, longForm)
    except getopt.GetoptError as e:
        print("Bad argument Getopt: ", e.msg)
        usage(2)

    for opt, arg in opts:
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o=''
        if o and arg:
            if(switches[o].__name__ == 'list'):
                argDict[o]=ast.literal_eval(arg)
            else:
                argDict[o]=arg

        if not o or not isinstance(argDict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    # Get project directory
    if(not os.path.exists(argDict['xf_project'])):
        print("XFdtd project path does not exist.")
        usage(2)

    if len(argDict['origin']) != 3:
        print("Bad regrid region origin.")
        usage(2)
    if len(argDict['lengths']) != 3:
        print("Bad regrid region dimensions.")
        usage(2)
    if len(argDict['deltas']) != 3:
        print("Bad regrid resolution.")
        usage(2)

    xfFieldW = XFFieldWriterUniform(argDict['xf_project'],
                                    int(argDict['sim']),
                                    int(argDict['run']))
    xfFieldW.setOrigin(argDict['origin'][0],
                       argDict['origin'][1],
                       argDict['origin'][2])
    xfFieldW.setLen(argDict['lengths'][0],
                    argDict['lengths'][1],
                    argDict['lengths'][2])
    xfFieldW.setGridSize(argDict['deltas'][0],
                         argDict['deltas'][1],
                         argDict['deltas'][2])

    xfFieldW.exportMatFile(argDict['field'], argDict['export_file'])

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done.")
