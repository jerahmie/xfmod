"""
Vopgen helper function to remove NaN, Inf, -Inf from numpy matrix and replace 
with zeros.
"""

import numpy as np

def removeNaNs(mat):
    """Replace NaN, +/- Inf values with zero."""
    mat[np.isnan(mat)] = 0
    mat[np.isinf(mat)] = 0
    return mat
