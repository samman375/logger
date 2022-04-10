# logger

This was created for the 'Something Awesome' project in COMP6841: Security Engineering in T122.

A keylogger for MacOS. Records a log of every key typed by a user in a file. I wanted this to be undetectable by the user, otherwise what was the point of having malware installed. This project consists of 2 main parts: the python logger and the deployment software. The installation file pretends to be a 'RAM Booster' that will significantly increase the user's RAM.

Note: the deployment .pkg file does not use the python logger, but a different adapted open-source keylogger written in C. Details provided in design details section. The deployment software is also adapted from an open-source project.

## Usage

Install and run at your own risk. I am not responsible for anything that occurs to your computer. The keylogger also does not log passwords, due to MacOS Security. The installation file contains many obvious hints that the software is not real to prevent people from genuinely thinking their RAM will be boosted.

### Part 1: Python Logger

The original python logger can be run via:

```
$ nohup python3 logger.py &
```

This outputs the keylogger to a **.output.txt** file in the same directory. 

Note: this requires _Input Monitoring_ and _Accessibility_ to be allowed to _Terminal_ under _Security and Privacy_ of _System Preferences_.

#### Termination

If the same terminal has not yet been closed, it can be terminated by running 

```
$ kill PID
```

with the correct process id obtained from:

```
$ ps
```

Otherwise the computer will need to be restarted.

### Part 2 Deployment

Before building, the desktop location needs to be changed in **./keylogger/keylogger.h** on line 13 as it is currently hard-coded to my local setup. To build a new **\*.pkg** file,

```
$ cd keylogger
$ make && make install
$ bash macos-installer-builder/macOS-x64/build-macos-x64.sh ramBooster VERSION_NUMBER
```

with `VERSION_NUMBER` replaced with appropriate version number. When prompted for a developer certificate answer no. The new **\*.pkg** file will be located in **./macos-installer-builder/macOS-x64/target/**. The installer will prompt the user to run:

```
$ nohup ramBooster-VERSION_NUMBER &
```

The installer will install the keylogger in **/Library/ramBooster/VERSION_NUMBER/**, and add a link to **/usr/local/bin**. The output file can be located on the desktop under **.keystroke.log**.

#### Termination

Terminate as with python logger above. Program can be uninstalled in **/Library/ramBooster/VERSION_NUMBER/** via

```
$ sudo bash uninstall.sh
```

## Design Details

### Python Code

For the python keylogger library, `pynput` was chosen over alternatives such as `keyboard` as it seemed the simplest to use with the most extensive documentation. The code will log on-press but not on-release as this provided little value, and difficult to read logs. The file opens and closes the `.output.txt` file after every key stroke as the program is generally terminated forcefully, and outputs are not written to file. 'Space' and 'Enter' keys are not treated as special keys and displayed as normal. Output is prefixed by `.` to hide it from `ls`. The program is made to run in the background even when the terminal is closed with the use of the `nohup` command. The `&` at the end of the command returns terminal control to the user. This hides the process (once terminal is closed) with the only way I could find to stop it being restarting the computer.

### Attempt to bypass MacOS Security

The python program was discovered to require permissions granted by the user, outlined in usage above. Alternatives to bypass this were considered. One of which was via a keylogger written in _Swift_. This was eventually found to have since been patched by Apple. A suggestion was found that lower level languages were required to bypass MacOS security at the keyboard level. This led me to the [open-source C project](https://github.com/caseyscarborough/keylogger) which utilises an Apple API that accesses the keyboard. This was also found to have since been patched by Apple. Another option was to run the program via `sudo`. This was infeasible as it would require the user enter a password, and most likely figure out what was going on. 

### Deployment Tool

I then had the idea that instead of trying to bypass MacOS security, I simply trick the user into thinking the program was something else and willingly install it. This led to the deployment tool outlined above. This utilises another [open-source project](https://github.com/KosalaHerath/macos-installer-builder) that I have forked and edited for my own use. This sub-repository is found under **./macos-installer-builder/**.

This project requires the application deployed to be a binary file. This could not be done as it is generally done via a python package called [_pyinstaller_](https://pyinstaller.readthedocs.io/en/stable/). This was eventually found to be incompatible with the complicated set up I had with the use of _pyenv_, as python packages were shared between versions. Multiple binary types were tried such as multiple file binary (found under **./bin/**) as well as a single file binary (found under **./build/** and **./dist/**). This could not be solved despite using methods such as creating an isolated virtual environment with [_virtualenv_](https://virtualenv.pypa.io/en/latest/user_guide.html). 

I then decided to use the open-source C project found earlier for deployment and forked it for my own use. This sub-repository is found under **./keylogger**. The makefile output location has been changed to **./macos-installer-builder/macOS-x64/application/** to allow for deployment. Any terminal messages are also removed to stop the user from catching on. 

The deployment pretends to be a fake 'RAM booster'. Something that should be completely stupid and no one should fall for. I could have also added the application to the **.zshrc** file to make it run whenever the computer was started again, to prevent the program from being stopped when the computer was restarted, but decided against this for obvious reasons. The desktop location was hard-coded to my local destination due to a lack of time. The installation **.pkg** file is littered with jokes and very obvious messages that this is a fake software, to prevent people from actually falling for it.
