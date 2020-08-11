#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
import sys
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools import setup, Command, Extension

import os
import platform
import subprocess
import urllib
import zipfile
import tarfile
import shutil
import struct


try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


HELICS_VERSION = "2.5.2"
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

if platform.system() == "Darwin":
    DEFAULT_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{helics_version}/Helics-shared-{helics_version}-macOS-x86_64.tar.gz".format(
        helics_version=HELICS_VERSION
    )
elif platform.system() == "Windows":
    if struct.calcsize("P") * 8 == 32:
        DEFAULT_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{helics_version}/Helics-shared-{helics_version}-win32.tar.gz".format(
            helics_version=HELICS_VERSION
        )
    else:
        DEFAULT_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{helics_version}/Helics-shared-{helics_version}-win64.tar.gz".format(
            helics_version=HELICS_VERSION
        )

elif platform.system() == "Linux":
    DEFAULT_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{helics_version}/Helics-shared-{helics_version}-Linux-x86_64.tar.gz".format(
        helics_version=HELICS_VERSION
    )
else:
    raise NotImplementedError("Unsupported platform {}".format(platform.system()))


class HELICSDownloadCommand(Command):
    description = "Download helics libraries dependency"
    user_options = [
        ("pyhelics-install=", None, "path to pyhelics install folder"),
    ]

    def initialize_options(self):
        self.helics_url = DEFAULT_URL
        self.pyhelics_install = os.path.join(CURRENT_DIRECTORY, "./helics/install")

    def finalize_options(self):
        pass

    def run(self):
        r = urlopen(self.helics_url)
        if r.getcode() == 200:
            content = io.BytesIO(r.read())
            content.seek(0)
            with tarfile.open(fileobj=content) as tf:
                dirname = tf.getnames()[0].partition("/")[0]
                tf.extractall()
            shutil.move(dirname, self.pyhelics_install)
            if platform.system() == "Linux":
                shutil.move(os.path.join(self.pyhelics_install, "lib64"), os.path.join(self.pyhelics_install, "lib"))


setup(
    name="helics",
    version="0.1.0",
    license="MIT",
    description="Python HELICS bindings",
    long_description=read("README.md"),
    author="Dheepak Krishnamurthy",
    author_email="me@kdheepak.com",
    url="https://github.com/GMLC-TDC/pyhelics",
    packages=find_packages("helics"),
    package_dir={"": "helics"},
    py_modules=[splitext(basename(path))[0] for path in glob("helics/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={"Issue Tracker": "https://github.com/GMLC-TDC/pyhelics/issues"},
    keywords=["helics", "co-simulation"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=["cffi>=1.0.0"],
    extras_require={
        "tests": ["pytest", "pytest-ordering", "pytest-cov"],
        "docs": ["mkdocs", "inari[mkdocs]", "mkdocs-material", "black", "pygments", "pymdown-extensions"],
    },
    # We only require CFFI when compiling.
    # pyproject.toml does not support requirements only for some build actions,
    # but we can do it in setup.py.
    setup_requires=["pytest-runner", "cffi>=1.0.0"],
    cmdclass={"download": HELICSDownloadCommand},
)
