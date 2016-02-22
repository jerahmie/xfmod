#!/usr/bin/env python3
"""
Export steady-state XFdtd field results using xfmatgrid module.
"""

# Ensure python 2 and 3 compatibility
from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys
import numpy as np
import scipy.io as spio
import xfmatgrid

class XFFieldWriterNonUniform(object):
    """Writes raw XFdtd to mat file with nonuniform grid."""
    def __init__(self, xfProjectDir, simID, runID ):
        self.fieldNonUniformGrid = xfmatgrid.XFFieldNonUniformGrid(xfProjectDir,
                                                            simID,
                                                            runID)
    def exportMatFile(self, fieldType, fileName):
        """Export the field data to matlab file."""
        export_dict = dict()
        export_dict['XDim'] = self.fieldNonUniformGrid.xdim
        export_dict['YDim'] = self.fieldNonUniformGrid.ydim
        export_dict['ZDim'] = self.fieldNonUniformGrid.zdim
        export_dict[fieldType + 'x'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'x')
        export_dict[fieldType + 'y'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'y')
        export_dict[fieldType + 'z'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'z')
        spio.savemat(fileName, export_dict, oned_as='column')
        

if __name__ == "__main__":
    print("Exporting XFdtd field data on nonuniformgrid.")
    xfFieldW = XFFieldWriterNonUniform('/mnt/DATA/XFdtd_Results/KU_64_7T_Duke_Head_2mm_000002.xf',2,1)
    xfFieldW.exportMatFile('B','testB.mat')
