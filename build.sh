#!/bin/env bash

rm -rf ./build
rm -rf ./dist
rm -rf ./src/pyduro.egg-info

echo -e "Building the package to './dist/'...\n"

python3 setup.py sdist bdist_wheel
