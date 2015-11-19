#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)
import sys, os
import struct
import unittest
import numpy as np
import scipy.io as spio
import numpy.testing as npt
import xfmatgrid

TEST_COIL_DIR = os.path.normpath(os.path.join(os.getcwd(), '..', '..',
                                              'Test_Data', 'Test_Coil.xf'))
RUN_OUT_DIR = os.path.join(TEST_COIL_DIR, 'Simulations', '000001',
                           'Run0001', 'output')
MULTIPOINT_SENSOR_FILE = os.path.realpath(os.path.join(RUN_OUT_DIR,
                                                       'MultiPoint_Solid_Sensor1_0_info.bin'))
FREQUENCIES_BIN = os.path.join(RUN_OUT_DIR, 'MultiPoint_Solid_Sensor1_0',
                               'frequencies.bin')

# Testing constants
TEST_FREQUENCY = 296500000.0  # 296.5 MHz

TEST_MULTIPOINT_DIRS = ['ss_Exit', 'ss_Exrt', 'ss_Eyit', 'ss_Eyrt', 'ss_Ezit', 'ss_Ezrt', 'ss_Hxit', 'ss_Hxrt', 'ss_Hyit', 'ss_Hyrt', 'ss_Hzit', 'ss_Hzrt', 'ss_Jxi', 'ss_Jxr', 'ss_Jyi', 'ss_Jyr', 'ss_Jzi', 'ss_Jzr', 'ss_Bxit', 'ss_Bxrt', 'ss_Byit', 'ss_Byrt', 'ss_Bzit', 'ss_Bzrt', 'ss_PddEx', 'ss_PddEy', 'ss_PddEz', 'ss_PddHx', 'ss_PddHy', 'ss_PddHz']

XF_MAT_FILE_NAME = os.path.normpath(os.path.join(os.getcwd(), '..', '..',
                                                 'Test_Data', 'Test_Coil.xf',
                                                 'Export', 'Raw', 
                                                 'total_B_field_data_raw_000001.mat' ))

X_DIM_VALS = [-0.13407564, -0.13207703, -0.13007841, -0.12807979, \
 -0.12608118, -0.12408256, -0.12208394, -0.12008533, -0.11808671, \
 -0.11608809, -0.11408948, -0.11296947, -0.11184946, -0.11046022, \
 -0.10907098, -0.10768175, -0.10592157, -0.10445878, -0.102996,   \
 -0.10153321, -0.10034622, -0.09929813, -0.09832934, -0.09736056, \
 -0.09624302, -0.09512548, -0.09409461, -0.09306374, -0.09203287, \
 -0.091002,   -0.08997113, -0.08894026, -0.08790939, -0.08727583, \
 -0.08664226, -0.08566929, -0.08469631, -0.08372333, -0.08275035, \
 -0.08207969, -0.08150052, -0.08092135, -0.0798847,  -0.07802921, \
 -0.07669205, -0.07535489, -0.07433428, -0.07331368, -0.0725479,  \
 -0.07178213, -0.07101635, -0.07025058, -0.06948481, -0.06871903, \
 -0.06795326, -0.06718748, -0.06642171, -0.06565594, -0.06489016, \
 -0.06412439, -0.06335861, -0.06255925, -0.06175988, -0.06096051, \
 -0.06016114, -0.05936177, -0.05856241, -0.05776304, -0.05696367, \
 -0.0561643,  -0.05536494, -0.05456557, -0.0537662,  -0.05322115, \
 -0.05267611, -0.05213106, -0.05158151, -0.05102742, -0.0500816,  \
 -0.04846713, -0.04651833, -0.04456954, -0.04270094, -0.04138479, \
 -0.03985471, -0.03832463, -0.03679456, -0.03526448, -0.03346445, \
 -0.03238463, -0.03173687, -0.03108911, -0.03044134, -0.02979358, \
 -0.02914581, -0.02849805, -0.02785029, -0.02720252, -0.02655544, \
 -0.02590836, -0.02526128, -0.0246142 , -0.02396712, -0.02332004, \
 -0.02267296, -0.02202588, -0.0213788 , -0.02073172, -0.02008464, \
 -0.01943756, -0.01879048, -0.0181434,  -0.01749632, -0.01684924, \
 -0.01620216, -0.01555508, -0.014908,   -0.01440803, -0.01390806, \
 -0.01340809, -0.01290813, -0.0119596,  -0.01016007, -0.00859767, \
 -0.00703527, -0.00547288, -0.00391048, -0.0023181,  -0.00072573, \
  0.00072572,  0.00231746,  0.00390921,  0.00543524,  0.00696127, \
  0.0084873,   0.01001333,  0.01181311,  0.01290811,  0.01357432, \
  0.01424052,  0.01490673,  0.01555381,  0.01620089,  0.01684797, \
  0.01749505,  0.01814213,  0.01878921,  0.01943629,  0.02008337, \
  0.02073045,  0.02137753,  0.02202461,  0.02267169,  0.02331877, \
  0.02396585,  0.02461293,  0.02526001,  0.0259071,   0.02655418, \
  0.02720126,  0.02784918,  0.0284971 ,  0.02914502,  0.02979294, \
  0.03044086,  0.03108878,  0.0317367 ,  0.03238462,  0.03346456, \
  0.0352646,   0.03679464,  0.03832469,  0.03985473,  0.04138478, \
  0.04270093,  0.04456827,  0.04618224,  0.0477962,   0.04941016, \
  0.05102413,  0.05213105,  0.05294698,  0.05376291,  0.05456228, \
  0.05536165,  0.05616102,  0.05696038,  0.05775975,  0.05855912, \
  0.05935849,  0.06015785,  0.06095722,  0.06175659,  0.06255596, \
  0.06335532,  0.06412135,  0.06488738,  0.0656534 ,  0.06641943, \
  0.06718545,  0.06795148,  0.06871751,  0.06948353,  0.07024956, \
  0.07101558,  0.07178161,  0.07254764,  0.07331366,  0.07442386, \
  0.07604823,  0.0776726,   0.07929697,  0.08092133,  0.08207524, \
  0.08274706,  0.08371975,  0.08469244,  0.08566512,  0.08663781, \
  0.08727137,  0.08790493,  0.08902647,  0.09014801,  0.09126956, \
  0.0923911,   0.09351264,  0.09463418,  0.09554132,  0.09644846, \
  0.0973556,   0.09832439,  0.09929318,  0.10034621,  0.1015332 , \
  0.1029945,   0.10445581,  0.10591712,  0.10767679,  0.10906768, \
  0.11045856,  0.11184945,  0.11296698,  0.11408452,  0.1159019,  \
  0.11771927,  0.11953664,  0.12135402,  0.12317139,  0.12498876, \
  0.12680614,  0.12862351,  0.13044088,  0.13225826 ]

