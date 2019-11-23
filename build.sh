#!/bin/bash

echo -e "Building the package to './dist/'...\n"

python3 setup.py sdist bdist_wheel
