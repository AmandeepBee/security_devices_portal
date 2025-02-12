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
 
Linux machine already come with Python3, however we need python 3.10, if not installed on machine, then install python 3.10 and update
Path environment variable with python3. Also make sure pip is installed and updated too, which is required to install packages,
in not installed run ("sudo pip install python3-pip"). When running "Run_Local_Setup_Linux.sh" shell script on linux,
it will ask sudo password, make sure to enter sudo password to proceed with installation.
 
Darwin machine (Mac Operating system) already come with Python3, however we need python 3.10, if not installed on machine, then install python 3.10 and update Path environment variable with python3. Also make sure pip is installed and updated too, which is required to
install packages. Install "tkinter" on machine by running "brew install tkinter". When running "Run_Local_Setup_Mac.sh" shell script on maOS, it will ask sudo password, make sure
to enter sudo password to proceed with installation.
 
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
 
 
    # Download Chromedriver For Windows Machine
  
    For test cases to run, if need to update chromedriver then to download latest chromedriver, below
    are the steps that need to be followed:
 
    # Go to directory location where project has been cloned from git. Go to folder "src"
      and follow below steps.
    # Run python file "DownloadChromeDriver.py", to download chromedriver for windows.
    # This python will download chromedriver as per the chrome browser version installed on
      machine.
 
 
### Linux Setup
    # Linux shell scripts which needed to download softwares to support automation setup, are under "setup" folder as "Run_Local_Setup_Linux.sh".
 
    For basic automation setup to run tests cases, follow below steps
    to install all required softwares and packages.
  
    As mentioned under "As expected" Python3 and Git already installed on linux machine.      
 
    # Open terminal as administrator at direcotry location, where project has been cloned from git.
      Go to folder "setup" and follow below steps.
    # Run shell script "sh Run_Local_Setup_Linux.sh".
    # This shell job will ask sudo password to be run and to do complete installation.
    # This shell job will install pip, if its not installed on machine.
    # After successful installation of supporting packages, you will see "Requirements has been installed on machine".
    # This shell script will also download chromedriver on machine along with setup.
    # After chromedriver download, scripts will display message as below:
        "All supporting requirements has been installed on machine."
        "Now you are ready to run Tests on your machine."
 
 
    # Download Chromedriver For Linux Machine
 
    For test cases to run, if need to update chromedriver then to download latest chromedriver, below are the steps that need to be followed:
 
    # Go to directory location where project has been cloned from git. Go to folder "src"
      and follow below steps.
    # Run python file "python3 DownloadChromeDriver.py", to download chromedriver for Linux.
    # This shell script will download chromedriver as per the chrome browser version installed on
      machine.
 
### MacOS Setup (M1 and Intel Processor)
    # All mac shell scripts which needed to download softwares to support automation setup For Mac Machine, are under "setup" folder.
 
    For basic automation setup to run tests cases, follow below steps to install all required softwares and packages.
  
    As mentioned under "As expected" Python3 and Git already installed on mac machine.      
 
    # Open terminal as administrator at direcotry location, where project has been cloned from git.
      Go to folder "src\setup" and follow below steps.
    # Run shell script "sh Run_Local_Setup_Mac.sh".
    # This shell job will ask sudo password to be run and to do complete installation.
    # This shell job will install pip, if its not installed on machine.
    # After successful installation of supporting packages, you will see "Requirements has been installed on machine".
    # This shell script will also download chromedriver on machine along with setup.
    # After chromedriver download, scripts will display message as below:
        "All supporting requirements has been installed on machine."
        "Now you are ready to run Tests on your machine."
 
 
    # Download Chromedriver For Mac Machine
 
    For test cases to run, if need to update chromedriver then to download latest chromedriver, below are the steps that need to be followed:
  
    # Go to directory location where project has been cloned from git. Go to folder "src" and follow below steps.
    # Run python file "python3 DownloadChromeDriver.py", to download chromedriver for Mac.
    # This shell script will download chromedriver as per the chrome browser version installed on
      machine.
 
### Python Setup
 
    Download the python exe file from link: https://www.python.org/downloads/
 
    Download python version from 3.8.9 and install it in local for Mac\Linux Machines.
    For Windows "Run_Local_Setup_Windows.bat" will take care of this.
 
 
### Code Base
 
    Clone Test Automation code base to local from link: https://github.com/BediAmandeep/security_devices_portal.git
 
### Installation of Dependencies
 
    As there are lots of dependencies, go to Command prompt or Terminal, in project root folder and
    run "pip install -r requirements.txt" to install all dependencies mentioned in the requirements.txt file
 
## Understanding Code Base Structure
 
    - output – Test results html/xml files, screenshots are maintained here
 
    - src > driver – Drivers are downloaded here automatically by script "DownloadChromeDriver.py"
 
    - src > main > locators – page object locators are maintained here (locators are maintained
      as tuples eg. TXT_USERNAME = (By.ID, "username") )
 
    - src > main > pages – actions related to the pages are maintained here
 
    - src > main > config – target environment related configurations are maintained here
 
    - src > main > webactions.py – Selenium wrapper methods are maintained here
 
    - src > testcases – All test classes/files are maintained here
 
    - requirements.txt – project dependencies are maintained here
 
### Note  
 
    We can run our Test Automation against any supported browser; we need to modify drivers
    initialization accordingly.
 
    To download current chromedrivre, to src and run DownloadChromeDriver.py. It will automatically install and place webdriver in the src folder.
 
 
### Configure Target environment & credentials
 
    Test automation scripts by default executes against stage environment
    - https://app.staging.drchrono.com/accounts/login/
 
    When required to execute against another environment following needs to be
    update in the config file available in {project_root}/src/env
 
    1. First row value in env
    stage(default) - should be used to run tests against staging environment.
    prod - should be used to run tests against prod environment.
 
    2. Second row value in env
    localmachine(default) - should be used to run tests on local machine.
    remote - should be used to run tests on remote (lambdatest) environment.
    mobile - should be used to run mobile tests.
 
    3. Third row value in env
    simulator(default) - should be used to run tests for mobile automation on ipad 10th generation simulator.
    ipad - should be used to run tests for mobile automation on real device connected to mac machine.
 
    Default credentials mentioned in src > main > config file will be used as per env settings in src > main > env file.
 
### Code formatting
    Test scripts should be formatted, before merging\pushing any change to branch. To achieve this need to run command 'black src'. It will auto format the code.
 
 
### Execute Tests in Local
 
    Test Automation scripts can be executed in local in multiple ways :
 
#### From command prompt
 
    To run all tests in a particular python file - pytest src/testcases/<file_name.py>
 
    To run specific test pytest marks can be used. Each test is marked with test case id
    to enable single test execution from command prompt – pytest -m <ts_0222>
 
    To run all tests with xml report & flaky –
    pytest --force-flaky --max-runs=2 --junit-xml=./output/test_results/smoke/results.xml
 
#### From PyCharm
 
    - In PyChram go to Run > Edit Configurations > Add > Python Tests > PyTest
 
    - To run all tests in a particular python file; In configuration select ‘Script path’
      in ‘Target’ and select the particular python file to execute
 
    - To run specific test; in configuration select ‘Custom’ in ‘Target’ and in
      ‘Additional Arguments’ type ‘-m <ts_0222>’