Y_DIM_VALS = [    -1.40863998e-01,  -1.38865382e-01,  -1.36866766e-01,
-1.34868149e-01,  -1.33029579e-01,  -1.31191009e-01,  -1.29478270e-01,
-1.27765531e-01,  -1.26052792e-01,  -1.24340053e-01,  -1.22568783e-01,
-1.20597750e-01,  -1.18896483e-01,  -1.17302315e-01,  -1.15708147e-01,
-1.13927426e-01,  -1.12146705e-01,  -1.11001562e-01,  -1.09934765e-01,
-1.08867968e-01,  -1.07801172e-01,  -1.06734375e-01,  -1.05667578e-01,
-1.04600782e-01,  -1.03533985e-01,  -1.02467188e-01,  -1.01400391e-01,
-1.00359992e-01,  -9.93195916e-02,  -9.82791917e-02,  -9.72387918e-02,
-9.61983919e-02,  -9.51579921e-02,  -9.41175922e-02,  -9.30771923e-02,
-9.24983532e-02,  -9.19195141e-02,  -9.10144376e-02,  -8.95992544e-02,
-8.76739645e-02,  -8.62746503e-02,  -8.48753362e-02,  -8.34760220e-02,
-8.18419743e-02,  -8.05783591e-02,  -7.93147439e-02,  -7.74634781e-02,
-7.62881769e-02,  -7.55420211e-02,  -7.47958652e-02,  -7.40497094e-02,
-7.33035535e-02,  -7.25573977e-02,  -7.18112418e-02,  -7.10650860e-02,
-7.03189301e-02,  -6.95727742e-02,  -6.88266184e-02,  -6.80206943e-02,
-6.72147703e-02,  -6.64088462e-02,  -6.56029221e-02,  -6.47969981e-02,
-6.39910740e-02,  -6.31851499e-02,  -6.23792259e-02,  -6.15733018e-02,
-6.07673777e-02,  -5.99614537e-02,  -5.91555296e-02,  -5.83496056e-02,
-5.75436815e-02,  -5.69989620e-02,  -5.64542425e-02,  -5.59095229e-02,
-5.49057365e-02,  -5.30560007e-02,  -5.17081582e-02,  -5.03603157e-02,
-4.84163190e-02,  -4.64723222e-02,  -4.45283254e-02,  -4.25783709e-02,
-4.06504647e-02,  -3.87225585e-02,  -3.67946524e-02,  -3.48667462e-02,
-3.31096952e-02,  -3.20360649e-02,  -3.13800328e-02,  -3.07240007e-02,
-3.00679685e-02,  -2.94119364e-02,  -2.87559043e-02,  -2.80998722e-02,
-2.74392761e-02,  -2.67786799e-02,  -2.61180838e-02,  -2.54574877e-02,
-2.47968916e-02,  -2.41362954e-02,  -2.34756993e-02,  -2.28151032e-02,
-2.21545071e-02,  -2.14939109e-02,  -2.08333148e-02,  -2.01727187e-02,
-1.95121226e-02,  -1.88515264e-02,  -1.81909303e-02,  -1.75303342e-02,
-1.68697381e-02,  -1.62091420e-02,  -1.55485458e-02,  -1.50487010e-02,
-1.45488563e-02,  -1.40490115e-02,  -1.35491667e-02,  -1.26120831e-02,
-1.08552863e-02,  -8.89356127e-03,  -6.93183620e-03,  -4.97011113e-03,
-3.00838606e-03,  -1.07004685e-03,   2.96700019e-09,   1.07005279e-03,
 3.00762913e-03,   4.93331306e-03,   6.85899699e-03,   8.78468092e-03,
 1.07103648e-02,   1.24672887e-02,   1.35491724e-02,   1.42153779e-02,
 1.48815833e-02,   1.55477888e-02,   1.62083849e-02,   1.68689811e-02,
 1.75295772e-02,   1.81901733e-02,   1.88507694e-02,   1.95113656e-02,
 2.01719617e-02,   2.08325578e-02,   2.14931539e-02,   2.21537501e-02,
 2.28143462e-02,   2.34749423e-02,   2.41355384e-02,   2.47961346e-02,
 2.54567307e-02,   2.61173268e-02,   2.67779229e-02,   2.74385190e-02,
 2.80991152e-02,   2.87552744e-02,   2.94114337e-02,   3.00675929e-02,
 3.07237522e-02,   3.13799114e-02,   3.20360706e-02,   3.31098049e-02,
 3.48668559e-02,   3.67947361e-02,   3.87226163e-02,   4.06504965e-02,
 4.25783768e-02,   4.45159531e-02,   4.64633109e-02,   4.84106687e-02,
 5.03580264e-02,   5.15941409e-02,   5.28302553e-02,   5.46807561e-02,
 5.59095288e-02,   5.67254605e-02,   5.75413922e-02,   5.83473163e-02,
 5.91532403e-02,   5.99591644e-02,   6.07650885e-02,   6.15710125e-02,
 6.23769366e-02,   6.31828606e-02,   6.39887847e-02,   6.47947088e-02,
 6.56006328e-02,   6.64065569e-02,   6.72124810e-02,   6.80184050e-02,
 6.88243291e-02,   6.95707145e-02,   7.03170998e-02,   7.10634852e-02,
 7.18098706e-02,   7.25562559e-02,   7.33026413e-02,   7.40490267e-02,
 7.47954120e-02,   7.55417974e-02,   7.62881828e-02,   7.74636647e-02,
 7.93149305e-02,   8.05784554e-02,   8.18419802e-02,   8.34760280e-02,
 8.48745770e-02,   8.62731261e-02,   8.76716752e-02,   8.90876234e-02,
 9.05035717e-02,   9.19195200e-02,   9.30684393e-02,   9.41094620e-02,
 9.51504847e-02,   9.61915075e-02,   9.72325302e-02,   9.82735529e-02,
 9.93145756e-02,   1.00355598e-01,   1.01396621e-01,   1.02463837e-01,
 1.03531054e-01,   1.04598270e-01,   1.05665486e-01,   1.06732702e-01,
 1.07799919e-01,   1.08867135e-01,   1.09934351e-01,   1.11001568e-01,
 1.12146710e-01,   1.13927431e-01,   1.15708152e-01,   1.17299900e-01,
 1.18891648e-01,   1.20593979e-01,   1.22568789e-01,   1.24335218e-01,
 1.26049167e-01,   1.27763116e-01,   1.29477065e-01,   1.31191014e-01,
 1.33027164e-01,   1.34863314e-01,   1.36680678e-01,   1.38498042e-01,
 1.40315406e-01]

