#!/usr/bin/env python
"""
Export mat files for given XFdtd results project.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import sys, os
import scipy.io as spio
import xfmatgrid

def main(xf_project_name):
    """Export data."""
    field_nugrid = xfmatgrid.XFFieldNonUniformGrid(xf_project_name, 1, 1)
    export_dict = dict()
    export_dict['X_Dimension_3'] = field_nugrid.xdim
    export_dict['Y_Dimension_2'] = field_nugrid.ydim
    export_dict['Z_Dimension_1'] = field_nugrid.zdim
    export_dict['Bx'] = field_nugrid.ss_field_data('B', 'x')
    export_dict['By'] = field_nugrid.ss_field_data('B', 'y')
    export_dict['Bz'] = field_nugrid.ss_field_data('B', 'z')
    spio.savemat('test.mat', export_dict)

if __name__ == "__main__":
    xf_project_dir = os.path.join('/Data','CMRR','rf_coil_scripts',
                               'python', 'Test_Data', 'Test_Coil.xf')
    if os.path.exists(xf_project_dir):
        main(xf_project_dir)
    else:
        print("Could not find XFdtd project: ", xf_project_dir)
