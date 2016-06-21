#!/usr/bin/env python3
"""
Vopgen writers for all mat files.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys
import ast
import getopt
import scipy.io as spio
from xfutils.xfproject import XFProjectInfo
import xfwriter.vopgen

def vopgen_all(arg_dict):
    """Run all vopgen writers."""
    # make output directory if it doesn't exist
    if not os.path.exists(arg_dict['export_dir']):
        os.makedirs(arg_dict['export_dir'])

    # E field map
    print("-> Generating E field map.")
    sim_ids = []
    project_info = XFProjectInfo(arg_dict['xf_project'])
    simulations = project_info.xf_sim_run_list
    for idx, sim in enumerate(simulations):
        if sim[0]:
            sim_ids.append(idx+1)

    ef_map = xfwriter.vopgen.VopgenEFMapArrayN(arg_dict['xf_project'], sim_ids)
    ef_map.set_grid_origin(arg_dict['origin'][0],
                           arg_dict['origin'][1],
                           arg_dict['origin'][2])
    ef_map.set_grid_len(arg_dict['lengths'][0],
                        arg_dict['lengths'][1],
                        arg_dict['lengths'][2])
    ef_map.set_grid_resolution(arg_dict['deltas'][0],
                               arg_dict['deltas'][1],
                               arg_dict['deltas'][2])
    ef_map.savemat(os.path.join(arg_dict['export_dir'], 'efmapArrayN.mat'))
    del ef_map

    # property map
    print("-> Generating property maps.")
    prop_map = xfwriter.vopgen.VopgenPropertyMap(arg_dict['xf_project'], 1, 1)
    prop_map.set_grid_origin(arg_dict['origin'][0],
                             arg_dict['origin'][1],
                             arg_dict['origin'][2])
    prop_map.set_grid_len(arg_dict['lengths'][0],
                          arg_dict['lengths'][1],
                          arg_dict['lengths'][2])
    prop_map.set_grid_resolution(arg_dict['deltas'][0],
                                 arg_dict['deltas'][1],
                                 arg_dict['deltas'][2])
    prop_map.savemat(os.path.join(arg_dict['export_dir'], 'propmap.mat'))
    del prop_map

    # sar mask
    print("-> Generating SAR mask.")
    sar_mask = xfwriter.vopgen.VopgenSarMask(arg_dict['xf_project'], 1, 1)
    sar_mask.set_grid_origin(arg_dict['origin'][0],
                             arg_dict['origin'][1],
                             arg_dict['origin'][2])
    sar_mask.set_grid_len(arg_dict['lengths'][0],
                          arg_dict['lengths'][1],
                          arg_dict['lengths'][2])
    sar_mask.set_grid_resolution(arg_dict['deltas'][0],
                                 arg_dict['deltas'][1],
                                 arg_dict['deltas'][2])
    sar_mask.savemat(os.path.join(arg_dict['export_dir'], 'sarmask_aligned.mat'))
    del sar_mask

    # mass density map
    print("-> Generating mass density map.")
    mden_map_3d = xfwriter.vopgen.VopgenMassDensityMap3D(arg_dict['xf_project'], 1, 1)
    mden_map_3d.set_grid_origin(arg_dict['origin'][0],
                             arg_dict['origin'][1],
                             arg_dict['origin'][2])
    mden_map_3d.set_grid_len(arg_dict['lengths'][0],
                          arg_dict['lengths'][1],
                          arg_dict['lengths'][2])
    mden_map_3d.set_grid_resolution(arg_dict['deltas'][0],
                                 arg_dict['deltas'][1],
                                 arg_dict['deltas'][2])
    mden_map_3d.savemat(os.path.join(arg_dict['export_dir'], 'massdensityMap3D.mat'))
    del mden_map_3d

def usage(exit_status = None):
    """Print the usage statement and exit with given status."""
    print("\nUsage: python vopgen.py --xf_project=project \\")
    print("                          [--export_dir=dir ]\\")
    print("                          [--origin='[x0,y0,z0]'] \\")
    print("                          [--lengths='[x,y,z]'] \\")
    print("                          [--deltas='[dx, dy, dz]']")
    print("  --xf_project: location of XFdtd project")
    print("  --export_dir: directory to write vopgen output, creates it if necessary.")
    print("  --origin: the origin coordinates, string representing a " +
          "Python list.")
    print("  --lengths: dimensions of the ROI, centered at the origin, " +
          "string prepresenting a Python list.")
    print("  --deltas: grid resolution, string representing a Python list.")
    print("")
    print("Example: ")
    print("  $ vopgen.py --xf_project='my_project.xf' --export_dir='/path/to/export' \ ")
    print("              --origin='[0.0,0.0,0.0]' --lengths='[0.01,0.01,0.02]' \ ")
    print("              --deltas='[0.02, 0.02, 0.02]'\n")
    if exit_status:
        sys.exit(exit_status)
    else:
        sys.exit()

def main(argv):
    """Parse command line arguments and make call to exporter."""
    arg_dict = {}
    switches = {'origin':list, 'lengths':list, 'deltas':list,
                'xf_project':str, 'export_dir':str}
    singles = ''
    long_form = [x + '=' for x in switches]
    d = {x[0] + ':' : '--' + x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError as e:
        print("Bad argument Getopt: ", e.msg)
        usage(2)

    for opt, arg in opts:
        if opt[1] + ':' in d: o = d[opt[1]+':'][2:]
        elif opt in d.values(): o = opt[2:]
        else: o = ''
        if o and arg:
            if switches[o].__name__ == 'list':
                arg_dict[o] = ast.literal_eval(arg)
            else:
                arg_dict[o] = arg

        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    # Get project directory
    if not os.path.exists(arg_dict['xf_project']):
        print("XFdtd project (", arg_dict['xf_project'], ") not found.")
        usage(2)
    # Check for valid arguments
    if len(arg_dict['origin']) != 3:
        print("Bad regrid region origin.")
        usage(2)
    if len(arg_dict['lengths']) != 3:
        print("Bad regrid region dimensions.")
        usage(2)
    if len(arg_dict['deltas']) != 3:
        print("Bad regrid resolution.")
        usage(2)

    # generate vopgen all files
    vopgen_all(arg_dict)

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Vopgen Done.")
