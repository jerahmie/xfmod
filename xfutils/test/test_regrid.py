#!/usr/bin/env python
"""
Test regrid helper functions.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import sys, os
import unittest
import numpy as np
import xfmatgrid, xfutils

TEST_COIL_DIR = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              '..','..','..',
                                              'Test_Data', 'Test_Coil.xf'))
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
try:
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
    plotEnabled=True
except ImportError:
    plotEnabled=False
    print("Visualization of regrid is disabled. " + \
          "Install matplotlib to get the full visual experience.")

if sys.version_info < (2,7,10):
    raise Exception("Python version must be 2.7.10 or newer.")
    sys.exit(-1)
    
class TestRegrid(unittest.TestCase):
    """Unit tests for regrid helper functions."""
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)
        cls.field_nugrid = xfmatgrid.XFFieldNonUniformGrid(TEST_COIL_DIR, 1, 1)
        

    def setUp(self):
        n2 = 64
        self.x2 = np.linspace(-5.0, 5.0, num=n2)
        self.y2 = np.linspace(-5.0, 5.0, num=n2)
        self.z2 = np.linspace(-5.0, 5.0, num=n2)

    def test_regrid_data_shape(self):
        """Verify exception is thrown if dimensions and data shapes mismatch."""
        print(self.id())
        n1 = 10
        x_try = np.linspace(1.0, 5.0, num=5)
        y_try = np.linspace(0.0, 1.0, num=10)
        z_try = np.linspace(1.0, 15.0, num=15)

        x2 = np.linspace(0.0, 10.0, num=n1)
        y2 = np.linspace(0.0, 10.0, num=n1)
        z2 = np.linspace(0.0, 10.0, num=n1)

        mat3d = np.arange(n1**3).reshape(n1,n1,n1)
        
        with self.assertRaises(xfutils.XFRegridError):
            xfutils.xf_regrid_3d_nearest((x_try,y_try,z_try),(x2,y2,z2),mat3d)

    def test_regrid_same_points(self):
        """Regrid data to same grid.  Data should be preserved."""
        print(self.id())
        n1 = 16
        x1 = np.linspace(0.0, 10.0, num=n1)
        y1 = np.linspace(0.0, 10.0, num=n1)
        z1 = np.linspace(0.0, 10.0, num=n1)
        mat3d = np.arange(n1**3).reshape(n1,n1,n1)

        regrid_mat3d = xfutils.xf_regrid_3d_nearest((x1,y1,z1),
                                                    (x1,y1,z1),
                                                    mat3d)
        self.assertTrue(np.allclose(mat3d, regrid_mat3d))

    @unittest.skip("Enable this test to visually compare regrid data.")
    def test_regrid(self):
        """Test the regrid routine."""
        print(self.id())
        n1 = 16
        zInd = 6
        
        x1 = np.linspace(-5.0, 5.0, num=n1)
        y1 = np.linspace(-5.0, 5.0, num=n1)
        z1 = np.linspace(-5.0, 5.0, num=n1)
        XX1, YY1 = np.meshgrid(x1,y1)
        R1 = np.sqrt(XX1**2 + YY1**2)
        mat3d = np.zeros((n1, n1, n1))
        for i in range(n1):
            mat3d[:,:,i] = np.sin(R1)

        #x2 = np.linspace(-5.0, 5.0, num=n2)
        #y2 = np.linspace(-5.0, 5.0, num=n2)
        #z2 = np.linspace(-5.0, 5.0, num=n2)

        zInd_regrid = np.argmin(np.absolute(z2-z1[zInd]))
        
        regrid_mat3d = xfutils.xf_regrid_3d_nearest((x1,y1,z1),
                                                   (self.x2,self.y2,self.z2),
                                                   mat3d)
        self.assertEqual(n1,np.shape(mat3d)[0])
        self.assertEqual(n1,np.shape(mat3d)[1])
        self.assertEqual(n1,np.shape(mat3d)[2])
        self.assertEqual((n2,n2,n2),np.shape(regrid_mat3d))
        
        if plotEnabled:
            XX2, YY2 = np.meshgrid(x2,y2)
            #f1 = plt.figure()
            #plt.subplot(1,2,1)
            #plt.pcolor(XX1,YY1,mat3d[:,:,zInd])
            #plt.title('z=' + str(z1[zInd]) + '\n' + str(np.shape(mat3d)))
            #plt.subplot(1,2,2)
            #plt.pcolor(XX2,YY2,regrid_mat3d[:,:,zInd_regrid])
            #plt.title('z=' + str(z2[zInd_regrid]) + '\n' +
            #          str(np.shape(regrid_mat3d)))
            #plt.draw()
            f2 = plt.figure()
            ax1 = f2.add_subplot(121, projection='3d')
            ax1.plot_surface(XX1,YY1,mat3d[:,:,zInd], antialiased=False,
                             linewidth=0, rstride=1, cstride=1,
                             cmap=cm.coolwarm)
            ax2 = f2.add_subplot(122, projection='3d')
            ax2.plot_surface(XX2, YY2, regrid_mat3d[:,:,zInd_regrid],
                             linewidth=0, rstride=1, cstride=1,
                             antialiased=False,
                             cmap=cm.coolwarm)
            plt.draw()
            #f3 = plt.figure()
            #ax3 = f2.add_subplot(121, projection='3d')
            #ax4 = f2.add_subplot(122, projection='3d')
            plt.show()

    def test_complex_regrid(self):
        """test regrid for complex numbers."""
        print(self.id())
        mat3d_regrid = xfutils.xf_regrid_3d_nearest((self.field_nugrid.xdim,
                                                     self.field_nugrid.ydim,
                                                     self.field_nugrid.zdim),
                                                    (self.x2,self.y2,self.z2),
                                                    self.field_nugrid.ss_field_data('B','z'))
        
        self.assertEqual(np.dtype(np.complex_),mat3d_regrid.dtype)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
