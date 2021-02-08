# Copyright 2017-2020 Kamil Sindi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import pytest

from implements import Interface, implements, get_mro


py36 = pytest.mark.skipif(sys.version_info < (3, 6), reason='requires py3.6')


def test_empty():
    class FooInterface(Interface):
        pass

    @implements(FooInterface)
    class FooImplementation:
        pass


def test_with_args_kwargs():
    class FooInterface(Interface):
        def foo(self, a, *args, b=1, **kwargs):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, a, *args, b=7):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, a, *args, b=1, **kwargs):
            pass


def test_with_kwarg_only():
    class FooInterface(Interface):
        def foo(self, a, *, b):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, a, b):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, a, *, b):
            pass


def test_property():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @property
        def foo(self):
            pass


def test_property_inverse():
    class FooInterface(Interface):
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def foo(self):
                pass


def test_setters():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

        @foo.setter
        def foo(self, val):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @property
        def foo(self):
            pass

        @foo.setter
        def foo(self, val):
            pass


def test_deleters():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

        @foo.deleter
        def foo(self, val):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @property
        def foo(self):
            pass

        @foo.deleter
        def foo(self, val):
            pass


def test_implementation_implements_more_descriptors():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

    #   An implementation must implement all data descriptors defined in
    #   the interface, however, the implementation could define more.
    #
    #   The case below must not generate errors because FooImplementationPass
    #   defines a foo.setter which isn't defined by FooInterface
    @implements(FooInterface)
    class FooImplementationPass:
        @property
        def foo(self):
            pass

        @foo.setter
        def foo(self, val):
            pass


def test_missing_method():
    class FooInterface(Interface):
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self):
            pass


def test_missing_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, arg):
            pass


def test_renamed_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, arrrrg):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, arg):
            pass


def test_extra_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, arg, ument):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, arg):
            pass


def test_different_defaults():
    class FooInterface(Interface):
        def foo(self, arg=7):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, arg=8):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, arg=7):
            pass


def test_different_order():
    class FooInterface(Interface):
        def foo(self, a, b):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, b, a):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, a, b):
            pass


def test_missing_kwargs():
    class FooInterface(Interface):
        def foo(self, **kwargs):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, **kwargs):
            pass


def test_missing_property():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):    # missing method
        @implements(FooInterface)
        class FooImplementationFail1:           # skipcq: PYL-W0612
            pass

    with pytest.raises(NotImplementedError):    # missing property decorator
        @implements(FooInterface)
        class FooImplementationFail2:           # skipcq: PYL-W0612
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @property
        def foo(self):
            pass


def test_bad_constructor():
    class FooInterface(Interface):
        def __init__(self, a):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def __init__(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def __init__(self, a):
            pass


def test_multiple_errors():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

        def __init__(self, a):
            pass

    # Bad constructor, missing method getter, and missing class attribute (3)
    match = r'^Found 3 errors in implementation:\n- .+\n- .+\n- .+\nwith .+'
    with pytest.raises(NotImplementedError, match=match):
        @implements(FooInterface)
        class FooImplementationFail:           # skipcq: PYL-W0612
            def __init__(self):
                pass


def test_static():
    class FooInterface(Interface):
        @staticmethod
        def foo(a, b, c):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail1:           # skipcq: PYL-W0612
            pass                    # missing foo

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail2:           # skipcq: PYL-W0612
            # skipcq: PYL-E0213
            def foo(a, b, c):       # missing staticmethod decorator
                pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail3:           # skipcq: PYL-W0612
            @classmethod            # classmethod instead of staticmethod
            def foo(cls, a, b, c):  # decorator-check fails before signature
                pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail4:           # skipcq: PYL-W0612
            @staticmethod
            def foo(m, n, o):       # staticmethod, but wrong signature
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @staticmethod
        def foo(a, b, c):
            pass


def test_classmethods():
    class FooInterface(Interface):
        @classmethod
        def foo(cls, a, b, c):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail1:           # skipcq: PYL-W0612
            pass                    # missing foo

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail2:           # skipcq: PYL-W0612
            # skipcq: PYL-E0213
            def foo(cls, a, b, c):  # missing classmethod decorator
                pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail3:           # skipcq: PYL-W0612
            @staticmethod           # staticmethod instead of classmethod
            def foo(a, b, c):       # decorator-check fails before signature
                pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail4:           # skipcq: PYL-W0612
            @classmethod
            def foo(cls, m, n, o):   # classmethod, but wrong signature
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        @classmethod
        def foo(cls, a, b, c):
            pass


def test_classmethod_signature_match():
    # For a classmethod, inspect.signature returns a signature with the first
    # element (cls) stripped. A classmethod with signature (cls, a, b, c) has
    # signature equivalence with a regular method with signature (a, b, c)
    #
    # Example:
    from inspect import signature

    class TestA:
        @classmethod
        def foo(cls, a, b, c):
            pass

    class TestB:
        # skipcq: PYL-E0213
        def foo(a, b, c):
            pass

    assert signature(TestA.foo) == signature(TestB.foo)

    # The test below ensures that the above case is flagged
    class FooInterface(Interface):
        @classmethod
        def foo(cls, a, b, c):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            # skipcq: PYL-E0213
            def foo(a, b, c):
                pass


def test_staticmethod_classmethod_with_decorator():
    class FooBarInterface(Interface):
        @staticmethod
        def foo(a, b, c):
            pass

        @classmethod
        def bar(cls, a, b, c):
            pass

    import functools

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner

    @implements(FooBarInterface)
    class FooBarImplementationPass:
        @staticmethod
        @decorator
        def foo(a, b, c):
            pass

        @classmethod
        @decorator
        def bar(cls, a, b, c):
            pass


def test_kwargs_only():
    class FooInterface(Interface):
        def foo(self, *, a):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, a):
                pass


