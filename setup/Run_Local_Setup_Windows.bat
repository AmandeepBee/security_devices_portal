@echo off
cd ..
:: Check for Curl Installation
%ALLUSERSPROFILE%
echo.
echo ....................................Checking Curl installation on machine..........................................
echo.
curl -V 7>NUL
if errorlevel 1 goto errorNoCurl
echo.
echo .........................................Curl is installed on machine..............................................
echo.

:: Check for Chocolatey Installation
echo.
echo ..................................Checking chocolatey installation on machine......................................
echo.
choco
if errorlevel 2 goto errorNoChocolatey
echo.
echo .........................................Chocolatey is installed on machine........................................
echo.

:: Check for Python Installation
:checkingPython
echo.
echo ...................................Checking python installation on machine.........................................
echo.
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: Upgrade pip
:pipUpgrade
echo.
echo ..........................................Python is installed on machine...........................................
echo.
echo.
echo ............................................Performing pip upgrade..................................................
echo.
python -m pip install --upgrade pip
echo.

:: Install project requirements
:checkingRequirements
echo.
echo ..............................................Checking requirements................................................
echo.
echo.
pip install -r requirements.txt
echo.
echo.
echo ......................................Requirements has been installed on machine...................................
echo.
goto messageDisplay

:: Python installation
:errorNoPython
echo.
echo Error^: Python not installed
curl https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -o python_install.exe
python_install.exe /quiet InstallAllUsers=1 PrependPath=1
del python_install.exe
cd scripts_windows
refreshenv
echo.
goto checkingPython

:: Curl installation
:errorNoCurl
echo.
echo Error^: Curl not installed on machine. Please install curl on machine and run this batch file again.
goto eof

:errorNoChocolatey
echo.
echo Error^: Chocolatey not installed on machine.
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
cd setup
refreshenv
goto checkingPython

:chromeDownload
echo.
echo Downloading chromedriver for windows.
DownloadChromeDriver.py
goto messageDisplay 

:messageDisplay
echo.
echo All supporting requirements has been installed on machine.
echo Now you are ready to run Tests on your machine.
cd setup
goto eof

:eof
