# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------------------

from setuptools import find_packages, setup

# --------------------------------------------------------------------------------------------------

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Clément PRÉVOT",
    author_email="clementprevot+pypi@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Home Automation",
        "Natural Language :: English",
        "Natural Language :: French",
        "Development Status :: 4 - Beta",
    ],
    description="A Pypi library to communicate with Aduro (H1) wood/pellet burner via NBE communication",
    install_requires=[],
    keywords="aduro h1 wood pellet burner nbe",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="pyduro",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[],
    python_requires=">=3.6",
    url="https://github.com/clementprevot/pyduro",
    version="2.0.0",
)
