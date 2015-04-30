"""
Generate a list of coordinates and unit normal vector components
for an ellipsoidal coil.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
import numpy as np
from scipy import pi, sqrt
from scipy.special import ellipe, ellipeinc
from scipy.optimize import fsolve

def usage():
    """
    Display usage message and exit.
    """
    print()
    print("Usage: ellip_coil.py a b N")
    print("  a: the major axis (x-axis) of ellipse")
    print("  b: the minor axis (y-axis) of ellipse")
    print("  N: number of coils")
    print()
    print("Example: ")
    print("  $ python ellip_coil.py 12.0 10.0 16 > ellip_coil_points.txt")
    print()
    sys.exit()

def rotatePointsAboutOrigin(x0, y0, theta):
    """
    Apply a rotation to the coil element coordinates about origin.
    x0 : list
    y0 : list
         x0, y0 are list of points to rotate about origin (x=0, y=0)
    theta : float
         The rotation angle (radians)
    list, list
         The rotated x, y points
    """
    if len(x0) == len(y0):
        rho0 = [np.sqrt(x0[i]**2 + y0[i]**2) for i in range(len(x0))]
        theta0 = [np.arctan2(y0[i],x0[i]) for i in range(len(x0))]
        x1 = [rho0[i]*np.cos(theta+theta0[i]) for i in range(len(x0))]
        y1 = [rho0[i]*np.sin(theta+theta0[i]) for i in range(len(x0))]
        return x1, y1
    else:
        print("rotatePointsAboutOrigin: x0 and y0 must be same length.")

def arcLenFunc(x, *data):
    """
    Optimization function for calculating angle from arc length
    """
    L = data[0]
    a = data[1]
    m = data[2]
    x0 = data[3]
    return L/a - (ellipeinc(x,m) - ellipeinc(x0,m))

def printPoints(x, y, z, ux, uy, uz):
    """
    Print the coordinates of the ellipsoidal elements.
    x : list
    y : list
    z : list
    ux : list
    uy : list
    uz : list
    """
    print("\nEllipse Coil Element Points (meters)\n")
    print("Coil\nElement\t\tx\t\ty\t\tz\t\tux\t\tuy\t\tuz")
    print("---------------------------------------------------------------------------------------------------")
    for i in range(len(x)):
        print(i,"\t",
              "{:10.6f}".format(x[i]), "\t",
              "{:10.6f}".format(y[i]), "\t",
              "{:10.6f}".format(z[i]), "\t",
              "{:10.6f}".format(ux[i]),"\t",
              "{:10.6f}".format(uy[i]),"\t",
              "{:10.6f}".format(uz[i]) )


def ellipCoil(a, b, N):
    """
    Caclulate the x,y points for rf coil elements positioned uniformly around
    ellipse.  Coil is centered at origin.
    """
    m = 1 - (b/a)**2
    L = (4*a/N) * ellipe(m)

    # Start the first coil element centered around theta
    L0 = L/2  # shift coil 0 by half the coil element spacing
    t0 = fsolve(arcLenFunc, 0, args=(L0, a, m, 0.0))[0]
    #t0 = 0.0
    theta = []
    rho = []
    if ( a > b ):
        # proper ellipse 
        while True:
            if t0 > 2.0*pi:
                break
            else:
                theta.append(t0)
                rho0 = ((np.sin(t0))**2/b**2 + (np.cos(t0))**2/a**2)**(-0.5)
                rho.append(rho0)
                t0 = fsolve(arcLenFunc, 0, args=(L, a, m, t0))[0]
    elif ( abs(a-b) < sys.float_info.epsilon ):
        # this is a circle
        t0 = 2.0*np.pi/N
        for i in range(N):
            theta.append(t0 * float(i))
            rho.append(a)
    
    x0 = rho*np.cos(theta)
    y0 = rho*np.sin(theta)
    ux0 = [ (2.0*x0[i]/a**2)/np.sqrt((2.0*x0[i]/a**2)**2+(2.0*y0[i]/b**2)**2) \
            for i in range(len(x0))]
    uy0 = [ (2.0*y0[i]/b**2)/np.sqrt((2.0*x0[i]/a**2)**2+(2.0*y0[i]/b**2)**2) \
            for i in range(len(y0))] 
    x, y = rotatePointsAboutOrigin(x0, y0, np.pi/2.0)
    ux, uy = rotatePointsAboutOrigin(ux0, uy0, np.pi/2.0)
    
    return x, y, ux, uy

if __name__ == '__main__':
    """
    ellip_coil main routine.
    """
    if len(sys.argv) == 4:
        scriptName, a, b, N = sys.argv
        x, y, ux, uy = ellipCoil(float(a), float(b), int(N))
        z = [0 for i in range(len(x))]
        uz = [0 for i in range(len(x))]
        printPoints(x, y, z, ux, uy, uz)
    else:
        usage()
