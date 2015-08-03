#!/usr/bin/env python
"""
Test xfmatmod
"""

from __future__ import (absolute_import, division, 
                        print_function, unicode_literals)

import sys
import xfmatmod

def main(argv):
    f = open(argv,"r")
    xf_geom = xfmatmod.XFGeometry(f)
    xf_geom.print_materials()
    #xf_geom.print_grid_data()
    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: xf_geometry.py <inputfile>')
        print(sys.argv)

