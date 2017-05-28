Implements
==========

.. image:: https://travis-ci.org/ksindi/implements.svg?branch=master
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

Advantages
----------

1. `Favor composition over inheritance <https://en.wikipedia.org/wiki/Composition_over_inheritance>`_.

2. Inheriting from multiple classes can be problematic, especially when the superclasses have the same method name but different signatures. Implements will throw a descriptive error if that happens to ensure integrity of contracts.

3. The decorators are evaluated at import time. Any errors will be raised then and not when an object is instantiated or a method is called.

4. It's cleaner. Using decorators makes it clear we want share behavior. Also, arguments are not allowed to be renamed.

5. Codebase is tiny: you can just copy the file over. This repo exists more for test coverage.

Usage
-----

Consider the implementation using inheritance:

.. code-block:: python

    class Duck:
        def __init__(self, age):
            self.age = age

    class Flyable:
        @staticmethod
        def migrate(direction):
            raise NotImplementedError("Flyable is an abstract class")

        def fly(self) -> str:
            raise NotImplementedError("Flyable is an abstract class")


    class Quackable:
        def fly(self) -> bool:
            raise NotImplementedError("Quackable is an abstract class")

        def quack(self):
            raise NotImplementedError("Quackable is an abstract class")


    class MallardDuck(Duck, Quackable, Flyable):

        def __init__(self, age):
            super(MallardDuck, self).__init__(age)
            pass

        def migrate(self, dir):
            return True

        def fly(self):
            pass


A couple drawbacks implementing it this way:

1. It's unclear without checking each parent class where super is being called.

2. Similarly the return types of ``fly`` in ``Flyable`` and ``Quackable`` are different. Someone unfamiliar with Python would have to read up on `Method Resolution Order <https://www.python.org/download/releases/2.3/mro/>`_.

3. We would only get a ``NotImplementedError`` when calling ``quack`` which can happen much later during runtime. Also, raising ``NotImplementedError`` everywhere looks clunky.

4. The writer of ``MallardDuck`` made method ``migrate`` an instance method and renamed the argument to ``dir`` which is confusing.

5. We really want to be differentiating between behavior and inheritance.

The advantage of using implements is it looks cleaner and you would get errors at import time instead of when the method is actually called.

In the above example we would rewrite everything as:

.. code-block:: python

    from implements import Interface, implements


    class Duck:
        def __init__(self, age):
            self.age = age


    class Flyable(Interface):
        def fly(self) -> str:
            pass

        @staticmethod
        def migrate(direction):
            pass


    class Quackable(Interface):
        def fly(self) -> bool:
            pass

        def quack(self):
            pass


    @implements(Flyable)
    @implements(Quackable)
    class MallardDuck(Duck):
        def __init__(self, age):
            super(MallardDuck, self).__init__(age)

        def migrate(self, dir):
            return True

        def fly(self):
            pass

The above would now throw the following errors:

.. code-block:: python

    NotImplementedError: 'MallardDuck' must implement method 'fly((self) -> bool)' defined in interface 'Quackable'
    NotImplementedError: 'MallardDuck' must implement method 'quack((self))' defined in interface 'Quackable'
    NotImplementedError: 'MallardDuck' must implement method 'migrate((direction))' defined in interface 'Flyable'

We can solve the errors by rewriting for example as:

.. code-block:: python

    class Quackable(Interface):
        def fly(self) -> str:
            pass

        def quack(self):
            pass

    @implements(Flyable)
    @implements(Quackable)
    class MallardDuck(Duck):
        def __init__(self, age):
            super(MallardDuck, self).__init__(age)

        @staticmethod
        def migrate(direction):
            pass

        def fly(self) -> str:
            pass

        def quack(self):
            pass

Credit
------

Implementation was inspired by a `PR <https://github.com/pmatiello/python-interface/pull/1/files>`_ of @elifiner.

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
