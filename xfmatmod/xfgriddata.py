"""
Class to store grid data extracted from XFdtd geometry.input
"""
# Ensure python 2 and 3 compatibility
from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

class XFGridData:
    """Class to store grid data properties."""

    def __init__(self):
        self._origin_x = 0
        self._origin_y = 0
        self._origin_z = 0
        self._num_x_cells = 0
        self._num_y_cells = 0
        self._num_z_cells = 0
        self._x_deltas = []
        self._y_deltas = []
        self._z_deltas = []

    @property
    def origin(self):
        """Returns origin of fdtd grid."""
        return [self._origin_x, self._origin_y, self._origin_z]

    @origin.setter
    def origin(self, origin):
        """Set the fdtd origin."""
        if len(origin) == 3:
            self._origin_x = float(origin[0])
            self._origin_y = float(origin[1])
            self._origin_z = float(origin[2])
        else:
            print("origin = [x0, y0, z0]")

    @origin.deleter
    def origin(self):
        """Delete the origin values of xfdtd grid."""
        del self._origin_x
        del self._origin_y
        del self._origin_z

    @property
    def num_x_cells(self):
        """Return number of X cells in fdtd grid."""
        return self._num_x_cells

    @num_x_cells.setter
    def num_x_cells(self, value):
        """Set number of X cells in fdtd grid."""
        self._num_x_cells = value

    @num_x_cells.deleter
    def num_x_cells(self):
        """Delete number of X cells."""
        del self._num_x_cells

    @property
    def num_y_cells(self):
        """Return number of Y cells in fdtd grid."""
        return self._num_y_cells

    @num_y_cells.setter
    def num_y_cells(self, value):
        """Set number of Y cells in fdtd grid."""
        self._num_y_cells = value

    @num_y_cells.deleter
    def num_y_cells(self):
        """Delete number of Y cells."""
        del self._num_y_cells

    @property
    def num_z_cells(self):
        """Return number of Z cells in fdtd grid."""
        return self._num_z_cells

    @num_z_cells.setter
    def num_z_cells(self, value):
        """Set number of Z cells in fdtd grid."""
        self._num_z_cells = value

    @num_z_cells.deleter
    def num_z_cells(self):
        """Delete number of Z cells."""
        del self._num_z_cells

    @property
    def x_deltas(self):
        """Return list of deltas in X direction of fdtd grid."""
        return self._x_deltas

    @x_deltas.setter
    def x_deltas(self, value):
        """Set the x-direction deltas in fdtd grid."""
        self._x_deltas = []
        if len(value[0]) == 2:
            for ind in range(len(value)):
                self._x_deltas.append([int(value[ind][0]), \
                                       float(value[ind][1])])
        else:
            print("Delta value 2-by-n list.")

    @x_deltas.deleter
    def x_deltas(self):
        """Delete the x-direction deltas in fdtd grid."""
        del self._x_deltas

    @property
    def y_deltas(self):
        """Return list of deltas in Y direction of fdtd grid."""
        return self._y_deltas

    @y_deltas.setter
    def y_deltas(self, value):
        """Set the y-direction deltas in fdtd grid."""
        self._y_deltas = []
        if len(value[0]) == 2:
            for ind in range(len(value)):
                self._y_deltas.append([int(value[ind][0]), \
                                           float(value[ind][1])])
        else:
            print("Delta value is 2-by-n list.")

    @y_deltas.deleter
    def y_deltas(self):
        """Delete the y-direction deltas in fdtd grid."""
        del self._y_deltas

    @property
    def z_deltas(self):
        """Return list of deltas in Z direction of fdtd grid."""
        return self._z_deltas

    @z_deltas.setter
    def z_deltas(self, value):
        """Set the z-direction deltas in fdtd grid."""
        self._z_deltas = []
        if len(value[0]) == 2:
            for ind in range(len(value)):
                self._z_deltas.append([int(value[ind][0]), \
                                       float(value[ind][1])])
        else:
            print("Delta value is 2-by-n list.")

    @z_deltas.deleter
    def z_deltas(self):
        """Delete the z-direction deltas in fdtd grid."""
        del self._z_deltas

    def x_coods(self):
        """Return the X coordinate values from origin and deltas."""
        cood_cumulative = self._origin_x  # cumulative x value
        coods = []                        # x value array

        for i in range(0, len(self._x_deltas)-1):
            for j in range(int(self._x_deltas[i][0]), \
                           int(self._x_deltas[i+1][0])):
                coods.append(cood_cumulative)
                cood_cumulative += self._x_deltas[i][1]

        for i in range(self._x_deltas[-1][0], self._num_x_cells):
            coods.append(cood_cumulative)
            cood_cumulative += self._x_deltas[-1][1]

        return coods

    def y_coods(self):
        """Return the Y coordinate values from origin and deltas."""
        cood_cumulative = self._origin_y  # cumulative y value
        coods = []                        # y value array

        for i in range(0, len(self._y_deltas)-1):
            for j in range(int(self._y_deltas[i][0]), \
                           int(self._y_deltas[i+1][0])):
                coods.append(cood_cumulative)
                cood_cumulative += self._y_deltas[i][1]

        for i in range(self._y_deltas[-1][0], self._num_y_cells):
            coods.append(cood_cumulative)
            cood_cumulative += self._y_deltas[-1][1]

        return coods

    def z_coods(self):
        """Return the Z coordinate values from origin and deltas."""
        cood_cumulative = self._origin_z  # cumulative z value
        coods = []                        # z value array

        for i in range(0, len(self._z_deltas)-1):
            for j in range(int(self._z_deltas[i][0]), \
                           int(self._z_deltas[i+1][0])):
                coods.append(cood_cumulative)
                cood_cumulative += self._z_deltas[i][1]

        for i in range(self._z_deltas[-1][0], self._num_z_cells):
            coods.append(cood_cumulative)
            cood_cumulative += self._z_deltas[-1][1]

        return coods
