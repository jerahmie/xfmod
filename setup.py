"""
Uses distutils to install python module.
"""

#from distutils.core import setup
from setuptools import setup

setup(name='xfmod',
      version='1.0.1',
      py_modules=['xfmod']
      #, 'xfmatgrid', 'xfsystem', 'xfutils', 'xfwriter']
)
