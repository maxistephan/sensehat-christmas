#!/bin/bash

set -e

BASEDIR=$(dirname $(readlink -e -- $0))

function show_help() {
    echo "Wrapper Script for rpi-season-screen"
    echo ""
    echo "Usage: $0 ([--docker] --build-deb|--install-pip|-h|--help)"
    echo ""
    echo "Arguments:"
    echo "----------"
    echo ""
    echo "   --build-deb        Build the Debian Packages"
    echo "   --install-pip      Install the python3-pip package inside a virtual environment only"
    echo "   --docker           Flag to build in a docker container"
    echo "-h|--help             Show this help text"
    echo ""
    echo "Examples:"
    echo "---------"
    echo ""
    echo "# Build the debian package using the docker container"
    echo " > $0 --docker --build deb"
    echo ""
    echo "# Install the python3-pip Package inside a virtual environment ($pwd/.venv)"
    echo " > $0 --install-pip"
}

function build_deb() {
    echo "Building Debian Package"
    # Remove old output
    sudo rm -rf build/ .pybuild/

    # build Package
    install_cmd="apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends -y --allow-downgrades"
    sudo mk-build-deps -t "${install_cmd}" -i -r debian/control
    sudo dpkg-buildpackage -rfakeroot --source-option=-Itest --source-option=-I.git --source-option=-Ivenv

    # Move packages to pwd
    cp ../*.deb . || true
}

function stop_venv() {
    echo "Creating venv"

    deactivate >/dev/null 2>&1
}

function setup_venv() {
    echo "Creating venv"

    cd "${BASEDIR}"
    python3 -m venv .venv
    . .venv/bin/activate
    pip3 install -r requirements.txt
    trap stop_venv EXIT
}

function install_pip() {
    echo "Installing Raspberry Pi Season Screen as Pip Package"

    cd "${BASEDIR}"
    pip3 install . --ignore-installed
}

DOCKER_CMD=""

while [ $# -gt 0 ] ;do
    case "$1" in
        --build-deb)
            BUILD_DEB="1"
            shift
            ;;
        --install-pip)
            INSTALL_PIP="1"
            shift
            ;;
        --docker)
            DOCKER_CMD="1"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            if [ -z "$1" ]; then
                echo "No Argument given."
            else
                echo "Unknown Argument \"$1\"."
            fi
            echo "Use \"$0 --help\" to get helping text."
            exit 1
            ;;
    esac
done

if [ -n "${BUILD_DEB}" ]; then
    if [ -z "${DOCKER_CMD}" ]; then
        build_deb
    else
        cd docker
        GROUP_NAME=$(id -n -g) USER_ID=$(id -u) GROUP_ID=$(id -g) \
            docker compose run --rm rpi-season-screen-env ./run.sh --build-deb
    fi
fi

if [ -n "$INSTALL_PIP" ]; then
    if [ -z "${DOCKER_CMD}" ]; then
        setup_venv
        install_pip
    else
        echo "Installing the pip package inside a docker container is not recommended!"
        exit 1
    fi
fi
