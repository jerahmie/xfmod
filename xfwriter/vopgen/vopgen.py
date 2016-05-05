#!/usr/bin/env python
"""
Vopgen data exporter class for 5-D E-Field data.
"""

from __future__ import (absolue_import, division,
                        print_function, unicode_literals)

import numpy as np
import xfwriter
import xfutils

class VopgenEFMapArrayN(XFMatWriter):
    """Matlab writer for 5-D E-Field data."""
    def __init__(self, xf_project_dir, sim_ids):
        self._xf_project_dir = xf_project_dir
        self._sim_ids = sim_ids
        self._num_coils = len(sim_ids)
        self._ef_map_array_N = None
        self._ex = None
        self._ey = None
        self._ez = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._net_input_power_per_coil = 

    

    #def _net_input_power(self):
    #    """Return array of net input powers, one per coil in simulation."""
    #    net_input_power_per_coil = np.empty([1, self._num_coils], dtype = np.dtype('d'))
    #    for sim_id in self._sim_ids:
            

    # def _ef_map_array_n(self):
        
    
