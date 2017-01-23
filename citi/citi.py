"""
CITI Data Format object.
"""

from __future__ import(absolute_import, division, generators,
                       print_function, unicode_literals)

import os
import sys
import re

class Citi(object):
    """
    Citi object stores data encapsulated in a CITI format file.
    """
    # regular expressions for matcthing citi file data
    _re_citifile = re.compile(r'^CITIFILE\s*([A-F0-9\.]*)$', re.MULTILINE)
    _re_name = re.compile(r'^NAME\s*([A-Z]*)$', re.MULTILINE)
    _re_data = re.compile(r'^(?:(?:RAW_)?DATA|(?:CAL_)(?:SET|KIT)|DELAY_TABLE)\s*([0-9A-Z\,\[\]]*)\s*(RI)$', re.MULTILINE)
    _re_var = re.compile(r'^VAR\s*([A-Z]*)\s*([A-Z]*)\s*([0-9]*)$', re.MULTILINE)
    _re_var_list = re.compile(r'^VAR_LIST_BEGIN$\n([e0-9\.\n\+\-]*)^VAR_LIST_END$', re.MULTILINE)
    _re_citi_data = re.compile(r'^BEGIN$\n([0-9e\+\-\,\.\n]*)^END$', re.MULTILINE)

    def __init__(self, file_name = None):
        self._file_name = file_name
        self._version = None
        self._name = None
        self._data_name = None    # DATA, etc.
        self._data_type = None    # Probably 'RI'
        self._var_name = None
        self._var_type = None
        self._var_num = None      # Number of data points
        self._var_list = None     # Variable, typically frequency
        self._citi_data = None    # CITI DATA
        if self._file_name:
            self._parse_citi()
        

    def _parse_citi(self):
        """
        Load and parse CITI file.
        """
        try:
            with open(self._file_name, 'r') as citi_file:
                citi_string = citi_file.read()
                
            self._version = self._re_citifile.search(citi_string).group(1)
            self._name = self._re_name.search(citi_string).group(1)
            data_match = self._re_data.search(citi_string)
            self._data_name = data_match.group(1)
            self._data_type = data_match.group(2)
            var_match = self._re_var.search(citi_string)
            self._var_name = var_match.group(1)
            self._var_type = var_match.group(2)
            self._var_num = int(var_match.group(3))
            var_list_match = self._re_var_list.search(citi_string).group(1).split('\n')
            self._var_list = [eval(elem) for elem in var_list_match[:-1]]
            citi_data = self._re_citi_data.search(citi_string).group(1)
            citi_data = citi_data.replace('\n', 'j\n')
            citi_data = citi_data.replace(r',', r' + ').replace(r' + -', r' - ')
            citi_data = citi_data.split('\n')
            self._citi_data = [eval(elem) for elem in citi_data[:-1]]

        except FileNotFoundError as err:
            print("[ERROR] Could not find file: " + self._file_name)
            raise err
         
    @property
    def version(self):
        """Return the CITI version."""
        return self._version

    @property
    def name(self):
        """Return the CITI file package name."""
        return self._name

    @property
    def var(self):
        """Returns the independent variable (e.g. FREQUENCY)."""
        return self._var_name

    @property
    def var_type(self):
        """Returns the type of the independent variable."""
        return self._var_type

    @property
    def var_num(self):
        """Returns the number of elements in the independent variable/data."""
        return self._var_num

    @property
    def data_name(self):
        """Returns the data variable name."""
        return self._data_name

    @property
    def data(self):
        """Returns the CITI data structure."""
        return self._citi_data

    @property
    def var_list(self):
        """Returns the independent variable list."""
        return self._var_list
    
    def file(self, file_name):
        """Set the file name and extract data."""
        self._file_name = file_name
        self._parse_citi()

    def data_at_var(self, var, interp='linear'):
        """Return data at given value."""
        PRECISION = 1.0e-6
        data_at_var = 0.0
        if interp=='linear':
            nearest_ind = self._find_nearest_ind(self._var_list, var)
            if abs(self._var_list[nearest_ind] - var) <= PRECISION:
                data_at_var =  self._citi_data[nearest_ind] 
            elif var > self._var_list[nearest_ind]:
                data_at_var = self._lin_fit(var,
                                            [self._var_list[nearest_ind], 
                                             self._var_list[nearest_ind + 1]],
                                            [self._citi_data[nearest_ind],
                                             self._citi_data[nearest_ind + 1]])
            elif var < self._var_list[nearest_ind]:
                data_at_var = self._lin_fit(var,
                                            [self._var_list[nearest_ind - 1],
                                             self._var_list[nearest_ind]],
                                            [self._citi_data[nearest_ind - 1],
                                             self._citi_data[nearest_ind]])

        return data_at_var
        
    def _lin_fit(self, xs, x0, y0):
        """Calculate linear fit given two points and sample point."""
        ai = (y0[1].imag - y0[0].imag)/(x0[1] - x0[0])
        ar = (y0[1].real - y0[0].real)/(x0[1] - x0[0])
        ysi = y0[0].imag + ai * (xs - x0[0])
        ysr = y0[0].real + ar * (xs - x0[0])

        return ysr + ysi*1.0j

    def _find_nearest_ind(self, data, val):
        """Return index nearest to value in data."""
        tmp = [abs(d-val) for d in data]
        idx = tmp.index(min(tmp))
        return idx

def main(argv):
    pass
    

if __name__ == "__main__":
    main(sys.argv[1:])
    print("[", __file__,  "] Done.")
