"""
XFdtd Data writer base class.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import abc

class XFMatWriter(object):
    """Base class for writing xfdata to Mat file."""
    __metaclass__ = abc.ABCMeta

    @property
    def net_input_power(self):
        """Desired net input power."""
        return self._net_input_power

    @net_input_power.setter
    def net_input_power(self, power):
        """Set the desired net input power for simulation."""
        self._net_input_power = power

    @abc.abstractmethod
    def savemat(self):
        """Save XFdtd data to a Mat file."""
        pass
