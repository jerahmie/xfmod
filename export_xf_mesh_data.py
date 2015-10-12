#!/usr/bin/env python
"""
Convert XFdtd geometry.input and material.input data to Mat file format.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys, os
from xfmatgrid.xfutils import xf_run_id_to_str, xf_sim_id_to_str
import xfgeomod

def main(input_path, sim_id, run_id, output_path):
    """ Convert XFdtd grid & mesh data."""
    xf_sim_run_path = os.path.join(input_path, 'Simulations',
                                   xf_sim_id_to_str(sim_id),
                                   xf_run_id_to_str(run_id))

    if not os.path.exists(xf_sim_run_path):
        print("Error: ", xf_sim_run_path , " does not exist.")
        return

    # Load XFdtd Geometry info
    xf_geom = xfgeomod.XFGeometry(xf_sim_run_path)
    xf_geom.print_materials()
    xf_geom.print_grid_data()

    # Load XFdtd Mesh data file
    xf_mesh = xfgeomod.XFMesh(xf_sim_run_path)

    # Setup exporter and write to mat file
    xf_export = xfgeomod.XFGridExporter(xf_geom, xf_mesh)
    xf_export.units = 'mm'
    xf_export.export_mesh_data(output_path)

def usage():
    print('Usage: xf_geometry.py <input_path> <sim #> <run #> <output_path>')

if __name__ == "__main__":
    if len(sys.argv) == 5:
        if not os.path.exists(sys.argv[1]):
            print("Could not find: ",  sys.argv[1])
            usage()
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        usage()
        print(sys.argv)
