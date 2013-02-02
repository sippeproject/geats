#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = "geats",
    version = "0.9",
    packages = find_packages(),
    package_data = { '': [ "*.rst", "LICENSE" ] },
    scripts = ["bin/vmctl"],
)
