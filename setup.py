# setup.py

from setuptools import find_packages, setup

setup(
    name="client_library",
    version="0.1.0",
    description="A client library to interact with the video translation server.",
    author="Yimo Xie",
    author_email="xieyimo996@berkeley.edu.com",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)