def test_multiple_interfaces():
    class FooInterface(Interface):
        def foo(self):
            pass

    class BarInterface(Interface):
        def bar(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(BarInterface)
        @implements(FooInterface)
        class FooImplementationNoBar:
            def foo(self, a):
                pass

    with pytest.raises(NotImplementedError):
        @implements(BarInterface)
        @implements(FooInterface)
        class FooImplementationNoFoo:
            def bar(self, a):
                pass

    @implements(BarInterface)
    @implements(FooInterface)
    class FooImplementation:
        def foo(self):
            pass

        def bar(self):
            pass


def test_interface_name_collision():
    class Foo1Interface(Interface):
        def foo(self):
            pass

    class Foo2Interface(Interface):
        def foo(self):
            pass

    @implements(Foo2Interface)
    @implements(Foo1Interface)
    class FooImplementation:
        def foo(self):
            pass


def test_interface_name_and_signature_collision():
    class Foo1Interface(Interface):
        def foo(self):
            pass

    class Foo2Interface(Interface):
        def foo(self) -> str:
            return 'foo'

    # Two interfaces with different signatures for a given method will
    # always result in failure for the implementing class, as the
    # implemented method's signature can only satisfy one of the interfaces.

    with pytest.raises(NotImplementedError):
        @implements(Foo2Interface)
        @implements(Foo1Interface)
        class FooImplementationFail:
            def foo(self):
                pass


def test_interface_inheritance():
    class BaseInterface(Interface):
        def bar(self):
            pass

    class FooInterface(BaseInterface):
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self):
            pass

        def bar(self):
            pass


def test_class_inheritance():
    class FooInterface(Interface):
        def foo(self):
            pass

    @implements(FooInterface)
    class ParentImplementation:
        def foo(self):
            pass

    @implements(FooInterface)
    class ChildImplementation(ParentImplementation):
        pass


def test_class_multiple_inheritance():
    # --------- INTERFACES -----------------------------------------------
    #
    class FooInterface(Interface):
        def foo(self, final):
            pass

    class BarInterface(Interface):
        def bar(self, final):
            pass

    class FooBarInterface(FooInterface, BarInterface):
        pass

    # --------- IMPLEMENTATION -------------------------------------------
    #
    class BaseFooImplementation:        # must get overridden
        def foo(self, override, my, args):
            pass

    @implements(FooInterface)
    class FooImplementation(BaseFooImplementation):
        def foo(self, final):           # skipcq: PYL-W0221
            pass

    @implements(BarInterface)
    class BarImplementation:
        def bar(self, final):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooBarInterface)
        class SubFooImplementation(FooImplementation):  # foo, no bar
            pass

    @implements(FooInterface)
    @implements(BarInterface)
    @implements(FooBarInterface)
    class FooBarImplementation(FooImplementation, BarImplementation):
        pass


def test_rtn_type_annotation():
    class FooInterface(Interface):
        def foo(self) -> str:
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self) -> int:
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self) -> str:
            pass


def test_arg_type_annotation():
    class FooInterface(Interface):
        def foo(self, arg: str):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            def foo(self, arg: int):
                pass

    @implements(FooInterface)
    class FooImplementationPass:
        def foo(self, arg: str):
            pass


def test_other_decorator_compat():
    def decorator(cls):
        class Wrapper:
            def __init__(self, *args):
                self.wrapped = cls(*args)

            def __getattr__(self, name):
                print('Getting the {} of {}'.format(name, self.wrapped))
                return getattr(self.wrapped, name, None)

        return Wrapper

    class FooInterface(Interface):
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        @decorator
        class FooImplementationFail:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def foo(self):
                pass

    @decorator
    @implements(FooInterface)
    class FooImplementationPass:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def foo(self):
            pass


