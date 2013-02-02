#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = "geats",
    version = "0.9",
    packages = find_packages(),
    package_data = { '': [ "*.rst", "LICENSE" ] },
    scripts = ["bin/vmctl"],
    license = "LGPL 2.1",
    keywords = "LXC virtualization",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ]
)
