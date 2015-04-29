"""
Generate a list of coordinates for an ellipsoidal coil.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
import numpy as np
from scipy import pi, sqrt
from scipy.special import ellipe, ellipeinc
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def usage():
    print()
    print("usage: ellip_coil.py a b theta")
    print("  a: the major axis (x-axis) of ellipse")
    print("  b: the minor axis (y-axis) of ellipse")
    print("  N: number of coils")
    print("  theta: the rotation from the x-axis")
    print()

def rotatePointsAboutAxis(x0, y0, theta):
    """
    Apply a rotation to the coil element coordinates about origin.
    """
    if len(x0) == len(y0):
        rho0 = [np.sqrt(x0[i]**2 + y0[i]**2) for i in range(len(x0))]
        theta0 = [np.arctan2(y0[i],x0[i]) for i in range(len(x0))]
        x1 = [rho0[i]*np.cos(theta+theta0[i]) for i in range(len(x0))]
        y1 = [rho0[i]*np.sin(theta+theta0[i]) for i in range(len(x0))]
        return x1, y1
    else:
        print("rotatePointsAboutAxis: x0 and y0 must be same length.")

def arcLenFunc(x, *data):
    """
    Optimization function for calculating angle from arc length
    """
    L = data[0]
    a = data[1]
    m = data[2]
    x0 = data[3]
    return L/a - (ellipeinc(x,m) - ellipeinc(x0,m))

def printPoints(x,y):
    """
    Print the coordinates of the ellipsoidal elements.
    """
    print("\nEllipse Coil Element Points:\n")
    print("Coil\nElement\t\tx\t\ty")
    print("--------------------------------------")
    if len(x) == len(y):
        for i in range(len(x)):
            print(i,"\t","{:10.4f}".format(x[i]), "\t","{:10.4f}".format(y[i]))
    else:
        print("printPoints: x and y must be same length.")
        print("len(x): ", len(x))
        print("len(y): ", len(y))

def ellipCoil(a, b, N):
    """
    Caclulate the x,y points for rf coil elements positioned uniformly around
    ellipse.  Coil is centered at origin.
    """
    print("Generating ellipsoidal coil...")
    m = 1 - (b/a)**2
    L = (4*a/N) * ellipe(m)

    # Start the first coil element centered around theta
    L0 = L/2  # shift coil 0 by half the coil element spacing
    t0 = fsolve(arcLenFunc, 0, args=(L0, a, m, 0.0))[0]
    #t0 = 0.0
    theta = []
    rho = []

    ellipPoints = []
    ellipPoints.append((t0,a))
    while True:
        if t0 > 2.0*pi:
            break
        else:
            theta.append(t0)
            rho0 = ((np.sin(t0))**2/b**2 + (np.cos(t0))**2/a**2)**(-0.5)
            rho.append(rho0)
            t0 = fsolve(arcLenFunc, 0, args=(L, a, m, t0))[0]

    x0 = rho*np.cos(theta)
    y0 = rho*np.sin(theta)
    x, y = rotatePointsAboutAxis(x0,y0, np.pi/2.0)
    
    return x, y

if __name__ == '__main__':
    """
    ellip_coil main routine.
    """
    if len(sys.argv) == 4:
        scriptName, a, b, N = sys.argv
        x, y = ellipCoil(float(a), float(b), int(N))
        printPoints(x, y)
        plt.figure()
        plt.plot(x,y,'*-r')
        plt.axis('equal')
        plt.show()
    else:
        usage()
