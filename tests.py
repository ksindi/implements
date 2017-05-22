"""pytest unittests"""
import pytest

from implements import Interface, implements


def test_empty():
    class FooInterface(Interface):
        pass

    @implements(FooInterface)
    class FooImplementation:
        pass


def test_with_args_kwargs():
    class FooInterface(Interface):
        def foo(self, a, b=7, *args, **kwargs):
            pass

    @implements(FooInterface)
    class FooImplementation:
        def foo(self, a, b=7, *args, **kwargs):
            pass


def test_property():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

    @implements(FooInterface)
    class FooImplementation:
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
        class FooImplementation:
            @property
            def foo(self):
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
        class FooImplementation:
            @property
            def foo(self):
                pass


def test_missing_method():
    class FooInterface(Interface):
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            pass


def test_missing_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self):
                pass


def test_renamed_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, arrrrg):
                pass


def test_extra_argument():
    class FooInterface(Interface):
        def foo(self, arg):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, arg, ument):
                pass


def test_different_defaults():
    class FooInterface(Interface):
        def foo(self, arg=7):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, arg=8):
                pass


def test_different_order():
    class FooInterface(Interface):
        def foo(self, a, b):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, b, a):
                pass


def test_missing_kwargs():
    class FooInterface(Interface):
        def foo(self, **kwargs):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self):
                pass


def test_missing_property():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            pass


def test_missing_set_property():
    class FooInterface(Interface):
        @property
        def foo(self):
            pass

        @foo.setter
        def foo(self, value):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            @property
            def foo(self):
                pass


def test_bad_constructor():
    class FooInterface(Interface):
        def __init__(self, a):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def __init__(self):
                pass


def test_static():
    class FooInterface(Interface):
        @staticmethod
        def foo():
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def __init__(self):
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

    @implements(BarInterface)
    @implements(FooInterface)
    class FooImplementation:
        def foo(self):
            pass

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

    with pytest.raises(NotImplementedError):
        @implements(Foo2Interface)
        @implements(Foo1Interface)
        class FooImplementation:
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
        class FooImplementation:
            def foo(self):
                pass


def test_class_inheritance():
    # TODO
    class FooInterface(Interface):
        def foo(self):
            pass

    @implements(FooInterface)
    class ParentImplementation:
        def foo(self):
            pass

    class ChildImplementation(ParentImplementation):
        pass


def test_rtn_type_annotation():
    class FooInterface(Interface):
        def foo(self) -> str:
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self) -> int:
                pass


def test_arg_type_annotation():
    class FooInterface(Interface):
        def foo(self, arg: str):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            def foo(self, arg: int):
                pass


def test_classmethods():
    class FooInterface(Interface):
        @classmethod
        def foo(cls):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        class FooImplementation:
            pass


def test_other_decorator_compat():
    def decorator(cls):
        class Wrapper(object):
            def __init__(self, *args):
                self.wrapped = cls(*args)

            def __getattr__(self, name):
                print('Getting the {} of {}'.format(name, self.wrapped))
                return getattr(self.wrapped, name)

        return Wrapper

    class FooInterface(Interface):
        def foo(self):
            pass

    @decorator
    @implements(FooInterface)
    class FooImplementationPass(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def foo(self):
            pass

    with pytest.raises(NotImplementedError):
        @implements(FooInterface)
        @decorator
        class FooImplementationFail(object):
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def foo(self):
                pass


def test_cache():
    pass
