# -*- coding: utf-8 -*-
# WakeOnLAN-API
# Project by https://github.com/rix1337

import setuptools

try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except:
    import io

    long_description = io.open('README.md', encoding='utf-8').read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="wol_api",
    version="0.1.4",
    author="rix1337",
    author_email="",
    description="A simple wake on LAN interface that accepts post commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rix1337/docker-wakeonlan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'wol_api = wol_api.web:main',
        ],
    },
)
