"""
oClass to store XFdtd system information for given simulation/run.
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import os
import re
from xfmatgrid.xfutils import xf_sim_id_to_str, xf_run_id_to_str

STEADY_STATE_FREQ_RE = "begin_<SteadyStateFrequency>\s*\n" + \
                       "Frequency\s*([0-9.eE\-+]*)\s*\n" + \
                       "end_<SteadyStateFrequency>\s*"

COMPUTED_POWER_RE = "begin_<ComputedPower>\s*\n" + \
                    "AvailablePower\s*([0-9.]*)\s*\n" + \
                    "NetInputPower\s*([0-9.eE\-+]*)\s*\n" + \
                    "FeedLoss\s*([0-9.eE\-+]*)\n" + \
                    "WaveguideLoss\s*([0-9.eE\-+]*)\n" + \
                    "DissipatedPower\s*([0-9.eE\-+]*)\n" + \
                    "DissipatedPowerInTissue\s*([0-9.eE\-+]*)\n" + \
                    "DissipatedPowerInNonTissue\s*([0-9.eE\-+]*)\n" + \
                    "RadiatedPower\s*([0-9.eE\-+]*)\n" + \
                    "PowerExittingFarZoneBox\s*([0-9.eE\-+]*)\n" + \
                    "end_<ComputedPower>"

class XFSystem(object):
    """Hold the XFdtd simulation system information."""
    def __init__(self, projectDir, simId, runId):
        self._projectDir = projectDir
        self._simId = simId
        self._runId = runId
        self._system_ssout = None
        self._set_system_ssout()
        self._frequency_ssout = None
        self._net_input_power = None
        self._available_power = None
        self._parse_system_ssout()


    def _set_system_ssout(self):
        """Set the simulation system file."""
        system_ssout = os.path.join(self._projectDir,
                                    'Simulations',
                                    xf_sim_id_to_str(self._simId),
                                    xf_run_id_to_str(self._runId),
                                    'output', 'SteadyStateOutput',
                                    'f0', 'system.ssout')
        if (os.path.exists(system_ssout)):
            self._system_ssout = system_ssout

    def _parse_system_ssout(self):
        """Parse system.ssout and populate simulation system data."""
        with open(self._system_ssout,'r') as fh:
            system_ssout = fh.read()

        try:
            self._frequency_ssout = float(re.findall(STEADY_STATE_FREQ_RE,system_ssout)[0])
        except TypeError:
            print("No valid steady state frequency found in: " +
                  self._system_ssout)

        try:
            computed_power = re.findall(COMPUTED_POWER_RE,system_ssout)[0]
            print(computed_power[0][0])
            self._available_power = float(computed_power[0])
            self._net_input_power = float(computed_power[1])
        except TypeError:
            print("No valid steady state frequency found in: " +
                  self._system_ssout)

        fh.close()

    @property
    def frequency(self):
        return self._frequency_ssout

    @property
    def net_input_power(self):
        return self._net_input_power
