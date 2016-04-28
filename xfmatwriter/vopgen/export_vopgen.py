#!/usr/bin/env python
"""
Export steady-state electric field data, property maps, SAR mask, mass density maps.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os, sys, ast, getopt
import xfsystem, xfmatgrid
from xfutils import xf_regrid_3d_nearest

verbose = True
verboseprint = print if verbose else lambda *a, **k: None

def usage(exit_status=None):
    """Print the usage statement and exit with given status."""
    print("\nUsage: export_vopgen.py project.xf [--origin='[x0,y0,z0]'] \\")
    print("                          [--lengths='[x,y,z]'] \\")
    print("                          [--deltas='[dx,dy,dz]']")
    print("  --origin: the origin coordinates, string representing a Python list.")
    print("  --lengths: dimensions of the ROI, centered at the origin, string prepresenting a Python list.")
    print("  --deltas: grid resolution, string representing a Python list.")
    print("")
    print("Example: ")
    print("  $ export_fields_uniform.py / --origin='[0.0,0.0,0.0]' --lengths='[0.01,0.01,0.02]' --deltas='[0.02, 0.02, 0.02]'")
    print("")
    
def main(argv):
    verboseprint('**** Verbose Print ****')
    arg_dict = {}
    switches = { 'origin':list, 'lengths':list, 'deltas':list,
                 'xf_project':str, 'run':str, 'sim':str,
                 'export_file':str, 'field':str }
    singles = ''
    long_form = [x+'=' for x in switches]
    d = {x[0]+':':'--'+x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError as err:
        print("Bad argument Getopt: ", err.msg)
        usage(2)

    for opt, arg in opts:
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o=''
        if o and arg:
            if(switches[o].__name__ == 'list'):
                arg_dict[o]=ast.literal_eval(arg)
            else:
                arg_dict[o]=arg

        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    # Get project directory
    try:
        if(not os.path.exists(arg_dict['xf_project'])):
            print("XFdtd project (", arg_dict['xf_project'] , ") not found.")
            usage(2)
        if len(arg_dict['origin']) != 3:
            print("Bad regrid region origin.")
            usage(2)
        if len(arg_dict['lengths']) != 3:
            print("Bad regrid region dimensions.")
            usage(2)
        if len(arg_dict['deltas']) != 3:
            print("Bad regrid resolution.")
            usage(2)
    except KeyError as err:
        print("Bad input argument: ", "".join([darg for darg in err.args]))
        usage(2)
        

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done.")
