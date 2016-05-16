#!/usr/bin/sh

# Download and extract test data for xfmod
#https://drive.google.com/open?id=0B9waCaG162I0U2pBdkhOaEhTc3M
GOOGLE_DRIVE_FILEID="0B9waCaG162I0U2pBdkhOaEhTc3M"
TEST_COIL_TARGZ=Test_Coil.xf.tar.gz
TEST_COIL_URL="https://googledrive.com/host/${GOOGLE_DRIVE_FILEID}"
echo "-> Downloading ${TEST_COIL_TARGZ}"
wget --verbose $TEST_COIL_URL
if [ -e "${GOOGLE_DRIVE_FILEID}" ]; then
    echo "-> Extracting test coil data."
    tar xvf ${GOOGLE_DRIVE_FILEID}
    rm ${GOOGLE_DRIVE_FILEID}
else
    echo "[ERROR] ${TEST_COIL_TARGZ} not found."
    exit -1
fi
