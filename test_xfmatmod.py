#!/usr/bin/env python
"""
Test xfmatmod
"""

from __future__ import (absolute_import, division, 
                        print_function, unicode_literals)
from pathlib import Path
import sys, os
import xfmatmod

def main(argv):
    # Load XFdtd Geometry info
    fpath = argv
    xf_geom = xfmatmod.XFGeometry()
    xf_geom.file_path = fpath
    xf_geom.load_materials()
    xf_geom.load_grid_data()
    #xf_geom.print_materials()
    #xf_geom.print_grid_data()
    
    # Load XFdtd Mesh data file
    xf_mesh = xfmatmod.XFMesh()
    xf_mesh.file_path = fpath
    xf_mesh.read_mesh_header()
    xf_mesh.dump_header_info()
    xf_mesh.read_edge_run_data()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: xf_geometry.py <input_path>')
        print(sys.argv)

