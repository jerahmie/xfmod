#!/usr/bin/env python3
"""
Export steady-state XFdtd field results using xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

# Ensure python 2 and 3 compatibility
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
        export_dict[fieldType + 'x'] = self.fieldNonUniformGrid.ss_field_data(fieldName, 'x')
        export_dict[fieldType + 'y'] = self.fieldNonUniformGrid.ss_field_data(fieldName, 'y')
        export_dict[fieldType + 'z'] = self.fieldNonUniformGrid.ss_field_data(fieldName, 'z')
        spio.savemat(fileName, export_dict, oned_as='column')
        

if __name__ == "__main__":
    print("Exporting XFdtd field data on nonuniformgrid.")
    
    
