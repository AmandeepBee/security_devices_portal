<summary>
<h1>Automation Setup</h1>
</summary>
 
## Automation Framework Setup
This document provide steps to configure Python(3.10.0)-Selenium(4.21.0) automation setup on machine, to run
test cases, and to develop new test cases. There are three types of setups, one to support Windows operating
system machines, second to support Linux operating system machines and third to support Mac operating
system machines. Kindly follow below steps as per your machines operating system.
 
## As expected (Please read carefully)
It's expected that GIT is already installed on your machine, to clone git repository on machine. If git is
not installed on machine, install Git first. Windows batch file will take care of installing Python and other
needed software packages.
 
### Windows Setup
    # Windows script which needed to download softwares to support automation
      setup, are under "setup" folder as "Run_Local_Setup_Windows.bat".
 
    For basic automation setup to run tests cases, follow below steps to install all required softwares and packages.
 
    # Open command prompt as administrator at directory location, where project has been cloned from git.
      Go to folder "setup" and follow below steps.
    # Run batch job "Run_Local_Setup_Windows.bat".
    # This batch job has to be run "Thrice"(3 times), to do complete installation.
    # This script will also download chromedriver on machine along with setup.
    # After chromedriver download, scripts will display message as below:
        "All supporting requirements has been installed on machine."
        "Now you are ready to run Tests on your machine."          
 
### Python Setup
 
    Download the python exe file from link: https://www.python.org/downloads/
 
    Download python version from 3.10.0 and install it in local for Mac\Linux Machines.
    For Windows "Run_Local_Setup_Windows.bat" will take care of this.
 
 
### Code Base
 
    Clone Test Automation code base to local from link: https://github.com/BediAmandeep/security_devices_portal.git
 
### Installation of Dependencies
 
    As there are lots of dependencies, go to Command prompt or Terminal, in project root folder as administrator and
    run "pip install -r requirements.txt" to install all dependencies mentioned in the requirements.txt file
 
## Understanding Code Base Structure
 
    - src > main > pages – actions related to the pages are maintained here
 
    - src > main > config – target environment related configurations are maintained here
 
    - src > main > webactions.py – Selenium wrapper methods are maintained here
 
    - src > testcases – All test classes/files are maintained here
 
    - requirements.txt – project dependencies are maintained here
 
### Note  
 
    We can run our Test Automation against any supported browser; we need to modify drivers
    initialization accordingly.
 
### Code formatting
    Test scripts should be formatted, before merging\pushing any change to branch. To achieve this need to run command 'python -m black src'. It will auto format the code.
 
 
#### From command prompt
 
    To run all tests in a particular python file - pytest src/testcases/<file_name.py>
 
    To run specific test pytest marks can be used. Each test is marked with test case id
    to enable single test execution from command prompt – pytest -m <ts_0222>
    