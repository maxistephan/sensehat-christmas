# Raspberry Pi Season Screen

RPI Sense Hat Display with different scenes in different times of the year.

An example of said scenes is the christmas tree during the winter holidays:

![Demo GIF](./doc/img/demo.gif)

## Getting started

There are two ways to install this project:

* As a debian package
* As only a pip package

### Debian Build

**note:** Building the package from source requires you to have the following debian packages
installed:

```bash
sudo apt-get install --no-install-recommends \
    python3 python3-venv python3-all-dev python3-setuptools python3-pip \
    gcc make \
    dpkg-dev devscripts equivs \
    libcap2-bin apt-utils \
    git-core
```

Use the *run.sh* script to build the package.

```bash
./run.sh --build-deb
```

This will output two *.deb* files:

* *python3-rpi-season-screen<VERSION>_all.deb* - rpi-season-screen Package
* *python-rpi-season-screen-doc_<VERSION>_all.deb* - Documentation Package

**Alternative:** [Docker](https://docs.docker.com/engine/install/debian/)

This step allows you to skip installing the debian packages and use the Docker Compose plugin 
instead:

```bash
./run.sh --docker --build-deb
```

**note:** This script uses the newer
[*docker-compose-plugin*](https://docs.docker.com/compose/install/linux/).
If you are still using docker-compose consider updating!

### Debian Installation

Installing the packages is then done by using `apt install <PACKAGE>`:

```bash
# Install the package
sudo apt install ./python3-rpi-season-screen<VERSION>_all.deb

# OPTIONAL: Install docs
sudo apt install ./python-rpi-season-screen-doc_<VERSION>_all.deb
```

Packages can be obtained at the
[Releases Page](https://github.com/maxistephan/rpi-season-screen/releases) or build
them from source as described above.

### Pip installation

The pip installation is rather easy.

To install the package directly onto your system, use the `pip3 install .` command.
A virtualenv wrapper is provided by the *run.sh* script and installs the package into a python
virtual environment:

```bash
./run.sh --install-pip
```

## Run

Run the systemd service (only after .deb installation available):

```bash
sudo systemctl start rpi-season-screen
```

Run the programm itself:

```bash
rpi-season-screen
```
