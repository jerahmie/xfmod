#!/bin/sh

# Webdir
base_url="http://www2.cmrr.umn.edu/~jerahmie"

# Test files
test_files=('Custom_Cosim.xf.tar.gz' \
                'Test_Coil.xf.tar.gz' \
		'Test_Coil_v771.xf.tar.gz' \
                'green_coil_7T_duke_2mm_vopgen.tar.gz' \
                'project-s11.cti')

# Check system and set variables accordingly
os_type=`uname -s`
if [ "${os_type}" == "Linux" ]; then
    md5_bin='md5sum'
elif [ "${os_type}" == "Darwin" ]; then
    md5_bin='md5'
fi

# wget params
url_timeout=60 # seconds before timeout
url_tries=10 # number of tries
progress_type="bar:noscroll"

# Function: md5sum_from_file
#   Returns the md5sum from a *.md5sum file
md5sum_from_file() 
{
    if [ -z "$1" ]; then
        echo "Usage: md5sum_from_file myfile.md5sum"
        exit -1
    fi
    echo `sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p' ${1}`
}

# Function: download_file server file
# ex:
#   download_file "http://my.server.com/~jerahmie" "myfile.txt"

download_file ()
{
    if [ -z "$1" ]; then
        echo "Parameter #1 is zero length."
        exit -1
    fi
    local download_req=1
    local url=${1}
    local data_file=${2}
    local md5sum_file="${2}.md5sum"
    local md5sum_url=${url}/${md5sum_file}
    printf "Downloading files %s\n" ${md5sum_url}
    local temp_dir=$(mktemp -d /tmp/test_dataXXXX)

    wget --tries=${url_tries} --timeout=${url_timeout} \
         --progress=${progress_type} \
         -O ${temp_dir}/${md5sum_file} ${md5sum_url}
    if [ ! -f ${temp_dir}/${md5sum_file} ]; then
        echo "Download error: " ${md5sum_file}
    fi
    local remote_md5sum=$(md5sum_from_file ${temp_dir}/${md5sum_file})
    if [ -f "${md5sum_file}" ]; then
        echo "Found local md5sum file: " ${md5sum_file}
        local local_md5sum=`md5sum_from_file ${md5sum_file}`
        if [ "${local_md5sum}" == "${remote_md5sum}" ]; then
            echo "Checksum match: ${md5sum_file}. Skipping ${data_file} download."
            download_req=0
        fi
    fi
    
    if [ "${download_req}" -eq 1 ]; then
        # Download required
        if [ -e "${data_file}" ]; then
            rm ${data_file}
        elif [ -e "${data_file%.tar.gz}" ]; then
            rm -r "${data_file%.tar.gz}"
        fi
        wget --tries=${url_tries} --timeout=${url_timeout}  \
             --progress=${progress_type} ${url}/${data_file}
        local df_md5sum=`${md5_bin} ${data_file} | sed -n 's/.*\([0-9a-f]\{32\}\).*/\1/p'`
        if [ "${df_md5sum}" != "${remote_md5sum}" ]; then
            echo "Download checksum failed"
            exit -1
        else
            if [ "${data_file: -6}" == "tar.gz"  ]; then
                tar xf ${data_file} && rm ${data_file}
            fi
            mv ${temp_dir}/${md5sum_file} .
        fi
    fi
    rm -r ${temp_dir}    
}


for idx in "${!test_files[@]}"
do
    download_file ${base_url} "${test_files[${idx}]}"
done

echo ""
echo "Test data setup is complete."
echo ""
