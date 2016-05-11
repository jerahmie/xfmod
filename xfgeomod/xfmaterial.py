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
        self._tissue = 0

    @property
    def name(self):
        """Return material name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set material name."""
        self._name = value

    @property
    def conductivity(self):
        """Return material conductivity."""
        return self._conductivity

    @conductivity.setter
    def conductivity(self, value):
        """Set material conductivity."""
        self._conductivity = value

    @property
    def density(self):
        """Returns material density."""
        return self._density

    @density.setter
    def density(self, value):
        """Set material density."""
        self._density = value

    @property
    def epsilon_r(self):
        """Return the material relative permittivity."""
        return self._epsilon_r

    @epsilon_r.setter
    def epsilon_r(self, value):
        """Set the material relative permittivity."""
        self._epsilon_r = value

    @property
    def tissue(self):
        """Return the tissue parameter.  0 = not tissue; !0 = tissue"""
        return self._tissue
    
    @tissue.setter
    def tissue(self, value):
        """Set the tissue value."""
        self._tissue = value

