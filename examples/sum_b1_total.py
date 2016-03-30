#!/usr/bin/env python3
"""
Sum B1 transmit/receive fields.  B1+ = B1x +/- j*conj(B1y)
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import sys, ast, getopt
import numpy as np
import scipy.io as spio
import xfmatgrid, xfsystem

class B1WriterNonUniform(object):
    """Export the average of B1 transmit fields for coil sub(B1+)/n_coils."""
    def __init__(self, xf_project_dir, sim_ids):
        self._xf_project_dir = xf_project_dir
        self._sim_ids = sim_ids
        self._run_id = 1
        self._num_coils = len(sim_ids)
        self._b1_tx = None
        self._net_input_power = 1.0  # Scale input power to this value.

    def _average_b1_fields(self):
        """
        Calculate the sum of B1 transmit fields and normalize to number
        of coils.
        """
        for sim_id in self._sim_ids:
            print("Adding fields from simulation: ", sim_id)
            nu_field = xfmatgrid.XFFieldNonUniformGrid(self._xf_project_dir,
                                                       sim_id,
                                                       self._run_id)
            field_norm = 1./np.sqrt(xfsystem.XFSystem(self._xf_project_dir, sim_id, self._run_id).net_input_power)
            if self._b1_tx is None:
                self._b1_tx = field_norm * \
                              (nu_field.ss_field_data('B','x') + \
                              1j*np.conj(nu_field.ss_field_data('B','y')))
                self._xdim = nu_field.xdim
                self._ydim = nu_field.ydim
                self._zdim = nu_field.zdim
            else:
                self._b1_tx += field_norm * \
                               (nu_field.ss_field_data('B','x') + \
                                1j*np.conj(nu_field.ss_field_data('B','y')))


    def export_b1_tx_mat(self, file_name):
        """
        Export the average B1 transmit fields in mat file format.
        """
        self._average_b1_fields()
        print("Exporting B1+ fields in mat file format: ", file_name)
        export_dict = dict()
        export_dict['XDim'] = self._xdim
        export_dict['YDim'] = self._ydim
        export_dict['ZDim'] = self._zdim
        export_dict['B1Tx'] = self._b1_tx
        spio.savemat(file_name, export_dict, oned_as='column')

def main(argv):
    """Parse command line arguments and export average B1 fields."""
    print("Exporting B1 TX fields.")
    arg_dict = {}
    switches = { 'sim':list, 'xf_project':str, 'export_file':str }
    singles = ''
    long_form = [x+'=' for x in switches]
    d = {x[0]+':':'--'+x for x in switches}

    # parse command line options
    try:
        opts, args = getopt.getopt(argv, singles, long_form)

    except getopt.GetoptError as e:
        print("Bad argument Getopt: ", e.msg)

    for opt, arg in opts:
        if opt[1]+':' in d:
            o=d[opt[1]+':'][2:]
        elif opt in d.values():
            o=opt[2:]
        else: o=''

        if o and arg:
            if (switches[o].__name__ == 'list'):
                arg_dict[o] = ast.literal_eval(arg)
            else:
                arg_dict[o] = arg

        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, "Error: bad arg")
            sys.exit(2)

    xf_b1tx_wr = B1WriterNonUniform(arg_dict['xf_project'],
                                    arg_dict['sim'])
    xf_b1tx_wr.export_b1_tx_mat(arg_dict['export_file'])

if __name__ == "__main__":
    main(sys.argv[1:])
