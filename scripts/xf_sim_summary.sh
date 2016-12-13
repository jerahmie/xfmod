#!/bin/bash

# Print summary of XF project simulations.
xfproj=$1
if [ ! -d "${xfproj}" ]; then
    echo "ERROR: Could not find project: ${xfproj}"
    exit -1
fi

simdirs=(${xfproj}/Simulations/*/)
separator="-------------------------------------------------------------------"
printf "\n%s\n" "${separator}"
printf "Sim ID\t%s\n" "$(basename ${xfproj})"
printf "%s\n" "${separator}"

for d in ${simdirs[@]}; do
    md="${d}/SimulationMetadata/metadata.xml"
    if [ -f "${md}" ]; then
        simid="$(basename ${d} | sed 's/^0*//')"
        sname="$(sed -n 's/.*sname=\"\([^\"]*\)\".*/\1/p' ${md})"
        printf "${simid}) ${sname}\n"

        simtype="$(sed -n 's/.*SimulationType=\"\([a-zA-Z]*\).*/\1/p' ${md})"
        printf "\tType:\t${simtype}\n" 

        notes="$(sed -n 's/.*<Notes>\(.*\)<\/Notes>/\1/p' ${md} | \
                       sed 's/%0A/\\n\\t\\t/g')"
        printf "\tNotes:\t${notes}\n"

    fi

done
