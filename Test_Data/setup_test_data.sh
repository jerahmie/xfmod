#!/usr/bin/sh

# Download and extract test data for xfmod
#https://drive.google.com/open?id=0B9waCaG162I0U2pBdkhOaEhTc3M
GOOGLE_DRIVE_FILEID="0B9waCaG162I0U2pBdkhOaEhTc3M"
TEST_COIL_TARGZ=Test_Coil.xf.tar.gz
TEST_COIL_URL="https://googledrive.com/host/${GOOGLE_DRIVE_FILEID}"
echo "-> Downloading ${TEST_COIL_TARGZ}"
wget --verbose $TEST_COIL_URL -O ${TEST_COIL_TARGZ}
if [ -e "${TEST_COIL_TARGZ}" ]; then
    echo "-> Extracting ${TEST_COIL_TARGZ}."
    tar xf ${TEST_COIL_TARGZ}
    echo "-> Removing ${TEST_COIL_TARGZ}"
    rm ${TEST_COIL_TARGZ}
else
    echo "[ERROR] ${TEST_COIL_TARGZ} not found."
    exit -1
fi
