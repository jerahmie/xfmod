#!/usr/bin/env python
"""
Test xfmatmod
"""

from __future__ import (absolute_import, division, 
                        print_function, unicode_literals)
import sys, os
import xfmatmod

def main(argv):
    # Load XFdtd Geometry info
    fpath = argv
    xf_geom = xfmatmod.XFGeometry()
    xf_export = xfmatmod.XFGridExporter()
    xf_geom.file_path = fpath
    xf_export.materials_list = xf_geom.load_materials()
    xf_geom.load_grid_data()
    xf_export.grid_x = xf_geom.grid_data.x_coods()
    xf_export.grid_y = xf_geom.grid_data.y_coods()
    xf_export.grid_z = xf_geom.grid_data.z_coods()
    xf_geom.print_materials()
    #xf_geom.print_grid_data()

    # Load XFdtd Mesh data file
    xf_mesh = xfmatmod.XFMesh()
    xf_mesh.file_path = fpath
    xf_mesh.read_mesh_header()
    #xf_mesh.dump_header_info()
    xf_mesh.read_edge_run_data()
    xf_export.ex_edge_runs = xf_mesh.ex_edge_runs
    xf_export.ey_edge_runs = xf_mesh.ey_edge_runs
    xf_export.ez_edge_runs = xf_mesh.ez_edge_runs
    xf_export.hx_edge_runs = xf_mesh.hx_edge_runs
    xf_export.hy_edge_runs = xf_mesh.hy_edge_runs
    xf_export.hz_edge_runs = xf_mesh.hz_edge_runs

    xf_export.set_mesh_data()
    xf_export.export_mesh_data('test.mat')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: xf_geometry.py <input_path>')
        print(sys.argv)