Z_DIM_VALS = [    -2.05277938e-02,  -1.86039625e-02,  -1.66801312e-02,
-1.47562999e-02,  -1.28324686e-02,  -1.09086373e-02,  -8.98480600e-03,
-7.06097470e-03,  -5.13714340e-03,  -3.14938088e-03,  -1.99861659e-03,
-1.33241111e-03,  -6.66205630e-04,  -1.49999998e-10,   6.66205330e-04,
 1.33241081e-03,   1.99861629e-03,   3.15193392e-03,   5.14852770e-03,
 7.11017244e-03,   9.07181718e-03,   1.10334619e-02,   1.29951067e-02,
 1.49567514e-02,   1.69183961e-02,   1.88800409e-02,   2.08416856e-02,
 2.28033304e-02,   2.47649751e-02,   2.67266198e-02,   2.86882646e-02,
 3.06499093e-02,   3.26115541e-02,   3.45731988e-02,   3.65348435e-02,
 3.84964883e-02,   4.04581330e-02,   4.24197778e-02,   4.43814225e-02,
 4.63430672e-02,   4.83047120e-02,   5.02663567e-02,   5.22280015e-02,
 5.41896462e-02,   5.61512909e-02,   5.81129357e-02,   6.00745804e-02,
 6.20362252e-02,   6.39978699e-02,   6.59595146e-02,   6.79211594e-02,
 6.98828041e-02,   7.18551032e-02,   7.30013826e-02,   7.36675881e-02,
 7.43337935e-02,   7.49999990e-02,   7.56662045e-02,   7.63324100e-02,
 7.69986155e-02,   7.81520270e-02,   8.01489458e-02,   8.21155117e-02,
 8.40820775e-02,   8.60486434e-02,   8.80152093e-02,   8.99817751e-02,
 9.19483410e-02,   9.39149068e-02,   9.58814727e-02,   9.78480385e-02,
 9.98146044e-02,   1.01781170e-01,   1.03747736e-01,   1.05714302e-01,
 1.07680868e-01,   1.09647434e-01,   1.11613999e-01,   1.13580565e-01,
 1.15547131e-01,   1.17513697e-01,   1.19480263e-01,   1.21446829e-01,
 1.23413395e-01,   1.25379960e-01,   1.27346526e-01,   1.29313092e-01,
 1.31279658e-01,   1.33246224e-01,   1.35212790e-01,   1.37179356e-01,
 1.39145921e-01,   1.41112487e-01,   1.43079053e-01,   1.45045619e-01,
 1.47012185e-01,   1.48978751e-01,   1.50945316e-01,   1.52911882e-01,
 1.54878448e-01,   1.56854125e-01,   1.58001386e-01,   1.58667591e-01,
 1.59333797e-01,   1.60000002e-01,   1.60666208e-01,   1.61332413e-01,
 1.61998619e-01,   1.63147772e-01,   1.65129974e-01,   1.67123137e-01,
 1.69116300e-01,   1.71109463e-01,   1.73102626e-01,   1.75095789e-01,
 1.77088952e-01,   1.79082115e-01,   1.81075278e-01,   1.83068441e-01,
 1.85061604e-01,   1.87054767e-01,   1.89047930e-01,   1.91041093e-01,
 1.93034256e-01,   1.95027419e-01,   1.97020582e-01,   1.99013746e-01,
 2.01006909e-01,   2.03000072e-01,   2.04993235e-01,   2.06986398e-01,
 2.08979561e-01,   2.10972724e-01,   2.12965887e-01,   2.14959050e-01,
 2.16952213e-01,   2.18945376e-01,   2.20938539e-01,   2.22931702e-01,
 2.24924865e-01,   2.26918028e-01,   2.28911191e-01,   2.30904354e-01,
 2.32897517e-01,   2.34890680e-01,   2.36883843e-01,   2.38877006e-01,
 2.40870169e-01,   2.42863332e-01,   2.44856495e-01,   2.46849658e-01,
 2.48842821e-01,   2.50835984e-01,   2.52829147e-01,   2.54822310e-01,
 2.56815473e-01,   2.58808636e-01,   2.60801799e-01,   2.62794962e-01,
 2.64788125e-01,   2.66781288e-01,   2.68774451e-01,   2.70767614e-01,
 2.72760777e-01,   2.74753940e-01,   2.76747103e-01,   2.78740266e-01,
 2.80733429e-01,   2.82726592e-01,   2.84719755e-01,   2.86712918e-01,
 2.88706081e-01,   2.90699244e-01,   2.92692407e-01,   2.94685570e-01,
 2.96678733e-01,   2.98671897e-01,   3.00665060e-01,   3.02658223e-01,
 3.04651386e-01,   3.06644549e-01,   3.08637712e-01,   3.10630875e-01,
 3.12624038e-01,   3.14617201e-01]

