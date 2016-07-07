#!/usr/bin/sh

# Download and extract test data for xfmod
DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOOGLE_DRIVE_FILEID="0B9waCaG162I0U2pBdkhOaEhTc3M"
TEST_COIL_TARGZ=${DIR}/Test_Coil.xf.tar.gz
TEST_COIL_URL="https://googledrive.com/host/${GOOGLE_DRIVE_FILEID}"
echo "-> Downloading ${TEST_COIL_TARGZ}"
wget -q -o /dev/null $TEST_COIL_URL -O ${TEST_COIL_TARGZ}
if [ -e "${TEST_COIL_TARGZ}" ]; then
    echo "-> Extracting ${TEST_COIL_TARGZ}."
    tar xf ${TEST_COIL_TARGZ} -C ${DIR}
    echo "-> Removing ${TEST_COIL_TARGZ}"
    rm ${TEST_COIL_TARGZ}
else
    echo "[ERROR] ${TEST_COIL_TARGZ} not found."
    exit -1
fi
