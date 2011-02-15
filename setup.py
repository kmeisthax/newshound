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
    
def modulescan(fldr, pkgname):
    ret = [pkgname]
    
    for root, dirs, files in os.walk(fldr):
        rel = os.path.relpath(root, fldr)
        components = []
        skip = False
        rest = rel
        
        while True:
            head, tail = os.path.split(rest)
            rest = head
            
            if tail == ".":
                skip = True
                break
            
            components.insert(0, tail)
                
            if head == "":
                break
        
        if skip:
            continue
                
        components.insert(0, pkgname)
        ret.append(".".join(components))
        
    return ret

if __name__ == "__main__":
    setup(name='NewsHound',
        version='0.0',
        description='News aggregator',
        author='David Wendt',
        author_email='dcrkid@yahoo.com',
        url='',
        packages=modulescan("newshound", "newshound"),
        data_files=dirscan("glade-ui", "/usr/share/newshound"),
        scripts=['scripts/newshound']
    )