def test_magic_methods():
    class FooInterface(Interface):
        def __add__(self, other):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            pass

    @implements(FooInterface)
    class FooImplementationPass:
        def __add__(self, other):
            pass


def test_attributes():
    class FooInterface(Interface):
        a = None

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            pass

    @implements(FooInterface)
    class FooImplementationPass:
        a = 1
        b = 2


def test_async():
    class AsyncInterface:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args, **kwargs):
            pass

    with pytest.raises(NotImplementedError):
        @implements(AsyncInterface)
        class AsyncImplementation:
            pass


def test_async_method():
    class AsyncFooInterface:
        async def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(AsyncFooInterface)
        class FooImplementationFail:                # skipcq: PYL-W0612
            def foo(self):
                pass

    @implements(AsyncFooInterface)
    class AsyncFooImplementation:                   # skipcq: PYL-W0612
        async def foo(self):
            pass


def test_generator():
    class GenFooInterface:
        def foo(self):                              # skipcq: PYL-R0201
            yield 1

    with pytest.raises(NotImplementedError):
        @implements(GenFooInterface)
        class FooImplementationFail:                # skipcq: PYL-W0612
            def foo(self):
                pass

    # must fail a generator which happens to be async
    with pytest.raises(NotImplementedError):
        @implements(GenFooInterface)
        class AsyncGenFooImplementationFail:        # skipcq: PYL-W0612
            async def foo(self):
                yield 1

    @implements(GenFooInterface)
    class GenFooImplementation:                     # skipcq: PYL-W0612
        def foo(self):                              # skipcq: PYL-R0201
            yield 1


def test_asyncgen_method():
    class AsyncGenFooInterface:
        async def foo(self):
            yield 1

    with pytest.raises(NotImplementedError):
        @implements(AsyncGenFooInterface)
        class AsyncFooImplementationFail:           # skipcq: PYL-W0612
            async def foo(self):
                pass

    with pytest.raises(NotImplementedError):
        @implements(AsyncGenFooInterface)
        class GenFooImplementationFail:             # skipcq: PYL-W0612
            def foo(self):                          # skipcq: PYL-R0201
                yield 1

    @implements(AsyncGenFooInterface)
    class AsyncGenFooImplementation:                # skipcq: PYL-W0612
        async def foo(self):
            yield 1


@py36
def test_new_style_descriptors():
    class IntField:
        def __get__(self, instance, owner):
            return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, int):
                raise ValueError('expecting integer in {}'.format(self.name))
            instance.__dict__[self.name] = value

        def __set_name__(self, owner, name):
            self.name = name                            # skipcq: PYL-W0201

    class FooInterface(Interface):
        int_field = IntField()

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            pass

    @implements(FooInterface)
    class FooImplementationPass:
        int_field = IntField()


@py36
def test_new_style_metaclasses():
    class Polygon:
        def __init_subclass__(cls, sides, **kwargs):
            cls.sides = sides
            if cls.sides < 3:
                raise ValueError('polygons need 3+ sides')

        @classmethod
        def interior_angles(cls):
            return (cls.sides - 2) * 180

    class PolygonInterface(Interface):
        def rotate(self):
            pass

    @implements(PolygonInterface)
    class Triangle(Polygon, sides=3):
        def rotate(self):
            pass


def test_descriptors_signature_getter():
    class FooInterface(Interface):
        @property
        def someprop(self) -> str:
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def someprop(self) -> int:
                pass


def test_descriptors_signature_setter():
    class FooInterface(Interface):
        @property
        def someprop(self):
            pass

        @someprop.setter
        def someprop(self, value: str) -> str:
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def someprop(self):
                pass

            @someprop.setter
            def someprop(self, value: int) -> float:
                pass


def test_descriptors_signature_deleter():
    class FooInterface(Interface):
        @property
        def someprop(self):
            pass

        @someprop.deleter
        def someprop(self) -> str:
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementationFail:
            @property
            def someprop(self):
                pass

            @someprop.deleter
            def someprop(self) -> int:
                pass


def test_get_mro():
    class RegularClass:
        pass

    mro = get_mro(RegularClass)
    assert object not in mro

    expected = RegularClass.mro()[:-1]
    assert mro == expected


def test_class_hierarchy_overlap_of_common_class():
    class CommonClass:
        pass

    class FooInterface(CommonClass):
        def abc(self) -> str:
            pass

    with pytest.raises(ValueError):
        @implements(FooInterface)
        class FooImplemenation(CommonClass):
            def abc(self) -> str:
                pass


def test_implementation_inheriting_from_interface():
    class FooInterface:
        def abc(self) -> str:
            pass

    with pytest.raises(ValueError):
        @implements(FooInterface)
        class FooImplemenation(FooInterface):
            def abc(self) -> str:
                pass
