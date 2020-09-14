# -*- coding: utf-8 -*-

"""The setup module."""

import setuptools
from setuptools import find_packages

if __name__ == "__main__":
    # BUG: for some reason, I have to use find_packages() in setuptoold.setup
    #  for it to work instead of inside of setup.cfg
    setuptools.setup()

    # BUG: for some reason, I need to use install_requires insdie of
    #  setuptools.setup for it to work
    # setuptools.setup(
    #     packages=find_packages(),
    #     install_requires=[
    #         "flask",
    #         "flask_restapi",
    #         "nltk",
    #         "textblob",
    #         "Click",
    #         "more_itertools",
    #         "requests",
    #         "requests_file",
    #         "tqdm",
    #     ],
    # )
