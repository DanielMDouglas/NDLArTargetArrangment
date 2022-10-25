#!/usr/bin/env python

import setuptools

VER = "0.0.1"

setuptools.setup(
    name="NDLArTargets",
    version=VER,
    author="Daniel D. and others",
    author_email="dougl215@slac.stanford.edu",
    description="A package for generating geometry CAD files for production of DUNE ND photocathodes",
    url="https://github.com/DanielMDouglas/NDLArTargetArrangement",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "pyyaml", "argparse", "ngsolve"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.2',
)
