#!/bin/bash
#
echo
echo This shell file is to check and install basic setup, to support automation testing.
echo
cd ..
# Checking if pip is installed on machine, if not then script will install pip.
pip -V | grep --quiet pip
if [ $? -eq 0 ] ; then
		echo
		echo Pip is installed on machine.
		echo
		pip install --upgrade pip
		echo
		sudo apt-get install python3-tk
		echo
		else
		echo
		echo Pip not installed, installing pip on machine.
		echo
		sudo apt install python3-pip -y
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
		pip install -r requirements.txt
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
cd setup/
echo