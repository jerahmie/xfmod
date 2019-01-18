"""
Helper class for XFdtd simulations contained within a project.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import re

class XFSimulationInfo(object):
    """Information for single xfdtd simulation.

    Args:
        sim      (int): Simulation number.
        sim_path (str): Project simulastion path.
    """
    def __init__(self, sim=None, sim_path=None):
        self._simulation_number = sim
        self._simulation_path = sim_path
        if self._simulation_path is not None:
            self._runs = self._find_runs()

    def _find_runs(self):
        """Find the runs in the current simulation directory.
        """
        run_re = r'Run[0-9]{3}'
        try:
            runs = [os.path.join(self._simulation_path, run) \
                    for run in os.listdir(self._simulation_path) \
                    if re.search(run_re, run)]
        except FileNotFoundError as err:
            print("Could not find Project Simulation directory: ",
                  self._simulation_path)
            raise

         
        
        
        
    
