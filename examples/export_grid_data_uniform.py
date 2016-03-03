#!/usr/bin/env python3
"""
Example grid data exporter on uniform grid.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os, sys
import numpy as np
import scipy.io as spio
from scipy.interpolate import griddata
from xfmatgrid.xfutils import xf_run_id_to_str, xf_sim_id_to_str
import xfgeomod

def main(xfProjectDir, simId, runId):
    if os.path.isdir(xfProjectDir):
        print("found: ", xfProjectDir)
    runDir=os.path.join(xfProjectDir, 'Simulations',
                        xf_sim_id_to_str(simId),
                        xf_run_id_to_str(runId))
    if os.path.isdir(runDir):
        print("found: ", runDir)

    xfGeometry = xfgeomod.XFGeometry(os.path.join(xfProjectDir,
                                                  'Simulations',
                                                  xf_sim_id_to_str(simId),
                                                  xf_run_id_to_str(runId)))
    xfMesh = xfgeomod.XFMesh(os.path.join(xfProjectDir,
                                          'Simulations',
                                          xf_sim_id_to_str(simId),
                                          xf_run_id_to_str(runId)))
    gridExporter = xfgeomod.XFGridExporter(xfGeometry, xfMesh)
    gridExporterRegrid = xfgeomod.XFGridExporterRegrid(xfGeometry, xfMesh)
    

if __name__ == '__main__':
    main('/home/jerahmie/workspace/xfmod/Test_Data/Test_Coil.xf', 1, 1)