class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    @classmethod
    def setUpClass(cls):
        cls.field_nugrid = xfmatgrid.XFFieldNonUniformGrid(TEST_COIL_DIR, 1, 1)
    def setUp(self):
        self.fieldName = r'B'

    def test_xf_run_id_to_str(self):
        """Verify XFdtd valid run string composition."""
        self.assertTrue(xfmatgrid.xfutils.is_valid_run_id(1))
        self.assertTrue(xfmatgrid.xfutils.is_valid_run_id(9999))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(-1))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(0))
        self.assertFalse(xfmatgrid.xfutils.is_valid_run_id(10000.0))
        self.assertEqual('Run0001', xfmatgrid.xfutils.xf_run_id_to_str(1))
        self.assertEqual('Run9999', xfmatgrid.xfutils.xf_run_id_to_str(9999))

    def test_xf_sim_id_to_str(self):
        """Verify XFdtd valid simulation string composition."""
        self.assertTrue(xfmatgrid.xfutils.is_valid_sim_id(1))
        self.assertTrue(xfmatgrid.xfutils.is_valid_sim_id(999999))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(-1.1))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(0))
        self.assertFalse(xfmatgrid.xfutils.is_valid_sim_id(1000000))
        self.assertEqual('000001', xfmatgrid.xfutils.xf_sim_id_to_str(1))
        self.assertEqual('999999', xfmatgrid.xfutils.xf_sim_id_to_str(999999))

    def test_project_file(self):
        self.assertEqual(TEST_COIL_DIR, self.field_nugrid.project_dir)
        self.assertEqual(MULTIPOINT_SENSOR_FILE,
                         self.field_nugrid._mp_ss_info_file[0])
        self.assertEqual('Rmpt', self.field_nugrid._mp_ss_info.header)

    def test_frequencies_bin(self):
        self.assertEqual(TEST_FREQUENCY,
                         self.field_nugrid._mp_freq._frequencies[0])

    def test_field_data(self):
        self.assertEqual(TEST_MULTIPOINT_DIRS,
                         self.field_nugrid._mp_field_types)

    def test_ranges(self):
        """Test x-, y-, and z-dimenions."""
        self.assertTrue(np.allclose(X_DIM_VALS, self.field_nugrid.xdim))
        self.assertTrue(np.allclose(Y_DIM_VALS, self.field_nugrid.ydim))
        self.assertTrue(np.allclose(Z_DIM_VALS, self.field_nugrid.zdim))

    def test_write_matfile(self):
        """Write and verify the x-, y-, and z-dimension values."""
        export_dict = dict()
        export_dict['X_Dimension_3'] = self.field_nugrid.xdim
        export_dict['Y_Dimension_2'] = self.field_nugrid.ydim
        export_dict['Z_Dimension_1'] = self.field_nugrid.zdim
        export_dict[self.fieldName + 'x'] = self.field_nugrid.ss_field_data(self.fieldName, 'x')
        export_dict[self.fieldName + 'y'] = self.field_nugrid.ss_field_data(self.fieldName, 'y')
        export_dict[self.fieldName + 'z'] = self.field_nugrid.ss_field_data(self.fieldName, 'z')
        spio.savemat('test.mat', export_dict)
        py_mat_file = spio.loadmat('test.mat')

        if os.path.exists(XF_MAT_FILE_NAME):
            print("Found: ", XF_MAT_FILE_NAME)
        xf_mat_file = spio.loadmat(XF_MAT_FILE_NAME)
        self.assertTrue(np.allclose(xf_mat_file['X_Dimension_3'],
                                    py_mat_file['X_Dimension_3']))
        self.assertTrue(np.allclose(xf_mat_file['Y_Dimension_2'], 
                                    py_mat_file['Y_Dimension_2']))
        self.assertTrue(np.allclose(xf_mat_file['Z_Dimension_1'], 
                                    py_mat_file['Z_Dimension_1']))

        # self.assertEqual(self.field_nugrid._mp_ss_info.num_points, np.size(mat_file[self.fieldName + 'x']))
        py_mat_file.close()
        xf_mat_file.close()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
