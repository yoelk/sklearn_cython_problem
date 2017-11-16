#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io

import os

import re
import sys
from glob import glob

from os import remove
from os.path import basename
from os.path import dirname
from os.path import join

from os.path import relpath

from os.path import splitext

from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

from setuptools import Extension

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


class MyBuildExt(build_ext):
    '''
    Our own build extension class
    '''

    def run(self):
        build_ext.run(self)

        global names

        # Delete the source files from the build folder
        build_path = join(dirname(__file__), self.build_lib)

        build_sources = \
            tuple(join(build_path, *list(p.split('.') + ['*.py']))
                  for p in packages)
        for source_pattern in build_sources:
            source_files = tuple(s for s in glob(source_pattern)
                                 if not s.endswith('__main__.py')
                                 and not s.endswith('__init__.py'))
            for f in source_files:
                remove(f)

# Prepare setup kwargs
setup_kwargs = dict(
    name='feature_union',
    version='0.1.0',
    license='Proprietary License',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: Other/Proprietary License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    setup_requires=['cython'],
    entry_points={
        'console_scripts': [
            'feature_union = feature_union.cli:main',
        ]
    },
)

# Create the extensions' list
packages = find_packages('src')
names = list(p + '.*' for p in packages)
sources = list([join('src', *list(p.split('.') + ['*.py']))]
               for p in packages)
extensions = list(Extension(names[i], sources[i])
                  for i, _ in enumerate(packages))

setup_kwargs['ext_modules'] = cythonize(extensions,
                                        build_dir="build",
                                        compiler_directives=dict(
                                            always_allow_keywords=True
                                        ))
setup_kwargs['cmdclass'] = dict(build_ext=MyBuildExt)

# Run the setup
setup(**setup_kwargs)
