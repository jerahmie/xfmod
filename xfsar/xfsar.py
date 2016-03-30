#!/usr/bin/env python3
"""
Calculate SAR on non-uniform grid from XFdtd simulation.
 -- SAR calculated on a 1g or 10g cubic averaging volume centered on cell.
 -- Non-uniform grid.
 -- Caputa, K., M. Okoniewski, and M. A. Stuchly, "An Algorithm for
      Computations of the Power Deposition in Human Tissue.", IEEE Antennas
      Propag. Mag., vol. 41, iss. 4, Aug 1999, pp.102-107.
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
    def __init__(self):
        pass

    def _find_tissue(self):
        """Return a list of indices with grid locations that are tissues."""
        pass

    def _avg_field_in_cube(self):
        """Calculate the average field inside the grid element."""
        pass

