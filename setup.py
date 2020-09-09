# -*- coding: utf-8 -*-

"""The setup module."""

import setuptools
from setuptools import find_packages

if __name__ == "__main__":
    setuptools.setup(
        packages=find_packages(),
        install_requires=[
            "flask",
            "flask_restapi",
            "nltk",
            "textblob",
            "click",
            "more_itertools",
            "requests",
            "requests_file",
            "tqdm",
        ],
    )
