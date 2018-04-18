"""
Class to store XFdtd system information for given simulation/run.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
import re
from xfutils import xf_sim_id_to_str, xf_run_id_to_str

STEADY_STATE_FREQ_RE = r"begin_<SteadyStateFrequency>\s*\n" + \
                       r"Frequency\s*([0-9.eE\-+]*)\s*\n" + \
                       r"end_<SteadyStateFrequency>\s*"

COMPUTED_POWER_RE = r"begin_<ComputedPower>\s*\n" + \
                    r"AvailablePower\s*([0-9.]*)\s*\n" + \
                    r"NetInputPower\s*([0-9.eE\-+]*)\s*\n" + \
                    r"FeedLoss\s*([0-9.eE\-+]*)\n" + \
                    r"(ComponentMatchingCircuitLoss\s*([0-9.eE\-+])\s*\n)?" +\
                    r"WaveguideLoss\s*([0-9.eE\-+]*)\n" + \
                    r"DissipatedPower\s*([0-9.eE\-+]*)\n" + \
                    r"DissipatedPowerInTissue\s*([0-9.eE\-+]*)\n" + \
                    r"DissipatedPowerInNonTissue\s*([0-9.eE\-+]*)\n" + \
                    r"RadiatedPower\s*([0-9.eE\-+]*)\n" + \
                    r"PowerExittingFarZoneBox\s*([0-9.eE\-+]*)\n" + \
                    r"end_<ComputedPower>"

class XFSystem(object):
    """Hold the XFdtd simulation system information."""
    def __init__(self, project_dir, sim_id, run_id):
        self._project_dir = project_dir
        self._sim_id = sim_id
        self._run_id = run_id
        self._system_ssout = None
        self._set_system_ssout()
        self._frequency_ssout = None
        self._net_input_power = None
        self._available_power = None
        self._parse_system_ssout()

    def _set_system_ssout(self):
        """Set the simulation system file."""
        system_ssout = os.path.join(self._project_dir,
                                    'Simulations',
                                    xf_sim_id_to_str(self._sim_id),
                                    xf_run_id_to_str(self._run_id),
                                    'output', 'SteadyStateOutput',
                                    'f0', 'system.ssout')
        if os.path.exists(system_ssout):
            self._system_ssout = system_ssout

    def _parse_system_ssout(self):
        """Parse system.ssout and populate simulation system data."""
        with open(self._system_ssout, 'r') as xf_sys_fh:
            system_ssout = xf_sys_fh.read()

        try:
            self._frequency_ssout = float(re.findall(STEADY_STATE_FREQ_RE,
                                                     system_ssout)[0])
        except TypeError:
            print("No valid steady state frequency found in: " +
                  self._system_ssout)

        try:
            computed_power = re.findall(COMPUTED_POWER_RE, system_ssout)[0]
            self._available_power = float(computed_power[0])
            self._net_input_power = float(computed_power[1])
        except TypeError:
            print("No valid steady state frequency found in: " +
                  self._system_ssout)

        xf_sys_fh.close()

    @property
    def frequency(self):
        """Return the steady-state frequency."""
        return self._frequency_ssout

    @property
    def net_input_power(self):
        """Return the net input power."""
        return self._net_input_power


