#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys, os
import xfmatgrid


def main(argv):
    print("In main...")
    print(argv[1])
    if os.path.exists(argv[1]):
        xf_nugrid = xfmatgrid.XFFieldNonUniformGrid(argv[1], 
                                                    int(argv[2]), 
                                                    int(argv[3]))
        print(xf_nugrid.mp_field_types)
    return xf_nugrid

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        a = main(sys.argv)
    else:
        print('Usage: xf_field_regrid.py <xfdtd_project_name> <simulation> <run>')
        print(sys.argv)
