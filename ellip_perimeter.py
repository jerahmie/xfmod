#!/usr/bin/env python

from scipy import pi, sqrt
from scipy.special import ellipe, ellipeinc

a = 12.0
b = 10.0

def ellip_perimeter():
    ellip_eccentricity = sqrt(1-(b/a)**2)
    return 4.0*a*ellipe(ellip_eccentricity)

if __name__ == "__main__":
    print ellip_perimeter()

