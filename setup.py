#!/usr/bin/env python3

import subprocess
from setuptools import setup, find_packages
import os

TARGET_DEV = os.getenv("TARGET_DEV")

install_requires = []
with open("requirements.txt") as requirements:
    install_requires=requirements.read().splitlines()

if TARGET_DEV is None:
    try:
        last_commit = subprocess.check_output("git rev-parse --verify --short HEAD", shell=True).strip().decode()
        commit_of_last_tag = subprocess.check_output("git rev-list --tags --max-count=1 --abbrev-commit", shell=True).strip().decode()
        tags = subprocess.check_output("git rev-list --tags --max-count=1", shell=True).strip().decode()
        last_tag = subprocess.check_output("git describe --tags --abbrev=0", shell=True).strip().decode()

        _version = last_tag if last_commit == commit_of_last_tag else "0.0.0"
    except:
        print("Error: Version could not be generated")
        raise
else:
    _version = "0.0.0"

setup(
    name="sensehat-christmas",
    version=_version,
    description="RPI Sense Hat Display of a Christmas Tree with Snowflakes",
    install_requires=install_requires,
    entry_points={"console_scripts": ["sensehat-christmas = sensehat_christmas.bin.christmas:main"]},
)