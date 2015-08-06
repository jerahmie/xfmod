"""
Class to store materials extracted from XFdtd geometry.input
"""

# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

class XFMaterial(object):
    """Class to store material properties"""

    def __init__(self):
        self._name = ''
        self._conductivity = ''
        self._density = ''
        self._epsilon_r = ''

    @property
    def name(self):
        """Return material name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set material name."""
        self._name = value

    @name.deleter
    def name(self):
        """Delete material name."""
        del self._name
        self._name = ''

    @property
    def conductivity(self):
        """Return material conductivity."""
        return self._conductivity

    @conductivity.setter
    def conductivity(self, value):
        """Set material conductivity."""
        self._conductivity = value

    @conductivity.deleter
    def conductivity(self):
        """Delete material conductivity."""
        del self._conductivity
        self._conductivity = ''

    @property
    def density(self):
        """Returns material density."""
        return self._density

    @density.setter
    def density(self, value):
        """Set material density."""
        self._density = value

    @density.deleter
    def density(self):
        """Delete material density."""
        del self._density
        self._density = ''

    @property
    def epsilon_r(self):
        """Return the material relative permittivity."""
        return self._epsilon_r

    @epsilon_r.setter
    def epsilon_r(self, value):
        """Set the material relative permittivity."""
        self._epsilon_r = value

    @epsilon_r.deleter
    def epsilon_r(self):
        """Delete material relative permittivity."""
        del self._epsilon_r
        self._epsilon_r = ''
