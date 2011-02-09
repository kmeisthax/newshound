#!/usr/bin/python

from distutils.core import setup
import os, os.path

def dirscan(fldr, base):
    ret = {}

    for root, dirs, files in os.walk(fldr):
        target = os.path.join(base, os.path.relpath(root, fldr))
        ret[target] = []
        for filename in files:
            ret[target].append(os.path.relpath(os.path.join(root, filename)))

    return ret.items()

setup(name='NewsHound',
    version='0.0',
    description='News aggregator',
    author='David Wendt',
    author_email='dcrkid@yahoo.com',
    url='',
    packages=['newshound'],
    data_files=dirscan("glade-ui", "/usr/share/newshound"),
    scripts=['scripts/newshound']
)
