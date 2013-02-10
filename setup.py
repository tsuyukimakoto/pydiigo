# -*- coding: utf8 -*-

# License: bsd license. 
# See 'license.txt' for more informations.

from distutils.core import setup
import os
import pydiigo
import pydiigotest

setup(
    name='pydiigo',
    version=pydiigo.VERSION,
    author=pydiigo.AUTHOR,
    author_email=pydiigo.AUTHOR_EMAIL,
    url=pydiigo.PROJECT_URL,
    description=pydiigo.DESCRIPTION,
    long_description=pydiigo.LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
    license = 'BSD',
    py_modules=['pydiigo','pydiigotest'],
    data_files=[('', ['lisence.txt'])]
    )

