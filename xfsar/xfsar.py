#!/usr/bin/env python3
"""
Calculate SAR on non-uniform grid from XFdtd simulation.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
import numpy as np
import scipy.io as spio
import xfgeomod, xfmatgrid
from xfutils import xf_sim_id_to_str, xf_run_id_to_str

class XFSar(object):
    """XFdtd SAR calculation class."""
    def __init__(self, project_dir, sim_id, run_id):
        run_path = os.path.join(project_dir, r'Simulations',
                                       xf_sim_id_to_str(sim_id),
                                       xf_run_id_to_str(run_id))
        
        
        self._geom = xfgeomod.XFGeometry(run_path)
        self._mesh = xfgeomod.XFMesh(run_path)
        self._grid_exporter = xfgeomod.XFGridExporter(self._geom, self._mesh)

    def _test_mesh(self):
        """test grid indexing"""
        print(self._geom)
        print(self._mesh)
        print("Grid dims: (", np.size(self._grid_exporter.grid_x), ",",
              np.size(self._grid_exporter.grid_y), ",",
              np.size(self._grid_exporter.grid_z), ")")
        self.assertEqual((np.size(self._grid_exporter.grid_x), 
                          np.size(self._grid_exporter.grid_y), 
                          np.size(self._grid_exporter.grid_z)), 
                         np.shape(self._grid_exporter.ex_sigma))
        self.assertEqual((), np.shape(self._grid_exporter.ex_epsilon_r))
        self.assertEqual((), np.shape(self._grid_exporter.ex_density))
        
