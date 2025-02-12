#!/bin/bash
#
echo
echo This shell file is to check and install basic setup, to support automation testing.
echo
cd ..
# Checking if pip is installed on machine, if not then script will install pip.
pip3 -V | grep --quiet pip
if [ $? -eq 0 ] ; then
		echo
		echo Pip is installed on machine.
		echo
		pip3 install --upgrade pip
		echo
		else
		echo
		echo Pip not installed, installing pip on machine.
		echo
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python3 get-pip.py
		echo
		echo Pip has been installed on machine.
		echo
		fi

# Checking python version on machine, and installing requirements
python3 -V | grep --quiet Python
if [ $? -eq 0 ] ; then
		echo
		echo Python3 is installed on machine, checking requirements
		echo
		cd ..
		echo Installing supporting requirements.
		echo
		pip3 install -r requirements.txt
		echo 
		echo Requirements has been installed on machine
		cd src/
		fi

# Downloading chrome driver on machine
python3 DownloadChromeDriver.py
echo 
echo All supporting requirements has been installed on machine.
echo Now you are ready to run Robot Tests on your machine.
echo
echo
cd setup/
echo 