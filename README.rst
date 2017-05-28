Implements
==========

.. image:: https://travis-ci.org/ksindi/implements.svg?branch=master
    :target: https://travis-ci.org/ksindi/ksindi/implements
    :alt: Build Status
.. image:: https://readthedocs.org/projects/implements/badge/?version=v0.1.1
    :target: http://implements.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/implements.svg
    :target: https://pypi.python.org/pypi/implements
    :alt: PyPI Version

*Pythonic interface using decorators*

Install
-------

Implements is available on PyPI can be installed with `pip <https://pip.pypa.io>`_::

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

Let's say we wanted to write a class ``MallardDuck`` that inherits from ``Duck`` and implements ``Flyable`` and ``Quackable``.

There are two idiomatic ways to write this. The first way is writing base classes raising ``NotImplementedError`` in each method.

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

        def migrate(self, dir):
            return True

        def fly(self):
            pass


But there are a couple drawbacks implementing it this way:

1. We would only get a ``NotImplementedError`` when calling ``quack`` which can happen much later during runtime. Also, raising ``NotImplementedError`` everywhere looks clunky.

2. It's unclear without checking each parent class where super is being called.

3. Similarly the return types of ``fly`` in ``Flyable`` and ``Quackable`` are different. Someone unfamiliar with Python would have to read up on `Method Resolution Order <https://www.python.org/download/releases/2.3/mro/>`_.

4. The writer of ``MallardDuck`` made method ``migrate`` an instance method and renamed the argument to ``dir`` which is confusing.

5. We really want to be differentiating between behavior and inheritance.

The advantage of using implements is it looks cleaner and you would get errors at import time instead of when the method is actually called.

Another way is to use abstract base classes from the built-in ``abc`` module:

.. code-block:: python

    from abc import ABCMeta, abstractmethod, abstractstaticmethod


    class Duck(metaclass=ABCMeta):
        def __init__(self, age):
            self.age = age


    class Flyable(metaclass=ABCMeta):
        @abstractstaticmethod
        def migrate(direction):
            pass

        @abstractmethod
        def fly(self) -> str:
            pass


    class Quackable(metaclass=ABCMeta):
        @abstractmethod
        def fly(self) -> bool:
            pass

        @abstractmethod
        def quack(self):
            pass


    class MallardDuck(Duck, Quackable, Flyable):
        def __init__(self, age):
            super(MallardDuck, self).__init__(age)

        def migrate(self, dir):
            return True

        def fly(self):
            pass

        def quack(self):
            pass

Using abstract base classes has the advantage of throwing an error early if a
method is not implemented and having static analysis tools warn if two methods
have different signatures. But it doesn't solve issues 2-4. It also in my
opinion doesn't look pythonic.

In the above example we could rewrite using implements as:

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

We can solve the above errors by rewriting for example as:

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
