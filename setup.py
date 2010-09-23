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
    license = 'BSD',
    py_modules=['pydiigo','pydiigotest'],
    data_files=[('', ['lisence.txt'])]
    )

