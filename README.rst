Implements
=============

.. image:: https://img.shields.io/travis/ksindi/ksindi/implements/master.svg
    :target: https://travis-ci.org/ksindi/ksindi/implements
    :alt: Linux and MacOS Build Status
.. image:: https://readthedocs.org/projects/implements/badge/?version=latest
    :target: http://implements.readthedocs.io
    :alt: Documentation Build Status
.. image:: https://img.shields.io/pypi/v/implements.svg
    :target: https://pypi.python.org/pypi/implements
    :alt: PyPI Version

Lighweight Pythonic interfaces

Install
-------

Implements is available on PyPI can be installed with `pip <https://pip.pypa.io>`_.::

    pip install implements

To install the latest development version from `GitHub <https://github.com/ksindi/implements>`_::

    pip install git+git://github.com/ksindi/implements.git

Usage
-----

After installing Implements you can use it like any other Python module.
Here's a very simple example:

.. code-block:: python

    from implements import Interface, implements

    class Quackable(Interface):
        def quack(self):
            pass

    @implements(Quackable)
    class MallardDuck:
        def quack(self):
            pass


    duck = MallardDuck()

API Reference
-------------

The `API Reference on readthedocs.io <http://implements.readthedocs.io>`_ provides API-level documentation.

Support / Report Issues
-----------------------

All support requests and issue reports should be
`filed on GitHub as an issue <https://github.com/ksindi/ksindi/implements/issues>`_.

Releasing
---------

::

    git checkout master
    git tag -a vX.Y.Z
    git push origin --tags

Test
----

Running unit tests::

    make test

Running linter::

    make lint

Running tox::

    make test-all

License
-------

MIT
