#!/usr/bin/env python3
"""
Export steady-state XFdtd field results using xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

from xfwriter import XFGridDataWriterNonUniform, XFFieldWriterNonUniform

if __name__ == "__main__":
    xf_project = '/run/media/jerahmie/Scratch/Loop_Dipole_10p5T_V3_Phantom.xf'
    xf_sim_id = 4
    xf_run_id = 1
    print("Exporting XFdtd grid data on nonunoform grid.")
    xfGridW = XFGridDataWriterNonUniform(xf_project, xf_sim_id, xf_run_id)
    xfGridW.savemat('Loop_Dipole_V3_Phantom_Loop_grid.mat')
    
    print("Exporting XFdtd field data on nonuniform grid.")
    #xfFieldW = XFFieldWriterNonUniform('/mnt/DATA/XFdtd_Projects/Loop_Dipole_10p5T_V2_Phantom.xf',18,1)
    xfFieldW = XFFieldWriterNonUniform(xf_project, xf_sim_id, xf_run_id)
    xfFieldW.net_input_power = 1.0
    #xfFieldW.savemat('E','Loop_Dipole_V3_Phantom_Loop_E.mat')
    #xfFieldW.savemat('B','Loop_Dipole_V3_Phantom_Loop_B.mat')
