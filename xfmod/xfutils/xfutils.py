"""
Helper functions for reading XFdtd data output files.
"""

from __future__ import (absolute_import, division, generators,
                        print_function, unicode_literals)

import re

MIN_RUN_ID = 1       # Minimum valid RunID
MAX_RUN_ID = 9999    # Maximum valid RunID
MIN_SIM_ID = 1       # Minimum valid Simulation ID
MAX_SIM_ID = 999999  # Maximum valid Simulation ID

def is_valid_run_id(run_id):
    """Check whether run_id is valid XFdtd run id."""
    if isinstance(run_id, int):
        if (run_id >= MIN_RUN_ID) and (run_id <= MAX_RUN_ID):
            return True
    return False

def is_valid_sim_id(sim_id):
    """Check whether sim_id is valid XFdtd simulatin id."""
    if isinstance(sim_id, int):
        if (sim_id >= MIN_SIM_ID) and (sim_id <= MAX_SIM_ID):
            return True
    return False

def is_valid_run_id_str(run_id_str):
    """Check whether run id string has proper form."""
    if re.match(r"^Run[0-9]{4}$", run_id_str):
        return True
    else:
        return False

def xf_run_id_to_str(run_id):
    """Converts a integer to XFdtd RunID string."""
    padded_string_length = 4
    run_id_string = 'Run'
    if is_valid_run_id(run_id):
        run_id_string_length = len(str(run_id))
        i = padded_string_length - run_id_string_length
        while i > 0:
            run_id_string += '0'
            i -= 1
        run_id_string += str(run_id)
        return run_id_string
    else:
        print("Invalid Run ID: ", run_id)
        return None

def xf_sim_id_to_str(sim_id):
    """Converts an integer to a valid XFdtd SimID string."""
    padded_string_length = 6
    sim_id_string = ''
    if is_valid_sim_id(sim_id):
        sim_id_string_length = len(str(sim_id))
        i = padded_string_length - sim_id_string_length
        while i > 0:
            sim_id_string += '0'
            i -= 1
        sim_id_string += str(sim_id)
        return sim_id_string
    else:
        print("Invalid Simulation ID: ", sim_id)
        return None

def xf_run_str_to_int(run_id_str):
    """"Converts run string to integer."""
    if is_valid_run_id_str(run_id_str):
        return int(run_id_str.split(r'Run')[1])
    
