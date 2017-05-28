"""Distutils setup file, used to install or test 'implements'."""
from __future__ import print_function

import textwrap
from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

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
        install_requires=[
            'setuptools_scm>=1.15.0',
        ],
        setup_requires=[
            'setuptools>=18.0',
            'pytest-runner',
            'setuptools_scm>=1.15.0',
            'sphinx_rtd_theme',
        ],
        tests_require=[
            'pytest',
            'pytest-flake8',
        ],
        zip_safe=False,
        include_package_data=True,
        classifiers=textwrap.dedent("""
            Development Status :: 5 - Production/Stable
            Intended Audience :: Developers
            License :: OSI Approved :: MIT License
            Natural Language :: English
            Programming Language :: Python :: 3
            Programming Language :: Python :: 3.5
            Programming Language :: Python :: 3.6
            """).strip().splitlines(),
        keywords=['implements', 'interfaces'],
        license='MIT',
    )
