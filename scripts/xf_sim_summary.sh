#!/bin/bash

# Print summary of XF project simulations.
xfproj=$1
if [ ! -d "${xfproj}" ]; then
    echo "ERROR: Could not find project: ${xfproj}"
    exit -1
fi

