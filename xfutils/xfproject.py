"""
Helper functions for XFdtd project directory.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
import re
from xfutils import xf_run_str_to_int

class XFProjectInfo(object):
    """Class to query and save xfproject metadata."""
    def __init__(self, xf_project_dir):
        self._xf_project_dir = xf_project_dir
        self._xf_sim_run = []
        self._find_sims_runs()

    def _find_sims_runs(self):
        """Find all simulations and runs in project."""
        sims_dir = os.path.join(self._xf_project_dir, 'Simulations')
        sim_re = r'[0-9]{6}'
        run_re = r'Run[0-9]{3}'
        sims = [os.path.join(self._xf_project_dir, 'Simulations', sim) \
                for sim in os.listdir(sims_dir) if re.search(sim_re, sim)]
        max_sim = len(sims)
        self._xf_sim_run = [[]] * max_sim
        for sim in sims:
            sim_index = int(os.path.basename(sim)) - 1
            runs = [xf_run_str_to_int(run) \
                    for run in os.listdir(sim) if re.search(run_re, run)]
            self._xf_sim_run[sim_index] = runs

    @property
    def xf_sim_run_list(self):
        """Return the simulation/run list."""
        return self._xf_sim_run
