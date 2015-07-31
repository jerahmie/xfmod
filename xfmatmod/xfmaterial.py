class XFMaterial:
    """Class to store material properties"""
    def __init__(self):
        self._matName = ''
        self._matConductivity = ''
        self._matDensity = ""
    
    @property
    def matName(self):
        """Returns material name."""
        return self._matName
    
    @matName.setter
    def matName(self, value):
        """Set material name."""
        self._matName = value

    @matName.deleter
    def matName(self):
        """Delete material name."""
        del(self._matName)

    @property
    def matConductivity(self):
        """Return material conductivity."""
        return self._matConductivity

    @matConductivity.setter
    def matConductivity(self, value):
        """Set material conductivity."""
        self._matConductivity = value

    @matConductivity.deleter
    def matConductivity(self):
        """Delete material conductivity."""
        del(self._matName)

    @property
    def matDensity(self):
        """Returns material density."""
        return self._matDensity

    @matDensity.setter
    def matDensity(self, value):
        """Set material density."""
        self._matDensity = value

    @matDensity.deleter
    def matDensity(self):
        """Delete material density."""
        del(self._matDensity)
