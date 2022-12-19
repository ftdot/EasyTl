# EasyTl documentation

## Installation on Windows

#### ![Python icon](../icons/python-icon.png) 1. Python installation
EasyTl requires the installed python 3.10+ versions (for 1.4.0+).
**NOTE THAT PYTHON 3.9+ VERSIONS CANNOT RUN ON THE WINDOWS 7 OR EARLIER. IT MEANS THAT EASYTL ISN'T ACTUALLY SUPPORT THE WINDOWS 7 AND EARLIER**

You can install it from [official site](https://www.python.org)

**Common python installation guide:**
1. Move your mouse to the `Downloads` tab on the top
2. Click to the Python 3.\*.\* and you will get the python installer
3. Run it
4. **IMPORTANT!** Down bellow you can see `Add python.exe to the PATH` you **MUST** check it!
5. Click **Install now**
6. Congratulations! You installed the python

#### ![Install icon](../icons/install-icon.png) 2. (User method) Installing the EasyTl (via Tags)
Go to the [Tags](https://github.com/ftdot/EasyTl/tags) and select the latest stable version (as example - v1.4.0).

1. You will see the `Assets` list, open it if it has hidden. Select `Source code (.zip)` and download it
2. Open downloaded archive and unpack it to any place. As example - to the Desktop
3. Enter the `EasyTl-master` directory, after also enter to the `src` directory
4. Execute the `install.bat` file
5. As optional, you can install the FFMPEG. It required for the `1STTLib` plugin (allows to convert speech to text). To do this, execute the `install_ffmpeg.bat` file
6. Congratulations! You installed the EasyTl

After you can execute it by the `run.bat` file in the `src` directory. But, before to do this you must configure the EasyTl [here](configuration.md)

#### ![Install icon](../icons/install-icon.png) 2. (Ultimate user method) Installing the EasyTl (via Git CLI)
Execute these commands:
```bash
git clone https://github.com/ftdot/EasyTl
cd EasyTl-master\src
start install.bat
```

As optional, you can install the FFMPEG. It required for the `1STTLib` plugin (allows to convert speech to text). To do this, execute it command after commands above:
```bash
start install_ffmpeg.bat
```

After you can execute it by the `run.bat` file in the `src` directory. But, before to do this you must configure the EasyTl [here](configuration.md)

## Installation on Linux

#### ![Python icon](../icons/python-icon.png) 1. Python installation
EasyTl requires the installed python 3.10+ versions (for 1.4.0+).

You can install it by these commands:
```bash
sudo apt-get update
sudo apt-get install python3.10 python3-pip
```

#### ![Install icon](../icons/install-icon.png) 2. Installing the EasyTl (via Git CLI)
Execute these commands:
```bash
sudo apt-get update
sudo apt-get install git
git clone https://github.com/ftdot/EasyTl
cd EasyTl-master/src
./install.sh
```

As optional, you can install the FFMPEG. It required for the `1STTLib` plugin (allows to convert speech to text). To do this, execute it command after commands above:
```bash
./install_ffmpeg.sh
```

After you can execute it by the `run.sh` file in the `src` directory. But, before to do this you must configure the EasyTl [here](configuration.md)
