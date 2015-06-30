#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from scipy import pi, sqrt
from scipy.special import ellipe, ellipeinc

a = 12.0
b = 10.0
# k = elliptical eccentricity
# k = sqrt(1-(b/a)**2)
# m = k**2
m = 1-(b/a)**2

def ellip_perimeter(m):
    return 4.0*a*ellipe(m)

if __name__ == "__main__":
    print("Circle perimeter: ", 2.0*pi*a )
    print("Ellipse perimeter m=", m, ": ", ellip_perimeter(m))

