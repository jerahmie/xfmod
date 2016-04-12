"""
Save the B1 tx/rx field plot.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, os
import numpy as np
import scipy as sp
import scipy.io as spio
import matplotlib.pyplot as plt

def plot_main(mat_file, z_val):
    eps = 1e-50
    """Plot the x-y cut of the data at the z_index nearest to z_val."""
    try:
        mat_data = spio.loadmat(mat_file)
        # z index of plot value
        print('z_val: ', z_val)
        z_ind = np.argmin(np.absolute(mat_data['ZDim']-z_val))
        print("Z(", z_ind, ") = ", mat_data['ZDim'][z_ind][0])
        x_dim = mat_data['XDim']
        y_dim = mat_data['YDim']
        XX, YY = np.meshgrid(x_dim, y_dim, indexing='ij')
        print('B1Tx: ',np.shape(mat_data['B1Tx']))
        b1Mod = abs(mat_data['B1Tx'])
        b1Mod[b1Mod < eps] = eps
        fig=plt.pcolor(XX,YY,
                       20.0*np.log10(b1Mod[:,:,z_ind]/1e-6),
                       cmap=plt.cm.get_cmap('bone'),
                       vmin=-32, vmax=25)
 
        plt.title("|B1+|, z=" + str(z_val))
        plt.xlabel('x (m)'); plt.ylabel('y (m)')
        plt.axis('equal')
        cb = plt.colorbar()
        cb.set_label('dB relative to microTesla/sqrt(Watt)')
        plt.tight_layout()
        plt.savefig(os.path.realpath(os.path.splitext(mat_file)[0]+'.png'))

    except FileNotFoundError as e:
        print("The mat file was not found: ", mat_file)
        raise

    except:
        print("Caught unexpeted error: ", sys.exc_info()[0])
        raise


if __name__ == "__main__":
    print("Plotting results.")
    if len(sys.argv) == 3:
        mat_file = sys.argv[1]
        z_val = float(sys.argv[2])
        plot_main(mat_file, z_val)
    else:
        print("Wrong number of inputs.")
    




