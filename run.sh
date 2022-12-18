#!/bin/bash

set -e

BASEDIR=$(pwd)

function show_help() {
    echo "Wrapper Script for Sensehat Christmas"
    echo ""
    echo "Usage: $0 (--build-dep|--install|-h|--help)"
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
    echo "Installing sensehat-christmas as Pip Package"

    cd "${BASEDIR}"
    pip3 install . --ignore-installed
}

while :
do
    case "$1" in
    --build-deb)
        build_deb
        exit 0
        ;;
    --install)
        setup_venv
        install_pip
        exit 0
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
    shift
done
