# christmaspi

RPI Sense Hat Display of a Christmas Tree with Snowflakes.

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
```

Use the *run.sh* script to build the package.

```bash
./run.sh --build-deb
```

This will output two *.deb* files:

* *python3-christmaspi.deb* - christmaspi Package
* *python-christmaspi-doc.deb* - Documentation Package

**Alternative:** [Docker](https://docs.docker.com/engine/install/debian/)

This step allows you to skip installing the debian packages and use the Docker Compose plugin 
instead:

```bash
./run.sh --docker --build-deb
```

### Debian Installation

Installing the packages is then done by using `apt install <PACKAGE>`:

```bash
# Install the package
sudo apt install ./python3-christmaspi.deb

# OPTIONAL: Install docs
sudo apt install ./python-christmaspi-doc.deb
```

### Pip installation

The pip installation is rather easy.

To install the package directly onto your system, use the `pip3 install .` command.
A virtualenv wrapper is provided by the *run.sh* script and installs the package into a python
virtual environment:

```bash
./run.sh --install-pip
```
