#!/bin/sh

# Check system and set variables accordingly
os_type=`uname -s`
if [ "${os_type}" == "Linux" ]; then
    md5_bin='md5sum'
elif [ "${os_type}" == "Darwin" ]; then
    md5_bin='md5'
fi

base_url="http://www2.cmrr.umn.edu/~jerahmie"
url_timeout=10 # seconds before timeout
url_tries=10 # number of tries

# Download and extract test data for xfmod
dir="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Download Test_Coil.xf project
test_coil_targz="Test_Coil.xf.tar.gz"
test_coil_md5sum="Test_Coil.xf.tar.gz.md5sum"
test_coil_targz_path=${dir}/${test_coil_targz}
test_coil_url=${base_url}/${test_coil_targz}
test_coil_md5sum_url=${base_url}/${test_coil_md5sum}
echo "-> Downloading ${test_coil_targz}"
#wget --tries=${url_tries} --timeout=${url_timeout} -q -o /dev/null \
#     ${test_coil_url}
echo "-> Downloading ${test_coil_md5sum}"
wget --tries=${url_tries} --timeout=${url_timeout} -q -o /dev/null \
     ${test_coil_md5sum_url}

echo ${test_coil_md5sum}
if [ -f "${test_coil_md5sum}" ]; then
    known_test_coil_md5sum=`sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p' ${test_coil_md5sum}`
    rm ${test_coil_md5sum}
else
    echo "[ERROR] could not download ${test_coil_md5sum}"
    exit -1
fi
if [ -e "${test_coil_targz}" ]; then
    echo "-> Verify ${test_coil_targz}"
    tc_md5sum=`${md5_bin} ${test_coil_targz} | sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p'`
    echo ${tc_md5sum}
    if [ "${tc_md5sum}" == "${known_test_coil_md5sum}" ]; then
        echo "-> ${test_coil_targz} valid."
        echo "-> Extracting ${test_coil_targz}."
        tar xf ${test_coil_targz} -C ${dir}
        echo "-> Removing ${test_coil_targz}"
        rm ${test_coil_targz}
    else
        echo "[ERROR] ${test_coil_targz} not valid."
        exit -1
    fi
else
    echo "[ERROR] ${test_coil_targz} not found."
    exit -1
fi

# Download test CITI file
citi_file="project-s11.cti"
citi_md5sum_file="project-s11-cti.md5sum"
citi_url=${base_url}/${citi_file}
citi_md5sum_url=${base_url}/${citi_md5sum_file}
citi_file_valid=0

echo "-> Downloading hash file: ${citi_md5sum_file}"
wget --tries=${url_tries} --timeout=${url_timeout} -q -o /dev/null \
     ${citi_md5sum_url} 
if [ -f "${citi_md5sum_file}" ]; then
    known_citi_md5sum=`sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p' ${citi_md5sum_file}`
else
    echo "[ERROR] Could not download ${citi_md5sum_url}"
    exit -1
fi

# Check if CITI file exists and is valid.  Otherwise try to download a new one.
if [ -f "${citi_file}" ]; then
    test_citi_md5sum=`${md5_bin} ${citi_file} | sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p'`
    if [ "${known_citi_md5sum}" == "${test_citi_md5sum}" ]; then
        echo "-> ${citi_file} valid."
        citi_file_valid=1
    else
        echo "-> Checking for new ${citi_file}"
        wget -q -o /dev/null ${citi_url}
    fi
else
    echo "-> Downloading CITI file: ${citi_url}"
    wget -q -o /dev/null ${citi_url}
fi

# Perform final check on CITI file, if necessary.
if [ "${citi_file_valid}" == 0 ]; then
    test_citi_md5sum=`${md5_bin} ${citi_file} | sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p'`
    echo "-> Verifying ${citi_file}"
    if [ "${known_citi_md5sum}" == "${test_citi_md5sum}" ]; then
        echo "-> ${citi_file} valid."
    else
        echo "[ERROR] ${citi_file} md5sum invalid."
        exit -1
    fi
fi

# Cleanup: remove the md5sum file
rm ${citi_md5sum_file}
