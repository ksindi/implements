Implements
==========

.. image:: https://img.shields.io/travis/ksindi/ksindi/implements/master.svg
    :target: https://travis-ci.org/ksindi/ksindi/implements
    :alt: Linux and MacOS Build Status
.. image:: https://readthedocs.org/projects/implements/badge/?version=latest
    :target: http://implements.readthedocs.io
    :alt: Documentation Build Status
.. image:: https://img.shields.io/pypi/v/implements.svg
    :target: https://pypi.python.org/pypi/implements
    :alt: PyPI Version

*Pythonic interface using decorators*

Install
-------

Implements is available on PyPI can be installed with `pip <https://pip.pypa.io>`_.::

    pip install implements

To install the latest development version from `GitHub <https://github.com/ksindi/implements>`_::

    pip install git+git://github.com/ksindi/implements.git

Advantages
----------

1. `Favor composition over inheritance<https://en.wikipedia.org/wiki/Composition_over_inheritance>`_.
2. Inheriting from multiple classes can be problematic, especially when the
superclasses have the same method name but different signatures. Implements will
throw a descriptive error if that happens to ensure integrity of contracts.
3. The decorators are evaluated at import time. Any errors will be raised then
and not when an object is instantiated or a method is called.
4. It's cleaner. Using decorators makes it clear we want share behavior. Also,
arguments are not allowed to be renamed.
5. Codebase is tiny: you can just copy the file over. This repo exists
more for test coverage.

Usage
-----

After installing Implements you can use it like any other Python module.
Here's a simple example:

.. code-block:: python

    from implements import Interface, implements

    class Quackable(Interface):
        def quack(self):
            pass

    @implements(Quackable)
    class MallardDuck:
        def quack(self):
            print("quack!")


    duck = MallardDuck()

Below will raise a ``NotImplementedError`` exception:

.. code-block:: python

    @implements(Quackable)
    class RubberDuck:
        pass

    NotImplementedError: 'RubberDuck' must implement method 'quack((self))' defined in interface 'Quackable'

You can find a more detailed example in ``example.py`` and by looking at ``tests.py``.

Credit
------

The implementation of this was inspired by a `PR <https://github.com/pmatiello/python-interface/pull/1/files>`_ @elifiner made.

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
