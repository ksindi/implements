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

import inspect
import types
import sys

from pkg_resources import get_distribution, DistributionNotFound


__title__ = 'implements'
__author__ = ('Kamil Sindi <ksindi@ksindi.com>, '
              'Praveen G Shirali <praveengshirali@gmail.com>')
__license__ = 'Apache License, Version 2.0'


try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


__all__ = ['Interface', 'implements']


class Interface:
    pass


def implements(interface_cls):
    """Verifies whether the decorated class implements the interface as
    defined by the `interface_cls`.
    """
    def _decorator(cls):
        verify_methods(interface_cls, cls)
        verify_properties(interface_cls, cls)
        verify_attributes(interface_cls, cls)
        return cls

    return _decorator


def getobj_via_dict(cls, name):
    for c in cls.__mro__:
        if name in c.__dict__:
            return c.__dict__[name]
    return None


def is_classmethod(obj):
    if sys.version_info < (3, 7):
        clsmethod_ident = classmethod
    else:
        clsmethod_ident = (classmethod, types.ClassMethodDescriptorType)
    return isinstance(obj, clsmethod_ident)


def is_staticmethod(obj):
    return isinstance(obj, (staticmethod, types.BuiltinMethodType))


def verify_method_type(method_typer, expected_type,
                       name, ifc_obj, cls_obj, ifc_name, cls_name):
    """Verify a method's type across interface and implementation. Raises
    an exception if they don't match.

    Args:
        method_typer (callable):
            A method type checker (single argument callable) which returns
            True if the supplied argument matches the method type
        expected_type (string):
            A string representation of the expected method type. This is
            used in the exception string
        name (string):
            Name of the attribute being checked
        ifc_obj (object):
            The fetched object from the interface, matched by name
        cls_obj (object):
            The fetched object from the implementation, matched by name
        ifc_name (string):
            Name of the interface class
        cls_name (string):
            Name of the implementation class
    """
    if method_typer(ifc_obj):
        if not method_typer(cls_obj):
            raise NotImplementedError(
                "'{}' must implement '{}' as {} as defined in interface '{}'"
                "".format(cls_name, name, expected_type, ifc_name)
            )


def verify_methods(interface_cls, cls):
    def methods_predicate(m):
        return inspect.isfunction(m) or inspect.ismethod(m)

    for name, method in inspect.getmembers(interface_cls, methods_predicate):
        signature = inspect.signature(method)
        cls_method = getattr(cls, name, None)
        cls_signature = None
        ifc_name = interface_cls.__name__
        cls_name = cls.__name__
        if cls_method and callable(cls_method):
            cls_signature = inspect.signature(cls_method)
        ifc_obj = getobj_via_dict(interface_cls, name)
        cls_obj = getobj_via_dict(cls, name)

        method_types_to_check = [
            (is_classmethod, "a classmethod"),
            (is_staticmethod, "a staticmethod"),
            (inspect.isasyncgenfunction, "an async genenerator-function"),
            (inspect.isgeneratorfunction, "a generator-function"),
            (inspect.iscoroutinefunction, "a coroutine-function")
        ]
        for (method_typer, expected_type) in method_types_to_check:
            verify_method_type(method_typer, expected_type,
                               name, ifc_obj, cls_obj, ifc_name, cls_name)

        if cls_signature != signature:
            raise NotImplementedError(
                "'{}' must implement method '{}{}' defined in interface '{}'"
                .format(cls_name, name, signature, ifc_name)
            )


def verify_properties(interface_cls, cls):
    prop_attrs = dict(fget='getter', fset='setter', fdel='deleter')
    descriptors = inspect.getmembers(interface_cls, inspect.isdatadescriptor)
    for name, prop in descriptors:
        cls_prop = getattr(cls, name, None)
        for attr in prop_attrs:
            # instanceof doesn't work for class function comparison
            ifc_prop_type = type(getattr(prop, attr, None))
            cls_prop_type = type(getattr(cls_prop, attr, None))
            if ifc_prop_type != cls_prop_type:
                cls_name = cls.__name__
                ifc_name = interface_cls.__name__
                proptype = prop_attrs[attr]
                raise NotImplementedError(
                    "'{}' must implement a {} for property '{}' defined in "
                    "interface '{}'".format(cls_name, proptype, name, ifc_name)
                )


def verify_attributes(interface_cls, cls):
    interface_attributes = get_attributes(interface_cls)
    cls_attributes = get_attributes(cls)
    for missing_attr in interface_attributes - cls_attributes:
        raise NotImplementedError(
            "'{}' must have class attribute '{}' defined in interface '{}'"
            .format(cls.__name__, missing_attr, interface_cls.__name__)
        )


def get_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return set(item[0] for item in inspect.getmembers(cls)  # skipcq: PTC-W0015
               if item[0] not in boring and not callable(item[1]))
