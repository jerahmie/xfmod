#!/usr/bin/env python3
"""
Export steady-state XFdtd field results using xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys
import numpy as np
import scipy.io as spio
import xfmatgrid

class XFFieldWriterNonUniform(object):
    """Writes raw XFdtd to mat file with nonuniform grid."""
    def __init__(self, xfProjectDir, sim_id, run_id ):
        self.fieldNonUniformGrid = xfmatgrid.XFFieldNonUniformGrid(xfProjectDir,
                                                                   sim_id,
                                                                   run_id)
    def exportMatFile(self, field_type, file_name):
        """Export the field data to matlab file."""
        export_dict = dict()
        export_dict['XDim'] = self.fieldNonUniformGrid.xdim
        export_dict['YDim'] = self.fieldNonUniformGrid.ydim
        export_dict['ZDim'] = self.fieldNonUniformGrid.zdim
        export_dict[field_type + 'x'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'x')
        export_dict[field_type + 'y'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'y')
        export_dict[field_type + 'z'] = self.fieldNonUniformGrid.ss_field_data(fieldType, 'z')
        spio.savemat(file_name, export_dict, oned_as='column')
        

if __name__ == "__main__":
    print("Exporting XFdtd field data on nonuniformgrid.")
    xfFieldW = XFFieldWriterNonUniform('/mnt/DATA/XFdtd_Results/KU_64_7T_Duke_Head_2mm_000002.xf',2,1)
    xfFieldW.exportMatFile('B','testB.mat')
