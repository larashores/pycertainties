import os

from setuptools import setup

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join("README.md")) as file:
    README = file.read()

setup(
    name="uncertainties",
    packages=["uncertainties"],
    package_dir={"": "src"},
    python_requires=">=3.8",
    version="1.0",
    author="Lara Shores",
    author_email="lara.shores@outlook.com",
    url="https://github.com/larashores",
    description="Module providing utilities for working with values with uncertainties",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
