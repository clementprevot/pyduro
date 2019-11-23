#!/bin/bash

REPOSITORY="testpypi"

while getopts hpr:t option; do
    case "${option}" in
        h)
            echo """
./publish.sh [-h] [-r <repository name>]|[-p]|[-t]
    -h                   - Display this help message
    -r <repository name> - Publish the package to the given repository (whose name should be available in .pypirc)
    -p                   - Publish the package to the public PyPi repository (you should have a 'pypi' repository in you .pypirc)
    -t                   - Default - Publish the package to the test PyPi repository (you should have a 'testpypi' repository in you .pypirc)
            """
            exit
            ;;
        r)
            REPOSITORY=${OPTARG}
            ;;
        p)
            REPOSITORY="pypi"
            ;;
        t)
            REPOSITORY="testpypi"
            ;;
    esac
done

echo -e "Publishing the package to '${REPOSITORY}'...\n"

python3 -m twine upload --repository $REPOSITORY dist/*
