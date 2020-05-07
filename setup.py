"""Distutils setup file, used to install or test 'implements'."""
from __future__ import print_function

import textwrap
from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

_INSTALL_REQUIRES = [
            'setuptools_scm>=1.15.0',
]
_SETUP_REQUIRES = [
            'setuptools>=18.0',
            'pytest-runner',
            'setuptools_scm>=1.15.0',
            'sphinx_rtd_theme',
]
_TEST_REQUIRES = [
            'pytest',
            'pytest-flake8',
]
_ALL_PACKAGES=[]
_ALL_PACKAGES.extend(_SETUP_REQUIRES)
_ALL_PACKAGES.extend(_TEST_REQUIRES)

if __name__ == '__main__':
    setup(
        name='implements',
        description='pythonic interfaces',
        long_description=readme,
        url='http://implements.readthedocs.io',
        use_scm_version=True,
        author='Kamil Sindi',
        author_email='ksindi@ksindi.com',
        maintainer='Kamil Sindi',
        maintainer_email='ksindi@ksindi.com',
        install_requires=_INSTALL_REQUIRES,
        setup_requires=_SETUP_REQUIRES,
        tests_require=_TEST_REQUIRES,
        all_packages=_ALL_PACKAGES,
        zip_safe=False,
        include_package_data=True,
        py_modules=['implements'],
        classifiers=textwrap.dedent("""
            Development Status :: 5 - Production/Stable
            Intended Audience :: Developers
            License :: OSI Approved :: Apache Software License
            Natural Language :: English
            Programming Language :: Python :: 3
            Programming Language :: Python :: 3.6
            Programming Language :: Python :: 3.7
            Programming Language :: Python :: 3.8
            """).strip().splitlines(),
        keywords=['implements', 'interfaces'],
        license='Apache License, Version 2.0',
    )
