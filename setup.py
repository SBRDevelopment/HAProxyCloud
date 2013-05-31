#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys, os
from haproxycloud import __version__
from haproxycloud.distutils import get_data_files

if sys.version_info <= (2,6) or sys.version_info >= (2,8):
    error = 'ERROR: HAProxy-Cloud requires Python Version 2.6 or 2.7 ...exiting.'
    print >> sys.stderr, error
    sys.exit(1)

src_path = os.path.dirname(__file__)

data_files = []
data_files.append(('/etc/haproxy-cloud/', ['haproxy-cloud.yaml']))
data_files.extend(get_data_files(src_path, '/etc/haproxy-cloud/', 'templates'))
data_files.extend(get_data_files(src_path, '/etc/haproxy-cloud/', 'conf.d'))

setup(  
        name='haproxy-cloud',
        version=__version__,
        description='HAProxy Python Management Tools',
        author='Brian Wight',
        author_email='bwight@sbrforum.com',
        url='https://github.com/SBRDevelopment/HAProxyCloud',
        platforms = 'POSIX',
        scripts=[
            'bin/update-haproxy-config'
        ],
        packages=[
            'haproxycloud'
        ],
        data_files=data_files,
        classifiers = [
            'Topic :: Internet',
            'Development Status :: 4 - Beta',
            'Programming Language :: Python',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Programming Language :: Python :: 2.6'
        ]
)
