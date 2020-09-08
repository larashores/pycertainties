from setuptools import setup
import os

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join("README.md")) as file:
    README = file.read()

setup(
    name="uncertainties",
    packages=["uncertainties"],
    package_dir={"": "src"},
    python_requires=">=3.4",
    version="1.0",
    author="Lara Shores",
    author_email="lara.shores@outlook.com",
    url="https://github.com/larashores",
    description="TODO: this",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ],
    install_requires=[
        "matplotobjlib"
    ]
)
